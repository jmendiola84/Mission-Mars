#Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import pprint
import requests
import time
import datetime
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def init_browser():
    #path to the chromedriver
    executable_path = {'executable_path': 'C:\\Users\\dawzk\\Desktop\\GitHubRepos\\Mission-Mars\\chromedriver.exe'}
    return Browser("chrome", **executable_path)


def scrape_data():
	#Splinter
	browser = init_browser()
	
	#News Scraping
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)

	html = browser.html
	soup = BeautifulSoup(html, "html.parser")

	#Get most recent news title and content
	news_title = soup.find(class_="content_title").text
	time.sleep(5)
	news_content = soup.find(class_="article_teaser_body").text
	print(str(datetime.datetime.now()) + " - Scraped News Title: " + str(news_title))
	print(str(datetime.datetime.now()) + " - Scraped News Content: " + str(news_content))
	
	#Image Scraping
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)
	time.sleep(3)
	browser.click_link_by_partial_text("FULL IMAGE")
	time.sleep(7)
	#Move to the next image
	actions = ActionChains(browser.driver)
	time.sleep(4)
	actions.send_keys(Keys.ARROW_RIGHT)
	actions.perform()
	time.sleep(5)
	browser.click_link_by_partial_text("more info")
	time.sleep(3)
	browser.click_link_by_partial_href("spaceimages/images/largesize")
	time.sleep(3)
	
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	
	#Get image
	featured_image_url  = soup.img['src']
	print(str(datetime.datetime.now()) + " - Scraped Image URL: " + str(featured_image_url))
	
	#Weather Scraping
	weather_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(weather_url)
	
	weather_html = browser.html
	soup = BeautifulSoup(weather_html, 'html.parser')
	
	tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
	#Loop through Twitter account to find the most recent post related to Mars weather
	for tweet in tweets:
		try:
			# Identify tweet text
			mars_weather = str(tweet.text)
	
			# Run only if tweet text starts with "Sol" like all the tweets related with weather
			if (mars_weather.startswith('Sol')):
				# Print results
				print(str(datetime.datetime.now()) + " - Scraped Weather Report: " + str(mars_weather))
				break
			else:
				continue
	
	
		except Exception as e:
			print(e)
	
	
	
	#Info Table Scraping
	facts_url = "https://space-facts.com/mars/"
	browser.visit(facts_url)
	
	facts_html = browser.html
	soup = BeautifulSoup(facts_html, 'html.parser')
	
	mars_table = soup.find('table', class_="tablepress tablepress-id-mars")
	mars_facts = mars_table.find_all('tr')
	
	key = []
	value = []
	
	#Loop to append all table data into Key and Value lists
	for row in mars_facts:
		table_data = row.find_all('td')
		key.append(table_data[0].text)
		value.append(table_data[1].text)
		print(str(datetime.datetime.now()) + " - Scraped Table Data: " + str(table_data[0]))
		print(str(datetime.datetime.now()) + " - Scraped Table Data: " + str(table_data[1]))


	
	#Create dataframe with values collected
	mars_df = pd.DataFrame({
		"Property": key,
		"Value": value
	})
	
	
	#Convert into HTML
	mars_facts_html = mars_df.to_html(header = False, index = False)	

	#Hemisphere Images Scraping
	hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemispheres_url)
	
	hemispheres_html = browser.html
	soup = BeautifulSoup(hemispheres_html, 'html.parser')
	
	mars_hemispheres = soup.find_all('h3')
	
	hemisphere_image_urls = []
	#Loop to scrap all hemispheres
	for row in mars_hemispheres:
		title = row.text
		browser.click_link_by_partial_text(title)
		time.sleep(3)
		
		img_html = browser.html
		soup_h = BeautifulSoup(img_html, 'html.parser')
		
		url_img = soup_h.find('div', class_='downloads').a['href']
		print(str(datetime.datetime.now()) + " - Scraped Hemisphere Name :" + str(title))
		print(str(datetime.datetime.now()) + " - Scraped Hemisphere URL :" + str(url_img))
		
		img_dict = {}
		img_dict['title'] = title
		img_dict['img_url'] = url_img
		
		hemisphere_image_urls.append(img_dict)
		
		browser.visit(hemispheres_url)
	
	print(str(datetime.datetime.now()) + " - Creating dictionary with retrieved information...")
	#Save all the scraped data in a dictionary
	mars = {
			"name" : "Mars",
			"news_title": news_title,
			"news_content": news_content,
			"featured_image_url": featured_image_url,
			"mars_weather": mars_weather,
			"mars_facts": mars_facts_html,
			"hemisphere_images": hemisphere_image_urls}
	
	print(str(datetime.datetime.now()) + " - Dictionary created!")

	return mars