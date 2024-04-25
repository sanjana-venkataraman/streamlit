import google.generativeai as genai


import os
import requests
import json
import apikey
import serpapi
import yfinance as yf
from yahooquery import Ticker


os.environ["SERPAPI_API_KEY"] = "6201f1fa0def52be865995aa2e010b535b2df0f7af4a87b1449620323f80a175"

company_name = "Adani Green Energy Ltd"


def get_company_news(company_name):
    params = {
        "engine": "google",
        "tbm": "nws",
        "q": company_name,
        "api_key": os.environ["SERPAPI_API_KEY"],
    }

    response = requests.get('https://serpapi.com/search', params=params)
    data = response.json()
    return data.get('news_results')



news = get_company_news(company_name)
print(news)

def get_stock_evolution(company_name, period="1y"):
    # Get the stock information
    stock = yf.Ticker(company_name)

    # Get historical market data
    hist = stock.history(period=period)

    # Convert the DataFrame to a string with a specific format
    data_string = hist.to_string()
    return data_string
stock = get_stock_evolution("ADANIGREEN.NS")
print(stock)
# yf.Ticker("INFY")

def get_financial_statements(ticker):
    # Create a Ticker object
    company = Ticker(ticker)

    # Get financial data
    balance_sheet = company.balance_sheet().to_string()
    cash_flow = company.cash_flow(trailing=False).to_string()
    income_statement = company.income_statement().to_string()
    valuation_measures = str(company.valuation_measures)
    return valuation_measures

finance= get_financial_statements("ADANIGREEN.NS")
print(finance)

news=str(news)
stock=str(stock)
finance=str(finance)
# news=''.join(news)
# stock=''.join(stock)
string="""write a detailled investment thesis to answer
                      the user request. Provide numbers to justify
                      your assertions, a lot ideally. Never mention
                      something like this:
                      However, it is essential to consider your own risk
                      tolerance, financial goals, and time horizon before
                      making any investment decisions. It is recommended
                      to consult with a financial advisor or do further
                      research to gain more insights into the company's f
                      undamentals and market trends. The user
                      already knows that"""

GEMINI_API_KEY = 'AIzaSyDKN20GfR93SRXToC-DdI6I2A6a9FHP82w'
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(string+news+stock+finance)
print(response)

response_string=""
for chunk in response:
  response_string += chunk.text
print(response_string)