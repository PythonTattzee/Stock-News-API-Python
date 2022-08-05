import os
import requests
from twilio.rest import Client
import datetime
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
news_parameters = {
    "q": COMPANY_NAME,
    "from":"2022-07-23&",
    "apiKey": "dab3b5ed98004493b0a62dc821388ff9"

}
av_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : "PGI9DQAWH3C17XEH",
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
av_response=requests.get("https://www.alphavantage.co/query", params=av_parameters)
av_data = av_response.json()
print(av_data)

news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
news_data = news_response.json()
title = news_data["articles"][0]["title"]
description = news_data["articles"][0]["description"]

price_is_bigger = False
yesterday_price = float(av_data["Time Series (Daily)"]["2022-07-22"]["4. close"])
before_yesterday_price = float(av_data["Time Series (Daily)"]["2022-07-21"]["4. close"])

# print(yesterday_price)
# print(before_yesterday_price)

change_percentage = 0

if yesterday_price > before_yesterday_price:
    change_percentage = round((yesterday_price - before_yesterday_price) / before_yesterday_price * 100)
    print(change_percentage)
elif yesterday_price < before_yesterday_price:
    change_percentage = round((before_yesterday_price - yesterday_price) / before_yesterday_price * 100)
    print(change_percentage)
if change_percentage == 5:
    print("Get News")
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
    body=f"{title}\n\n{description}\n\n{change_percentage}",
    from_='+18508135306',
    to='+48517187001'
)

print(message.sid)

# remainder = ((before_yesterday_price / 100) % 0.05)*100
# second_remainder = ((before_yesterday_price / 100) % (yesterday_price / 100))
# if remainder = 5:
# print(data["Time Series (Daily)"]["2022-07-22"]["4. close"])

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

