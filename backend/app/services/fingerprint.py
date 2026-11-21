import io
import os
import tempfile
import hashlib
import base64
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import imagehash
import pdqhash
from app.core.config import settings


@dataclass
class FingerprintResult:
    sha256: str
    pdq_hash: str
    pdq_quality: int
    phash: str
    dhash: str
    ahash: str
    keypoints_summary: Optional[Dict[str, Any]] = None


@dataclass
class MatchComparisonResult:
    is_candidate: bool
    similarity_score: float
    confidence_band: str  # HIGH, MEDIUM, LOW, NONE
    reasons: List[str]
    pdq_distance: Optional[int] = None
    phash_distance: Optional[int] = None
    dhash_distance: Optional[int] = None
    ahash_distance: Optional[int] = None
    is_exact_sha256: bool = False
    is_crop_match: bool = False


def _pack_pdq_bits_to_hex(bits: np.ndarray) -> str:
    """Pack 256-bit binary numpy array into 64-character hexadecimal string."""
    return np.packbits(bits).tobytes().hex()


def _unpack_pdq_hex_to_bits(hex_str: str) -> np.ndarray:
    """Unpack 64-character hex string into 256-bit binary numpy array."""
    raw_bytes = bytes.fromhex(hex_str)
    return np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))


def hamming_distance_hex(hex1: str, hex2: str) -> int:
    """Compute Hamming distance between two hex-encoded hash strings of equal length."""
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    min_len = min(len(b1), len(b2))
    distance = sum(bin(x ^ y).count("1") for x, y in zip(b1[:min_len], b2[:min_len]))
    if len(b1) != len(b2):
        distance += abs(len(b1) - len(b2)) * 8
    return distance


def pdq_hamming_distance(pdq_hex1: str, pdq_hex2: str) -> int:
    """Compute 256-bit Hamming distance between two PDQ hex hashes."""
    return hamming_distance_hex(pdq_hex1, pdq_hex2)


def compute_image_fingerprints(image_bytes: bytes) -> FingerprintResult:
    """
    Compute multi-modal cryptographic and perceptual fingerprints for an image:
    - SHA-256: Exact bitwise match
    - PDQ (256-bit + quality): Perceptual DCT hash resilient to edits and compression
    - pHash (64-bit): Frequency DCT perceptual hash
    - dHash (64-bit): Gradient difference hash
    - aHash (64-bit): Low-frequency average hash
    - Multi-scale spatial center crop pHash: Invariant to perimeter crops/borders
    - ORB Keypoint descriptor summary: Invariant local feature keypoints
    """
    # 1. Exact SHA-256
    sha256_hash = hashlib.sha256(image_bytes).hexdigest()

    # Load with PIL
    pil_img = Image.open(io.BytesIO(image_bytes))
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    # 2. Perceptual hashes via ImageHash
    phash_val = str(imagehash.phash(pil_img))
    dhash_val = str(imagehash.dhash(pil_img))
    ahash_val = str(imagehash.average_hash(pil_img))

    # Center crop (80% box) for crop detection
    w, h = pil_img.size
    center_box = (int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9))
    center_img = pil_img.crop(center_box)
    center_phash = str(imagehash.phash(center_img))

    # 3. PDQ Hash (256-bit) via pdqhash
    cv_img = np.array(pil_img)
    pdq_bits, pdq_quality = pdqhash.compute(cv_img)
    pdq_hex = _pack_pdq_bits_to_hex(pdq_bits)

    # 4. ORB feature detection (for local invariant keypoints against heavy crops)
    keypoints_summary = {
        "center_phash": center_phash,
        "keypoint_count": 0,
        "descriptors_b64": None,
    }
    try:
        gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        orb = cv2.ORB_create(nfeatures=250)
        kps, descs = orb.detectAndCompute(gray, None)
        if descs is not None and len(descs) > 0:
            top_descs = descs[:150]
            b64_descs = base64.b64encode(top_descs.tobytes()).decode("ascii")
            keypoints_summary.update({
                "keypoint_count": len(kps),
                "descriptor_count": len(top_descs),
                "descriptors_b64": b64_descs,
            })
    except Exception:
        pass

    return FingerprintResult(
        sha256=sha256_hash,
        pdq_hash=pdq_hex,
        pdq_quality=int(pdq_quality),
        phash=phash_val,
        dhash=dhash_val,
        ahash=ahash_val,
        keypoints_summary=keypoints_summary,
    )


