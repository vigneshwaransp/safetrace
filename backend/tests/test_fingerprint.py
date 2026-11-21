import io
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from app.services.fingerprint import (
    compute_image_fingerprints,
    compute_video_keyframes_fingerprints,
    compare_fingerprints,
    pdq_hamming_distance,
    hamming_distance_hex,
)


def _generate_test_image(size=(300, 300)) -> bytes:
    """Generate a rich synthetic test image with shapes, gradients, and text-like blocks."""
    img = Image.new("RGB", size, color=(240, 230, 210))
    # Draw colored rectangles and distinct patterns
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 140, 140], fill=(220, 50, 80), outline=(10, 10, 10), width=3)
    draw.ellipse([100, 100, 260, 260], fill=(20, 120, 200), outline=(255, 255, 255), width=4)
    draw.polygon([(150, 30), (280, 80), (220, 160)], fill=(240, 180, 40))
    draw.line([0, 150, 300, 150], fill=(0, 0, 0), width=2)
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def _generate_unrelated_image(size=(300, 300)) -> bytes:
    """Generate a completely distinct geometric pattern."""
    img = Image.new("RGB", size, color=(10, 30, 20))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    for i in range(0, 300, 25):
        draw.line([i, 0, 300 - i, 300], fill=(0, 250, 150), width=3)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def test_exact_image_match():
    original = _generate_test_image()
    fp_orig = compute_image_fingerprints(original)
    fp_copy = compute_image_fingerprints(original)

    result = compare_fingerprints(fp_orig, fp_copy)
    assert result.is_candidate is True
    assert result.similarity_score == 100.0
    assert result.confidence_band == "HIGH"
    assert result.is_exact_sha256 is True
    assert result.pdq_distance == 0


def test_resize_transformation():
    original_bytes = _generate_test_image((400, 400))
    fp_orig = compute_image_fingerprints(original_bytes)

    # Resize down to 120x120
    pil_img = Image.open(io.BytesIO(original_bytes))
    resized_img = pil_img.resize((120, 120), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    resized_img.save(buf, format="JPEG", quality=90)
    resized_bytes = buf.getvalue()

    fp_resized = compute_image_fingerprints(resized_bytes)
    result = compare_fingerprints(fp_orig, fp_resized)

    assert result.is_candidate is True
    assert result.confidence_band in ["HIGH", "MEDIUM"]
    assert result.pdq_distance is not None
    assert result.pdq_distance <= 20  # Strong candidate


def test_cropping_transformation():
    original_bytes = _generate_test_image((350, 350))
    fp_orig = compute_image_fingerprints(original_bytes)

    # Crop 15% from borders
    pil_img = Image.open(io.BytesIO(original_bytes))
    w, h = pil_img.size
    cropped_img = pil_img.crop((int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9)))
    buf = io.BytesIO()
    cropped_img.save(buf, format="JPEG", quality=90)
    cropped_bytes = buf.getvalue()

    fp_cropped = compute_image_fingerprints(cropped_bytes)
    result = compare_fingerprints(fp_orig, fp_cropped)

    assert result.is_candidate is True
    assert result.similarity_score >= 65.0
    assert result.is_crop_match is True
    assert result.confidence_band in ["HIGH", "MEDIUM"]


def test_jpeg_recompression_transformation():
    original_bytes = _generate_test_image()
    fp_orig = compute_image_fingerprints(original_bytes)

    # Recompress heavily to quality=25
    pil_img = Image.open(io.BytesIO(original_bytes))
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=25)
    compressed_bytes = buf.getvalue()

    fp_comp = compute_image_fingerprints(compressed_bytes)
    result = compare_fingerprints(fp_orig, fp_comp)

    assert result.is_candidate is True
    assert result.confidence_band == "HIGH"
    assert result.pdq_distance is not None
    assert result.pdq_distance <= 10


def test_brightness_and_contrast_transformation():
    original_bytes = _generate_test_image()
    fp_orig = compute_image_fingerprints(original_bytes)

    pil_img = Image.open(io.BytesIO(original_bytes))
    # Adjust brightness +20% and contrast +20%
    bright = ImageEnhance.Brightness(pil_img).enhance(1.20)
    contrast = ImageEnhance.Contrast(bright).enhance(1.20)
    buf = io.BytesIO()
    contrast.save(buf, format="JPEG", quality=90)

    fp_adjusted = compute_image_fingerprints(buf.getvalue())
    result = compare_fingerprints(fp_orig, fp_adjusted)

    assert result.is_candidate is True
    assert result.confidence_band in ["HIGH", "MEDIUM"]
    assert result.similarity_score >= 70.0


def test_light_filter_blur_transformation():
    original_bytes = _generate_test_image()
    fp_orig = compute_image_fingerprints(original_bytes)

    pil_img = Image.open(io.BytesIO(original_bytes))
    blurred = pil_img.filter(ImageFilter.GaussianBlur(radius=1.5))
    buf = io.BytesIO()
    blurred.save(buf, format="JPEG", quality=90)

    fp_filter = compute_image_fingerprints(buf.getvalue())
    result = compare_fingerprints(fp_orig, fp_filter)

    assert result.is_candidate is True
    assert result.confidence_band == "HIGH"
    assert result.pdq_distance <= 15


def test_unrelated_images_do_not_match():
    img1_bytes = _generate_test_image()
    img2_bytes = _generate_unrelated_image()

    fp1 = compute_image_fingerprints(img1_bytes)
    fp2 = compute_image_fingerprints(img2_bytes)

    result = compare_fingerprints(fp1, fp2)
    assert result.pdq_distance is not None
    assert result.pdq_distance > 45
    assert result.confidence_band == "NONE"
    assert result.is_candidate is False


def test_video_keyframes_sampling():
    """Create a synthetic in-memory video and assert keyframe fingerprints extraction."""
    width, height = 160, 120
    fps = 10
    num_frames = 20

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_name = tmp.name

    out = cv2.VideoWriter(tmp_name, fourcc, fps, (width, height))
    for i in range(num_frames):
        frame = np.full((height, width, 3), (i * 10 % 255, 100, 150), dtype=np.uint8)
        out.write(frame)
    out.release()

    with open(tmp_name, "rb") as f:
        video_bytes = f.read()

    import os
    os.remove(tmp_name)

    keyframes_fps = compute_video_keyframes_fingerprints(video_bytes, max_frames=5)
    assert len(keyframes_fps) >= 1
    assert all(len(fp.pdq_hash) == 64 for fp in keyframes_fps)
    assert all(len(fp.sha256) == 64 for fp in keyframes_fps)
