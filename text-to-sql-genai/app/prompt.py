def build_prompt(user_question: str) -> str:
    schema = """
You are a SQL assistant.

Database: Databricks
Table: ayush_maurya.claims_db.claims

Columns:
- claim_id (string)
- member_id (string)
- amount (double)
- service_date (date)

Rules:
- Only generate SELECT queries
- Do not use DELETE, UPDATE, INSERT, DROP
- Return only SQL, no explanation
"""

    return f"{schema}\nUser question: {user_question}"
