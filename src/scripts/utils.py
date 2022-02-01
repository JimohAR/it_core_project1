import os


def set_path(folder="data"):
    if ("data" in os.listdir()) or ("src" in os.listdir()):
        # script running at parent directory
        path = (os.path.abspath(os.getcwd() + f"/{folder}") + "/").replace("\\", "/")
    else:
        # script running at script location
        path = (os.path.abspath(os.getcwd() + f"/../../" + f"{folder}") + "/").replace("\\", "/")
    try:    
        print(f"\n>> set to: \n...\tit_core_project1{path.split('it_core_project1')[1]}")
    except:
        print(f"\n>> set to: \n...\t{path}")
    return path

def format_column_names(cols: list):
    new_cols = [i.strip().lower().replace(" ", "_") for i in cols]
    return new_cols

