import pandas as pd
import numpy as np
from datetime import datetime
import sys

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split


data_path = "./covid-19-data/us-states.csv"
days_to_train_on = float(sys.argv[1])

def pullState(data_path = data_path):
	#convert date col to datetime object
	stateDF = pd.read_csv(data_path)
	stateDF['date'] = pd.to_datetime(stateDF['date'], format='%Y/%m/%d').dt.date

	#select only the required dates
	cutoff_date = stateDF["date"].iloc[-1] - pd.Timedelta(days=days_to_train_on)
	stateDF = stateDF[stateDF['date'] > cutoff_date]

	#drop useless columns
	stateDF = stateDF.drop(columns = ["fips","deaths", "date"])

	stateDF = pd.get_dummies(stateDF)
	return stateDF

def create_model(stateDF):
	reg_model = LinearRegression()
	y = stateDF["cases"]
	X = stateDF.drop(columns="cases")
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state = 42)
	reg_model.fit(X_train, y_train)
	#print(reg_model.score(X_test, y_test))
	return reg_model


	



def make_prediction(model, stateDF):
	data = []
	n = len(stateDF.columns)
	for i in range(n):
		array = np.zeros(n, dtype = object)
		array[i] = 1
		data.append(array)
	prediction = pd.DataFrame(data, columns=stateDF.columns)
	prediction = prediction.drop(columns = "cases").iloc[1:]
	
	
	y_pred = model.predict(prediction)
	#insert it to the first column to match the format of stateDF	
	prediction.insert(0, "cases", y_pred)
	
	return prediction


def make_3day_prediction(model, stateDF):
	result = pd.DataFrame(columns=stateDF.columns)
	for i in range(3):
		print("this is the" ,i, "iteration" )
		prediction = make_prediction(model, stateDF)
		stateDF = stateDF.append(prediction, ignore_index = True)
		print(len(stateDF))
		y = stateDF["cases"]
		X = stateDF.drop(columns="cases")
		model.fit(X, y)
		result = result.append(prediction, ignore_index = True)
	return result


	##1. stateDF append new data
	##2. use the model to fit new data
	##3. repeat the process


stateDF = pullState()
model = create_model(stateDF)
result = make_3day_prediction(model, stateDF)
result.to_csv('predictions.csv')












