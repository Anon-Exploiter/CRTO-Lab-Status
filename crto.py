from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from os import getenv

import requests


def fetch_environ_vars():
    if (
        getenv("EMAIL")
        and getenv("PASSWORD")
        and getenv("WEBHOOK_URL")
    ):
        email = getenv("EMAIL")
        password = getenv("PASSWORD")
        webhook_url = getenv("WEBHOOK_URL")

        return email, password, webhook_url

    else:
        exit(
            "[!] Load the config.sh after populating with creds/url:\nsource config.sh"
        )


def post_to_discord(webhook, text):
    print("[*] Posting status on Discord")
    msg_status = requests.post(webhook, json={"content": text})
    if msg_status.status_code == 200:
        print("[+] Posted on Discord")


def post_to_slack(webhook, text):
    print("[*] Posting status on Slack")
    msg_status = requests.post(webhook, json={"text": text})
    if msg_status.status_code == 200:
        print("[+] Posted on Slack")


def initiate_driver():
    chrome_service = Service(ChromeDriverManager().install())

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        # "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]

    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(
        service=chrome_service, options=chrome_options
    )

    return driver


def delay_for_page(
    driver, search_method, search_query, success_msg, delay_msg
):
    while True:
        try:
            WebDriverWait(
                driver, 2
            ).until(  # 2 seconds delay before next checks
                EC.presence_of_element_located(
                    (search_method, search_query)
                )
            )
            if success_msg:
                print(success_msg)
            break

        except TimeoutException:
            if delay_msg:
                print(delay_msg)


def login(driver, email, password):
    print("[*] Opening site")
    driver.get("https://dashboard.snaplabs.io/")

    # Wait for the site to load properly
    delay_for_page(
        driver, By.XPATH, "//input[@type='email']", None, None
    )

    print("[*] Entering username")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(
        email
    )

    print("[*] Entering password")
    driver.find_element(
        By.XPATH, "//input[@type='password']"
    ).send_keys(password)

    print("[*] Logging in")
    driver.find_element(
        By.XPATH,
        "//div[@id='app']/div/div[2]/div/div[2]/div/div[4]/button",
    ).click()
    print("[+] Logged in successfully\n")


def access_course(driver):
    delay_for_page(
        driver,
        "link text",
        "Red Team Ops Lab",
        "[+] Found link text 'Red Team Ops Lab', proceeding..",
        "[-] Waiting on 'Red Team Ops Lab' link text to appear",
    )
    print()

    print("[*] Opening the Course")
    driver.find_element("link text", "Red Team Ops Lab").click()

    print("[*] Fetching hours remaining...")
    delay_for_page(
        driver,
        By.XPATH,
        "//div[@id='content-wrapper']/div/div[2]/div/div/div/div/div[2]/div",
        "[+] Found 'remaining hours' element",
        "[-] Waiting on 'remaining hours' element to appear",
    )


def get_course_stats(driver):
    hours_remaining = driver.find_element(
        By.XPATH,
        "//div[@id='content-wrapper']/div/div[2]/div/div/div/div/div[2]/div",
    ).text
    print(f"\n[+] {hours_remaining}")

    lab_status = driver.find_element(
        By.XPATH,
        "//div[@id='content-wrapper']/div/div[2]/div/div/div/div/div/span/span",
    ).text
    print(f"[+] Lab Status: {lab_status}\n")

    if "Running" in lab_status:
        text = f"[#] CRTO Lab Stats\n\n"
        text += f"Lab Status: **{lab_status}**\n"
        text += hours_remaining

        return text

    else:
        exit("Labs aren't running, not posting anything..")


def main():
    email, password, webhook_url = fetch_environ_vars()
    driver = initiate_driver()

    login(driver, email, password)
    access_course(driver)

    text = get_course_stats(driver)
    if "slack" in webhook_url:
        post_to_slack(webhook_url, text)

    else:
        post_to_discord(webhook_url, text)


if __name__ == "__main__":
    main()
