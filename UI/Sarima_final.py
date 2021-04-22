import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pickle

books = pd.read_csv('books_data.csv')
sales = books['Sum of Sales']
date = books['Year_Month']

# running the model
mod = sm.tsa.statespace.SARIMAX(sales,
                                order=(1, 0, 0),
                                seasonal_order=(0, 1, 1, 12))
results = mod.fit()
print(results.summary())
results.plot_diagnostics(figsize=(16, 8))
plt.show()

# saving the final model
pickle.dump(results, open('sarima_model.pkl', 'wb'))
print("Model Saved")
