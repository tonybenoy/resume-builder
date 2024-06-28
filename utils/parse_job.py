from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_job_details(link):
    match link:
        case link if "https://www.linkedin.com" in link:
            return get_job_details_linkedin(link)
        case link if "https://meetfrank.com/" in link:
            return get_job_details_meetfrank(link)
        case _:
            raise ValueError("Invalid URL")


def get_job_details_linkedin(link):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(link)
    job_title = driver.find_element(
        By.CSS_SELECTOR,
        ".top-card-layout__title.font-sans.text-lg.papabear\\:text-xl.font-bold.leading-open.text-color-text.mb-0.topcard__title",
    ).text
    org_name = driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link.topcard__flavor--black-link").text
    button = driver.find_element(
        By.CSS_SELECTOR, ".show-more-less-html__button.show-more-less-button.show-more-less-html__button--more.ml-0\\.5"
    )
    button.click()
    job_description = driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup.relative.overflow-hidden").text
    result = {"job_title": job_title, "org_name": org_name, "job_description": job_description, "url": link}
    driver.quit()
    return result


def get_job_details_meetfrank(link):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(link)
    driver.implicitly_wait(10)
    # job_title = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]/h1").text
    # print(job_title)
    button = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".role-read-more"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    driver.execute_script("arguments[0].click();", button)
    job_title = driver.find_element(By.CSS_SELECTOR, ".opening-title").text
    org_name = driver.find_element(By.CSS_SELECTOR, ".company-name").text.split("•")[0]

    job_description = driver.find_element(By.CSS_SELECTOR, ".opening-descriptions").text
    result = {
        "job_title": job_title,
        "org_name": org_name,
        "job_description": job_description,
        "url": driver.current_url,
    }
    driver.quit()
    return result


if __name__ == "__main__":
    print(get_job_details_meetfrank("https://meetfrank.com/jobs/helmes/progress-openedge-developer"))
