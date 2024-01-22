from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By


class Website:
    def __init__(self, url, d=None):
        # Defining the articles URL
        self.url = f"https://www.nytimes.com{url}"
        self.date = url[1:10]
        # Using BeautifulSoup and Selenium to extract relevant article information
        d.get(self.url)                                     # Loading article in headless browser
        soup = BeautifulSoup(d.page_source, "html.parser")  # Parsing HTML information through BeautifulSoup
        self.title = soup.find('title').getText()
        self.text = '\n'.join([para.getText() for para in soup.findAll("div",
                                                                       class_="css-s99gbd StoryBodyCompanionColumn")
                               ])
        self.authors = [auth.getText() for auth in soup.findAll('a', class_="css-n8ff4n e1jsehar0")]
        del soup

    def printText(self):
        print(f"{self.title}\n")
        print(f"{self.text}\n")


def returnArticles(num: int, keyword: str):
    # Creating Selenium browser
    options = webdriver.FirefoxOptions()  # Creating a settings object for browser
    options.add_argument("-headless")  # Hiding browser window (aka running headless)
    driver = webdriver.Firefox(options=options)  # Creating browser instance with options

    # Defining starting URL and loading it in our browser
    url = f"https://www.nytimes.com/search?dropmab=false&query={keyword}&sort=best&types=article"
    try:
        driver.get(url)
    except Exception:
        return None

    # Isolate new article loading button on search page
    button = driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div/div[2]/div[3]/div/button")

    # Click button 'n' times to load n*10 total articles
    for i in range(int((num / 10) - 1)):
        button.click()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []  # Find all elements with the tag <a>
    websites = []
    for hyperlink in tqdm(soup.find_all("a")):
        link = hyperlink.get("href")
        if "?searchResultPosition" in link and link[0] == '/':
            # print("Link:", link)
            websites.append(Website(link, driver))
    driver.close()

    return websites
