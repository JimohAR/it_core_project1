# Model deployment tracking- deploy the model
# and monitor your model. Here you can use Docker
# or other MlOps tools which can help you
# to track your model’s change.
# Your model tracking report includes code version,
# start and end time, source, parameters,
# metrics (loss convergence),
# and artifacts or any output file regarding each specific run.
# (CSV file, screenshot)

import os
import pickle
import sys

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import RidgeCV
from sklearn.metrics import accuracy_score, r2_score

base_path = os.path.abspath(os.getcwd().split("src")[0])
if base_path not in sys.path:
    sys.path.append(base_path)
    
from src.scripts.utils import get_gdrive_files, set_path

path = set_path("data")
get_gdrive_files()

@st.cache
def load_data(nrows=500):
    data = pd.read_csv(path + "user_engagement_data.csv", index_col='MSISDN').iloc[:nrows]
    return data


# make the sidebar
bar = st.sidebar
options = bar.radio("Choose Option", ("Sample Data", "Stats", "Get Predictions"), index=0)

# title
align_center = """\
<h1 style='text-align: center; color: black;'>
    {}
</h1>"""
st.write(align_center.format("it core".upper()), unsafe_allow_html=True)

st.write("#### __MODEL NAME : `Ridge regression`__")

st.write("#### __PERFORMANCE METRIC : `r2 score(coefficient of determination)`__")

st.write("#### __MODEL PARAMETERS__")
st.code("""\
{'alpha_per_target': False,
'alphas': array([ 0.1,  1. , 10. ]),
'cv': 5,
'fit_intercept': True,
'gcv_mode': None,
'normalize': 'deprecated',
'scoring': None,
'store_cv_values': False}""")

placeholder = st.empty()

# open show sample data pane
if options == "Sample Data":
    with placeholder.container():
        st.write("""#### __SAMPLE DATA__""")
        st.dataframe(load_data())

########## open get_predictions pane ##########
if options == "Get Predictions":
    placeholder.empty()
    with placeholder.container():
        st.write("""#### __GET PREDICTIONS__""")
        # load the model 
        model = pickle.load(open(path + "model.pkl", "rb"))
        # get the column names
        data1 = pd.read_csv(path + "test_case.csv", index_col=0)

        # there will be two input methods: manually or through a file
        input_method = st.radio("choose method", ("manual", "upload data"))
        if input_method == "manual":
            inputs = {}
            for col in data1.columns:
                df = data1[col]
                value = st.number_input(col, df.min(), df.max(), df.mean(), (df.max() - df.min()) / 100.0)
                inputs[col] = value
            new_input = np.array(list(inputs.values())).reshape(1, -1)
            if st.button("predict"):
                st.success(f"#### __RESULT__: {model.predict(new_input)[0]}")
            else:
                st.empty()
        elif input_method == "upload data":
            inputs = st.file_uploader("upload a csv file with the input(s)", ["csv"])
            if inputs != None:
                new_input = pd.read_csv(inputs, header=None).to_numpy().reshape(1, -1)
                if st.button("predict"):
                    st.success(f"#### __RESULT__: {model.predict(new_input)[0]}")
                else:
                    st.empty()

# view src
st.markdown(""" """)
link = """[<center> <img src= https://raw.githubusercontent.com/JimohAR/it_core_project1/83f661b2beb7ad2be52c8fd47a2d9deab38e865f/data/github.svg alt="view source"/> </center>](https://github.com)"""
link2 = \
"""<center> 
    <a href="https://github.com/JimohAR/it_core_project1/tree/reformat_codebase" target="_blank" rel="noopener noreferrer">
        <img src= https://raw.githubusercontent.com/JimohAR/it_core_project1/83f661b2beb7ad2be52c8fd47a2d9deab38e865f/data/github.svg alt="view source"/>
    </a>
</center>"""
st.markdown(link2, unsafe_allow_html=True)
