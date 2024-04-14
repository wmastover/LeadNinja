from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time
from urllib.parse import urlparse, urljoin

def scrape_website(url, driver):
    # Function to find all links in the webpage that belong to the same domain
    def find_links(driver, base_url):
        hrefs = [element.get_attribute('href') for element in driver.find_elements(By.XPATH, "//a[@href]")]
        return [href for href in hrefs if href and urlparse(href).netloc == urlparse(base_url).netloc]

    # Function to scrape a webpage for emails and social media links
    def scrape_page(driver, root):
        # Get the source code of the webpage
        page_source = driver.page_source
        
        # Find all emails in the webpage using the email pattern
        # Find all emails in the webpage using the email pattern
        found_emails = re.findall(email_pattern, page_source)
        emails = []
        for email in found_emails:
            if ".png" not in email:
                emails.append(email)

        # Get all links from the webpage
        all_link_elements = driver.find_elements(By.TAG_NAME, 'a')
        all_links = []
        for eachLink in all_link_elements:
            link = eachLink.get_attribute('href')
            if link:
                all_links.append(link)
        
        # Initialize an array to store social media links
        social_links = []
        socialSites = ["facebook.com", "twitter.com", "linkedin.com/in", "linkedin.com/company/" , "instagram.com", "youtube.com", "tiktok.com"]
        # For each social media platform, find all links in the webpage using the platform's pattern
        for link in all_links:
            for site in socialSites:
                if site in link:
                    social_links.append(link)
        
        # Return the found emails and social media links
        return emails if emails else [], social_links if social_links else []
    
    # Setting up the webdriver
  
    base_url = url
    driver.get(base_url)
    time.sleep(5)

    # Patterns for finding emails and social media links
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Variables to store the scraped data
    all_emails = []
    all_social_links = []
    visited_urls = set()
    urls_to_visit = {base_url}

    # Main loop to visit all URLs and scrape data
    # Start the main loop to visit all URLs and scrape data
    loop_count = 0
    priority_links = ['about', 'contact']
    root_url = base_url.rstrip('/').split('/')[-1]
    # Print the root URL for debugging purposes
    print("Root URL: ", root_url)
    
    while urls_to_visit and loop_count < 10:
        # Get the current URL from the set of URLs to visit
        current_url = None
        for url in urls_to_visit:
            if any(link in url for link in priority_links) or root_url in url:
                current_url = url
                break
        if not current_url:
            current_url = urls_to_visit.pop()
        else:
            urls_to_visit.remove(current_url)
        visited_urls.add(current_url)
        # Navigate to the current URL
        driver.get(current_url)

        print(current_url)
        # Wait for the page to load
        time.sleep(5)
        # Scrape the page for emails and social links
        emails, social_links = scrape_page(driver, root_url)
        # Add the found emails to the set of all emails

        for email in emails:
            all_emails.append(email)

        for social_link in social_links:
            all_social_links.append(social_link)
          
        # Find new links in the page
        new_links = find_links(driver, base_url)
        # For each new link, if it has not been visited, add it to the set of URLs to visit
        for link in new_links:
            if link not in visited_urls:
                urls_to_visit.add(link)

        loop_count += 1
    # Close the driver after scraping
    

    # Remove duplicates from all_emails and all_social_links
    all_emails = list(set(all_emails))
    all_social_links = list(set(all_social_links))
    print("Emails: ", all_emails)
    print("Social Links: ", all_social_links)
    # return all_emails, all_social_links
    return all_emails if all_emails else [], all_social_links if all_social_links else []

# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Set to headless mode
# webdriver_service = Service('/usr/local/bin/chromedriver')
# driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# emails, social = scrape_website("https://frontdoor.xyz", driver)

# print(emails)
# print(social)
# # print(scrape_website("https://messageninja.ai"))
# # print(scrape_website("https://haema.co"))

