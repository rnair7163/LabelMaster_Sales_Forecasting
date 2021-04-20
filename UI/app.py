import numpy as np
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import dateutil.relativedelta
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
model = pickle.load(open('sarima_model.pkl', 'rb'))


@app.route('/books')
def home():
    return render_template('index.html')


def model_data():
    books = pd.read_csv('books_data.csv')
    books = books.dropna(axis = 1)
    sales = books['Sum of Sales']
    date = books['Year_Month']
    date = pd.to_datetime(date)
    pred_uc = model.get_forecast(steps=12)
    pred_ci = pred_uc.conf_int()
    pred_unscaled_ind = pred_uc.predicted_mean
    pred_unscaled = pred_unscaled_ind .reset_index(drop=True)
    return date, pred_unscaled, sales, pred_ci, pred_unscaled_ind


@app.route('/')
def welcome():
    return render_template('welcome.html')


def future_dates(date):
    future = []
    for i in range(1,13):
        future.append(datetime.strftime(date.iloc[-1] + dateutil.relativedelta.relativedelta(months=i), '%Y-%m'))
    return future


@app.route('/predict',methods=['POST'])
def predict():
    date, pred_unscaled, sales, pred_ci, pred_unscaled_ind = model_data()
    future = future_dates(date)
    headings = ("Date", "Total Sales ($)")
    data = []
    for i in range(len(future)):
        data.append([future[i],round(pred_unscaled[i],3)])
    return render_template('index.html', headings=headings, data=data)


@app.route('/plot',methods=['POST'])
def plot():
    date, pred_unscaled, sales, pred_ci, pred_unscaled_ind = model_data()
    fig, ax = plt.subplots()
    ax = sales.plot(label='observed', figsize=(14, 7))
    pred_unscaled_ind.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Number of Observations')
    ax.set_ylabel('Sales')
    plt.legend()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


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
