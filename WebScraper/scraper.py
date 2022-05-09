'''
pip install selenium
pip install re

Download geckodriver from https://github.com/mozilla/geckodriver/releases
and put it in /usr/bin directory
'''

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import sys
import re

def scrape_value_yahoo(stock):
    #Create the url
    url = "https://finance.yahoo.com/quote/" + stock
    #Configure Selenium
    driver = Firefox()
    driver.get(url)
    #Bypass the Cookies wall
    try:
        #Cookie wall
        elem = driver.find_element(by=By.XPATH, value="//div[@class='wizard-body']//button[@name='agree']")
        elem.click()
        #If the redirection doesn't work automatically
        elem = driver.find_element(by=By.XPATH, value="//div[@class='loader-container']//a")
        elem.click()
    except:
        #no cookies wall or no redirection -> so weird, but ok!
        pass

    #Finding Stock market price
    elem = driver.find_element(by=By.XPATH, value="//fin-streamer[@data-symbol='"+stock+"'][@data-field='regularMarketPrice']")
    value = elem.get_attribute("value")
    #Close the browser driver
    driver.close()
    #Return the stock maket price
    return value



def purify_input(input):
    result = re.sub(r'[^a-zA-Z.]', '', input)
    return result.upper()


def main():
    #argument check
    if( len(sys.argv) != 2 ):
        print('Illegal arguments...')
        sys.exit(1)
    #purify input
    stock = purify_input(sys.argv[1])
    #print(stock)
    #scrape stock value
    stock_value = scrape_value_yahoo(stock)
    print(stock_value)

    #save_comment(user_id, stock_name, stock_value, ml_result, reliability)

if __name__ == "__main__":
    main()
