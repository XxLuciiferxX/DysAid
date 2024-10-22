
from flask import Flask, render_template, redirect, url_for, request, flash
import subprocess
import webbrowser
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # For flashing messages

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['contact_db']  # Database name
contacts_collection = db['contacts']  # Collection name
subscribe_collection = db['subscribe']

# Route for the landing page (index.html)
@app.route('/', methods=['GET', 'POST'])

def landing_page():
    if request.method == 'POST':
        if 'subscribe_email' in request.form:  # Subscribe form submitted
            email = request.form['subscribe_email']

            # Create a new subscriber document
            new_subscriber = {
                "email": email
            }

            # Insert the document into MongoDB
            subscribe_collection.insert_one(new_subscriber)

            flash('Thank you for subscribing!', 'success')
            return redirect(url_for('landing_page'))

        elif 'contact_name' in request.form:  # Contact Us form submitted
            name = request.form['contact_name']
            email = request.form['contact_email']
            message = request.form['contact_message']

            # Create a new contact document
            new_contact = {
                "name": name,
                "email": email,
                "message": message
            }

            # Insert the document into MongoDB
            contacts_collection.insert_one(new_contact)

            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('landing_page'))

    return render_template('index.html')
@app.route('/exp')
def experience_page():
    return render_template('exp.html')

# Route to start Streamlit app
@app.route('/run-streamlit')

def run_streamlit():
    # Start the Streamlit app using subprocess
    subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
   
    # Redirect to the Streamlit app URL
    return redirect('http://localhost:8501')

if __name__ == '__main__':
    app.run(debug=True)