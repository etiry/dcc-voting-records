import hashlib
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def start_headless_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    return driver

def generate_subject_id(subject: str) -> str:
    return hashlib.sha256(subject.encode("utf-8")).hexdigest()[:16]

def generate_motion_id(subject: str, motion_text: str, meeting_date: datetime) -> str:
    raw = f"{subject}|{motion_text}|{meeting_date}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def generate_vote_id(motion_id: str, member: str, meeting_date: datetime) -> str:
    raw = f"{motion_id}|{member}|{meeting_date}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def find_date_in_line(line: str) -> str | None:
    # Match full month name, 1 or 2 digit day, and 4 digit year
    pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}"
    match = re.search(pattern, line)
    if match:
        date_str = match.group(0)
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.date().isoformat()
    return None
