# =====================================================
# contails all typed issues ( low + medium + high + critical )
# ======================================================
transcript_3 = """Customer: We are experiencing several issues across the platform.

Agent: Please explain.

Customer: The company logo appears blurry on the homepage.

Customer: The reports page takes nearly 15 seconds to load.

Customer: Several users cannot reset their passwords.

Customer: The inventory synchronization service stopped updating products since yesterday.

Customer: Online payments are intermittently failing.

Customer: We found that some customer orders have disappeared from the database.

Customer: Also, one notification message contains a spelling mistake.

Agent: Thank you. We will investigate these issues."""

mixed_issues = [
    {
        "id": "001",
        "issue": "Blurry company logo on homepage",
        "description": "The company logo displayed on the homepage appears blurry to users.",
        "confidence_score": 1.0
    },
    {
        "id": "002",
        "issue": "Slow loading reports page",
        "description": "The reports page takes approximately 15 seconds to load.",
        "confidence_score": 1.0
    },
    {
        "id": "003",
        "issue": "Password reset functionality failure",
        "description": "Several users are unable to successfully reset their account passwords.",
        "confidence_score": 1.0
    },
    {
        "id": "004",
        "issue": "Inventory synchronization service failure",
        "description": "The inventory synchronization service has stopped updating product information since yesterday.",
        "confidence_score": 1.0
    },
    {
        "id": "005",
        "issue": "Intermittent online payment failures",
        "description": "Online payment processing is failing for customers on an intermittent basis.",
        "confidence_score": 1.0
    },
    {
        "id": "006",
        "issue": "Customer order data loss",
        "description": "Some customer orders are missing from the database.",
        "confidence_score": 1.0
    },
    {
        "id": "007",
        "issue": "Typographical error in notification",
        "description": "A spelling mistake was identified in one of the notification messages.",
        "confidence_score": 1.0
    }
]

mixed_severity_issues = [
    {
        "issue": "Blurry company logo on homepage",
        "description": "The company logo displayed on the homepage appears blurry to users.",
        "severity": "low"
    },
    {
        "issue": "Slow loading reports page",
        "description": "The reports page takes approximately 15 seconds to load.",
        "severity": "medium"
    },
    {
        "issue": "Password reset functionality failure",
        "description": "Several users are unable to successfully reset their account passwords.",
        "severity": "high"
    },
    {
        "issue": "Inventory synchronization service failure",
        "description": "The inventory synchronization service has stopped updating product information since yesterday.",
        "severity": "high"
    },
    {
        "issue": "Intermittent online payment failures",
        "description": "Online payment processing is failing for customers on an intermittent basis.",
        "severity": "critical"
    },
    {
        "issue": "Customer order data loss",
        "description": "Some customer orders are missing from the database.",
        "severity": "critical"
    },
    {
        "issue": "Typographical error in notification",
        "description": "A spelling mistake was identified in one of the notification messages.",
        "severity": "low"
    }
]
