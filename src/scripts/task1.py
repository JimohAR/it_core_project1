from tabulate import tabulate
import pandas as pd
class task1:
    def __init__(self, data):
        self.data = data 
        pass 

    def user_overview_analysis(self):
        ## stripping out the column names for easy parsing
        new_data_col = [i.strip() for i in list(self.data.columns)]
        self.data.columns = new_data_col

        handset_data = self.data[['Handset Manufacturer', 'Handset Type',]]
        top10_handet = handset_data["Handset Type"][handset_data["Handset Type"] != "undefined"].value_counts()[:10]
        print(">> top 10 handsets used by customers")
        print(tabulate(top10_handet.to_frame(), tablefmt= "grid"))

        top3_manufacturers = handset_data["Handset Manufacturer"][handset_data["Handset Manufacturer"] != "undefined"].value_counts().head(3)
        print("\n>> top 3 handsets manufacturers patronized by customers")
        print(tabulate(top3_manufacturers.to_frame(), tablefmt= "grid"))

        handsets_by_top3_manufacturers = handset_data.set_index(keys= ["Handset Manufacturer"]).loc[top3_manufacturers.keys()]
        top5_of_top3_manufacturers_dict = dict()
        for i in top3_manufacturers.keys():
            top5_of_top3_manufacturers_dict[i] = handsets_by_top3_manufacturers.loc[i, "Handset Type"].value_counts().head(5)
        
        top5_of_top3_manufacturers = pd.DataFrame.from_dict(top5_of_top3_manufacturers_dict, orient= "index").stack()
        top5_of_top3_manufacturers.name = "count"
        top5_of_top3_manufacturers = top5_of_top3_manufacturers.to_frame()

        print("\n>> top 5 handsets produced by the top 3 handset manufacturers patronized by customers")
        print(tabulate(top5_of_top3_manufacturers, tablefmt= "grid"))





    def get_aggregate_data(self):
        pass

    def analyse_aggregates(self):
        pass