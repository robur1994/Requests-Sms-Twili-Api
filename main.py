import requests
from twilio.rest import Client

ACOUNT_SID = "sid"
AUTH_TOKEN = "token"
PHONE_NUM = "num_phone"
client = Client(ACOUNT_SID, AUTH_TOKEN)

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.com
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
API_URL_PRICE = "https://www.alphavantage.co/query"
API_KEY_PRICE = "api_key"
PARAMETER_API_PRICE = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_PRICE,
}
stock = requests.get(API_URL_PRICE, params=PARAMETER_API_PRICE)
stock.raise_for_status()
data_stock = stock.json()
print(data_stock)
before_yesterday_price_close = float(
    data_stock['Time Series (Daily)']['2024-01-09']['4. close'])
yesterday_price_close = float(
    data_stock['Time Series (Daily)']['2024-01-10']['4. close'])
print(before_yesterday_price_close)
print(yesterday_price_close)
diference = yesterday_price_close - before_yesterday_price_close

up_down = None
if diference > 0:
  up_down = "⬆"
else:
  up_down = "⬇"

diference = abs(diference)
dif_procent = round(diference / yesterday_price_close * 100, 2)
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

API_URL_NEWS = "https://newsapi.org/v2/everything"
API_KEY_NEWS = "api_key"
PARAMETER_API_NEWS = {
    "q": "tesla",
    "from": "2024-01-10",
    "sortBy": "publishedAt",
    "apiKey": API_KEY_NEWS,
}
## STEP 3: Use https://www.twilio.com
print(dif_procent)
# Send a seperate message with the percentage change and each article's title and description to your phone number.
if dif_procent > 5:
  news_api = requests.get(API_URL_NEWS, params=PARAMETER_API_NEWS)
  news_api.raise_for_status()
  data_news = news_api.json()['articles']
  # print(data_news)
  article_news = data_news[:3]

  formated_article = [
      f"{STOCK}: {up_down} {dif_procent}% \nHeadlines: {article['title']}. \nBrief: {article['description']}"
      for article in article_news
  ]
  for article in formated_article:

    message = client.messages.create(body=article,
                                     from_=PHONE_NUM,
                                     to="+380961544914")

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
