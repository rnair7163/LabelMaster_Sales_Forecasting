import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import data_prep as dp
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
import random
from flask import Response

app = Flask(__name__)

from flask_table import Table, Col

@app.route('/books')
def home():
    return render_template('index.html')


def model_data():
    books = pd.read_csv('books_data.csv')
    books = books.dropna(axis = 1)
    sales = books[['Year_Month','Sum of Sales']]
    df = sales.sort_values("Year_Month").set_index("Year_Month")
    train = df[:int(0.8*(len(sales)))]
    test = df[int(0.8*(len(sales))):]
    model = ExponentialSmoothing((train["Sum of Sales"]), trend="add", seasonal="mul", seasonal_periods=12)
    fit = model.fit()
    output = fit.forecast(len(test))
    return test,output


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/predict',methods=['POST'])
def predict():

    test, output = model_data()
    items = []
    headings = ("Date", "Total Sales ($)")
    data = []
    for i in output.index:
    	data.append([i.strftime("%Y-%m"),round(output[i],3)])
    #table = ItemTable(items)
    return render_template('index.html', headings=headings,data = data)


@app.route('/plot',methods=['POST'])
def plot():
    test, output = model_data()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(output.values, label = "Forecast")
    axis.plot(test.values, label = "Actual")
    axis.set_title('Forecast vs Actual Values')
    axis.set_xlabel('TimeLine')
    axis.set_ylabel('Total Sales')
    axis.legend()
    result = io.BytesIO()

    FigureCanvas(fig).print_png(result)
    return Response(result.getvalue(), mimetype='image/png')


@app.route('/update',methods=['POST'])
def update():
    main_data = dp.main_data_transform()
    books = dp.books_data(main_data)
    # external = dp.external_database()
    # data = dp.final_data(books, external)
    books.to_csv('books_data.csv')
    statement = 'Books data has been updated'
    return render_template('index.html', statement=statement)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4415)),debug=True)
