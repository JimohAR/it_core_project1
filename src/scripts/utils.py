import os
import gdown 


def get_gdrive_files():
    path = set_path()
    ids = ["1YaYSDui8cefj0aYmlY_i6eKz-q0fnNbN", "1LorBoIoTw1dKgPiUo9-1AfYZmU9UUBFQ"]
    file_paths = [path + "telco.csv", path + "user_engagement_data.csv"]
    try:    
        path.split('it_core_project1')[1]
    except IndexError:
        # on remote (heroku/github)
        # need to download the some data for analysis
        if not (os.path.isfile(path + "telco.csv")):
            gdown.download(id=ids[0], output=file_paths[0], quiet=False)
        if not (os.path.isfile(path + "user_engagement_data.csv")):
            gdown.download(id=ids[1], output=file_paths[1], quiet=False)

            

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


