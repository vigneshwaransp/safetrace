from app.schemas.resources import (
    OfficialResourcesResponse,
    OfficialChannelResource,
    HelplineResource,
)


def get_official_resources_catalog() -> OfficialResourcesResponse:
    """
    Returns official government channels, 24x7 crisis helplines, and platform escalation guides.
    Ethics rule: Do not auto-submit to government portals; assist, deep-link, and provide documents.
    """
    helplines = [
        HelplineResource(
            name="Cybercrime Helpline (India)",
            number="1930",
            available_hours="24x7",
            coverage="National (India)",
            description="Toll-free emergency helpline for reporting cyber fraud, online harassment, and cybercrime incidents."
        ),
        HelplineResource(
            name="Women Helpline (National Commission for Women / Emergency)",
            number="181",
            available_hours="24x7",
            coverage="National (India)",
            description="24x7 emergency response and referral service for women facing domestic violence, sexual harassment, or digital abuse."
        ),
        HelplineResource(
            name="National Commission for Women (NCW) Cyber Cell",
            number="7827170170",
            available_hours="24x7 (WhatsApp / Call)",
            coverage="National (India)",
            description="Dedicated NCW cyber complaint portal and helpline for women in distress."
        ),
        HelplineResource(
            name="KIRAN Mental Health Helpline",
            number="1800-599-0019",
            available_hours="24x7",
            coverage="National (India)",
            description="Toll-free mental health support helpline for psychological first aid, trauma, and distress management."
        ),
    ]

    official_channels = [
        OfficialChannelResource(
            id="cybercrime-gov-in",
            name="National Cybercrime Reporting Portal",
            category="GOVERNMENT",
            helpline="1930",
            url="https://cybercrime.gov.in",
            description="Official Ministry of Home Affairs portal for lodging cybercrime complaints against women and children.",
            submission_steps=[
                "Visit cybercrime.gov.in and click 'Report Crime Related to Women/Children'.",
                "Choose 'Report Anonymously' or 'Report and Track' based on your comfort level.",
                "Fill in incident details: Date, Time, Platform/Website, and Suspect Information if known.",
                "Attach the SafeTrace Evidence & Complaint PDF dossier as proof.",
                "Save your Complaint Acknowledgment Number for official tracking."
            ],
            legal_statutes=[
                "Information Technology Act, 2000 (Section 66E - Privacy violation)",
                "Information Technology Act, 2000 (Section 67 & 67A - Obscenity and sexually explicit content)",
                "Bharatiya Nyaya Sanhita (BNS) Section 354C (Voyeurism)",
                "Bharatiya Nyaya Sanhita (BNS) Section 354D (Cyberstalking)"
            ]
        ),
        OfficialChannelResource(
            id="ncw-portal",
            name="National Commission for Women (NCW) Complaints",
            category="GOVERNMENT",
            helpline="7827170170",
            url="https://ncwapps.nic.in",
            description="Statutory body protecting women's rights in India. Investigates complaints and facilitates police escalation.",
            submission_steps=[
                "Navigate to ncwapps.nic.in/onlinecomplaintsv2/.",
                "Register with mobile/email or file through the victim support wing.",
                "Paste the formal notice from SafeTrace into the complaint description.",
                "Upload the SafeTrace PDF evidence dossier under supporting documents."
            ],
            legal_statutes=[
                "National Commission for Women Act, 1990",
                "Protection of Women's Constitutional & Statutory Rights"
            ]
        ),
        OfficialChannelResource(
            id="stopncii-org",
            name="StopNCII.org",
            category="GLOBAL_TAKEDOWN",
            helpline=None,
            url="https://stopncii.org",
            description="Global privacy-first initiative operated by Revenge Porn Helpline/SWGfL that creates cryptographic hash blocks across major platforms.",
            submission_steps=[
                "Visit stopncii.org on your device.",
                "Select images directly in your browser. Raw images are hashed locally on your device and NEVER uploaded.",
                "Submit the generated hash hashes to participating tech platforms (Meta, TikTok, Bumble, OnlyFans).",
                "Keep your Case Number and PIN safely to track participating platform takedowns."
            ],
            legal_statutes=[
                "Global Non-Consensual Intimate Imagery Privacy Standard",
                "Hash-Sharing Consortium Zero-Knowledge Protocol"
            ]
        ),
        OfficialChannelResource(
            id="ncmec-take-it-down",
            name="NCMEC Take It Down",
            category="GLOBAL_TAKEDOWN",
            helpline="1-800-843-5678",
            url="https://takeitdown.ncmec.org",
            description="Service for people who were under 18 when the explicit images/videos were taken, or for parents/guardians.",
            submission_steps=[
                "Go to takeitdown.ncmec.org.",
                "Assign hashes locally on your device without transmitting raw images.",
                "Generate a hash blocklist for global social media de-indexing."
            ],
            legal_statutes=[
                "Protection of Children from Sexual Offences (POCSO) Act, 2012",
                "U.S. 18 U.S.C. 2258A / Interpol Child Protection Standards"
            ]
        ),
    ]

    platform_escalations = [
        OfficialChannelResource(
            id="meta-reporting",
            name="Meta (Instagram & Facebook) Takedown",
            category="PLATFORM",
            helpline=None,
            url="https://www.facebook.com/help/contact/263149623790465",
            description="Emergency reporting form for non-consensual intimate imagery and privacy violations on Facebook and Instagram.",
            submission_steps=[
                "Access the Meta Privacy Rights Form.",
                "Select 'Someone is sharing an intimate image or video of me without my consent'.",
                "Provide the direct Instagram/Facebook post or story URLs from your SafeTrace Evidence List.",
                "Cite Rule 3(2)(b) of the IT Rules 2021 requiring takedown within 24 hours."
            ],
            legal_statutes=["IT Rules 2021 Rule 3(2)(b) - Mandatory 24-hour intermediary takedown"]
        ),
        OfficialChannelResource(
            id="x-reporting",
            name="X (Twitter) Private Media & NCII Escalation",
            category="PLATFORM",
            helpline=None,
            url="https://help.twitter.com/forms/nudity",
            description="Direct reporting route for non-consensual nudity and unauthorized private media on X.",
            submission_steps=[
                "Open the X Non-Consensual Nudity form.",
                "Select 'I am the individual pictured'.",
                "List all identified tweet URLs preserved in SafeTrace.",
                "Attach your certified SafeTrace PDF complaint dossier."
            ],
            legal_statutes=["X Safety Policy - Non-consensual nudity violation"]
        ),
        OfficialChannelResource(
            id="reddit-reporting",
            name="Reddit Non-Consensual Media Report",
            category="PLATFORM",
            helpline=None,
            url="https://www.reddit.com/report?reason=it-is-involuntary-pornography",
            description="Direct safety channel to report involuntary pornography and non-consensual sharing on Reddit.",
            submission_steps=[
                "Navigate to reddit.com/report.",
                "Select 'I want to report other issues' > 'It is involuntary pornography'.",
                "Paste the Reddit submission/comment URLs from SafeTrace.",
                "Reddit Trust & Safety will remove content and permanently suspend offending accounts."
            ],
            legal_statutes=["Reddit Content Policy Rule 3"]
        ),
        OfficialChannelResource(
            id="youtube-reporting",
            name="YouTube Privacy Complaint Process",
            category="PLATFORM",
            helpline=None,
            url="https://www.youtube.com/reportabuse",
            description="Formal privacy complaint procedure for videos containing non-consensual depictions.",
            submission_steps=[
                "Open the YouTube Privacy Complaint form.",
                "Provide video URLs and timestamp markers identified in SafeTrace.",
                "YouTube issues a 48-hour notice to the uploader before permanent takedown."
            ],
            legal_statutes=["YouTube Community Guidelines - Privacy violation"]
        ),
    ]

    return OfficialResourcesResponse(
        crisis_helplines=helplines,
        official_channels=official_channels,
        platform_escalations=platform_escalations,
    )
