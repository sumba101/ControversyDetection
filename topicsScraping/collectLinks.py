import pandas as pd

from datetime import date,timedelta
dates=list()
link = "https://us.trend-calendar.com/trend/"
today = date.today()
today = today - timedelta(days=1)
number_of_days = 30
for _ in range(number_of_days):
    dates.append(today)
    today = today - timedelta(days=1)
temp = {
    'input':dates
}
df = pd.DataFrame(temp, columns=['input'])
df.to_csv("input_links.csv")
