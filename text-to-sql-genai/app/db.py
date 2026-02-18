import os
from databricks import sql
from dotenv import load_dotenv

load_dotenv()

def run_query(query: str):
    connection = None
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        print("Query executed successfully.\n")

        return {
            "columns": columns,
            "data": result
        }

    except Exception as e:
        # 🔍 DEBUG: Print error with SQL
        print("\n********** DATABASE ERROR **********")
        print("Error:", str(e))
        print("Failed SQL:")
        print(query)
        print("************************************\n")
        raise e

    finally:
        if connection:
            connection.close()
