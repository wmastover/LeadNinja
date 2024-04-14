import time
import readCSV
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from getEmailsAndSocials import scrape_website



def getProduct(website):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Set to headless mode
    webdriver_service = Service('/usr/local/bin/chromedriver')
    
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        print(f"Navigating to: {website}")
        driver.get(website)
        time.sleep(5)
    except Exception as e:
        print(f"Error getting website: {e}")

    # get company name
    companyName = ""
    companyTagline = ""
    try:
        companyName = driver.find_element(By.TAG_NAME, "h1").text
        companyTagline = driver.find_element(By.TAG_NAME, "h2").text
    except Exception as e:
        print(f"Error getting company name and tagline: {e}")

    # go to product page
    product_link = None
    try:
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and '/products/' in href:
                product_link = href
                print(f"Navigating to: {product_link}")
                driver.get(product_link)
                time.sleep(4)
                break
    except Exception as e:
        print(f"Error navigating to product page: {e}")
    
    # get company links
    
    companyLink = ""
    try:
        visitCompanyButton = driver.find_element(By.XPATH, "//*[@data-test='product-header-visit-button']")
        href = visitCompanyButton.get_attribute('href')
        companyLink = href 

    except Exception as e:
        print(f"Error getting company links: {e}")

    # navigate to team
    try:
        linkToTeam = driver.find_element(By.LINK_TEXT,'Team').get_attribute('href')
        print(f"Navigating to: {linkToTeam}")
        driver.get(linkToTeam)
    except Exception as e:
        print(f"Error navigating to team: {e}")
    
     # get links to company team members
    try:
        time.sleep(4)
        team_links = []
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if "@" in href and href not in team_links:
                team_links.append(href)
    except Exception as e:
        print(f"Error getting team links: {e}")
    
    # go to each team member
    teamArray = []

    for link in team_links:

        name = ""
        try:
            print(f"Navigating to: {link}")
            driver.get(link)
            time.sleep(3)
            
            name = driver.find_element(By.TAG_NAME, "h1").text
            
        except Exception as e:
            print(f"Error navigating to team member: {e}")
        profileLinksArray = []

        try:
            linksTitle = driver.find_element(By.XPATH, "//*[contains(text(), 'Links')]")

            parentElement = linksTitle.find_element(By.XPATH, "..")
  
            profileLinks = parentElement.find_elements(By.TAG_NAME, 'a')
            
            profileLinksArray = []
            for profileLink in profileLinks:
                href = profileLink.get_attribute('href')
                profileLinksArray.append(href)
            
    
        except Exception as e:
            print(f"Error getting profile links: {e}")
    

        teamArray.append({
                "name": name,
                "link1": link,
                "link2": profileLinksArray[0] if len(profileLinksArray) > 0 else None,
                "link3": profileLinksArray[1] if len(profileLinksArray) > 1 else None,
                "link4": profileLinksArray[2] if len(profileLinksArray) > 2 else None,
            })
        time.sleep(5)



    # scrape websites
    try:
        print(f"Scraping: {companyLink}")
        emails, socials = scrape_website(companyLink, driver)
            
    except Exception as e:
        print(f"Error scraping company website {e}")

    
    profile_details = {
            "team": teamArray,
            "productHuntLink": product_link,
            "companySocial3": socials[2] if len(socials) > 2 else None,
            "companySocial2": socials[1] if len(socials) > 1 else None,
            "companySocial1": socials[0] if len(socials) > 0 else None,
            "companyEmail3": emails[2] if len(emails) > 2 else None,
            "companyEmail2": emails[1] if len(emails) > 1 else None,
            "companyEmail1": emails[0] if len(emails) > 0 else None,
            "companyLink": companyLink,
            "companyTagline": companyTagline,
            "companyName": companyName,
        }
    
    driver.quit()

    return(profile_details)
    # Create a dictionary to store all profile details
   

