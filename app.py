import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('regmodel_insurance_cost.pkl', 'rb'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        # Get values from form
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = 1 if request.form['smoker'].lower() == "yes" else 0

        # Gender mapping
        gender_map = {"male": 0, "female": 1}
        gender = gender_map.get(request.form['gender'].lower(), 0)

        # Region mapping
        region_map = {"southwest":0, "southeast":1, "northwest":2, "northeast":3}
        region = region_map.get(request.form['region'].lower(), 0)

        # Make prediction
        prediction = model.predict([[age, gender, bmi, children, smoker, region]])
        predicted_cost = round(prediction[0], 2)

        # Render result page
        return render_template('result.html', cost=predicted_cost)

    # GET request just shows the form
    return render_template('form.html')

# Redirect root to /form
@app.route('/')
def home():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)
