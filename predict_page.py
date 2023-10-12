import streamlit as st
import pickle
import numpy as np

def load_model():
     with open('saved_steps_01.pkl', 'rb') as file:
        data = pickle.load(file)
     return data
    
data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_age=data["le_age"]
le_remote=data["le_remote"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "India",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Italy",
        "Poland",
        "Sweden",
        "Russian Federation",
        "Switzerland",
    )

    education_d = (
        "Master’s degree",
        "Bachelor’s degree",
        "Less than a Bachelors",
        "Post grad"
    )

    age_d={
        "25-34 years old",
        "35-44 years old",    
        "18-24 years old",    
        "45-54 years old",     
        "55-64 years old" 
    }

    remote_d={
        "Fully remote",
        "Hybrid (some remote, some in-person)"
    }

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education_d)
    expericence = st.slider("Years of Experience", 0, 50, 3)
    age=st.selectbox("Age",age_d)
    remote=st.selectbox("Mode of Work",remote_d)
    ok = st.button("Calculate Salary")

    if ok:
        X = np.array([[country, education, expericence, age, remote]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X[:, 3] =le_age.transform(X[:,3])
        X[:, 4] =le_remote.transform(X[:,4])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")