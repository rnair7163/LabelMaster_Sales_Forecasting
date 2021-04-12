import numpy
import pandas as pd
import sklearn
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pickle

print("Loading Data")
books = pd.read_csv('/Users/omkarpawar/Downloads/Books_ext_fs.csv')
books = books.dropna(axis = 1)
sales = books[['Year_Month','Sum of Sales']]

print("Train Test Setting")
df = sales.sort_values("Year_Month").set_index("Year_Month")
train = df[:int(0.8*(len(sales)))]
test = df[int(0.8*(len(sales))):]

print("Modelling")
model = ExponentialSmoothing((train["Sum of Sales"]), trend="add", seasonal="mul", seasonal_periods=12)
fit = model.fit()

print("Predicting")
pred = fit.forecast(len(test))
print(pred)
pickle.dump(model, open('model.pkl','wb'))
print("Model Saved")


