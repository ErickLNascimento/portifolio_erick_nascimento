import concurrent.futures
import pandas as pd

from concurrent.futures import ProcessPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from transformers import pipeline

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")
chromedriver_path = 'F:\\Download\\chromedriver-win64\\chromedriver.exe'
urlarray = [
    'https://github.com/collections/machine-learning',
    'https://minilua.net/',
]


def create_webdriver():
    service = Service(chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_option)


def scrape_url(url):
    new_browser = create_webdriver()
    new_browser.get(url)

    project = new_browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed'] | //div[@class='item-details']")

    data_list = {}
    proj_name = ''
    proj_url = ''
    for element in project:
        if element.tag_name == 'h1' and 'h3 lh-condensed' in element.get_attribute('class'):
            proj_name = element.text
            proj_url = element.find_element(By.XPATH, ".//a").get_attribute('href')
        elif element.tag_name == 'div' and 'item-details' in element.get_attribute('class'):
            proj_name = element.text
            proj_url = element.find_element(By.XPATH, ".//a").get_attribute('href')

        data_list[proj_name] = proj_url

    new_browser.quit()
    return data_list


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        future_results = {executor.submit(scrape_url, url) for url in urlarray}

    results = []
    for future in concurrent.futures.as_completed(future_results):
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            print(f"An error occurred: {e}")

    combined_scraped = {}
    for result in results:
        combined_scraped.update(result)

    project_df = pd.DataFrame.from_dict(combined_scraped, orient='index')
    project_df['project_name'] = project_df.index
    project_df.columns = ['project_url', 'project_name']
    project_df = project_df.reset_index(drop=True)

    project_df.to_csv('list_csv\\combined_scraped_data.csv')

    text = list(combined_scraped.keys())
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    sentimental_rating = {}
    for i in range(len(text)):
        resultados = sentiment_pipeline(str(text[i]))
        result = resultados[0]
        feelings = result['label']
        if (feelings == "1 star") or (feelings == "2 stars"):
            feelings = "Inappropriate Content"

        elif feelings == "3 stars":
            feelings = "Content Neutral"
        else:
            feelings = "Free Content"

        sentimental_rating[i] = str(text[i]) + ": " + feelings

    project_toxicity = pd.DataFrame.from_dict(sentimental_rating, orient='index')

    project_toxicity.to_csv('list_csv\\result_for_toxicity.csv')
