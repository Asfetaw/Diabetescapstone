"""importing standard library """
import os
import pandas as pd
import numpy as np
import dill
from flask import Flask, render_template, request #, redirect


APP = Flask(__name__)
#APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#DB = SQLAlchemy(APP)

PEOPLE_FOLDER = os.path.join('/static', 'image')
APP.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

"""
Function to process the input requests
"""

@APP.route('/', methods=['POST', 'GET'])
@APP.route('/mainform', methods=['POST', 'GET'])
def capstoneproject():

    result = request.form.to_dict()
    estimator = dill.load(open("./static/image/KNN_est.dill", "rb"))
    predict_input = pd.DataFrame(columns=['AGE', 'SEX', 'BMI', 'BP', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'] )
    inputvalue = np.zeros(10)
    for index, val in enumerate(list(result.values())):
        if val == 'female':
            inputvalue[index] = 1
        elif val == 'male':
            inputvalue[index] = 2
        elif val == "":
            #check if your didn't input value after the fourth serum. use the average value
            average_imputation = {7:4.07 , 8:4.6, 9:91.26 }
            inputvalue[index] = average_imputation[index]
        else:
            try:
                inputvalue[index] = float(val)
            except:
                predicted_value = "Ooops!  Unabale to process your request . please provide only  numeric data " # + str(e)
                return render_template('Capstoneproject.html', Result = predicted_value)


    
      
    predict_input.loc[0] = inputvalue

    try:
        predicted_value = float(estimator.predict(predict_input)) - 43.01
        flag = ""
        if predicted_value >= 55 and predicted_value <= 109:
            flag = "Normal"
        if predicted_value >= 110 and predicted_value <= 125:
            flag = "Pre-diabetic"
        if predicted_value >= 126:
            flag = "Diabetic"
        return render_template('Capstoneproject.html', Result = predicted_value , Flag=flag)
    except Exception as e:
        predicted_value = "Ooops!  Unabale to process your request . please provide only  numeric data " # + str(e)
        return render_template('Capstoneproject.html', Result = predicted_value)


@APP.route('/Visualize/')
def Visualize():
    
    return render_template('Visualize.html')

@APP.route('/contact/')
def contact():
    
    return render_template('contact.html')

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(debug=True, port=PORT)
