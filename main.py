import time
from bs4 import BeautifulSoup
import datetime
import requests
import smtplib
from links import BEST_BUY_URL, MICRO_CENTER_URL, NEWEGG_URL

EMAIL = "EMAIL"
PASSWORD = "PASSWORD"
USER_AGENT = "USER_AGENT"
ACCEPT_LANGUAGE = "ACCEPT_LANGUAGE"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

smtplib_connection = smtplib.SMTP(host="EMAIL", port=)
smtplib_connection.starttls()
smtplib_connection.login(user=EMAIL, password=PASSWORD)


best_buy_request = requests.get(BEST_BUY_URL[0], headers=HEADERS)
best_buy_connection = best_buy_request.text

micro_center_request = requests.get(MICRO_CENTER_URL[0], headers=HEADERS)
micro_center_connection = micro_center_request.text

newegg_request = requests.get(NEWEGG_URL[0], headers=HEADERS)
newegg_connection = newegg_request.text

time.sleep(5)
if best_buy_request.status_code or micro_center_request.status_code or newegg_request.status_code == 200:

    def BestBuyScrapper(bb_connection_link):
        best_buy_request = requests.get(BEST_BUY_URL[bb_connection_link], headers=HEADERS)
        best_buy_connection = best_buy_request.text

        best_buy_soup = BeautifulSoup(best_buy_connection, "html.parser")
        bb_title = best_buy_soup.find(name="h1", class_="heading-4 leading-6 font-500").getText().strip()
        bb_price = best_buy_soup.find(name="div", class_="priceView-hero-price priceView-customer-price").getText().replace(
            "Your price for this item is ", "! ")
        getting_price = bb_price.partition("!")
        formatted_price = getting_price[0].replace("$", " ")
        final_price = float(formatted_price)

        print("Best Buy")
        if bb_title:
            print(f"Item: {bb_title}")
        else:
            print("Could not find Best Buy item")
        if bb_price:
            print(f"Price: {final_price}")
        else:
            print("Could not find Best Buy price\n")

        if bb_connection_link == 0 and final_price < 10.00 and bb_title:
            smtplib_connection.sendmail(from_addr=EMAIL, to_addrs="EMAIL",
                                        msg=f"Subject: Price Drop! Item: {bb_title}\n\n"
                                            f"The price for {bb_title} dropped to ${final_price}\n"
                                            f"{BEST_BUY_URL[bb_connection_link]}")

    def MicroCenterScrapper():
        micro_center_soup = BeautifulSoup(micro_center_connection, "html.parser")
        m_c_title = micro_center_soup.find(name="span", class_="ProductLink_660429").getText()
        m_c_price = micro_center_soup.find(name="p", class_="big-price").getText()

        print("Micro Center")
        if m_c_title:
            print(f"Item: {m_c_title}")
        else:
            print("Could not find Micro Center item")

        if m_c_price:
            m_c_price_wo_sign = m_c_price.replace('$', '')
            m_c_price_float = m_c_price_wo_sign
            print(f"Price: {m_c_price_float}")
        else:
            print("Could not find Micro Center price")


    def NeweggScrapper():
        newegg_soup = BeautifulSoup(newegg_connection, "html.parser")
        newegg_item = newegg_soup.find(name="h1", class_="product-title").getText()
        newegg_price = newegg_soup.find_all("div", class_="product-price")

        print("Newegg")
        if newegg_item:
            print(f"Item: {newegg_item}")
        else:
            print("Could not find Newegg item")

        if newegg_price:
            dollars = [money.strong.getText() for money in newegg_price]
            cents = [money.sup.getText() for money in newegg_price]
            d_plus_c = dollars + cents
            d_join_c = ''.join(d_plus_c)
            total_price = float(d_join_c)
            print(f"Price: ${total_price}")
        else:
            print("Could not find Newegg price")

    mynum = 0
    for number in range(5):
        time.sleep(5)
        BestBuyScrapper(bb_connection_link=mynum)
        mynum += 1

else:
     print("Website: Micro Center\nConnection Error:", micro_center_request.raise_for_status())
     print("Website: Best Buy\nConnection Error:", best_buy_request.raise_for_status())
     print("Website: Newegg\nConnection Error:", newegg_request.raise_for_status())