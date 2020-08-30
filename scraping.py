# pip install bs4

# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup 
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executiable path and initialize the chrome browser in splinter 
    executable_path = {'executable_path':'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    browser = Browser('chrome', **executable_path)

    news_title, news_paragraph = mars_news(browser)
    
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "last_modified":dt.datetime.now()
    }
    #Close the browser
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # <body> We want to collect the most recent news article along with its summary from 
        # this particular website. Remember, the code for this will eventually be used in an application 
        # that will scrape live data with the click of a button—this site is dynamic and the articles will 
        # change frequently, which is why  removing the manual task of retrieving each new article is 
        # necessary.</body>
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p


#  Above step could provide summary

# ### Work on Featured Image

# Visit URL
def fearuted_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None, None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url


# ### Extract Facts
def mars_facts():
    #Add try/except for error handling
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    #Assigning columns & set index of df
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    #Convert datafram into HTML add bootstrap
    return df.to_html(classes="table table-striped")


if __name__=="__main__":
    
    print(scrape_all())
    
    
    
    