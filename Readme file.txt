# 🤖 X-to-Gmail Automated Intelligence Bot

An end-to-end automation tool that monitors X (formerly Twitter) for specific trending topics, scrapes the latest high-value tweet, and delivers a detailed report directly to your Gmail inbox.

Built with **Python**, **Selenium (Undetected-Chromedriver)**, and verified with a robust **Pytest** suite.

## 🚀 What It Does
1.  **Stealth Login:** Logs into X using credentials without triggering immediate bot detection flags.
2.  **Smart Search:** Navigates to the "Latest" tab for a specific hashtag (e.g., `#pythonframework`).
3.  **Data Extraction:** Scrapes the text and direct link of the most recent tweet.
4.  **Email Delivery:** Logs into Gmail securely and sends the scraped data to a specified recipient.
5.  **Automated Verification:** Includes a full test suite to verify every step of the pipeline.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Browser Automation:** Selenium WebDriver
* **Anti-Detection:** `undetected-chromedriver` (Bypasses "Chrome is being controlled..." flags)
* **Testing Framework:** Pytest & Pytest-Order

---

## 🚧 The Development Journey (Challenges & Bottlenecks)
Building this wasn't just about writing code; it was about fighting modern anti-bot defenses and complex DOM structures. Here are the major hurdles we overcame:

### 1. The "Bot Detected" Banner
* **The Failure:** Standard Selenium drivers immediately triggered X's security banner: *"Chrome is being controlled by automated test software."* This caused instant login blocks.
* **The Fix:** Switched to `undetected-chromedriver`, which patches the driver to mask automation flags, making the browser appear "human."

### 2. The Gmail "To" Field Nightmare
* **The Failure:** Gmail's "To" field is not a standard HTML `<input>`. Our script kept crashing with `ElementNotInteractableException` or typing into the void.
* **The Fix:** We engineered a logic that clicks the "To" label to force browser focus, then uses `driver.switch_to.active_element` to type directly into whichever element Gmail decides is active.

### 3. Timing & Race Conditions
* **The Failure:** The script would often try to tweet or email before the page loaded, causing crashes.
* **The Fix:** Replaced hard `time.sleep()` with dynamic `WebDriverWait` conditions to ensure elements are clickable before interacting.

---

## ⚠️ Known Limitations & Risks

### 🛑 X (Twitter) Verification Checks
**The script is designed for a clean login flow.** However, X security is aggressive.
* **If X asks for a CAPTCHA / Puzzle:** The script will fail.
* **If X asks for an email verification code:** The script will fail.
* **If X flags "Suspicious Activity":** The script will fail.
* **Workaround:** If this happens, you must log in manually in a regular browser to "clear" the security flag before running the bot again.

---

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/x-to-gmail-bot.git](https://github.com/yourusername/x-to-gmail-bot.git)
    cd x-to-gmail-bot
    ```

2.  **Install Dependencies:**
    ```bash
    pip install selenium undetected-chromedriver pytest pytest-order
    ```

3.  **Configuration:**
    Open `test_google.py` (or `google_test.py`) and update the configuration block.
    * **CRITICAL:** For Gmail, you **must** use an **App Password** if you have 2FA enabled. Your regular password will not work.

    ```python
    X_USERNAME = "Your_X_Username"
    X_PASSWORD = "Your_X_Password"
    GMAIL_EMAIL = "your_email@gmail.com"
    GMAIL_PASSWORD = "YOUR_16_CHAR_APP_PASSWORD" 
    RECIPIENT_EMAIL = "receiver@gmail.com"
    ```

---

## 🏃‍♂️ How to Run

### Option 1: Run the Bot Directly
To execute the full workflow once:

---> python test_google.py

Option 2: Run the Test Suite (Recommended)
To run the automated tests which check Login, Search, and Email functionalities step-by-step:

---> python -m pytest -v test_bot.py


*IF YOU WANT TO ONLY RUN THE PROGRAM, THEN CLONE ONLY test_google FILE AND THEN RUN THE COMMAND ---> python test_google.py IN THE TERMINAL*

📄 Disclaimer
This project was created strictly for educational purposes to learn software testing, DOM manipulation, and web automation. It is not intended for commercial scraping, spamming, or violating the Terms of Service of X or Google. Use responsibly.