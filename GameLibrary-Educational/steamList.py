import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
from requests.sessions import Session
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,local

headers = ["appid", "name", "release_date", "english", "developer", "publisher", "platforms", "required_age", "categories", "genres", "steamspy_tags", "positive_ratings", "negative_ratings", "price", "link", "imglink", "desc"] 
with open('./GameLibrary-Educational/educational_videogames.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    f.close()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome()

# driver = webdriver.Chrome(executable_path='D:\JP\TUP\Software Engineering 2\Data Collection\chromedriver.exe')

driver.get("https://store.steampowered.com/search/?term=education")
# Wait for the page to load
driver.implicitly_wait(50)

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Get page source and pass it to BeautifulSoup
page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

educGamesLinks = []
# Find the links
links = soup.find_all("a", class_="search_result_row")  
print("LEN:", len(links))

for i, link in enumerate(links):
    href = link.get("href")
    educGamesLinks.append(href)
    print(i, href)

thread_local = local()

def get_session() -> Session:
    if not hasattr(thread_local,'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def download_link(url:str):
    session = get_session()
    with session.get(url) as response:
        html_content = response.content

        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Find the relevant elements and extract txhe desired information
        name = soup.find("div", class_="apphub_AppName").get_text(strip=True)
        release_date = soup.find("div", class_="date").get_text(strip=True)

        rows = soup.find_all('tr')

        # Iterate over the rows and check for English language
        for row in range(len(rows)-1):
            # Extract the text from the first column
            # language = row.find("td", class_='ellipsis').get_text(strip=True)
            language = soup.find_all("td", {"class": "ellipsis"})[row].text.replace('\t', '')

            # Check if the language is English
            if 'English' in language:
                english = 1
                break
        else:
            english = 0

        appid = url.split("/")[-3]

        # developer_element = soup.select_one(".dev_row a[href*='/developer/']")

        # developer = developer_element.get_text(strip=True) if developer_element else "N/A"
        # developer = [developer.get_text(strip=True) for developer in soup.select(".dev_row a[href*='/developer/']")]
        developer_element = soup.find("div", class_="dev_row")

        # Extract the developer name
        developers = set()
        developer = developer_element.find_all("a")
        for dev in developer:
            devName = dev.text
            developers.add(devName)

        developers = " / ".join(developers)

        publisher_element = soup.select_one(".game_header_image_ctn a[href*='/publisher/']")
        publisher = publisher_element.get_text(strip=True) if publisher_element else "N/A"


        # # Find the available system platforms
        # platforms = system_requirements.find('div', class_='sysreq_tab')

        # # Extract the platform names
        try:
            system_requirements = soup.find('div', class_='sysreq_tabs')

            available_platforms = [platform.text.replace('\t', '') for platform in system_requirements.find_all('div', class_='sysreq_tab')]
            platforms = set()
            # Print the available system requirements
            for platform in available_platforms:
                if "Windows" in  platform:
                    platforms.add("windows")
                if "macOS" in platform:
                    platforms.add("mac")
                if "Linux" in platform:
                    platforms.add("linux")

            platforms = ";".join(platforms)
        except:
            if soup.find(class_='game_area_sys_req_full') is not None:
                system_requirements = soup.find('div', class_='game_area_sys_req_full')
                platforms = set()
                if "Windows" in  system_requirements.text:
                    platforms.add("windows")
                if "macOS" in system_requirements.text:
                    platforms.add("mac")
                if "Linux" in system_requirements.text:
                    platforms.add("linux")

                platforms = " ".join(platforms)
            elif soup.find(class_='game_area_sys_req_leftCol') is not None:
                system_requirements = soup.find('div', class_='game_area_sys_req_leftCol')
                system_requirements = system_requirements.find('ul', class_='bb_ul')

                platforms = set()

                for platform in system_requirements.find_all('li'):
                    if "Windows" in  platform.text:
                        platforms.add("windows")
                    if "macOS" in platform.text:
                        platforms.add("mac")
                    if "Linux" in platform.text:
                        platforms.add("linux")

                platforms = " ".join(platforms)

        try:
            game_age = soup.find('div', class_='game_rating_icon')
            img_tag = game_age.find('img')
            if img_tag:
                src = img_tag['src']
                filename = src.split('/')[-1]
                age_requirements = filename.split(".")[0]
            else:
                age_requirements = 0
        except:
            age_requirements = 0

        # categories_block = soup.find_all("a", class_="game_area_details_specs_ctn")
        categories = [categories_block.get_text(strip=True) for categories_block in soup.select(".label")]
        categories = ";".join(categories)
        genres = [genre.get_text(strip=True) for genre in soup.select(".details_block a[href*='/genre/']")]
        genres = ";".join(genres)
        tags = [tag.get_text(strip=True) for tag in soup.select(".app_tag")]
        tags = ";".join(tags[:-1])

        positive_ratings_element = soup.find("div", {"class": "summary_section"})
        positive_ratings = int(''.join(filter(str.isdigit, positive_ratings_element.select_one(":nth-child(3)").text))) if positive_ratings_element else 0

        try:
            negative_ratings_element = soup.find("div", {"class": "summary_section"})
            negative_ratings = negative_ratings_element.select_one(":nth-child(2)") if negative_ratings_element else 0
            negative_ratings = str(negative_ratings)

            start_index = negative_ratings.find('data-tooltip-html="') + len('data-tooltip-html="')
            end_index = negative_ratings.find('%')
            negative_ratings_percentage = int(negative_ratings[start_index:end_index])

            # Extract the user reviews
            start_index = negative_ratings.find('of the ') + len('of the ')
            end_index = negative_ratings.find('user reviews for this game are ', start_index)
            user_reviews = negative_ratings[start_index:end_index]
            total_negative_ratings = int(user_reviews.replace(',', '').strip())

            negative_ratings = round(total_negative_ratings / (negative_ratings_percentage / 100)) - positive_ratings
        except:
            negative_ratings = 0

        try:
            price_element = soup.find_all("div", {"class": "game_purchase_action_bg"})[1]
            price = price_element.select_one(":nth-child(1)").text if price_element else 0
            price = float(price[price.find('P')+1:])
        except:
            price = 0

        # Find the image element with the class "game_header_image_full"
        image_element = soup.find("img", class_="game_header_image_full")

        # Extract the source attribute from the image element
        image_src = image_element["src"]

        # Find the game description using the class "game_area_description"
        description = soup.find(class_='game_description_snippet')
        desc = description.get_text().strip()
        # Print the extracted information
        # print("Name:", name)
        # print("Release Date:", release_date)
        # print("English:", english)
        # print("Developer:", developers)
        # print("Publisher:", publisher)
        # print("Platforms:", platforms)
        # print("Age Requirements:", age_requirements)
        # print("Categories:", categories)
        # print("Genres:", genres)
        # print("Tags:", tags)
        # print("Positive Ratings:", positive_ratings)
        # print("Negative Ratings:", negative_ratings)
        # print("Price:", price)

        with open('./GameLibrary-Educational/educational_videogames.csv', 'a', encoding="utf-8", newline='') as f:
            educGame = [appid, name, release_date, english, developers, publisher, platforms, age_requirements, categories, genres, tags, positive_ratings, negative_ratings, price, url, image_src, desc]
            writer = csv.writer(f)
            writer.writerow(educGame) 

def download_all(urls:list) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_link,educGamesLinks)

start = time.time()
download_all(educGamesLinks)
end = time.time()
print(f'download {len(educGamesLinks)} links in {end - start} seconds')