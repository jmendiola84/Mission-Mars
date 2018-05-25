#Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import pprint
import requests
import time
from selenium import webdriver 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:\\Users\\dawzk\\Desktop\\GitHubRepos\\Mission-Mars\\chromedriver.exe'}
    return Browser("chrome", **executable_path)


def scrape_data():
	#browser = webdriver.Chrome('C:\\Users\\dawzk\\Desktop\\GitHubRepos\\Mission-Mars\\chromedriver.exe')

	#Splinter
	browser = init_browser()

	#NASA website news
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)

	html = browser.html
	soup = BeautifulSoup(html, "html.parser")

	#Get the most recent news in the page
	news_title = soup.find(class_="content_title").text
	news_content = soup.find(class_="article_teaser_body").text
	
	
	
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)
	
	browser.click_link_by_partial_text("FULL IMAGE")
	time.sleep(10)
	browser.click_link_by_partial_text("more info")
	time.sleep(10)
	browser.find_by_tag('figure').click()
	
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	
	featured_image_url  = soup.img['src']
	
	
	
	weather_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(weather_url)
	
	weather_html = browser.html
	
	soup = BeautifulSoup(weather_html, 'html.parser')
	
	
	tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
	
	for tweet in tweets:
		try:
		# Identify and return title of listing
			
			mars_weather = str(tweet.text)
	
			# Run only if title, price, and link are available
			if (mars_weather.startswith('Sol')):
				# Print results
				print(mars_weather)
				break
			else:
				continue
	
	
		except Exception as e:
			print(e)
	
	
	
	
	facts_url = "https://space-facts.com/mars/"
	browser.visit(facts_url)
	
	facts_html = browser.html
	soup = BeautifulSoup(facts_html, 'html.parser')
	
	mars_table = soup.find('table', class_="tablepress tablepress-id-mars")
	mars_facts = mars_table.find_all('tr')
	
	key = []
	value = []
	
	for row in mars_facts:
		table_data = row.find_all('td')
		key.append(table_data[0].text)
		value.append(table_data[1].text)
	
	
	
	mars_df = pd.DataFrame({
		"Property": key,
		"Value": value
	})
	
	mars_df
	
	
	mars_facts_html = mars_df.to_html(header = False, index = False)
	mars_facts_html
	
	
	hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemispheres_url)
	
	hemispheres_html = browser.html
	soup = BeautifulSoup(hemispheres_html, 'html.parser')
	
	mars_hemispheres = soup.find_all('h3')
	
	hemisphere_image_urls = []
	
	for row in mars_hemispheres:
		title = row.text
		browser.click_link_by_partial_text(title)
		time.sleep(10)
		
		img_html = browser.html
		soup_h = BeautifulSoup(img_html, 'html.parser')
		
		url_img = soup_h.find('div', class_='downloads').a['href']
		
		img_dict = {}
		img_dict['title'] = title
		img_dict['img_url'] = url_img
		
		hemisphere_image_urls.append(img_dict)
		
		browser.visit(hemispheres_url)
	
	
	mars = {
			"name" : "Mars",
			"news_title": news_title,
			"news_content": news_content,
			"featured_image_url": featured_image_url,
			"mars_weather": mars_weather,
			"mars_facts": mars_facts_html,
			"hemisphere_images": hemisphere_image_urls}
	
	return mars