import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as BS


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", executable_path, headless = False)



def scrape():
    browser = init_browser()
    mars = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)
    
    html = browser.html
    soup = BS(html, 'html.parser')

    
    mars["top_art"] = soup.find('li', class_="slide").find('div', class_="content_title").text
    mars["para_art"] = soup.find('li', class_="slide").find('div', class_="article_teaser_body").text

    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    browser.click_link_by_partial_text('.jpg')
    time.sleep(1)

    html = browser.html
    soup = BS(html, 'html.parser')
    mars["featured_image"] = soup.find('img')['src']

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    
    data = pd.read_html(url)
    mars_df = data[0]
    mars_df = mars_df.rename(columns={0: "Info Type", 1: "Info"})
    mars_df = mars_df.set_index("Info Type")
    mars["table"] = mars_df.to_html()
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BS(html, "html.parser")
    hem = soup.find_all('div', class_='item')

    link_list = []
    for h in hem:
        first_link = h.find('a')['href']
        link_list.append(first_link)

    url_2 = "https://astrogeology.usgs.gov"
    hem_img_list = []

    for l in link_list:
        url = url_2 + l
        browser.visit(url)
    
        html = browser.html
        soup = BS(html, 'html.parser')
    
        img_url = soup.find('div', class_="downloads").find('a')["href"]
        title = soup.find('section', class_="block metadata").find('h2', class_="title").text
    
        url_dict = {}
        url_dict["title"] = title
        url_dict["img_url"] = img_url
        hem_img_list.append(url_dict)
    
    mars["hemispheres"] = hem_img_list
    
    browser.quit()
    
    return mars

