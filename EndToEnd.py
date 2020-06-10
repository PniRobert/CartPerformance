import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep

domainName = "splus-wip3.pnistaging.com"
applicationPath = "/services/printing"
np.random.seed(0)
productKeys = np.array(["880e9a0b0a627f97", "0334a43adccf687a", "550f7cadad98fe98",
                        "660e1c58e314b38e", "0a0e1568742a5a2e", "fadb30ec37bdebc8"])

if __name__ == "__main__":
    startUrl = f"https://{domainName}{applicationPath}/legacy/station/6B696F736b5F72696B/126/redirect/"
    driverOptions = Options()
    driverOptions.headless = False
    driver = webdriver.Firefox(options=driverOptions)
    try:
        driver.maximize_window()
        driver.get(startUrl)
        for _ in range(3):
            startUrl = f"https://{domainName}{applicationPath}/"
            driver.get(startUrl)
            sleep(2)
            productKey = np.random.choice(a=productKeys)
            startUrl = f"https://{domainName}{applicationPath}/product/{productKey}/builder/"
            driver.get(startUrl)
            sleep(2)
            builderUrl = driver.current_url
            nextUrl = builderUrl.replace("Builder", "review")
            endPos = nextUrl.find("#")
            nextUrl = nextUrl[:endPos] + "/"
            driver.get(nextUrl)
            sleep(5)
            driver.find_element_by_css_selector(
                "label.test_approvalCheckbox").click()
            driver.find_element_by_css_selector(
                "button.tag-advance-to-upsell-button").click()
            sleep(5)
            buttons = driver.find_elements_by_css_selector(
                "button.checkmark-icon")
            if buttons is not None and len(buttons) > 6:
                buttons[6].click()
            driver.find_element_by_css_selector(
                "button.tag-add-to-cart-button").click()
            sleep(20)
            driver.find_elements_by_css_selector(
                "input.btn-primary")[1].click()
            sleep(10)
            pickupName = driver.find_element_by_id("txtPickupFullName")
            pickupName.send_keys("No Body")
            pickupName.send_keys(Keys.RETURN)
            pickupPhone = driver.find_element_by_id("txtPickupPhoneNumber")
            pickupPhone.send_keys("9999999999")
            pickupPhone.send_keys(Keys.RETURN)
            pickupEmail = driver.find_element_by_id("txtPickupEmail")
            pickupEmail.send_keys("nobody@nowhere.com")
            pickupEmail.send_keys(Keys.RETURN)
            sleep(5)
            driver.find_element_by_id("btnCheckout").click()
            sleep(20)

    finally:
        driver.quit()
