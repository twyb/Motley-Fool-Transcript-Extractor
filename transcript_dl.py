from bs4 import BeautifulSoup
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import os

#Function to create Beautiful Soup object 
def make_soup(url):

    #User agent to be used 
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
                "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
                "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0",
                "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5",
                "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
                "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0"]

    headers={'User-Agent':user_agent[random.randint(0, len(user_agent) - 1)],} 
    req = urllib.request.Request(url,None,headers)
    try:
        html = urllib.request.urlopen(req)
        read_html = html.read()
        soup = BeautifulSoup(str(read_html, "utf-8"), "html5lib")
        return soup
    except:
        return None

#Web Crawler Setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path="Chrome/chromedriver.exe", options = chrome_options)

#Getting Ticker Transcripts
ticker_list = ['BIDU', 'LOPO', 'JD'] #For Input Can be Modified

#List to put tickers that can't be found
ticker_unfound = []
fool = 'https://www.fool.com/'

#Message to Show start of Transcript Extraction
print("------------------------------------------------------------")
print('Starting Transcript Extraction')
print("------------------------------------------------------------")
print()

#Access main Website
driver.get(fool)

#Go through each ticker to be used
for ticker in ticker_list:

    print("------------------------------------------------------------")
    print('Current ticker: ' + str(ticker))
    print("------------------------------------------------------------")
    print()

    #List to store all URLs
    transcript_urls = []

    # Search for the search input
    search_input = driver.find_elements_by_name('query')[0]

    # Search for the intended ticker (Slowed down the input into the search bar as Fool's HTTP response to quick inputs may not yield intended results)
    for character in ticker:
        search_input.send_keys(character)
        time.sleep(0.3)

    driver.implicitly_wait(5)

    #Check if any results appear
    try:
        search_results = driver.find_element_by_css_selector('.ticker-input-results-result')

        #Sleep to ensure object appears before clicking it
        time.sleep(3)

        #Click the object
        driver.find_element_by_css_selector('.ticker-input-results-result').click()

    except:
        search_results = None

    #Check results exist and perform extraction
    if(search_results is not None):

        #Click on the Earnings Tab
        earnings_tab = driver.find_element_by_id('earnings').click()

        #Getting all the WebElements with the transcript URLs
        transcript_webelements = driver.find_elements_by_css_selector("#quote_page_earnings_listing>.quote-page-list-content >div >article> div > a")

        #Getting all the transcript URLs and append them into a list
        for transcript_webelement in transcript_webelements:
            
            #Retrieve the href for each of the WebElement and append to the transcript list
            transcript_urls.append(transcript_webelement.get_attribute('href'))

        #Create a Folder to store all the Transcripts to be used in a Dataframe later
        try:
            path = 'Transcripts/' + ticker
            os.makedirs(path)
        except:
            pass

        #Go through each transcript URLs to download the info
        for transcript_url in transcript_urls:
            
            #Sleep to prevent crawler from getting banned
            time.sleep(5)

            #Create the soup object to extract the content
            transcript_soup = make_soup(transcript_url)
            
            #For each URL, download the transcript in a HTML file
            transcript = transcript_soup.select('#article-1 > div.main-col')

            #Labelling the file
            file_name = path + '/' + transcript_soup.select('#article-1 > section > header > h1')[0].text + '.html'

            #Downloading the files
            with open(file_name, 'w') as f:
                f.write(str(transcript[0]))

            #Message to notify on progress
            print('Downloaded Successfully: ' + transcript_soup.select('#article-1 > section > header > h1')[0].text)

    else:
        #Tickers that can't be found
        ticker_unfound.append(ticker)

        #Clear the search bar 
        search_input.clear()

        pass
    
#Message to Notify that the extraction has been completed
print("------------------------------------------------------------")
print('Transcript Extraction is Completed')
print("------------------------------------------------------------")
print("Following Tickers can't be found: " + str(ticker_unfound))
print("------------------------------------------------------------")

#Stop Crawler
driver.close()