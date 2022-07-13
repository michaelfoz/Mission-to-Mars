# Self-note: This file (scraping.py) derives from Mission_to_Mars.ipynb 

# Mission_to_Mars.ipynb--created in Module 10.3.3: Scrape Mars Data: The News (code started)
# Mision_to_Mars.ipynb = Module 10.3.3-->10.3.5: Scrape Mars Data: Mars Facts (code completed)
# Module 10.3.6: Export to Python (code from Mission_to_Mars.ipynb exported to-->scraping.py)



# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup # Use the alias "soup" to simplify code when later referencing
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Note form text about Splinter:
# "Splinter provides us with many ways to interact with webpages. 
# It can input terms into a Google search bar for us and click the Search button, 
# or even log us into our email accounts by inputting a username and password combination."



def scrape_all():
    # Initiate headless driver for deployment/set the executabler path and initialize a browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # Self-note: if you see 'headless=False', it means that all of the brower's actions 
    # will be displayed in a Chrome window so we can see them.
    # **executable_path unpacks the dictionary [we've] stored the path in (e.g., "like unpacking a suitecase")
    # The opened browser will belong to Splinter (for the duration of the coding process)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


# -----------(SELF-NOTES BELOW)-----------

# 10.3.1: Use Splinter
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-1-use-splinter?module_item_id=498524
# Refer to practice.ipynb (this Module starts practice.ipynb file)

    # Self-note: summary of Module
    # (1) Splinter automates the browser, in this module we watch the browser work by running the written code
    #       (versus clicking anywhere on the website or typing in fields such as using a search bar/next button).
    # (2) After Splinter is running, we scrape data using BeautifulSoup
    #       (a) apply practice with HMTL tags
    #       (b) in order to scrape data, we tell BeautifulSoup which HTML tag is being used + if it has a specific class or id
    #           Self note: tutorial on HTML tags found in Module 10.2.2: Using Chrome Developer Tools
    #           https://courses.bootcampspot.com/courses/1225/pages/10-dot-2-2-using-chrome-developer-tools?module_item_id=498511
    #
    # The the code:
    # Libraries/scraping tools:
    #       (a) the Browser instance from splinter
    #       (b) the BeautifulSoup object
    #       (c) ChromeDriverManger (which is the driber object for Chrome)
    #       (d) Use "soup" as an alias to simplify the code when referencing it later
    #       (e) Set the executable path and initialize a broswer
    # When running the code:
    #       (a) An instance of a Splinter browswer is created, meaning we prep the automated browser.
    #       (b) It's specified that Chrome will be used as the browser
    #       (c) An empty page [Chrome] page automatically opens, ready for instructions
    #               (Special message: "Chrome is being controlled by an automated test software."--
    #               the browser belings to Splinter for the duration of coding.)
# ---------------------------------------------------------------------------------------------------------------------------------
# 10.3.2: Practice with Splinter & BeautifulSoup
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-3-scrape-mars-data-the-news?module_item_id=498538
# Refer to practice.ipynb (this module completes practice.ipynb file)

    # Self-note: summary of Module
    # (1) Module provides a practice website for scraping (http://quotes.toscrape.com/)
    # (2) Scrape performed on:
    #       (a) top 10 Tags (use of DevTools by performing right click + selecting 'Inspect', then clicking on the 'Inspect' icon)
    #           (we find that the data is an <h2 /> tag)
    #       (b) title (same process)
    #       (c) all of the tags
    #       (d) across pages (using a for loop)
# ---------------------------------------------------------------------------------------------------------------------------------
# 10.3.3: Scrape Mars Data: The News
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-3-scrape-mars-data-the-news?module_item_id=498538
# Mission_to_Mars.ipynb is first created (that is exported as scraping.py[this file])

    # Self-note: summary of Module
    # (Application of same process in practice.ipynb)
    #
    # In the code:
    # (1) libraries/scraping tools are imported
    # (2) executable path is set
    # (3) instruct Chrome browser to visit the url
    # (4) set up HTML parser
    # (5) .find used to scrape the title
    # (6) .find + .get_text() used to print news_title
    # (7) use parent element to find paragraph text

# 10.3.4: Scrape Mars Data: Featured Image
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-4-scrape-mars-data-featured-image?module_item_id=498545
# Mission_to_Mars.ipynb continued (that is exported as scraping.py[this file])

    # Self-note: summary of Module
    # In the code:
    # (1) a new automated browser visits url (https://spaceimages-mars.com)
    #       (a) click "Full Image" button on website, which directs browser to image slideshow
    #       (b) inspect button's HTML tag/attributes with DevTools
    #       (c) HTML tag = <button>; elemenbt has 2 classes: (1) btn & (2) btn-outline-light
    #       (d) button's string reads "FULL IMAGE"
    #       (e) Use DevTools to search for all 'button' elements
    #       (f) there is a total of 3 buttons; we want to click the full-size image by using the HTML tag in our code
    #       (g) write code to find and click the image button
    # (2) parse resulting html with soup
    # (3) find relative image URL
    #       (a) use same page as automated browser page
    #       (b) activate DevTools-->find image link for [that] image
    #           (note that the value of the 'src' will be different every time the page is updated
    #       (c) DevTools: <img class=="fancybox-image" src="image/featured/mars3.jpg" alt>
    #           (use the image tag and class <img /> and 'fancybox-img' to build the URL to the full-size image)
    #       (d) img_soup.find('img', class='fancybox-image').get('src')
    # (4) add the base URL to our code

