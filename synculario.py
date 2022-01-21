import pandas as pd
from bs4 import BeautifulSoup
import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from browser_handler import BrowserHandler


def get_synculario_offers() -> pd.DataFrame:

    link = "https://synculario.odoo.com/academyjobs"
    base_url = "https://synculario.odoo.com"

    browser_handler = BrowserHandler(True)
    browser_handler.set_driver()
    browser_handler.get_url(link)

    pause = 1
    pages = []
    while True:
        time.sleep(pause)
        pagination = browser_handler.find_elements((By.CSS_SELECTOR, ".page-item"))
        element = pagination[len(pagination)-1]
        pages.append(browser_handler.get_driver.page_source)
        try:
            browser_handler.scroll_to_given_element(element)
            element.click()
        except ElementClickInterceptedException:
            break

    browser_handler.quit_driver()
    data = []
    for html in pages:
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.findAll("div", attrs="job-list")
        for row in rows:
            job_title = row.find_all("h2")
            link = row.find_all("a", attrs="button-read2")
            location = row.find_all("h5")
            job_type = row.find_all("li", "company")
            pay_rate = row.find_all("li", "job-type temporary")
            data.append([str(job_title[0].text).strip(), f"{base_url}{link[0]['href']}", "synculario", str(location[0].text).strip(), "", str(job_type[0].text).strip().replace("Contract type:\n", ""), "", str(pay_rate[0].text).strip().replace("Salary:\n\n", ""), ""])
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data, columns=['job_title', 'url', 'agency', 'location', 'job_type', 'emp_type', 'pay_interval', 'pay_rate', 'start_length'])
    return df

if __name__ == '__main__':
    print(get_synculario_offers())