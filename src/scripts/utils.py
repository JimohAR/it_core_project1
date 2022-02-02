import os
import gdown 
import streamlit as st

@st.cache
def get_gdrive_file():
    id = "1LorBoIoTw1dKgPiUo9-1AfYZmU9UUBFQ"
    file_path = set_path() + "user_engagement_data.csv"
    try:    
        set_path().split('it_core_project1')[1]
    except IndexError:
        # on remote (heroku/github)
        # need to download the data for analysis
        gdown.download(id=id, output=file_path, quiet=False)


def set_path(folder="data"):
    if ("data" in os.listdir()) or ("src" in os.listdir()):
        # script running at parent directory
        path = (os.path.abspath(os.getcwd() + f"/{folder}") + "/").replace("\\", "/")
    else:
        # script running at script location
        path = (os.path.abspath(os.getcwd() + f"/../../" + f"{folder}") + "/").replace("\\", "/")
    return path

def format_column_names(cols: list):
    new_cols = [i.strip().lower().replace(" ", "_") for i in cols]
    return new_cols


