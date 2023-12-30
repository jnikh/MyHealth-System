import streamlit as st
import sqlite3
import hashlib
import pickle

# Loading the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('userdata.db')
    return conn

# Function to create a user table if it doesn't exist
def create_user_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function for user signup
def signup(username, password):
    conn = create_connection()
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        st.success("You've successfully signed up!")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")

# Function for user signin
def signin(username, password):
    conn = create_connection()
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

# SessionState class to manage session data
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

session_state = SessionState(page=None)

def auth_page():
    st.title('Sign Up / Sign In')
    create_user_table(create_connection())
    menu = st.sidebar.selectbox("Menu", ["Sign Up", "Sign In"])

    if menu == "Sign Up":
        st.header("Sign Up")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Sign Up"):
            signup(new_username, new_password)

    elif menu == "Sign In":
        st.header("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Sign In"):
            if signin(username, password):
                session_state.page = 'prediction'  # Update session state
                prediction_page()

def prediction_page():
    st.title("My Health - Predictions")
    selected = st.sidebar.selectbox('Choose Prediction', ['Diabetes', 'Heart Disease', 'Parkinsons'])

    if session_state.page == 'prediction':  # Ensure the session is in the prediction phase
        if selected == 'Diabetes':
            # Your code for Diabetes prediction here
            st.subheader('Diabetes Prediction')
            # Data input using columns
            col1,col2,col3=st.columns(3)
            with col1:
                Pregnancies=st.text_input('Number of Pregnancies')
            with col2:
                Glucose=st.text_input('Glucose Level')
            with col3:
                BloodPressure=st.text_input('Blood Pressure Value')
            with col1:
                SkinThickness=st.text_input('Skin Thickness value')
            with col2:
                Insulin = st.text_input('Insulin Level')
            with col3:
                BMI = st.text_input('BMI value')
            with col1:
                DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
            with col2:
                Age = st.text_input('Age of the Person')

         # code for Prediction
            diab_diagnosis = ''

            if st.button('Diabetes Test Result'):
                diab_prediction=diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
                if(diab_prediction[0]==1):
                    diab_diagnosis='The Person is diabetic'
                else:
                    diab_diagnosis='The Person is not diabetic'

            st.success(diab_diagnosis)

            
            # ...
        elif selected == 'Heart Disease':
            # Your code for Heart Disease prediction here
            pass
        elif selected == 'Parkinsons':
            # Your code for Parkinsons prediction here
            pass
    else:
        st.write("Please sign in to access predictions.")


        
  

def main():
    if session_state.page is None:
        auth_page()
    else:
        prediction_page()

if __name__ == "__main__":
    main()