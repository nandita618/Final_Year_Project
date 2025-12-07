import os
import pickle
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Heart Disease Predictor",
    layout="wide",
    page_icon="❤️",
    initial_sidebar_state="expanded"
)

# Working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load Heart Disease model
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))

# Custom CSS for fully readable UI
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #ccefff, #99e6ff);
        }
        .form-card {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            margin-bottom: 30px;
        }
        .stTextInput>div>div>input, 
        .stNumberInput>div>input {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
            background-color: #ffffff; 
            color: #000000;
        }
        label, .stMarkdown p {
            color: #000000;
            font-weight: 600;
        }
        .result-card {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
        }
        .positive {
            background-color: #ffe5e5; 
            color: #d9534f;
        }
        .negative {
            background-color: #e5ffe5; 
            color: #28a745;
        }
        div.stButton > button:first-child {
            background-color: #007acc;
            color: white;
            padding: 12px 30px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        }
        div.stButton > button:first-child:hover {
            background-color: #005f99;
        }
        ::placeholder {
            color: #999999;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Heart Disease Page ----------
st.title("❤️ Heart Disease Predictor")
st.write("Enter your details below to check your heart disease risk:")

with st.form("heart_form"):
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    # Arrange input fields in 3 columns
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', min_value=1, max_value=120, value=30)
        trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=50, max_value=250, value=120)
        restecg = st.number_input('Resting ECG results (0,1,2)', min_value=0, max_value=2, value=0)
        oldpeak = st.number_input('ST depression induced by exercise', min_value=0.0, max_value=10.0, value=1.0)
        thal = st.number_input('Thalassemia (0,1,2)', min_value=0, max_value=2, value=1)
    with col2:
        sex = st.number_input('Sex (0=Female, 1=Male)', min_value=0, max_value=1, value=1)
        chol = st.number_input('Serum Cholesterol (mg/dl)', min_value=100, max_value=600, value=200)
        thalach = st.number_input('Maximum Heart Rate Achieved', min_value=60, max_value=250, value=150)
        slope = st.number_input('Slope of peak exercise ST segment (0,1,2)', min_value=0, max_value=2, value=1)
    with col3:
        cp = st.number_input('Chest Pain Type (0-3)', min_value=0, max_value=3, value=0)
        fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl (0=No,1=Yes)', min_value=0, max_value=1, value=0)
        exang = st.number_input('Exercise Induced Angina (0=No,1=Yes)', min_value=0, max_value=1, value=0)
        ca = st.number_input('Major vessels colored by fluoroscopy (0-4)', min_value=0, max_value=4, value=0)

    st.markdown('</div>', unsafe_allow_html=True)

    submit = st.form_submit_button("🔍 Predict Heart Disease")

if submit:
    try:
        user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
        heart_prediction = heart_disease_model.predict([user_input])
        result = "The person has heart disease ❤️" if heart_prediction[0] == 1 else "The person does not have heart disease ✅"
        color = "positive" if heart_prediction[0] == 1 else "negative"
        st.markdown(f"<div class='result-card {color}'>{result}</div>", unsafe_allow_html=True)
    except:
        st.error("Please fill all fields with valid numeric values.")
