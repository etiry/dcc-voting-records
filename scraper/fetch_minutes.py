from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

from config import BASE_URL, FIRST_YEAR, LAST_YEAR
from utils.utils import start_headless_driver

def generate_urls(first_year, last_year):
    urls = []
    for year in range(first_year, last_year + 1):
        url = f"{BASE_URL}?term=&CIDs=4,&startDate=01/01/{year}&endDate=12/31/{year}&dateRange=&dateSelector="
        urls.append(url)
    return urls

def get_regular_meeting_links(driver, url, link_list):
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        meetings = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'tr.catAgendaRow')))

        for meeting in meetings:
            # Get the meeting title
            title_elem = meeting.find_element(By.CSS_SELECTOR, 'td p a')
            title = title_elem.text.strip()

            # Filter only regular City Council Meetings
            if "City Council Meeting" in title and "Work Session" not in title:
                try:
                    minutes_link = meeting.find_element(By.CSS_SELECTOR, 'td.minutes a')
                    link_list.append(minutes_link.get_attribute("href"))
                except:
                    # If there's no Minutes link, skip
                    continue
    except:
        pass

    return link_list

def get_minutes_pdfs():
  urls = generate_urls(FIRST_YEAR, LAST_YEAR)
  driver = start_headless_driver()
  links = list()

  for url in urls:
    links.extend(get_regular_meeting_links(driver, url, links))

  driver.quit()

  return links

print(get_minutes_pdfs())
