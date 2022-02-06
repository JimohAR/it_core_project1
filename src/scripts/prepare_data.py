import os
import sys

import pandas as pd

base_path = os.getcwd().split("it_core_project1")[0] + "it_core_project1"
sys.path.append(base_path)
from src.scripts.utils import set_path
from src.scripts.utils import get_gdrive_files
from src.scripts.utils import format_column_names


path = set_path()
get_gdrive_files()


data = pd.read_csv(path + "telco.csv").iloc[:-1, :]

# creates consistent column names format
data.columns = format_column_names(data.columns)

cols = [
   "msisdn/number" , "dur._(ms)", "avg_rtt_dl_(ms)", "avg_rtt_ul_(ms)", "avg_bearer_tp_dl_(kbps)",
   "avg_bearer_tp_ul_(kbps)", "tcp_dl_retrans._vol_(bytes)", "tcp_ul_retrans._vol_(bytes)", "http_dl_(bytes)",
   "http_ul_(bytes)", "handset_manufacturer", "handset_type", "social_media_dl_(bytes)", "social_media_ul_(bytes)",
   "google_dl_(bytes)", "google_ul_(bytes)", "email_dl_(bytes)", "email_ul_(bytes)", "youtube_dl_(bytes)", "youtube_ul_(bytes)", 
   "netflix_dl_(bytes)", "netflix_ul_(bytes)", "gaming_dl_(bytes)", "gaming_ul_(bytes)", "other_dl_(bytes)", "other_ul_(bytes)", 
   "total_ul_(bytes)", "total_dl_(bytes)"
]

useful_data = data[cols]
useful_data.to_csv(path + "useful_data.csv", index=False)