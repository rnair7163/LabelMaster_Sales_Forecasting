import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import data_prep as dp
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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


@app.route('/predict',methods=['POST'])
def predict():

    books = pd.read_csv('/Users/omkarpawar/Downloads/Books_ext_fs.csv')
    books = books.dropna(axis = 1)
    sales = books[['Year_Month','Sum of Sales']]
    df = sales.sort_values("Year_Month").set_index("Year_Month")
    train = df[:int(0.8*(len(sales)))]
    test = df[int(0.8*(len(sales))):]

    model = ExponentialSmoothing((train["Sum of Sales"]), trend="add", seasonal="mul", seasonal_periods=12)
    fit = model.fit()
    output = fit.forecast(len(test))
    items = []
    for i in output.index:
        items.append(Item(i,output[i]))

    table = ItemTable(items)

    return render_template('index.html', prediction_text=table)


@app.route('/update',methods=['POST'])
def update():
    main_data = dp.main_data_transform()
    books = dp.books_data(main_data)
    external = dp.external_database()
    data = dp.final_data(books, external)
    return data

@app.route('/plot.png',methods=['POST'])
def chartTest():
    plt.plot(output.values)
    plt.plot(test.values)
    plt.title("Comparision of Actual Sales with Predictions")
    plt.xlabel("TimeLine")
    plt.ylabel("Sales")  
    plt.savefig("templates/Sales.png")
    return render_template('index.html', name = plt.show(), url ='templates/Sales.png')

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
