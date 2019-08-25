import numpy as np
import pandas as pd 
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser


def initBrowser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)
    

def scrape(url):
    browser = initBrowser()
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    browser.quit()
    return soup

    
def scrape_mars_news():
    url = 'https://mars.nasa.gov/news/'
    soup = scrape(url)
    
    slides = soup.find_all('li', class_='slide')
    
    for slide in slides:
        title = slide.find('div', class_="content_title").text
        text = slide.find('div', class_="article_teaser_body").text
     
    return title, text

def scrape_jpl_images():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    soup = scrape(url)
    
    featured_image = soup.find('article', class_='carousel_item')
    image_path = featured_image.a['data-fancybox-href']
    featured_image_url = f"https://www.jpl.nasa.gov{image_path}"
    
    return featured_image_url

def scrape_mars_weather():
    url = 'https://twitter.com/marswxreport?lang=en'
    soup = scrape(url)
    
    tweet_raw = soup.find('p', class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    tweet = tweet_raw.contents[0]
    tweet = tweet.replace('\n', ' ')
    
    return tweet

def scrape_facts():
    url = 'https://space-facts.com/mars/' 
    mars_data = pd.read_html(url)
    mars_data = pd.DataFrame(mars_data[1])
    mars_facts = mars_data.to_html(header = False, index = False)

    return mars_facts

def scrape_hemisphere(): 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    soup = scrape(url)
    
    mars_hemispheres = soup.find_all('h3')
    hemisphere_titles = [hemisphere.text.replace(' Enhanced', '') for hemisphere in mars_hemispheres]
    
    hemisphere_url_base = 'https://astrogeology.usgs.gov'
    url_path = soup.find_all('div', class_='description')
    hemisphere_url_path = [hemisphere_url_base + path.a['href'] for path in url_path]
    
    hemisphere_img_url = []
    for url in hemisphere_url_path:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find('li')
        hemisphere_img_url.append(results.a['href'])
    
    hemisphere_dict= [{"title": hemisphere_titles[i], "img_url": hemisphere_img_url[i]} for i in range(len(hemisphere_img_url))]

    return hemisphere_titles, hemisphere_img_url, hemisphere_dict



def scrape_results():
    print("scraping Mars news")
    title, text = scrape_mars_news()
    print("scraping JPL images")
    featured_img_url = scrape_jpl_images()
    print("scraping Twitter weather")
    tweet = scrape_mars_weather()
    print("scraping facts")
    mars_facts = scrape_facts()
    print("scraping Mars hemisphere")
    hemisphere_titles, hemisphere_img_url, hemisphere_dict = scrape_hemisphere()

    results = {
        "news_title": title, 
        "news_teaser": text,
        "featured_img_url": featured_img_url,
        "mars_weather": tweet, 
        "mars_facts": mars_facts,
        "hemisphere_title": hemisphere_titles,
        "hemisphere_dict": hemisphere_dict
    }

    
    return results
    
    
    


