import logging
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash, session
import sqlite3
from configparser import ConfigParser
from chatbot import ChatBot
 # Import the model object from chatbot module
import pandas as pd
import os
from io import StringIO, BytesIO
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'IzaSyB6bQY2PYnlwcmBhKnAWc59i1KNwuhLGX8'


# app = Flask(__name__)

# Load API key from credentials.ini
config = ConfigParser()
config.read('credentials.ini')
api_key = config['gemini_ai']['API_KEY']

# Initialize chatbot
chatbot = ChatBot(api_key=api_key)
chatbot.start_conversation()

# Route for home page
@app.route('/')
def home():
    return render_template('homepage.html', title='Home')

# Route to handle user input and return bot response
@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['message']

    try:
        response = chatbot.send_prompt(user_input)
        return jsonify({'bot_response': response})  # Return JSON response
    except Exception as e:
        return jsonify({'error': str(e)})  # Return JSON response for errors


'''def send_message_to_gemini(message):
    try:
        response = model.generate_content(prompt=message, max_length=50)
        return response.text
    except Exception as e:
        logging.error(f"Error occurred while generating response: {e}")
        return None
'''

# Function to create users table
def create_users_table():
    with sqlite3.connect('users.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL,
                            college TEXT,
                            class TEXT,
                            roll_no TEXT,
                            blood_group TEXT,
                            phone_number TEXT,
                            address TEXT,
                            date_of_birth TEXT,
                            parent_details TEXT
                          )''')
        conn.commit()

# Call the function to create the users table
create_users_table()



# Route to serve the chatbot page
@app.route('/chatbot')
def show_chatbot_page():
    return render_template('chatbot.html')

# Route to send message to Gemini AI
'''
@app.route('/send-message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        if message is None:
            abort(400)
        # Log the message before sending it to the Gemini API
        logging.info(f"Sending message to Google Gemini API: {message}")
        # Send the message to the Gemini API and get the response
        response = send_message_to_gemini(message)
        # Log the response from the Gemini API
        logging.info(f"Response from Google Gemini API: {response}")
        return jsonify({'response': response})
'''
# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Placeholder for login logic
        username = request.form['username']
        password = request.form['password']
        # Verify credentials in the database
        with sqlite3.connect('users.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = cursor.fetchone()
        if user:
            flash(f'Welcome, {username}!', 'success')
            session['user_info'] = {
                'id': user[0],
                'username': user[1],
                'name': user[3],
                'email': user[4],
                'college': user[5],
                'class': user[6],
                'roll_no': user[7],
                'blood_group': user[8],
                'phone_number': user[9],
                'address': user[10],
                'date_of_birth': user[11],
                'parent_details': user[12]
            }
            return redirect(url_for('dashboard'))  # Redirect to dashboard page on successful login
        else:
            flash('Invalid login credentials. Please try again.', 'error')
    return render_template('homepage.html', title='Login')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get registration form data
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        college = request.form['college']
        class_ = request.form['class']
        roll_no = request.form['roll_no']
        blood_group = request.form['blood_group']
        phone_number = request.form['phone_number']
        address = request.form['address']
        date_of_birth = request.form['date_of_birth']
        parent_details = request.form['parent_details']
        # Insert user details into the database
        with sqlite3.connect('users.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, password, name, email, college, class, roll_no, blood_group,
                                                phone_number, address, date_of_birth, parent_details)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (username, password, name, email, college, class_, roll_no, blood_group,
                            phone_number, address, date_of_birth, parent_details))
            conn.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('homepage.html', title='Register')

# Route for user dashboard
@app.route('/dashboard')
def dashboard():
    user_info = session.get('user_info')
    if user_info:
        return render_template('dashboard.html', title='Dashboard', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for editing user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_info = session.get('user_info')
    if user_info:
        if request.method == 'POST':
            # Placeholder for profile editing logic
            pass
        return render_template('edit_profile.html', title='Edit Profile', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_info = session.get('user_info')
    if user_info:
        if request.method == 'POST':
            # Placeholder for settings logic
            pass
        return render_template('settings.html', title='Settings', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user profile
@app.route('/profile')
def profile():
    user_info = session.get('user_info')
    if user_info:
        return render_template('profile.html', title='User Profile', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Route for exploratory data analysis (EDA) form
@app.route('/example')
def eda():
    return render_template('eda.html')

@app.route('/upload', methods=['POST'])
def uploadeda():
    if 'file' not in request.files:
        return render_template('eda.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('eda.html', error='No selected file')

    if file:
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension == '.xlsx':
            df = pd.read_excel(file)
        else:
            return render_template('eda.html', error='Unsupported file format. Please upload Excel (.xlsx) ')

        # Calculate missing values
        missing_values = df.isnull().sum()

        # Display missing values as a table
        missing_values_table = missing_values[missing_values > 0].to_frame(name='Missing Values').sort_values(by='Missing Values', ascending=False)

        # Convert the table to HTML
        missing_values_html = missing_values_table.to_html(classes='data')

        # Exclude non-numeric columns from the DataFrame
        numeric_columns = df.select_dtypes(include=['number']).columns
        df_numeric = df[numeric_columns]

        # Perform EDA on the numeric DataFrame
        describe_results = df_numeric.describe().to_html(classes='data')

        # Redirect info output to a string
        info_buffer = StringIO()
        df.info(buf=info_buffer, verbose=True)  # Set verbose to True
        info_results = info_buffer.getvalue()

        # Extract unique values from each numeric column
        unique_values = {col: df_numeric[col].unique() for col in df_numeric.columns}

        # Extract column datatypes
        column_datatypes = {col: str(df.dtypes[col]) for col in df.columns}

        # Compute correlation matrix
        correlation_matrix = df_numeric.corr()

        # Generate heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
        ax.set_title('Correlation Heatmap')

        # Save the heatmap plot to a BytesIO object
        heatmap_stream = BytesIO()
        FigureCanvasAgg(fig).print_png(heatmap_stream)
        heatmap_image = base64.b64encode(heatmap_stream.getvalue()).decode('utf-8')

        # Generate box plots for each numeric column
        boxplot_images = {}
        for col in df_numeric.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(x=df_numeric[col], ax=ax)
            ax.set_title(f'Box Plot - {col}')
            boxplot_stream = BytesIO()
            FigureCanvasAgg(fig).print_png(boxplot_stream)
            boxplot_images[col] = base64.b64encode(boxplot_stream.getvalue()).decode('utf-8')

        # Generate pair plot
        pairplot_fig = sns.pairplot(df_numeric)
        pairplot_stream = BytesIO()
        pairplot_fig.savefig(pairplot_stream, format='png')
        pairplot_image = base64.b64encode(pairplot_stream.getvalue()).decode('utf-8')

        return render_template('eda_result.html',
                               df=df,
                               describe_results=describe_results,
                               info_results=info_results,
                               unique_values=unique_values,
                               column_datatypes=column_datatypes,
                               heatmap_image=heatmap_image,
                               boxplot_images=boxplot_images,
                               missing_values_table=missing_values_html,
                               pairplot_image=pairplot_image)

@app.route('/gpa',methods=['GET', 'POST'])
def gpa_calculator():
    return render_template('gpa.html',title='GPA Calculator')

@app.route('/result')
def result():
    return render_template("result.html",title='resulthtml')

def calculate_sgpa(grades, credits):
    total_points = sum(grades[i] * credits[i] for i in range(len(grades)))
    total_credits = sum(credits)

    if total_credits == 0:
        return 0  # Return 0 if total credits are zero

    sgpa = total_points / total_credits
    return sgpa

def calculate_cgpa(sgpa_list, credits_list):
    total_points = sum(sgpa_list[i] * credits_list[i] for i in range(min(len(sgpa_list), len(credits_list))))
    total_credits = sum(credits_list)

    if total_credits == 0:
        return 0  # Return 0 if total credits are zero

    cgpa = total_points / total_credits
    return cgpa

def cgpa_to_percentage(cgpa):
    percentage_equivalence = (cgpa - 0.5) * 10
    return percentage_equivalence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_semesters = int(request.form['num_semesters'])

        all_sgpa = []
        all_credits = []

        for semester in range(1, num_semesters + 1):
            semester_grades = list(map(int, request.form.getlist(f'semester{semester}_grades[]')))
            semester_credits = list(map(int, request.form.getlist(f'semester{semester}_credits[]')))

            sgpa = calculate_sgpa(semester_grades, semester_credits)
            all_sgpa.append(sgpa)
            all_credits.extend(semester_credits)

        print("All SGPA:", all_sgpa)
        print("All Credits:", all_credits)

        cgpa = calculate_cgpa(all_sgpa, all_credits)
        percentage_equivalence = cgpa_to_percentage(cgpa)

        print("CGPA:", cgpa)
        print("Percentage Equivalence:", percentage_equivalence)

        return render_template('result.html', cgpa=cgpa, percentage_equivalence=percentage_equivalence, semester_sgpa=all_sgpa, num_semesters=num_semesters)

    return render_template('gpa.html')
if __name__ == '__main__':
    app.run(debug=True)
