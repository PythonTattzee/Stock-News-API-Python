import os
import requests
from twilio.rest import Client
from datetime import datetime


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# here I create the environment variables to secure my data
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
#here I define the parameters for the connection to news server
news_parameters = {
    "q": COMPANY_NAME,
    "from":"2022-07-23&",
    "apiKey": "dab3b5ed98004493b0a62dc821388ff9"

}
#here I define the parameters for the connection to stock server
av_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : "PGI9DQAWH3C17XEH",
}

# connect and get data from stock server
av_response=requests.get("https://www.alphavantage.co/query", params=av_parameters)
av_data = av_response.json()
print(av_data)

# connect and get data from news server
news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
news_data = news_response.json()

#here I get out the news title and description and save it to variables
title = news_data["articles"][0]["title"]
description = news_data["articles"][0]["description"]

# price_is_bigger = False
# here I get the stock prices for yesterday and the day before yestreday and save them into variables
yesterday_price = float(av_data["Time Series (Daily)"]["2022-07-22"]["4. close"])
before_yesterday_price = float(av_data["Time Series (Daily)"]["2022-07-21"]["4. close"])

# print(yesterday_price)
# print(before_yesterday_price)
#here I create the procentage variable thatI can use and change later
change_percentage = 0
#here I check if the price changed between yestreday and day before
#and if it has changed I count the percentage of change and round it to a whole number
if yesterday_price > before_yesterday_price:
    change_percentage = round((yesterday_price - before_yesterday_price) / before_yesterday_price * 100)
    # print(change_percentage)
elif yesterday_price < before_yesterday_price:
    change_percentage = round((before_yesterday_price - yesterday_price) / before_yesterday_price * 100)
    print(change_percentage)
#after that I check the percentage if the percentage equal to five
if change_percentage == 5:
    print("Get News")
    #if the procent is equal to 5 I finnaly send the message with news via sms
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"{title}\n\n{description}\n\n{change_percentage}",
        from_='+18508135306',
        to='+48517187001'
    )

    print(message.sid)

