import pandas as pd
from datetime import datetime

#____________________________________________________
df = pd.read_csv("sphist.csv")

df["Date"] = pd.to_datetime(df["Date"])


df = df.sort_values(by=["Date"], ascending = True)


#____________________________________________________
df["Avg_Price_5days"] = df["Close"].rolling(5).mean()
df["Avg_Price_5days"] = df["Avg_Price_5days"].shift()

df["Avg_Price_15days"] = df["Close"].rolling(15).mean()
df["Avg_Price_15days"] = df["Avg_Price_15days"].shift()

df["Ratio_5/15days"] = df["Avg_Price_5days"]/df["Avg_Price_15days"]
df["Ratio_5/15days"] = df["Ratio_5/15days"].shift()

df["Avg_Price_365days"] = df["Close"].rolling(261).mean()
df["Avg_Price_365days"] = df["Avg_Price_365days"].shift()

#___________________________________________________
df = df[df["Date"] > datetime(year=1951, month =1 ,day=2)]
df = df.dropna(how="any", axis=0)

train = df[df["Date"] <datetime(year=2013, month =1 ,day=1)]
test = df[df["Date"] >=datetime(year=2013, month =1 ,day=1)]

#__________________________________________________
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

lr = LinearRegression()

cols = ["Avg_Price_5days"]

x = train[cols]
y = train["Close"]

lr.fit(x,y)
predictions = lr.predict(test[cols])

error = mean_absolute_error(predictions, test["Close"])

print(error)
