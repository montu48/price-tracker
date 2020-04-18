import requests
from bs4 import BeautifulSoup
import smtplib
import time


def getUserInput():
    PRODUCT_URL = input("Please Paste Product URL Here from flipkart.com: ");
    CURRENT_PRICE = getCurrentPrice(PRODUCT_URL);
    CONVERTED_CURRENT_PRICE = float(CURRENT_PRICE[1:10].replace(",",""));
    print("Product Current Price is: " + CURRENT_PRICE)
    EXPECTED_PRICE = input("Please Enter Your Expected Price when you want notification: ");
    CONVERTED_EXPECTED_PRICE = float(EXPECTED_PRICE[0:10].replace(",",""));
    EMAIL_ADDRESS = input("Please Enter Your For Email Notification: ")
    checkForPriceDrop(PRODUCT_URL,CONVERTED_CURRENT_PRICE,CONVERTED_EXPECTED_PRICE,EMAIL_ADDRESS)
  
    

def getCurrentPrice(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    price = findById('div','_1vC4OE _3qQ9m1', soup)
    return price

def findById(htmlElement, className, soup):
    for s in soup.findAll(htmlElement,{'class':className}):
        text = s.contents[0]
        return text

def checkForPriceDrop(PRODUCT_URL,CURRENT_PRICE,EXPECTED_PRICE,EMAIL_ADDRESS):
    print("Hang on we will notify you")
    while (True):
        price_drops = check_price(PRODUCT_URL,CURRENT_PRICE,EXPECTED_PRICE,EMAIL_ADDRESS)
        if not price_drops:
            time.sleep(60)
        else:
            price("Check Your Mail")
            break

def check_price(PRODUCT_URL,CURRENT_PRICE,EXPECTED_PRICE,EMAIL_ADDRESS):
    page = requests.get(PRODUCT_URL)
    soup = BeautifulSoup(page.content,'html.parser')
    price = findById('div','_1vC4OE _3qQ9m1', soup)
    title = findById('span','_35KyD6', soup)
    LATEST_PRICE = float(price[1:10].replace(",",""))
    print(LATEST_PRICE)
    print(EXPECTED_PRICE)
    if(LATEST_PRICE <= EXPECTED_PRICE):
        print("Price Decreased")
        send_mail(PRODUCT_URL,EMAIL_ADDRESS)
        return True
    else:
        print("You have to wait")
        return False

def send_mail(PRODUCT_URL, EMAIL_ADDRESS):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('your@email.com','password')
    subject="Price Fell Down"
    body="Check the Flipkart Link " + PRODUCT_URL

    msg = f"Subject:{subject}\n\n{body}"

    server.sendmail(
        "promocode8856@gmail.com",
        EMAIL_ADDRESS,
        msg
    )
    print("Email has been sent")
    server.quit()

getUserInput()


