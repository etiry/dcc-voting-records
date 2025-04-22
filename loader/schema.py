from google.cloud.bigquery import SchemaField

Subject = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("title", "STRING"),
    SchemaField("created_at", "TIMESTAMP")
]

Motion = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("subject_id", "STRING"),
    SchemaField("motion_text", "STRING", mode="REQUIRED"),
    SchemaField("meeting_date", "DATE", mode="REQUIRED"),
    SchemaField("created_at", "TIMESTAMP")
]

Vote = [
  SchemaField("id", "STRING", mode="REQUIRED"),
  SchemaField("motion_id", "STRING", mode="REQUIRED"),
  SchemaField("vote", "STRING", mode="REQUIRED"),
  SchemaField("member", "STRING", mode="REQUIRED"),
  SchemaField("created_at", "TIMESTAMP")
]

Member = [
  SchemaField("first_name", "STRING", mode="REQUIRED"),
  SchemaField("last_name", "STRING", mode="REQUIRED"),
  SchemaField("created_at", "TIMESTAMP")
]
