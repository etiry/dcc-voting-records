from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

from config import BASE_URL
from utils.utils import start_headless_driver

def get_next_year(driver):
  current_year = driver.find_element(By.CLASS_NAME, 'current')

  next_year = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(current_year))

  if next_year.text == 'View More':
    # popout = driver.find_element(By.CLASS_NAME, 'popoutBtm')
    return False
  
  next_year.click()
  return True

def get_regular_meeting_links(driver, link_list):
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

def get_minutes_pdfs(url):
  driver = start_headless_driver()
  driver.get(url)
  links = list()

  links = get_regular_meeting_links(driver, links)

  while get_next_year(driver):
    links.extend(get_regular_meeting_links(driver, links))

  driver.quit()

  return links

# print(get_minutes_pdfs(BASE_URL))