# ---------------------------------------------------------------------------------------------------------------------------------
# 10.3.5: Scrape Mars Data: Mars Facts
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-5-scrape-mars-data-mars-facts?module_item_id=498553
# Mission_to_Mars.ipynb continued (that is exported as scraping.py[this file])

    # Self-note: summary of Module
    # (1) DevTools-->all of the data needed is in a <table /> tag
    # (2) break down/name each component


# ---------------------------------------------------------------------------------------------------------------------------------
# 10.3.6: Export to Python
# Mission_to_Mars.ipynb completed (that is exported as scraping.py[this file])
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-3-6-export-to-python?module_item_id=498560

    # Final code from Mision_to_Mars.ipynb exported as scraping.py: 
    # (Commented out, kept in this file for future reference)

    # Comment: First, import libraries
    # Import Splinter, BeautifulSoup, and Pandas
    # from splinter import Browser
    # from bs4 import BeautifulSoup as soup
    # import pandas as pd
    # from webdriver_manager.chrome import ChromeDriverManager

    # Self-note: this has to be done separate/in another cell after importing libraries--per text in Module 10.3.3
    # Comment: Set up Splinter/Use Splinter (this automates the browser for the scrape--scrape will be done via BeautifuLSoup)
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

        # Self-note: if you see 'headless=False', it means that all of the brower's actions 
        # will be displayed in a Chrome window so we can see them.
        # **executable_path unpacks the dictionary [we've] stored the path in (e.g., "like unpacking a suitecase")
        # The opened browser will belong to Splinter (for the duration of the coding process)

    # Comment: Visit the Mars news site
    # url = 'https://redplanetscience.com/'
    # browser.visit(url)

        # Self-note: Assign link to URL, which tells Splinter which site we want to visit

    # Comment: Optional delay for loading the page
    # browser.is_element_present_by_css('div.list_text', wait_time=1)
    
        # Self-note: browser.is_element_present_by_css('div.list_text', wait_time=1 does 2 things:
        #   (1) we're searching for elements with a specific combination of tag (div) and the attribute (list_text)
        #   (2) tells browser to wait 1 second before searching for components
        #           (optional delay is useful because sometimes dynamic pages take a little while to load, esp. if they are image-heavy)
    
    # Comment: Convert the browser html to a soup object and then quit the browser
    # html = browser.html
    # news_soup = soup(html, 'html.parser')

    # slide_elem = news_soup.select_one('div.list_text')
        # Self-note: we assigned slide_elem as the variable to look for the <div /> tag & its descendent/or other tags within the <div /> element.
        #   (1) div = parent element = element that holds all other elements within
        #   (2) we reference this parent element (div) when we want to filter search results even futher
        #   (3) . <-- is used for selecting classes (e.g., list_text)
        #   (4) 'div.list_text' pinpoints the <div /> tag with the class of list_text
        #   (5) CSS works from R to L (examples such as returning the last item on the list instead of the first)
        #   (6) because of this, when using 'select_one' the first matching element returned will be an <li /> element with a class of slide + all nested elements within it

    # Comment: Find the title (10.3.3)
    # slide_elem.find('div', class_='content_title')

    # Comment: Use the parent element to find the first a tag and save it as `news_title` (10.3.3)
    # news_title = slide_elem.find('div', class_='content_title').get_text()
    # news_title

    # Comment: Use the parent element to find the paragraph text (10.3.3)
    # news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    # news_p

    # Heading: ## JPL Space Images Featured Image

    # Comment: Visit URL (10.3.4)
    # url = 'https://spaceimages-mars.com'
    # browser.visit(url)

    # Comment: Find and click the full image button (10.3.4)
    # full_image_elem = browser.find_by_tag('button')[1]
    # full_image_elem.click()

    # Comment: Parse the resulting html with soup (10.3.4)
    # html = browser.html
    # img_soup = soup(html, 'html.parser')

    # Comment: Find the relative image url (10.3.4)
    # img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    # img_url_rel

    # Comment: Use the base url to create an absolute url (10.3.4)
    # img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    # Heading: ## Mars Facts 

    # Comment: Create new DataFrame from the HTML table (10.3.5)
    # df = pd.read_html('https://galaxyfacts-mars.com')[0]
    # df.head()

        # Self-note: 
        # (1) The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
        # (2) By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, 
        # or the first item in the list. 
        # (3) Then, it turns the table into a DataFrame.

    # Comment: Assign columns to the new DataFrame for additional clarity
    # df.columns=['Description', 'Mars', 'Earth']

    # Comment: Turn the Description column into the DataFrame's index (by using .set_index())
    # df.set_index('Description', inplace=True)
    # df

        # Self-note: inplace=True means that the updated index will remain in place
        # (without having to reassign the DataFrame to a new variable)

    # Comment: Pandas function to convert Dataframe back into HTML-ready code:
    # df.to_html()

    # End the session
    # browser.quit()