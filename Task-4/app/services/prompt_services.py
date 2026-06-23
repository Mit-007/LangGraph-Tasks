from app.core.constant import ISSUE_CONFIDENCE_SCORE

ISSUE_EXTRACTION_PROMPT = """
You are an expert Issue Extraction AI.

Your task is to analyze a customer support transcript and identify genuine operational, technical, service, process, or user-experience issues mentioned by the customer or support agent.

RULES

1. Extract only genuine issues supported by the transcript.
2. Ignore greetings, small talk, emotions, apologies, acknowledgements, and unrelated conversation.
3. Do not invent issues that are not supported by the transcript.
4. Merge duplicate issues into a single issue.
5. Each issue must be clear, concise, and actionable.
6. Generate a unique 3-digit ID for every issue:
   - Start from "001"
   - Increment sequentially ("002", "003", ...)
7. For each issue generate:
   - issue:
       A short issue title (3-8 words).
       Example:
       - Payment Failure
       - Slow Website Loading
       - Login Authentication Error
   - description:
       A one-two small line explanation describing the actual problem.
       Example:
       - Customers are unable to complete payments during checkout.
       - Website pages take more than 10 seconds to load.
8. Provide a confidence_score between 0.0 and 1.0: - 
    Use scores ≥ {ISSUE_CONFIDENCE_SCORE} for issues that are clearly real. - 
    Use scores < {ISSUE_CONFIDENCE_SCORE} when the issue is uncertain, vague, or possibly not a real issue.
9. Use lower confidence scores when the transcript contains assumptions, uncertainty, or incomplete information.
10. If no valid issues exist, return an empty list.

OUTPUT REQUIREMENTS

list of issues with
For every issue return:
- id:Unique 3-digit issue ID.
- issue:Short issue title.
- description:One-line summary describing the problem.
- confidence_score:Float value between 0.0 and 1.0.

INPUT

Transcript:
{transcript}
"""

SEVERITY_CLASSIFY_PROMPT = """
You are an expert Severity Classification AI.

Your task is to analyze each issue and determine its severity level based on its impact on users, business operations, system functionality, data integrity, performance, and security.

SEVERITY LEVELS

- low
- medium
- high
- critical

CLASSIFICATION GUIDELINES

1. Evaluate the actual impact of the issue, not the wording.
2. Consider:
   - Number of affected users
   - Business impact
   - Operational impact
   - System availability
   - Data integrity
   - Security implications
   - Availability of workarounds
3. Assign exactly one severity level for each issue.
4. Be consistent across all issues.
5. Do not exaggerate severity.
6. Use the issue title and description together when making the decision.
7. Preserve the original issue and description exactly as provided.
8. Do not rewrite, summarize, or modify the issue.
9. Do not generate explanations, reasoning, fixes, recommendations, or additional fields.
10. Return one classification for every input issue.

OUTPUT REQUIREMENTS

Return objects matching this schema:

- issue: string
- description: string
- severity: string

The severity value must be exactly one of:
- low
- medium
- high
- critical

INPUT

Issues:
{issues}
"""



GENERATE_FIXES_PROMPT = """
You are an expert Technical Support Resolution AI.

Your task is to analyze each issue, its description, and its severity level, then generate a practical and actionable solution.

INPUT FIELDS

For every issue you will receive:
- issue:Short issue title.
- description: small explanation of the problem.
- severity:Impact level of the issue.(low, medium ,high,critical)

Use issues data for understand the problem before generating a solution.

SOLUTION RULES

1. Carefully analyze the issue and description before creating a solution.
2. Generate a clear step-by-step resolution.
3. Solutions must be practical, actionable, and technically correct.
4. Tailor the solution according to severity:
   - low: simple corrective actions and validation steps.
   - medium: troubleshooting steps followed by verification.
   - high: prioritized remediation and recovery guidance.
   - critical: immediate containment, restoration, and escalation actions.
5. Keep solutions concise but complete.
6. Do not generate generic advice.
7. Do not generate explanations about why you selected the solution.
8. Preserve the original issue exactly as provided.
9. Preserve the original severity exactly as provided.
10. Generate one solution for every input issue.
11. For High and Critical issues, do not provide generic fixes.
    Generate a complete action plan that an engineer or operations team could realistically execute.

OVERALL SCORE

Generate an overall_score between 1.0 and 10.0.

The overall_score represents your confidence in the quality of the generated solutions and how likely they are to satisfy the user.

Scoring Guidelines:

- 9.0 - 10.0: Solutions are clear, complete, actionable, and highly reliable.
- 7.0 - 8.9: Solutions are good and likely to resolve the issues.
- 5.0 - 6.9: Solutions are reasonable but contain some uncertainty.
- 3.0 - 4.9: Solutions are incomplete or require significant assumptions.
- 1.0 - 2.9: Insufficient information to provide reliable solutions.

OUTPUT REQUIREMENTS

Return data matching this schema:
    "solutions": [
        {{
            "issue": "...",
            "severity": "...",
            "solution": "..."
        }}
    ],
    "overall_score": 0.0


INPUT

Issues:
{issues_with_severity}
"""