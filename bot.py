import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Hardcoded email, password, and message
EMAIL = ''  # Replace with your email
PASSWORD = ''  # Replace with your password
MESSAGE = "I am seeking for work from home !"  # Message content

# Function to login to Facebook
def login_to_facebook(driver):
    driver.get('https://www.facebook.com')
    
    # Locate email and password fields
    email_elem = driver.find_element(By.ID, "email")
    password_elem = driver.find_element(By.ID, "pass")
    
    # Fill in email and password
    email_elem.send_keys(EMAIL)
    password_elem.send_keys(PASSWORD)
    
    # Submit the login form
    password_elem.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

# Function to send a message to a Facebook group
def send_message_to_group(driver, group_url):
    driver.get(group_url)  # Navigate to the group page
    time.sleep(5)  # Wait for the group page to load
    
    try:
        time.sleep(5)
        # Find the post box and enter the message (may need to adjust selector based on Facebook's UI changes)
        post_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div[2]')
        post_box.click()
        time.sleep(5)
        post_box.send_keys(MESSAGE)
        time.sleep(2)
        
        # Press post button (adjust selector if necessary)
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='Post']")
        post_button.click()
        time.sleep(3)  # Wait for the post to be submitted
    except Exception as e:
        print(f"Failed to post in the group {group_url}: {e}")

# Read Excel data
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# Main function
def main():
    # Chrome options to block popups and notifications
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Block notifications

    # Set up WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Login to Facebook once
    login_to_facebook(driver)
    
    # Read the Excel sheet containing group links
    excel_data = read_excel("groups.xlsx")
    
    # Iterate over each group link and send the message
    for index, row in excel_data.iterrows():
        group_url = row['group']  # Assuming the column is named 'group' in the Excel file
        send_message_to_group(driver, group_url)
        
    driver.quit()

if __name__ == "__main__":
    main()
