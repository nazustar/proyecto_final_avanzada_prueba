# https://youtu.be/bluclMxiUkA
"""
Application that predicts heart disease percentage in the population of a town
based on the number of bikers and smokers. 

Trained on the data set of percentage of people biking 
to work each day, the percentage of people smoking, and the percentage of 
people with heart disease in an imaginary sample of 500 towns.

"""

import numpy as np
from flask import Flask, request, render_template
import pickle
import os


#Creación de la base de datos.
from flask_sqlalchemy import SQLAlchemy #Importar biblioteca.

#identificacion de rutas para que sepa donde esta todo 
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'modelo', 'model.pkl')
app = Flask(__name__, template_folder='../vista')

#Para que encuentre el directorio que es:
db_path = os.path.abspath(os.path.join(base_dir, 'database.db'))

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Para poder usar db.
db = SQLAlchemy(app)

class Prediccion(db.Model): #Crea la tabla.

    #Llave identificadora de la consulta.
    id=db.Column(db.Integer, primary_key=True)

    #Resutados de la consulta.
    biking = db.Column(db.Float)
    smoking = db.Column(db.Float)
    result = db.Column(db.Float)

    def __repr__(self):
        return f'<Prediccion {self.id}>'

try:
    model = pickle.load(open(model_path, 'rb'))
except Exception as e:
    print(f"error al cargar el modelo: {e}. asegurese de que model.pkl exista en la carpeta modelo/")
    model = None

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.


@app.route('/')
def home():
    return render_template('index.html')

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output
@app.route('/predict',methods=['POST'])
def predict():

    int_features = [float(x) for x in request.form.values()] #Convert string inputs to float.
    features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
    prediction = model.predict(features)  # features Must be in the form [[a, b]]

    output = round(prediction[0], 2)

    #Para ser guardado en la base al ejecutar.
    pred = Prediccion(
        biking = int_features[0],
        smoking = int_features[1],
        result = output
    )
    db.session.add(pred)
    db.session.commit()

    return render_template('index.html', prediction_text='Percent with heart disease is {}'.format(output))


#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).
