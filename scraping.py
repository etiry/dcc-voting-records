from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

driver = webdriver.Chrome()
url = "https://www.durhamnc.gov/AgendaCenter/City-Council-4"

def get_next_year():
  current_year = driver.find_element(By.CLASS_NAME, 'current')

  next_year = driver.find_element(locate_with(By.TAG_NAME, 'a').to_right_of(current_year))

  if next_year.text == 'View More':
    # popout = driver.find_element(By.CLASS_NAME, 'popoutBtm')
    return False
  
  next_year.click()
  return True

def get_links(link_list):
  wait = WebDriverWait(driver, 10)

  try:
    minutes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/AgendaCenter/ViewFile/Minutes/"]')))
    for doc in minutes:
      link_list.append(doc.get_attribute('href'))
  except:
    pass
  
  return link_list

def scrape(url):
  driver.get(url)
  links = list()

  links = get_links(links)

  while get_next_year():
    links.append(get_links(links))

  return links

agenda_links = scrape(url)

print(agenda_links)


# Close the browser window
driver.quit()