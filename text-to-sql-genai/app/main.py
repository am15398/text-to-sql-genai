from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.models import PromptRequest
from app.llm import generate_sql
from app.db import run_query

load_dotenv()

app = FastAPI()

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")


@app.post("/query")
def query_data(request: PromptRequest):
    try:
        sql = generate_sql(request.question)

        # Guardrail: only allow SELECT
        if not sql.lower().startswith("select"):
            raise Exception("Only SELECT queries are allowed")

        result = run_query(sql)

        return {
            "generated_sql": sql,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
