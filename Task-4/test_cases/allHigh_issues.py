# =====================================================
# all issues High + critical
# ======================================================

transcript_2 = """
Customer: We have multiple major problems affecting our business operations.

Agent: Please describe them.

Customer: None of our users can log in to the platform since this morning.

Customer: The payment gateway is completely failing and all transactions are being rejected.

Customer: We also discovered that customer records are missing from the database after yesterday's deployment.

Customer: Some users are reporting unauthorized access to their accounts.

Customer: The website is frequently unavailable and returns server errors.

Agent: We are escalating this immediately.
"""

high_critical_issues = [
    {
        "id": "001",
        "issue": "Platform login authentication failure",
        "description": "Users are currently unable to log in to the platform.",
        "confidence_score": 1.0
    },
    {
        "id": "002",
        "issue": "Payment gateway transaction rejection",
        "description": "The payment gateway is failing, causing all customer transactions to be rejected.",
        "confidence_score": 1.0
    },
    {
        "id": "003",
        "issue": "Data loss in customer database",
        "description": "Customer records have gone missing following a recent deployment.",
        "confidence_score": 1.0
    },
    {
        "id": "004",
        "issue": "Unauthorized account access reports",
        "description": "Users are reporting incidents of unauthorized access to their accounts.",
        "confidence_score": 0.9
    },
    {
        "id": "005",
        "issue": "Website instability and server errors",
        "description": "The website is frequently unavailable and returning server errors.",
        "confidence_score": 1.0
    }
]

high_critical_severity_issues = [
    {
        "issue": "Platform login authentication failure",
        "description": "Users are currently unable to log in to the platform.",
        "severity": "critical"
    },
    {
        "issue": "Payment gateway transaction rejection",
        "description": "The payment gateway is failing, causing all customer transactions to be rejected.",
        "severity": "critical"
    },
    {
        "issue": "Data loss in customer database",
        "description": "Customer records have gone missing following a recent deployment.",
        "severity": "critical"
    },
    {
        "issue": "Unauthorized account access reports",
        "description": "Users are reporting incidents of unauthorized access to their accounts.",
        "severity": "critical"
    },
    {
        "issue": "Website instability and server errors",
        "description": "The website is frequently unavailable and returning server errors.",
        "severity": "high"
    }
]

