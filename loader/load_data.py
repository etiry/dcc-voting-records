from google.cloud import bigquery
import os
from datetime import datetime, timezone

from config import GOOGLE_SERVICE_ACCOUNT

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_SERVICE_ACCOUNT

client = bigquery.Client()

def load_to_bigquery(table_id, file_name, extracted_text):
    row = {
        "file_name": file_name,
        "text": extracted_text,
        "date_created": datetime.now(timezone.utc).isoformat()
    }
    errors = client.insert_rows_json(table_id, [row])
    if errors:
        print("Errors inserting row:", errors)
    else:
        print("Inserted row into BigQuery.")
