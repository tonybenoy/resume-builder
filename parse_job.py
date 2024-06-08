from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_job_details_linkedin(link):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(link)
    job_title = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title.font-sans.text-lg.papabear\\:text-xl.font-bold.leading-open.text-color-text.mb-0.topcard__title").text
    org_name = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link.topcard__flavor--black-link").text
    button = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__button.show-more-less-button.show-more-less-html__button--more.ml-0\\.5")
    button.click()
    job_description = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup.relative.overflow-hidden").text
    result = {
        "job_title": job_title,
        "org_name": org_name,
        "job_description": job_description,
        "url": link
    }
    driver.quit()
    return result
