import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pickle

pack = pd.read_csv('packaging_data.csv')
sales = pack['Sum of Sales']
date = pack['Year_Month']

# running the model
mod = sm.tsa.statespace.SARIMAX(sales,
                                order=(0, 1, 1),
                                seasonal_order=(0, 1, 1, 12))


results = mod.fit()
print(results.summary())
results.plot_diagnostics(figsize=(16, 8))
plt.show()

# saving the final model
pickle.dump(results, open('sarima_packaging_model.pkl', 'wb'))
print("Model Saved")