# importing the necessary dependencies
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import os

app = Flask(__name__)  # initializing a flask app


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/predict', methods=['POST', 'GET'])  # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chloride = float(request.form['chloride'])
            f_sulfar_dioxide = float(request.form['free_sulfar_dioxide'])
            t_sulfar_dioxide = float(request.form['total_sulfar_dioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphate = float(request.form['sulphate'])
            alcohol = float(request.form['alcohol'])
            filename = 'red_wine.pickle'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
            # predictions using the loaded model file
            prediction = loaded_model.predict([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chloride,
                                                f_sulfar_dioxide, t_sulfar_dioxide, density, pH, sulphate, alcohol]])
            print('prediction is', prediction)
            if prediction[0] == 3:
                result = 'Bad'
                price=14.41
            elif prediction[0] == 4:
                result = 'Below Average'
                price=24.94
            elif prediction[0] == 5:
                result = 'Average'
                price=280
            elif prediction[0] == 6:
                result = 'Good'
                price=310
            elif prediction[0] == 7:
                result = 'Very Good'
                price=400
            else:
                result = 'Excellent'
                price=400+'+'
            return render_template('results.html', prediction=result,price=price)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'Something Went Wrong with server'
    # return render_template('results.html')
    else:
        return render_template('index.html')

port = int(os.getenv('PORT'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
