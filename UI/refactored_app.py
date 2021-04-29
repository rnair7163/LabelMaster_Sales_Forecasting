import io
import pickle
import pandas as pd
from flask import Flask, render_template, Response
from datetime import datetime
import dateutil.relativedelta
import data_prep as dp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
model_books = pickle.load(open('models/sarima_model.pkl', 'rb'))
model_package = pickle.load(open('models/sarima_packaging_model.pkl', 'rb'))


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/books')
def home():
    return render_template('books.html')


@app.route('/packaging')
def packaging():
    return render_template('packaging.html')


@app.route('/updateBooks',methods=['POST'])
def updateBooks():
    main_data = dp.main_data_transform()
    books = dp.books_data(main_data)
    books.to_csv('dataframes/books_data.csv')
    dp.sarima_books(books)
    statement = 'Books data has been updated'
    return render_template('books.html', statement=statement)


@app.route('/updatePackaging',methods=['POST'])
def updatePackaging():
    main_data = dp.main_data_transform()
    packaging = dp.packaging_data(main_data)
    packaging.to_csv('dataframes/packaging_data.csv')
    dp.sarima_package(packaging)
    statement = 'Packaging data has been updated'
    return render_template('packaging.html', statement=statement)


def model_data(filepath):
    data = pd.read_csv(filepath)
    data = data.dropna(axis = 1)
    sales = data['Sum of Sales']
    date = data['Year_Month']
    date = pd.to_datetime(date)
    if filepath == 'dataframes/books_data.csv':
        pred_uc = model_books.get_forecast(steps=12)
    else:
        pred_uc = model_package.get_forecast(steps=12)
    pred_ci = pred_uc.conf_int()
    pred_unscaled_ind = pred_uc.predicted_mean
    pred_unscaled = pred_unscaled_ind.reset_index(drop=True)
    return date, pred_unscaled, sales, pred_ci, pred_unscaled_ind


def books_forecast(filepath):
    date, pred_unscaled, sales, pred_ci, pred_unscaled_ind = model_data(filepath)
    future = future_dates(date)
    headings = ("Date", "Total Sales ($)")
    data = []
    for i in range(len(future)):
        data.append([future[i],round(pred_unscaled[i],3)])
    return (headings, data)


def package_forecast(filepath):
    date, pred_unscaled, sales, pred_ci, pred_unscaled_ind = model_data(filepath)
    future = future_dates(date)
    headings = ("Date", "Total Sales ($)")
    data = []
    for i in range(len(future)):
        data.append([future[i],round(pred_unscaled[i],3)])
    return (headings, data)


def future_dates(date):
    future = []
    for i in range(1,13):
        future.append(datetime.strftime(date.iloc[-1] + dateutil.relativedelta.relativedelta(months=i), '%Y-%m'))
    return future


def plot(filepath):
    date, pred_unscaled, sales, pred_ci, pred_unscaled_ind = model_data(filepath)
    fig = Figure(figsize=(25,15))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(sales, label='Observed', linewidth=5)
    ax.plot(pred_unscaled_ind, label='Forecast', linewidth=5)
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_title('Forecast for Next 12 months', fontsize=25)
    ax.set_xlabel('Number of Observations', fontsize=20)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(20)
    ax.set_ylabel('Sales', fontsize=20)
    ax.legend(prop={"size":20})
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/predictBooks',methods=['POST'])
def predictBooks():
    books_data_filepath = "dataframes/books_data.csv"
    headings, data = books_forecast(books_data_filepath)
    return render_template('books.html', headings=headings, data=data)


@app.route('/predictPackaging',methods=['POST'])
def predictPackaging():
    packaging_data_filepath = "dataframes/packaging_data.csv"
    headings, data = package_forecast(packaging_data_filepath)
    return render_template('packaging.html', headings=headings, data=data)


@app.route('/plotBooks',methods=['POST'])
def plotBooks():
    books_data_filepath = "dataframes/books_data.csv"
    return plot(books_data_filepath)


@app.route('/plotPackaging',methods=['POST'])
def plotPackaging():
    packaging_data_filepath = "dataframes/packaging_data.csv"
    return plot(packaging_data_filepath)


if __name__ == "__main__":
    app.run()