def compute_video_keyframes_fingerprints(video_bytes: bytes, max_frames: int = 8) -> List[FingerprintResult]:
    """
    Sample keyframes from a video file and extract fingerprints for each frame.
    """
    results: List[FingerprintResult] = []
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    try:
        cap = cv2.VideoCapture(tmp_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            return results

        interval = max(1, total_frames // max_frames)
        frame_idx = 0
        collected = 0

        while cap.isOpened() and collected < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % interval == 0:
                success, enc_buf = cv2.imencode(".jpg", frame)
                if success:
                    fp = compute_image_fingerprints(enc_buf.tobytes())
                    results.append(fp)
                    collected += 1
            frame_idx += 1
        cap.release()
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    return results


def _check_orb_match(t_summary: Optional[Dict[str, Any]], c_summary: Optional[Dict[str, Any]]) -> Tuple[int, float]:
    """Check ORB descriptor matches between two keypoint summaries."""
    if not t_summary or not c_summary:
        return 0, 0.0
    t_b64 = t_summary.get("descriptors_b64")
    c_b64 = c_summary.get("descriptors_b64")
    if not t_b64 or not c_b64:
        return 0, 0.0

    try:
        t_bytes = base64.b64decode(t_b64)
        c_bytes = base64.b64decode(c_b64)
        d1 = np.frombuffer(t_bytes, dtype=np.uint8).reshape(-1, 32)
        d2 = np.frombuffer(c_bytes, dtype=np.uint8).reshape(-1, 32)
        if len(d1) < 5 or len(d2) < 5:
            return 0, 0.0

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(d1, d2)
        good = [m for m in matches if m.distance < 45]
        good_count = len(good)
        ratio = good_count / min(len(d1), len(d2))
        return good_count, ratio
    except Exception:
        return 0, 0.0


def compare_fingerprints(
    target_fp: FingerprintResult | Dict[str, Any],
    candidate_fp: FingerprintResult | Dict[str, Any]
) -> MatchComparisonResult:
    """
    Compare two image fingerprints using a multi-metric similarity model:
    - Exact SHA-256 equality = 100% score (HIGH confidence)
    - PDQ distance <= 20: HIGH confidence candidate
    - PDQ distance <= 31: MEDIUM confidence candidate
    - Multi-scale spatial center crop alignment & ORB feature inliers for tough crops
    - Combined score = 0.50 * PDQ + 0.30 * pHash + 0.10 * dHash + 0.10 * aHash
    """
    # Extract fields whether dict or FingerprintResult
    t_sha = target_fp.sha256 if isinstance(target_fp, FingerprintResult) else target_fp.get("sha256") or target_fp.get("sha256_hash")
    c_sha = candidate_fp.sha256 if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("sha256") or candidate_fp.get("sha256_hash")

    t_pdq = target_fp.pdq_hash if isinstance(target_fp, FingerprintResult) else target_fp.get("pdq_hash")
    c_pdq = candidate_fp.pdq_hash if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("pdq_hash")

    t_phash = target_fp.phash if isinstance(target_fp, FingerprintResult) else target_fp.get("phash")
    c_phash = candidate_fp.phash if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("phash")

    t_dhash = target_fp.dhash if isinstance(target_fp, FingerprintResult) else target_fp.get("dhash")
    c_dhash = candidate_fp.dhash if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("dhash")

    t_ahash = target_fp.ahash if isinstance(target_fp, FingerprintResult) else target_fp.get("ahash")
    c_ahash = candidate_fp.ahash if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("ahash")

    t_summary = target_fp.keypoints_summary if isinstance(target_fp, FingerprintResult) else target_fp.get("keypoints_summary")
    c_summary = candidate_fp.keypoints_summary if isinstance(candidate_fp, FingerprintResult) else candidate_fp.get("keypoints_summary")

    # 1. Exact SHA-256 match
    if t_sha and c_sha and t_sha.lower() == c_sha.lower():
        return MatchComparisonResult(
            is_candidate=True,
            similarity_score=100.0,
            confidence_band="HIGH",
            reasons=["Exact cryptographic match (SHA-256: 100%)"],
            is_exact_sha256=True,
            pdq_distance=0,
            phash_distance=0,
            dhash_distance=0,
            ahash_distance=0,
        )

    reasons: List[str] = []
    scores = []
    weights = []

    # 2. PDQ Distance (256-bit scale)
    pdq_dist = None
    if t_pdq and c_pdq:
        pdq_dist = pdq_hamming_distance(t_pdq, c_pdq)
        pdq_score = max(0.0, min(100.0, 100.0 * (1.0 - (pdq_dist / 64.0))))
        scores.append(pdq_score)
        weights.append(0.50)
        reasons.append(f"PDQ distance: {pdq_dist}/256 ({pdq_score:.1f}% perceptual similarity)")

    # 3. pHash Distance (64-bit scale)
    phash_dist = None
    if t_phash and c_phash:
        phash_dist = hamming_distance_hex(t_phash, c_phash)
        phash_score = max(0.0, min(100.0, 100.0 * (1.0 - (phash_dist / 24.0))))
        scores.append(phash_score)
        weights.append(0.30)
        reasons.append(f"pHash distance: {phash_dist}/64 ({phash_score:.1f}%)")

    # 4. dHash Distance (64-bit scale)
    dhash_dist = None
    if t_dhash and c_dhash:
        dhash_dist = hamming_distance_hex(t_dhash, c_dhash)
        dhash_score = max(0.0, min(100.0, 100.0 * (1.0 - (dhash_dist / 24.0))))
        scores.append(dhash_score)
        weights.append(0.10)

    # 5. aHash Distance (64-bit scale)
    ahash_dist = None
    if t_ahash and c_ahash:
        ahash_dist = hamming_distance_hex(t_ahash, c_ahash)
        ahash_score = max(0.0, min(100.0, 100.0 * (1.0 - (ahash_dist / 24.0))))
        scores.append(ahash_score)
        weights.append(0.10)

    # Calculate base combined similarity
    if scores and sum(weights) > 0:
        total_weight = sum(weights)
        combined_score = sum(s * w for s, w in zip(scores, weights)) / total_weight
    else:
        combined_score = 0.0

    # 6. Check Spatial Center Crop & ORB Inliers (for heavy cropping & edits)
    is_crop_match = False
    t_center = t_summary.get("center_phash") if t_summary else None
    c_center = c_summary.get("center_phash") if c_summary else None

    if t_center and c_phash:
        dist_tc = hamming_distance_hex(t_center, c_phash)
        if dist_tc <= 8:
            is_crop_match = True
            crop_score = 88.0 - (dist_tc * 2.0)
            if crop_score > combined_score:
                combined_score = crop_score
            reasons.append(f"Spatial crop alignment detected (center pHash distance: {dist_tc}/64)")

    if not is_crop_match and c_center and t_phash:
        dist_ct = hamming_distance_hex(c_center, t_phash)
        if dist_ct <= 8:
            is_crop_match = True
            crop_score = 88.0 - (dist_ct * 2.0)
            if crop_score > combined_score:
                combined_score = crop_score
            reasons.append(f"Spatial crop alignment detected (candidate center pHash distance: {dist_ct}/64)")

    # 7. Check ORB local invariant descriptors
    good_matches, match_ratio = _check_orb_match(t_summary, c_summary)
    if good_matches >= 8 or match_ratio >= 0.20:
        orb_score = min(95.0, 65.0 + (good_matches * 2.5))
        if orb_score > combined_score:
            combined_score = orb_score
        is_crop_match = True
        reasons.append(f"Invariant local keypoints matched: {good_matches} verified feature inliers")

    # Determine confidence band
    confidence_band = "NONE"
    is_candidate = False

    is_high_pdq = (pdq_dist is not None and pdq_dist <= settings.PDQ_THRESHOLD_HIGH)
    is_med_pdq = (pdq_dist is not None and pdq_dist <= settings.PDQ_THRESHOLD_MEDIUM)

    if is_high_pdq or combined_score >= 80.0:
        confidence_band = "HIGH"
        is_candidate = True
    elif is_med_pdq or is_crop_match or combined_score >= 62.0:
        confidence_band = "MEDIUM"
        is_candidate = True
    elif combined_score >= 48.0 or (pdq_dist is not None and pdq_dist <= 45):
        confidence_band = "LOW"
        is_candidate = True

    return MatchComparisonResult(
        is_candidate=is_candidate,
        similarity_score=round(combined_score, 2),
        confidence_band=confidence_band,
        reasons=reasons,
        pdq_distance=pdq_dist,
        phash_distance=phash_dist,
        dhash_distance=dhash_dist,
        ahash_distance=ahash_dist,
        is_exact_sha256=False,
        is_crop_match=is_crop_match,
    )
