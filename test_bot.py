import pytest
from selenium.webdriver.common.by import By

# Import the functions we want to test from your original script
from test_google import (
    login_to_x, 
    search_and_copy_first_tweet_and_link, 
    login_to_gmail, 
    send_email_via_gmail,
    X_USERNAME, 
    X_PASSWORD, 
    GMAIL_EMAIL, 
    GMAIL_PASSWORD, 
    RECIPIENT_EMAIL, 
    EMAIL_SUBJECT
)

# --- Configuration for Tests ---
HASHTAG = "#HindiNews"  # Hashtag to search on X
TEST_EMAIL_BODY = "This is a test email body."

# We mark tests as 'order(1)', 'order(2)' etc. to force them to run in sequence
# because you can't search (test 2) before you log in (test 1).
# You'll need to run 'pip install pytest-order' for this.

@pytest.mark.order(1)
def test_x_login_success(driver, wait):
    """
    Tests if the X login function completes successfully.
    It passes if it returns True.
    """
    print("Testing X Login...")
    assert login_to_x(driver, wait, X_USERNAME, X_PASSWORD) == True
    print("✅ X Login Successful")

@pytest.mark.order(2)
def test_search_and_copy(driver, wait):
    """
    Tests if the search function successfully returns text and a link.
    It passes if 'tweet_data' is not None and contains two items.
    """
    print("Testing X Search...")
    global tweet_data # Save the data for the email test
    tweet_data = search_and_copy_first_tweet_and_link(driver, wait, HASHTAG)
    
    assert tweet_data is not None
    assert len(tweet_data) == 2 # Check it returned a (text, link) tuple
    assert "https://" in tweet_data[1] # Check the link looks like a link
    print("✅ X Search Successful")

@pytest.mark.order(3)
def test_gmail_login_success(driver, wait):
    """
    Tests if the Gmail login function completes successfully.
    It passes if it returns True.
    """
    print("Testing Gmail Login...")
    # NOTE: This requires your GMAIL_PASSWORD to be correct in the config!
    assert login_to_gmail(driver, wait, GMAIL_EMAIL, GMAIL_PASSWORD) == True
    print("✅ Gmail Login Successful")

@pytest.mark.order(4)
def test_send_email_fills_fields(driver, wait):
    """
    Tests if the send_email function correctly fills all fields
    and clicks the 'Send' button.
    """
    print("Testing Email Compose...")
    # This test will find and fill all fields, then click Send.
    # It passes if the send_email_via_gmail function runs without error.
    try:
        send_email_via_gmail(
            driver, 
            wait, 
            RECIPIENT_EMAIL, 
            EMAIL_SUBJECT, 
            f"{tweet_data[0]}\n\nLink: {tweet_data[1]}"
        )
        print("✅ Email Function Executed (Check inbox for real email)")
        assert True
    except Exception as e:
        # If any error happens (e.g., element not found), the test fails
        print(f"❌ Email Function Failed: {e}")
        assert False