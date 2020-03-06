#we can borrow most of the code from the jupyter notebook
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

executable_path = {"executable_path": r"C:/bin/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    all_data = {}
    output = marsnews()
    all_data["mars_news"] = output[0]
    all_data["mars_paragraph"] = output[1]
    all_data["mars_image"] = marsimage()
    all_data["mars_weather"] = marsweather()
    all_data["mars_facts"] = marsfacts()
    all_data["mars_hemisphere"] = marshemisphere()
    return all_data

def marsnews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    content = soup.find("div", class_='list_text')
    news_title = content.find("div", class_="content_title").text
    news_p = content.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

def marsimage():
    source_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(source_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find_all("img")[3]["src"]
    featured_image_url = f"https://www.jpl.nasa.gov/{image}"
    return featured_image_url

def marsweather():
    

    return mars_weather

def marsfacts():
    space_facts_url = "https://space-facts.com/mars/"
    browser.visit(space_facts_url)
    mars_data = pd.read_html(space_facts_url)
    mars_data_df = pd.DataFrame(mars_data[0])
    mars_data_df.columns = ["Description", "Values"]
    mars_data_df = mars_data_df.set_index("Description")
    mars_facts = mars_data_df.to_html(header = True, index = True)
    return mars_facts

def marshemisphere():
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []
    results = soup.find("div", class_ = "result-list")
    hemispheres = results.find_all("div", class_ = "item")

    for hemi in hemispheres:
        title = hemi.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemi.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere
