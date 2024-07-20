from twilio.rest import Client
import requests


VIRTUAL_TWILIO_NUMBER = "+12706813843"
VERIFIED_NUMBER = "+918383055528"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"


s_api_key = "12YT039O8SIUGX2J"
n_api_key = "2976b5442a6343f38beb348c19801eb2"
twilio_account_sid = "AC77bee70ee085de910da3a4f01f6a1e80"
twilio_auth_token = "436b6685c424526bc11ca4097677867e"

stock_params = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'apikey': s_api_key,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_cp = day_before_yesterday_data["4. close"]
print(day_before_yesterday_cp)

difference = float(yesterday_closing_price) - float(day_before_yesterday_cp)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > -1:
    news_params = {
        "apikey": n_api_key,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [
        f"{STOCK_NAME}:{up_down}{diff_percent}%\nHeadline:{article['title']}.\nBrief:{article['description']}"for
        article in three_articles]
    print(formatted_articles)

    client = Client(twilio_account_sid, twilio_auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
