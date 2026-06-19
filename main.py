from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
import csv
from datetime import datetime
import time

website = "https://torob.com/p/370ec9b2-9629-4663-ba7f-5e8b25bd3ae4/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%84%D9%86%D9%88%D9%88-loq-16gb-ram-512gb-ssd-i5-13450hx-vga-rtx5050/"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

drive = webdriver.Chrome(options=options)

class TorobPriceChecker:
    def save_history(price):
        with open("price_history.csv", 'a', newline="",encoding='utf-8') as file:
            writer = csv.writer(file)

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([time_now, price])


    def notification(msg):
        toast = ToastNotifier()

        toast.show_toast(
            "Torob Price Alert",
            msg,
            duration=5
        )


    def price_to_int(price):
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        english_digits = "0123456789"

        translation = str.maketrans(persian_digits, english_digits)
        price = price.translate(translation)
        price = price.replace('٫', '')
        price = price.replace(" تومان", "")

        return int(price)

    def get_price():

        drive.get(website)

        price = drive.find_element(By.CSS_SELECTOR, "#cheapest-seller > div.Showcase_ellipsis__FxqVh > div:nth-child(2)").text
        
        return price

    def save_price(save_price):
        with open("price.txt", 'w', encoding='utf-8') as file:
            file.write(str(save_price))
        

    def compare_price(compare_price):

        try:
            with open("price.txt", 'r', encoding='utf-8') as file:
                old_price = int(file.read().replace(",", ""))

            if compare_price != old_price:
                difference = compare_price - old_price

                if difference > 0:
                    msg = f"Price increased by {difference:,} Toman"
                    print(msg)
                    TorobPriceChecker.notification(msg=msg)
                elif difference < 0:
                    msg = f"Price decreased by {abs(difference):,} Toman"
                    print(msg)
                    TorobPriceChecker.notification(msg=msg)
                else:
                    print("No change")

            else:
                print("no change")

        except FileNotFoundError:
            print("First run")

while True:
    try:
        current_price = TorobPriceChecker.price_to_int(TorobPriceChecker.get_price())

        TorobPriceChecker.compare_price(current_price)
        TorobPriceChecker.save_price(current_price)
        TorobPriceChecker.save_history(current_price)

        print("Wait For One Hour")
        time.sleep(3600)
    except Exception as e:
        print(f"Error is: {e}")
        print("Wait For One Hour")
        time.sleep(3600)

    finally:
        drive.quit()