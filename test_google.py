import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

# --- Configuration (UPDATE THIS) ---
# 1. X Credentials
X_USERNAME = "Enter username here"
X_PASSWORD = "Enter password here"

# 2. Gmail Credentials
GMAIL_EMAIL = "Enter your Gmail here"
GMAIL_PASSWORD = "Enter your password here" # <-- !! UPDATE THIS (App Password if you have 2FA) !!

# 3. Hashtag to search on X
HASHTAG_TO_SEARCH = "#HindiNews"

# 4. Email Settings
RECIPIENT_EMAIL = "ADD_RECIPIENT_EMAIL_HERE"
EMAIL_SUBJECT = f"Latest tweet by this \"{HASHTAG_TO_SEARCH}\" today"
# ------------------------------------

# --- Helper Function ---
def human_like_typing(element, text):
    """Types text into a field one character at a time."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

# --- FUNCTION 1: Login to X ---
def login_to_x(driver, wait, username, password):
    """Logs into X with credentials."""
    try:
        driver.get("https://x.com/i/flow/login")
        print("✅ Opened X login page")

        username_field = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
        )
        username_field.clear() 
        human_like_typing(username_field, username)
        print("✅ Typed X username")
        
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        )
        next_button.click()
        print("✅ Clicked 'Next'")
        
        password_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_field.clear()
        human_like_typing(password_field, password)
        print("✅ Typed X password")
        
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
        )
        login_button.click()
        print("✅ Clicked 'Log in'")
        
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']"))
        )
        print("🎉 X Login successful! On the home page.")

        time.sleep(2) # Wait for pop-up to fully render
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            print("✅ Sent ESCAPE key to dismiss pop-ups.")
        except:
            print("ℹ️ No pop-up to dismiss.")
        
        return True
        
    except Exception as e:
        print(f"❌ A critical error occurred during X login: {e}")
        driver.save_screenshot("error_x_login.png")
        return False

# --- FUNCTION 2: Search and Copy Tweet + Link ---
def search_and_copy_first_tweet_and_link(driver, wait, hashtag):
    """
    Finds the search bar, types, goes to 'Latest', and copies the first tweet's text AND link.
    """
    try:
        print(f"\nAttempting to search for '{hashtag}'...")
        search_box = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search query']"))
        )
        
        human_like_typing(search_box, hashtag)
        time.sleep(random.uniform(0.5, 1))
        search_box.send_keys(Keys.RETURN)
        print(f"✅ Searched for: {hashtag}")
        
        latest_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Latest']"))
        )
        latest_tab.click()
        print("✅ Switched to 'Latest' tab.")
        
        time.sleep(random.uniform(2, 4)) 

        first_tweet_article = wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//article[@data-testid='tweet'])[1]"))
        )
        tweet_text = first_tweet_article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        tweet_link_element = first_tweet_article.find_element(By.XPATH, ".//a[contains(@href, '/status/') and @role='link']")
        tweet_link = tweet_link_element.get_attribute('href')
        
        if not tweet_text or not tweet_link:
            print("❌ Found tweet, but text or link was empty.")
            return None
            
        print(f"✅ Copied tweet: {tweet_text[:50]}...")
        print(f"✅ Copied link: {tweet_link}")
        return (tweet_text, tweet_link) 

    except Exception as e:
        print(f"❌ An error occurred on X while searching: {e}")
        driver.save_screenshot("error_x_search.png")
        return None

# --- FUNCTION 3: Login to Gmail ---
def login_to_gmail(driver, wait, email, password):
    """Logs into Gmail with credentials."""
    try:
        print("\nNavigating to Gmail...")
        driver.get("https://accounts.google.com/signin")
        
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        human_like_typing(email_field, email)
        email_field.send_keys(Keys.ENTER)
        print("✅ Typed Gmail email")
        
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        human_like_typing(password_field, password)
        password_field.send_keys(Keys.ENTER)
        print("✅ Typed Gmail password")
        
        print("...Login complete, navigating to Gmail inbox...")
        time.sleep(3) # Give account page a moment to load
        driver.get("https://mail.google.com/mail/u/0/#inbox")
        
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Compose']")))
        print("🎉 Gmail Login successful! In inbox.")
        return True
        
    except Exception as e:
        print(f"❌ A critical error occurred during Gmail login: {e}")
        print("   - Did you update GMAIL_PASSWORD?")
        print("   - If you have 2FA, you MUST use an 'App Password'.")
        driver.save_screenshot("error_gmail_login.png")
        return False

# --- FUNCTION 4: Send Email via Gmail ---
def send_email_via_gmail(driver, wait, recipient, subject, body):
    """Composes a new email and sends the message (assumes already logged in)."""
    try:
        # 1. Click the 'Compose' button
        compose_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Compose']"))
        )
        compose_button.click()
        print("✅ Clicked 'Compose'.")
        
        time.sleep(random.uniform(1.5, 2.5))

        # 2. Fill the 'To' field
        to_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='To']"))
        )
        to_label.click()
        print("✅ Clicked 'To' field label.")
        
        time.sleep(0.5) 
        
        active_element = driver.switch_to.active_element
        human_like_typing(active_element, recipient)
        print(f"✅ Filled 'To': {recipient}")

        # 3. Fill the 'Subject' field
        subject_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "subjectbox"))
        )
        human_like_typing(subject_field, subject)
        print(f"✅ Filled 'Subject': {subject}")

        # 4. Fill the 'Body' field
        body_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Message Body']"))
        )
        human_like_typing(body_field, body)
        print("✅ Pasted tweet text and link into email body.")

        # 5. Click the 'Send' button
        send_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Send' and @role='button']"))
        )
        send_button.click()
        print("🎉 Successfully sent email!")
        time.sleep(3) 

    except Exception as e:
        print(f"❌ An error occurred while sending email: {e}")
        driver.save_screenshot("error_gmail_send.png")

# --- MAIN BOT FUNCTION ---
def run_x_to_email_bot():
    
    if "YOUR_GMAIL" in GMAIL_PASSWORD:
        print("❌ ERROR: Please update the GMAIL_PASSWORD variable in the '--- Configuration ---' section.")
        return

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # Disable "Save password?" popup
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    
    driver = None
    try:
        driver = uc.Chrome(options=options)
        print("✅ Driver started.")
        
        wait = WebDriverWait(driver, 25) 

        # --- Step 1: Login to X ---
        if not login_to_x(driver, wait, X_USERNAME, X_PASSWORD):
            raise Exception("X Login Failed.")
        
        print("...Allowing X homepage to load...")
        time.sleep(random.uniform(4, 6))

        # --- Step 2: Search and Get Tweet + Link ---
        tweet_data = search_and_copy_first_tweet_and_link(driver, wait, HASHTAG_TO_SEARCH)
        
        if tweet_data:
            # Unpack the tuple
            tweet_text, tweet_link = tweet_data
            
            # --- Step 3: Login to Gmail ---
            if not login_to_gmail(driver, wait, GMAIL_EMAIL, GMAIL_PASSWORD):
                raise Exception("Gmail Login Failed.")
            
            # --- Step 4: Send Email ---
            time.sleep(random.uniform(2, 4))
            
            email_body = (
                f"Hello,\n\n"
                f"Here is the latest tweet for '{HASHTAG_TO_SEARCH}':\n\n"
                f"---\n\n"
                f"{tweet_text}\n\n"
                f"Link to post: {tweet_link}\n\n"
                f"---\n\n"
                f"Sent by your Python bot."
            )
            
            send_email_via_gmail(driver, wait, RECIPIENT_EMAIL, EMAIL_SUBJECT, email_body) # Now sends to new recipient
        else:
            print("❌ Did not find tweet data. Skipping email.")
            
        print("\n✅✅✅ Bot has finished all tasks! ✅✅✅")
        time.sleep(10) # Final pause

    except Exception as e:
        print(f"❌ A critical error occurred in the main block: {e}")
        if driver:
            driver.save_screenshot("error_critical.png")
        print("📸 Screenshot taken on error.")
        time.sleep(5) 

    finally:
        if driver:
            driver.quit()
            print("✅ Driver quit.")

# --- FIX: Corrected the syntax error ---
if __name__ == "__main__":
    run_x_to_email_bot()