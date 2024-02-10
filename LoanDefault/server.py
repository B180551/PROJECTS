from flask import Flask, request, render_template
import pickle

# Load the model
with open('/home/ak/PROJECT/APPLICATION/rfcmodel', 'rb') as file:
    model = pickle.load(file)

# Create a Flask application
app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    # Read the file contents and send them to the client
    return render_template('index.html')

@app.route("/classify", methods=["POST"])
def classify():
    # Get the values entered by the user
    age = float(request.form.get("Age"))
    income = float(request.form.get("Income"))
    loan_amount = float(request.form.get("LoanAmount"))
    credit_score = float(request.form.get("CreditScore"))
    months_employed = float(request.form.get("MonthsEmployed"))
    interest_rate = float(request.form.get("InterestRate"))
    loan_term = float(request.form.get("LoanTerm"))
    employment_type = request.form.get("EmploymentType")
    has_mortgage = float(request.form.get("HasMortgage"))
    has_dependents = float(request.form.get("HasDependents"))
    has_co_signer = float(request.form.get("HasCoSigner"))

    # Prepare the input data for prediction
    input_data = [
        [age, income, loan_amount, credit_score, months_employed, interest_rate, loan_term, employment_type, has_mortgage, has_dependents, has_co_signer]
    ]

    # Make the prediction
    prediction = model.predict(input_data)

    # Display the prediction result
    result = "Loan Approved" if prediction[0] == 1 else "Loan Denied"
    
    return render_template('result.html', result=result)

# Start the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

