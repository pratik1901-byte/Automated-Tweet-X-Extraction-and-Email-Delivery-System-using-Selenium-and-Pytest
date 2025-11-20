import pytest
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="session")
def driver():
    """
    This fixture creates a single browser session for all tests.
    It starts the driver and yields it to the tests.
    After all tests run, it quits the driver.
    """
    print("\n--- Setting up browser ---")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # Disable "Save password?" popup
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    
    driver_instance = uc.Chrome(options=options)
    
    # Yield the driver to the test functions
    yield driver_instance
    
    # This code runs *after* all tests are finished
    print("\n--- Tearing down browser ---")
    driver_instance.quit()

@pytest.fixture(scope="session")
def wait(driver):
    """
    This fixture creates a reusable WebDriverWait object.
    It depends on the 'driver' fixture.
    """
    return WebDriverWait(driver, 25) 