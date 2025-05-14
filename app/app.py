from flask import Flask, redirect, render_template, request, url_for
import pickle

app = Flask(__name__)

# Load the trained Random Forest model
import os

# Get the absolute file path 2
file_path = os.path.abspath('C:/Users/hegde/OneDrive/Desktop/Datasets/models/RandomForest.pkl')

# Load the trained Random Forest model
with open(file_path, 'rb') as model_file:
    model = pickle.load(model_file)


valid_users = {
    'admin': '123',
    'shashank': 'abc123',
    'guest': 'xyz123'
}

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password are valid
        if username in valid_users and valid_users[username] == password:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password. Please try again.')
    else:
        return render_template('login.html')

# Route for index page (requires authentication)
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')


# Route for logout (not used in this version)
@app.route('/logout')
def logout():
    return redirect(url_for('home'))

# Define route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from form
    N = float(request.form['N'])
    P = float(request.form['P'])
    K = float(request.form['K'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['rainfall'])
    
    # Perform prediction using the loaded model
    prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # Redirect to the result page with the prediction result as a query parameter
    return redirect(url_for('result', prediction=prediction[0]))

# Define route for displaying prediction result on a new page
@app.route('/result')
def result():
    # Get the prediction result from the URL parameter
    prediction = request.args.get('prediction')
    
    # Render the result template and pass the prediction result to it
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
