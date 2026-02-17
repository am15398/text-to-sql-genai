import os
from databricks import sql
from dotenv import load_dotenv

load_dotenv()

# Set your connection details
SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
ACCESS_TOKEN = os.getenv("DATABRICKS_TOKEN")


def build_prompt(user_question: str) -> str:
    catalog = "healthcare"
    schema = "hmis"

    with sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN
    ) as connection:
        cursor = connection.cursor()

        # ----------------------------
        # Get tables
        # ----------------------------
        cursor.execute(f"""
            SELECT table_name, comment
            FROM {catalog}.information_schema.tables
            WHERE table_schema = '{schema}'
            ORDER BY table_name
        """)
        tables_data = cursor.fetchall()

        tables = {row[0]: row[1] for row in tables_data}

        # ----------------------------
        # Get columns
        # ----------------------------
        cursor.execute(f"""
            SELECT table_name, column_name, data_type, comment
            FROM {catalog}.information_schema.columns
            WHERE table_schema = '{schema}'
            ORDER BY table_name, ordinal_position
        """)
        columns_data = cursor.fetchall()

    # Group columns
    columns = {}
    for table, col, dtype, comment in columns_data:
        if table not in columns:
            columns[table] = []

        col_line = f"- {col} ({dtype})"
        if comment:
            col_line += f": {comment}"

        columns[table].append(col_line)

    # Build schema text
    schema_text = f"""
You are a SQL assistant.

Database: Databricks
Catalog: {catalog}
Schema: {schema}

Tables:
"""

    for table, comment in tables.items():
        schema_text += f"\nTable: {table}\n"
        if comment:
            schema_text += f"Description: {comment}\n"

        for col in columns.get(table, []):
            schema_text += f"{col}\n"

    rules = """
Rules:
- Only generate SELECT queries
- Do not use DELETE, UPDATE, INSERT, DROP, ALTER, or TRUNCATE
- Use fully qualified table names: healthcare.hmis.table_name
- Return only SQL, no explanation
"""

    return f"{schema_text}\n{rules}\nUser question: {user_question}"
