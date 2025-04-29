from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import time

# Setup
service = Service(executable_path="C://browserdriver//geckodriver.exe")
driver = webdriver.Firefox(service=service)

try:
    driver.get("http://10.10.99.18:8002/auditor")

    # Login
    wait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("chlmntl123@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Dost2123")
    driver.find_element(By.ID, "login").click()
    print("Login submitted...")

    time.sleep(3)  # Wait for dashboard

    # Validate page title
    actual_title = driver.title
    expected_title = "ICQ Lists"
    if expected_title not in actual_title:
        raise AssertionError("Login Test Failed: Page title mismatch")
    print("IAMS Login Successfully!")

    # Grouped validations
    try:
        # DOST Logo
        logo = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'dost.png')]")))
        assert logo.is_displayed(), "DOST logo not displayed"
        assert logo.get_attribute("alt") == "DOST Logo", "Alt text mismatch for logo"
        print("DOST logo displayed")

        # DOST Name
        dost_name = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Department of Science and Technology')]")))
        assert dost_name.is_displayed(), "DOST name not visible"
        print("DOST name displayed")

        # Internal Audit Service title
        iams_title = wait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'fw-bold') and contains(text(), 'Internal Audit Service')]")
        ))
        assert iams_title.is_displayed(), "Internal Audit Service title not visible"
        print("Internal Audit Service title displayed")

        # Page Title
        page_title = wait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//h5[contains(text(), 'INTERNAL CONTROL QUESTIONNAIRE')]")
        ))
        assert page_title.is_displayed(), "Page title not visible"
        assert "INTERNAL CONTROL QUESTIONNAIRE (ICQ)" in page_title.text.upper(), "Page title text mismatch"
        print("Page title displayed correctly")

        # Audit Link
        audit_link = wait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-fnd-icq-id='47']")))
        assert audit_link.text != "", "Audit link is empty"
        print(f"Found audit link: {audit_link.text}")
        audit_link.click()

        # Detail Page
        # wait(driver, 10).until(EC.url_contains("http://10.10.99.18:8002/icq/47"))
        #wait(driver, 20).until(EC.presence_of_element_located((By.ID, "aud_title")))
        #print("Navigated to audit detail page")

    except Exception as section_error:
        print("UI verification failed:", section_error)

except Exception as main_error:
    print("Test encountered an exception:", main_error)

finally:
    time.sleep(5)
    driver.quit()
