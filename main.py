from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from bs4 import BeautifulSoup
import base64
from io import BytesIO
from PIL import Image

debug = True # Set True to launch visible browser
scroll_interval = 1 # Interval to fetch each page image
download_books_from = 1 # 何巻からDLするか

base_url = 'https://kids-km3.shogakukan.co.jp'

def get_book_ids(base_url: str = base_url):
    response = request.urlopen(base_url)
    soup = BeautifulSoup(response, features='html.parser')
    response.close()
    thumbnails = soup.find_all('div', class_='thumbnail')
    ids = []
    for thumbnail in thumbnails:
        # thumbnail: ['\n', <a></a>, '\n']
        a = thumbnail.contents[1]
        url = a.get('href')
        id = url.split('/')[-1]
        ids.append(id)
    return ids

def get_page_image(driver, book_id: str, page: int):
    url = f'{base_url}/books/{book_id}?page={page}'
    driver.get(url)
    time.sleep(scroll_interval)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    imgs = soup.find('div', id='book').contents
    if len(imgs) == 0:
        return None
    imageSrc = imgs[0].get('src')
    base64Image = imageSrc.replace('data:image/jpg;base64,', '')
    data = BytesIO(base64.b64decode(base64Image))
    return Image.open(data).convert('RGB')

def get_meta_data(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    title = soup.title.string
    description = soup.find('meta', attrs={
        'name': 'desctiption' # SIC (原文ママ)
    }).get('content')
    return { 'title': title, 'description': description }

if __name__ == '__main__':
    book_ids = get_book_ids()
    options = Options()
    options.add_argument('--window-size=500,750') # portrait
    if not debug:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    for book_id in book_ids[download_books_from-1:]:
        images = []
        for page in range(1, 200):
            try:
                new_images = get_page_image(driver, book_id, page)
            except binascii.Error:
                print('Failed to load correct data. Trying again...')
                new_images = get_page_image(driver, book_id, page)
            if new_images:
                images.append(new_images)
            else:
                meta = get_meta_data(driver)
                main_title = meta['title'].split('|')[0].strip()
                author = meta['title'].split('|')[1].strip()
                break
        images[0].save(f'pdf/{main_title}.pdf',
            save_all = True,
            append_images = images[1:],
            title = main_title,
            author = author)
    driver.quit()