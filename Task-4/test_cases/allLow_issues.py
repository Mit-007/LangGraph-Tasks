## =====================================================
# all issue low + medium
# ======================================================

transcript_1 = """
Customer: Hi, I wanted to report a few minor issues with your website.

Agent: Sure, please tell me.

Customer: The profile picture on my account page appears slightly stretched.

Customer: Also, some buttons are not perfectly aligned on the settings page.

Customer: The dashboard takes about 3-4 seconds longer than usual to load, but it still works.

Customer: I noticed a typo in one of the notification messages.

Customer: Everything is functional otherwise.

Agent: Thank you for reporting these issues.
"""

low_medium_issues = [
    {
        "id": "001",
        "issue": "Profile picture display distortion",
        "description": "The user's profile picture on the account page appears stretched.",
        "confidence_score": 1.0
    },
    {
        "id": "002",
        "issue": "UI button alignment inconsistency",
        "description": "Buttons on the settings page are not perfectly aligned.",
        "confidence_score": 1.0
    },
    {
        "id": "003",
        "issue": "Dashboard load time delay",
        "description": "The dashboard takes 3-4 seconds longer than usual to load.",
        "confidence_score": 1.0
    },
    {
        "id": "004",
        "issue": "Typo in notification message",
        "description": "There is a typographical error present in one of the notification messages.",
        "confidence_score": 1.0
    }
]

low_medium_severity_issues = [
    {
        "issue": "Profile picture display distortion",
        "description": "The user's profile picture on the account page appears stretched.",
        "severity": "low"
    },
    {
        "issue": "UI button alignment inconsistency",
        "description": "Buttons on the settings page are not perfectly aligned.",
        "severity": "low"
    },
    {
        "issue": "Dashboard load time delay",
        "description": "The dashboard takes 3-4 seconds longer than usual to load.",
        "severity": "medium"
    },
    {
        "issue": "Typo in notification message",
        "description": "There is a typographical error present in one of the notification messages.",
        "severity": "low"
    }
]

