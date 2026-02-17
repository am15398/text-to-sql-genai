from fastapi import FastAPI
from app.db import get_connection
from app.models import Claim

app = FastAPI()

TABLE_NAME = "ayush_maurya.claims_db.claims"  # change to your catalog.schema.table


@app.get("/")
def health():
    return {"status": "API running"}


@app.post("/insert")
def insert_claim(claim: Claim):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    INSERT INTO {TABLE_NAME}
    (claim_id, member_id, amount)
    VALUES (?, ?, ?)
    """

    cursor.execute(query, (
        claim.claim_id,
        claim.member_id,
        claim.amount
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "inserted", "claim_id": claim.claim_id}


@app.put("/update")
def update_claim(claim: Claim):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
    UPDATE {TABLE_NAME}
    SET amount = ?
    WHERE claim_id = ?
    """

    cursor.execute(query, (
        claim.amount,
        claim.claim_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "updated", "claim_id": claim.claim_id}


@app.get("/claims")
def get_claims():
    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM {TABLE_NAME} LIMIT 20"
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return result
