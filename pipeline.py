from scraper.fetch_minutes import get_minutes_pdfs
from extractor.extract_text import extract_contents
from loader.load_data import load_to_bigquery
from loader.schema import Subject, Motion, Vote
from config import BASE_URL, PROJECT_ID, SUBJECT_TABLE_ID, MOTION_TABLE_ID, VOTE_TABLE_ID

def run_pipeline():
    for url in get_minutes_pdfs(BASE_URL):
        print(f'Extracting {url}...')
        extracted_text = extract_contents(url)
        print(f'Uploading to BigQuery...')
        load_to_bigquery(
            data=extracted_text['subjects'],
            table_id=SUBJECT_TABLE_ID,
            project_id=PROJECT_ID,
            schema=Subject
        )
        load_to_bigquery(
            data=extracted_text['motions'],
            table_id=MOTION_TABLE_ID,
            project_id=PROJECT_ID,
            schema=Motion
        )
        load_to_bigquery(
            data=extracted_text['votes'],
            table_id=VOTE_TABLE_ID,
            project_id=PROJECT_ID,
            schema=Vote
        )
        print(f'Finished processing {url}.')

if __name__ == '__main__':
    run_pipeline()
