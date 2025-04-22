from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig, SchemaField
from google.api_core.exceptions import NotFound
import io
import json
import os
from typing import List, Dict, Optional

from config import GOOGLE_SERVICE_ACCOUNT

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_SERVICE_ACCOUNT

def get_existing(
    client: bigquery.Client,
    table_id: str
) -> List[str]:
    query = f"""
        SELECT DISTINCT id
        FROM `{table_id}`
    """
    
    query_job = client.query(query)
    result = query_job.result()
    existing_ids = [row.id for row in result]
    
    return existing_ids

def create_table_if_not_exists(
    client: bigquery.Client,
    project_id: str,
    table_id: str,
    schema: List[bigquery.SchemaField]
) -> None:
    """
    Creates a BigQuery table with the given schema if it doesn't already exist.

    Args:
        project_id: GCP project ID.
        dataset_id: BigQuery dataset ID.
        table_name: Name of the table to create.
        schema: List of bigquery.SchemaField objects.
    """
    table_address = f"{project_id}.{table_id}"

    try:
        client.get_table(table_address)
        print(f"Table {table_address} already exists.")
    except NotFound:
        table = bigquery.Table(table_address, schema=schema)
        client.create_table(table)
        print(f"Created table {table_address}.")

def load_to_bigquery(
    data: List[Dict],
    table_id: str,
    project_id: Optional[str] = None,
    schema: Optional[List[SchemaField]] = None,
    write_disposition: str = "WRITE_APPEND"
) -> None:
    """
    Uploads data (list of dicts) to a BigQuery table.

    Args:
        data: List of dictionaries (rows).
        table_id: Full table ID (e.g., 'your_dataset.your_table').
        project_id: Optional GCP project ID.
        schema: Optional list of bigquery.SchemaField objects.
        write_disposition: 'WRITE_APPEND', 'WRITE_TRUNCATE', or 'WRITE_EMPTY'.
    """
    client = bigquery.Client(project=project_id)

    create_table_if_not_exists(client, project_id, table_id, schema)

    existing_ids = get_existing(client, table_id)

    new_data = [
        row for row in data if row["id"] not in existing_ids
    ]
    if not new_data:
        print("No new data to load.")
        return

    job_config = LoadJobConfig(
        write_disposition=write_disposition,
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    json_data = "\n".join(json.dumps(row) for row in new_data)
    json_bytes = io.BytesIO(json_data.encode("utf-8"))

    job = client.load_table_from_file(
        json_bytes,
        table_id,
        job_config=job_config
    )

    job.result()
    print(f"Loaded {job.output_rows} rows to {table_id}.")
