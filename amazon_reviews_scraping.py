# Required modules
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver
driver = webdriver.Chrome()

# Starting with Amazon Sign in page (Necessary)
driver.get("https://www.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=gbflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

time.sleep(1) # Making the process slow to mimic a human to make website know it's not a bot

email = driver.find_element(By.ID, "ap_email")

# Add Amazon email ID at @@@@@@
email.send_keys("@@@@@@")

driver.find_element(By.ID, "continue").click()

time.sleep(1)

password = driver.find_element(By.ID, "ap_password")

# Add AMazon password at xxxxx
password.send_keys("xxxxx")

driver.find_element(By.ID, "signInSubmit").click()

time.sleep(1)

def extract_reviews(product_url, num_reviews_to_scrape=100):
    """
    Function to extract the reviews after going to 'view all reviews' tab.
    Extracts 10 review a time.

    Input: Product URL ending with /asin/ and number of reviews to scrape which is 10*10 = max 100
    Output: List of 10 reviews at a time
    """
    driver.get(product_url)
    time.sleep(2)

    # Looking for 'view all reviews' button
    try:
        
        see_all_reviews_link = driver.find_element(By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]')
        
        driver.execute_script("arguments[0].scrollIntoView(true);", see_all_reviews_link)
        time.sleep(1)  
        see_all_reviews_link.click()
        time.sleep(2)  
        print("Successfully clicked the link!")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    # This block of code extracts the product name for an accurate csv name
    try:
        prod = driver.find_element(By.CSS_SELECTOR, 'a[data-hook="product-link"]')
        product_name = prod.text.strip()[:30]
    except Exception as e:
        print("Exception at:", e)
    
    # Initial empty review list which will be appended after every one pagination
    reviews = []
    while len(reviews) < num_reviews_to_scrape:
        review_elements = driver.find_elements(By.CSS_SELECTOR, '.a-section.review')
        for review_element in review_elements:
            review = {}
            review['author'] = review_element.find_element(By.CSS_SELECTOR, '.a-profile-name').text.strip()
            review['rating'] = review_element.find_element(By.CSS_SELECTOR, 'span.a-icon-alt').get_attribute('innerHTML').strip()[0]
            review['title'] = review_element.find_element(By.CSS_SELECTOR, 'a[data-hook="review-title"]').text.strip()
            review['text'] = review_element.find_element(By.CSS_SELECTOR, '.review-text-content').text.strip()
            review['date'] = review_element.find_element(By.CSS_SELECTOR, '.review-date').text.strip().split('on ', 1)[1]

            reviews.append(review)
            print(review)
            if len(reviews) >= num_reviews_to_scrape:
                break

        # Pagination for viewing more reviews        
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '.a-last a')
            # If 'view more reviews' button exists/clickable
            if next_button.is_displayed():
                next_button.click()
                time.sleep(2)  
            else:
                break
        except NoSuchElementException:
            break  

    driver.quit()
    return reviews, product_name

def export_csv(reviews, product_name):
    """
    A simple list iterater to csv extracting
    """
    csv_filename=f"{product_name}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Author', 'Rating', 'Title',  'Review', 'Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for review in reviews:
            writer.writerow({'Author': review['author'], 'Rating': review['rating'], 'Title': review['title'],  'Review': review['text'], 'Date': review['date']})

# Product URl should end with a /dp/asin/
product_url = "https://www.amazon.co.uk/Samsung-Galaxy-Android-Smartphone-Phantom/dp/B09NRRVPZ7/"

# Calling the function to extract the function
reviews_data, product_name = extract_reviews(product_url, num_reviews_to_scrape=1000)  

# Writing and Exporting the CSV
export_csv(reviews_data, product_name)