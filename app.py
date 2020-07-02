from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

app=Flask(__name__)
a=open("car.pkl","rb")
model=pickle.load(a)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year=int(request.form['Year'])
        Present_Price=int(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])

        Fuel_Type=request.form['Fuel_Type']
        if(Fuel_Type=='Petrol'):
                Fuel_Type=2

        elif(Fuel_Type=='Diesel'):

            Fuel_Type=1
        else:
            Fuel_Type=0
        Year=2020-Year

        Seller_Type=request.form['Seller_Type']
        if(Seller_Type=='Individual'):
            Seller_Type=1
        else:
            Seller_Type=0

        Transmission=request.form['Transmission']
        if(Transmission=='Mannual'):
            Transmission=1
        else:
            Transmission=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type,Seller_Type,Transmission]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
