from sklearn.metrics import mean_squared_error,mean_absolute_error
from math import sqrt
import numpy as np


# Bias of the model
def find_bias(predictions,actual):
	error = np.array(actual) - np.array(predictions)
	bias = sum(error)/len(error)
	return  bias

# Mean Squared Error
def mean_squared_error(predictions,actual):
	MSE = (sum(actual-predictions)**2)/len(predictions)
	RMSE = sqrt(MSE)
	return MSE,RMSE

# Mean Absolute Error
def mean_absolute_error(predictions,actual):
	MAE = (sum(abs(actual-predictions)))/len(predictions)
	return MAE

# Mean Absolute Percentage Error
def mean_absolute_percent_error(predictions,actual):
	y_true, y_pred = np.array(actual), np.array(predictions)
	return np.mean(np.abs((y_true - y_pred) / y_true))

# Print the results
def evaluate_model(predictions,actual):

	BIAS = find_bias(predictions,actual)
	MAE = mean_absolute_error(predictions,actual)
	MAPE = mean_absolute_percent_error(predictions,actual)
	MSE, RMSE= mean_squared_error(predictions,actual)

	print("===================================================================\n\t\t\tModel Performance\n===================================================================")
	print("\nMean Absolute Percentage Error" + str(MAPE))
	print(f"\nMean Absolute Error {MAE}")
	print(f"\nBIAS: {BIAS}")
	print(f"\nMean Squared Error {MSE}")
	print(f"\nRoot Mean Squared Error {RMSE}")
	print("===================================================================")
