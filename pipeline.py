from scraper.fetch_minutes import get_minutes_pdfs
from extractor.extract_text import extract_contents
from loader.load_data import load_to_bigquery
from utils.utils import get_filename_from_url
from config import BASE_URL, TABLE_ID

def run_pipeline():
    for url in get_minutes_pdfs(BASE_URL):
        print(f'Extracting {url}...')
        extracted_text = extract_contents(url)
        print(f'Uploading to BigQuery...')
        filename = get_filename_from_url(url)
        load_to_bigquery(TABLE_ID, filename, extracted_text)

if __name__ == '__main__':
    run_pipeline()
