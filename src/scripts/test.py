import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

## run from the topmost folder i.e it_core_project1
## or adjust the path as approriate
path = os.getcwd() + "/data/"
data = pd.read_csv(path + "telco.csv").iloc[:-1]

from task1 import Task1

####### USER OVERVIEW ANALYSIS#######
overview = Task1(data)
overview.user_overview_analysis()

####### DATA USAGE BY CUSTOMERS ######
overview.get_aggregate_data()