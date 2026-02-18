import os
from groq import Groq
from dotenv import load_dotenv
from app.prompt import build_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question: str) -> str:
    prompt = build_prompt(question)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You generate SQL queries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Clean SQL output
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Extract only SELECT part
    if "select" in sql.lower():
        sql = sql[sql.lower().index("select"):]

    return sql
