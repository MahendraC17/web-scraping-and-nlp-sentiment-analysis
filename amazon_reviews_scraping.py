# Importing all the required libraries
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Replace the Amazon link below with your login URL
driver.get("https://www.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=gbflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

time.sleep(1) # Wait for a few seconds to ensure the page loads completely

email = driver.find_element(By.ID, "ap_email")

# Replace the xxx with your Amazon email
email.send_keys("choudharymahendra183@gmail.com")

driver.find_element(By.ID, "continue").click()

time.sleep(1)

password = driver.find_element(By.ID, "ap_password")

# Replace the xxx with your Amazon password
password.send_keys("Ch0udhary17")

driver.find_element(By.ID, "signInSubmit").click()

time.sleep(1)

def extract_reviews(product_url, num_reviews_to_scrape=100):
    # Requesting the Amazon product's URL
    driver.get(product_url)
    time.sleep(2)  # Wait for page to load
    try:
        see_all_reviews_link = driver.find_element(By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]')
        
        # Scroll to the element and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", see_all_reviews_link)
        time.sleep(1)  # Wait for any scrolling to complete
        see_all_reviews_link.click()
        time.sleep(2)  # Wait for the reviews page to load
        print("Successfully clicked the link!")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
    
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

        # Attempt to click the "Next" button if available
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '.a-last a')
            if next_button.is_displayed():
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            else:
                break
        except NoSuchElementException:
            break  # Exit loop if no more pages

    # Terminating the WebDriver
    driver.quit()
    return reviews

# Creating a function to export the data to CSV
def export_csv(reviews, csv_filename='reviews_data.csv'):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Author', 'Rating', 'Title',  'Review', 'Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for review in reviews:
            writer.writerow({'Author': review['author'], 'Rating': review['rating'], 'Title': review['title'],  'Review': review['text'], 'Date': review['date']})

# Product URL
product_url = "https://www.amazon.co.uk/Samsung-Galaxy-Android-Smartphone-Phantom/dp/B09NRRVPZ7/"
# Calling the extract_reviews() function
reviews_data = extract_reviews(product_url, num_reviews_to_scrape=1000)  # Increase the number of reviews to scrape

# Export data to a CSV file
export_csv(reviews_data)

