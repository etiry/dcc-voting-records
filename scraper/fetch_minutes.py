from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

from config import BASE_URL

def get_next_year(driver):
  current_year = driver.find_element(By.CLASS_NAME, 'current')

  next_year = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(current_year))

  if next_year.text == 'View More':
    # popout = driver.find_element(By.CLASS_NAME, 'popoutBtm')
    return False
  
  next_year.click()
  return True

def get_links(driver, link_list):
  wait = WebDriverWait(driver, 10)

  try:
    minutes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/AgendaCenter/ViewFile/Minutes/"]')))
    for doc in minutes:
      link_list.append(doc.get_attribute('href'))
  except:
    pass
  
  return link_list

def get_minutes_pdfs(url):
  driver = webdriver.Chrome()
  driver.get(url)
  links = list()

  links = get_links(driver, links)

  # while get_next_year(driver):
  #   links.append(get_links(driver, links))

  driver.quit()

  return links

# print(get_minutes_pdfs(BASE_URL))
