import os

import numpy as np

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
        if not os.path.isfile(path + "telco.csv"):
            gdown.download(id=ids[0], output=file_paths[0], quiet=False)
        if not os.path.isfile(path + "user_engagement_data.csv"):
            gdown.download(id=ids[1], output=file_paths[1], quiet=False)


def set_path(folder="data"):
    if ("data" in os.listdir()) or ("src" in os.listdir()):
        # script running at parent directory
        path = (os.path.abspath(os.getcwd() + f"/{folder}") + "/").replace("\\", "/")
    else:
        # script running at script location
        path = (os.path.abspath(os.getcwd() + "/../../" + f"{folder}") + "/").replace("\\", "/")
    return path

def format_column_names(cols: list):
    new_cols = [i.strip().lower().replace(" ", "_") for i in cols]
    return new_cols

def resolve_outlier_iqr(df, quantiles=[.25,.75]):
    data = df.copy()
    for i in data.select_dtypes(["int", "float"]).keys():
        Q1,Q3 = data[i].quantile(quantiles)
        IQR = Q3 - Q1
        lower_range = Q1 - (1.5 * IQR)
        upper_range = Q3 + (1.5 * IQR)

        lr_ind = data[i][data[i] < lower_range].keys()
        ur_ind = data[i][data[i] > upper_range].keys()

        data.loc[lr_ind, i] = np.nan
        data[i].fillna(data[i].quantile(.1), inplace= True)

        data.loc[ur_ind, i] = np.nan
        data[i].fillna(data[i].quantile(.9), inplace= True)
    return data

def resolve_outlier_z_score(df, alpha=3):
    data = df.copy()
    for i in data.select_dtypes(["int", "float"]).keys():
        lr_ind = (data[i]
                        [(data[i] - data[i].mean()) / data[i].std() < -alpha]
                        .keys()
                        )
        
        ur_ind = (data[i]
                        [(data[i] - data[i].mean()) / data[i].std() > -alpha]
                        .keys()
                        )

        data.loc[lr_ind, i] = np.nan
        data[i].fillna(data[i].quantile(.1), inplace= True)

        data.loc[ur_ind, i] = np.nan
        data[i].fillna(data[i].quantile(.9), inplace= True)
    return data


def resolve_outlier(df, quantiles=[.25,.75], alpha=3):
    ## using z-score, then iqr
    data = df.copy()
    data = resolve_outlier_iqr(
            resolve_outlier_z_score(data, alpha),
            quantiles
            )
    return data
