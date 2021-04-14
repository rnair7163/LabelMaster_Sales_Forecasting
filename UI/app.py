import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
from flask import Response

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# import things
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    date = Col('Date')
    sales = Col('Sales Prediction')

# Get some objects
class Item(object):
    def __init__(self, date, sales):
        self.date = date
        self.sales = sales

@app.route('/')
def home():
    return render_template('index.html')

def model_data():
    books = pd.read_csv('/Users/omkarpawar/Downloads/Books_ext_fs.csv')
    books = books.dropna(axis = 1)
    sales = books[['Year_Month','Sum of Sales']]
    df = sales.sort_values("Year_Month").set_index("Year_Month")
    train = df[:int(0.8*(len(sales)))]
    test = df[int(0.8*(len(sales))):]

    #output = model.forecast(len(test))
    model = ExponentialSmoothing((train["Sum of Sales"]), trend="add", seasonal="mul", seasonal_periods=12)
    fit = model.fit()
    output = fit.forecast(len(test))
    return test,output

@app.route('/predict',methods=['POST'])
def predict():

    test, output = model_data()
    items = []
    for i in output.index:
    	items.append(Item(i,output[i]))
    table = ItemTable(items)
    return render_template('index.html', prediction_text=table)

@app.route('/plot',methods=['POST'])
def plot():
    test, output = model_data()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(output.values)
    axis.plot(test.values)
    axis.set_title('Forecast vs Actual Values')
    axis.set_xlabel('TimeLine')
    axis.set_ylabel('Total Sales')
    result = io.BytesIO()
    FigureCanvas(fig).print_png(result)
    return Response(result.getvalue(), mimetype='image/png')

@app.route('/update',methods=['POST'])
def update():
    main_data = dp.main_data_transform()
    books = dp.books_data(main_data)
    external = dp.external_database()
    data = dp.final_data(books, external)
    return data

if __name__ == "__main__":
    app.run(debug=True)
