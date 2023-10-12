import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    #df = df[['Country', "EdLevel", "YearsCodePro", "Employment", 'ConvertedCompYearly']]
    dff=df[['MainBranch','Employment','RemoteWork','EdLevel','YearsCodePro','Country','Age','ConvertedCompYearly']]
    dff = dff[dff["ConvertedCompYearly"].notnull()]
    dff = dff.dropna()
    dff = dff[dff["Employment"] == "Employed, full-time"]
    dff = dff.drop("Employment", axis=1)
    dff=dff[dff['MainBranch']=='I am a developer by profession']
    dff=dff.drop('MainBranch',axis=1)
    dff=dff[dff['RemoteWork']!='Full in-person']

    age_map={'25-34 years old':'25-34 years old','35-44 years old':'35-44 years old','18-24 years old':'18-24 years old','45-54 years old':'45-54 years old','55-64 years old':'55-64 years old','65 years or older':'others','Prefer not to say':'others','Under 18 years old':'others'}
    dff['Age'] = df['Age'].map(age_map)
    dff=dff[dff['Age']!='others']

    country_map = shorten_categories(dff.Country.value_counts(), 400)
    dff["Country"] = dff["Country"].map(country_map)
    dff = dff[dff["ConvertedCompYearly"] <= 250000]
    dff = dff[dff["ConvertedCompYearly"] >= 10000]
    dff = dff[dff["Country"] != "Other"]

    dff["YearsCodePro"] = dff["YearsCodePro"].apply(clean_experience)
    dff["EdLevel"] = dff["EdLevel"].apply(clean_education)
    dff = dff.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return dff

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()
    st.write("""#### Number of Data from different countries""")
    fig = px.pie(values=data.values, names=data.index)
    st.plotly_chart(fig)

    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data_s = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    fig1 = px.bar(y=data_s.index,x=data_s.values,labels={'y':'Countries','x':'Average Salary'},orientation='h')
    st.plotly_chart(fig1)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data_y = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data_y)
    
    data_a = df.groupby(["Age"])["Salary"].mean().sort_values(ascending=True)

    st.write(
        """
    #### Mean Salary Based On Age
    """
    )

    fig3 = px.bar(y=data_a.index,x=data_a.values,labels={'y':'Age groups','x':'Average Salary'},orientation='h')
    st.plotly_chart(fig3)



    

