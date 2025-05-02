import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import os

service = Service(executable_path="C://browserdriver//geckodriver.exe")
driver = webdriver.Firefox(service=service)

try:
    driver.get("http://10.10.99.18:8002/login")

    # Login
    wait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("chlmntl123@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Dost2123")
    driver.find_element(By.ID, "login").click()
    print("Login submitted...")

    time.sleep(3)  # Wait for dashboard

    # Validate page title
    actual_title = driver.title
    expected_title = "Dashboard"
    if expected_title not in actual_title:
        raise AssertionError("Login Test Failed: Page title mismatch")
    print("IAMS Login Successfully!")

    # input validations
    try:
        driver.get("http://10.10.99.18:8002/auditeeDetails/2")
        time.sleep(3)

        documents = wait(driver, 10).until(EC.presence_of_element_located((By.ID, "addDocumentAttachment")))
        documents.click(); time.sleep(3)

        modal = wait(driver, 10).until(EC.visibility_of_element_located((By.ID, "DocumentAttachmentModal")))
        modal_title = modal.find_element(By.CLASS_NAME, "modal-title")
        expected_modal_title = "Documentary Requirements"
        assert modal_title.text == expected_modal_title, f"Unexpected modal title: '{modal_title.text}'"
        print("Documentary requirements modal opened")

        # upload file with complete fields
        dropdown_element = wait(driver, 5).until(EC.presence_of_element_located((By.ID, "fle_doc_typ_id")))
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text("Audit Report"); time.sleep(3)
        driver.find_element(By.ID, "fle_desc").send_keys("Sample file"); time.sleep(3)

        file_path = "C:\\testing\\AU212\\gantt-2.pdf"
        assert os.path.exists(file_path), "File not found!"

        file_input = driver.find_element(By.ID, "fle_name")
        file_input.send_keys(file_path)
        print("File uploaded successfully."); time.sleep(3)

        success = wait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title")))
        actual_message = success.text.strip()
        print("Actual modal text:", actual_message)

        expected_message = "Documentary requirement added successfully"
        assert expected_message in actual_message, f"Success message mismatch! Actual: '{actual_message}'"

        ok_button = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm")))
        ok_button.click(); time.sleep(5)

        # with error message
        driver.find_element(By.ID, "fle_desc").clear()
        driver.find_element(By.ID, "fle_desc").send_keys("Name of file"); time.sleep(3)
        wait(driver, 3).until(EC.element_to_be_clickable((By.ID, "addAuditeeDocument"))).click()
        error_msg = driver.find_element(By.ID, "error-fle_doc_typ_id").text
        print("Validation Message:", error_msg)

        # 150 + 1 characters
        input_text = "a" * 151  # or any test input
        title_input = driver.find_element(By.ID, "fle_desc")
        title_input.clear(); time.sleep(3)
        title_input.send_keys(input_text); time.sleep(3)

        typed_value = title_input.get_attribute("value")

        if len(typed_value) > 150:
            print("Failed to limit characters — input exceeds 150 characters.")
        else:
            print(f"Input had {len(typed_value)} characters. Submitting...")
            driver.find_element(By.ID, "addAuditeeDocument").click()

        # add entry without attachment
        driver.find_element(By.ID, "fle_desc").clear(); time.sleep(5)
        dropdown_element = wait(driver, 5).until(EC.presence_of_element_located((By.ID, "fle_doc_typ_id")))
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text("Internal Audit Department");time.sleep(3)
        driver.find_element(By.ID, "fle_desc").send_keys("Audit");time.sleep(3)

        # wait(driver, 3).until(EC.element_to_be_clickable((By.ID, "addAuditeeDocument"))).click()
        # success = wait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title")))
        # assert success.text == "Documentary requirement added successfully", "Success message mismatch!"
        # print("Message:", success.text)

        wait(driver, 3).until(EC.element_to_be_clickable((By.ID, "addAuditeeDocument"))).click()
        wait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "swal2-title"), "Documentary requirement added successfully"))
        success = driver.find_element(By.ID, "swal2-title")
        assert success.text.strip() == "Documentary requirement added successfully", "Success message mismatch!"
        print("Message:", success.text.strip())

        ok_button = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm")))
        ok_button.click()

        table = wait(driver, 10).until(EC.presence_of_element_located((By.ID, "DataTables_Table_0")))
        time.sleep(3)

        table_rows = table.find_elements(By.CSS_SELECTOR, "tr.disabled-row")
        description_found = any("Audit" in row.text for row in table_rows)
        assert description_found, "Failed to confirm the new entry in the table."
        print("Add entry to the list without an attachment")

        # search box
        search_inputs = [
            "osec",
            "osec123455678212541",
             "ñ",
             "os&c",
             "  osec",
             "  test  ",
             # " ",
             # ""
        ]
        search_box = driver.find_element(By.CSS_SELECTOR, "input.form-control.document-attachment-custom-search")
        clear_button = driver.find_element(By.CSS_SELECTOR, ".document-attachment-clear-icon .fas.fa-times")

        for search_input in search_inputs:
            search_box.clear()
            search_box.send_keys(search_input)
            search_box.send_keys(u'\ue007')  # Simulates pressing the 'Enter' key
            time.sleep(3)

            # Locate the table and rows
            table = driver.find_element(By.ID, "DataTables_Table_0")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            no_data_message = table.find_elements(By.CSS_SELECTOR, "td.dt-empty")
            if no_data_message:
                print(f"No data available for input '{search_input}'.")
            else:
                # Check if any row contains the search input
                search_found = any(search_input in row.text for row in rows if row.is_displayed())
                if search_found:
                    print(f"Confirmed search input '{search_input}' in the table")
                else:
                    print(f"Failed to confirm the input '{search_input}' in the table.")

        # clear button
        try:
            clear_button.click()
            time.sleep(3)

            cleared_value = search_box.get_attribute("value")
            assert cleared_value == "", "Clear button did not work as expected. The search box is not empty."
            print(f"Search input cleared successfully after clicking clear button.")
        except AssertionError as e:
            print(f"Error: {e}")

        # view attachment table
        driver.find_element(By.CSS_SELECTOR, "input.form-control.document-attachment-custom-search").clear();time.sleep(5)
        table = driver.find_element(By.ID, "DataTables_Table_0")
        assert table.is_displayed(), "Attachment table not visible"
        print("View Attachment Table")

        # view column name
        expected = ["Type", "Name/Title", "Last Updated"]
        headers = [th.text.strip() for th in driver.find_elements(By.CLASS_NAME, "dt-column-title")]
        assert headers == expected, f"FAILED: Headers {headers} != {expected}"
        print("Correct Column name - PASSED")

        # hover over table
        rows = driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr")
        assert rows, "No rows found in the attachment table"

        first_row = rows[0]
        actions = ActionChains(driver)
        actions.move_to_element(first_row).perform()
        time.sleep(3)  # Allow UI to reveal icons on hover

        copy_icon = first_row.find_element(By.CSS_SELECTOR, "button.copy-auditee-document-attachment")
        delete_icon = first_row.find_element(By.CSS_SELECTOR, "button.delete-auditee-document-attachment")

        assert copy_icon.is_displayed(), "Copy Link icon not shown on hover"
        assert delete_icon.is_displayed(), "Delete icon not shown on hover"
        print("Hover icons appear: Copy Link & Delete")

        copy_icon.click()
        print("Copy link button clicked")
        time.sleep(1)

        delete_icon.click()
        print("Delete button clicked")
        time.sleep(1)

        success = wait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title")))
        assert success.text == "Are you sure you want to delete this item?", "Confirmation message mismatch!"
        print("Message:", success.text); time.sleep(3)
        ok_button = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm")))
        ok_button.click()

        rows_before = len(driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr"))

        success = wait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title")))
        assert success.text == "Documentary requirement deleted successfully", "Completion message mismatch!"
        print("Message:", success.text); time.sleep(3)
        ok_button = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm")))
        ok_button.click()

        wait(driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr")) < rows_before)
        rows_after = len(driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr"))
        assert rows_after == rows_before - 1, f"FAILED: Row count did not decrease. Before: {rows_before}, After: {rows_after}"
        print("Attachment row successfully deleted.")

        # toggle sorter
        headers = [th.text.strip() for th in driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 thead th")]
        rows = lambda: driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 tbody tr")
        for col_name in ["Type", "Name/Title", "Last Updated"]:
            idx = headers.index(col_name)
            th = driver.find_elements(By.CSS_SELECTOR, "#DataTables_Table_0 thead th")[idx]
            # capture pre-sort
            before = [r.find_elements(By.TAG_NAME, "td")[idx].text for r in rows()]
            th.click(); time.sleep(5)
            after = [r.find_elements(By.TAG_NAME, "td")[idx].text for r in rows()]
            assert before != after, f"FAILED: '{col_name}' did not sort"
            print(f"Sorter on '{col_name}' toggles order")

        # email button
        driver.find_element(By.ID, "addToEmail").click()
        email_modal = wait(driver,10).until(EC.visibility_of_element_located((By.ID, "EmailNotificationModal" )))
        assert email_modal.is_displayed(), "Email Modal did not open"
        print("Email Modal Form Opened"); time.sleep(3)

        close_button = wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#EmailNotificationModal .btn-close")))
        ActionChains(driver).move_to_element(close_button).click().perform()

        # Wait until modal is hidden (not necessarily removed from DOM)
        wait(driver, 10).until(lambda d: not d.find_element(By.ID, "EmailNotificationModal").is_displayed())
        print("Email Modal Closed")

        time.sleep(3)
        wait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#DocumentAttachmentModal .btn-close"))).click()
        wait(driver, 5).until(lambda d: not d.find_element(By.ID, "DocumentAttachmentModal").is_displayed())
        modal = driver.find_element(By.ID, "DocumentAttachmentModal")
        assert not modal.is_displayed(), "Document Attachment Modal did not close"
        print("Document Attachment modal closed")

    except Exception as section_error:
        print("UI verification failed:", section_error)

except Exception as main_error:
    print("Test encountered an exception:", main_error)

finally:
    time.sleep(5)
    driver.quit()


