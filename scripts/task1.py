from tabulate import tabulate
class task1:
    def __init__(self, data):
        self.data = data 
        pass 

    def user_overview_analysis(self):
        ## stripping out the column names for easy parsing
        new_data_col = [i.strip() for i in list(self.data.columns)]
        self.data.columns = new_data_col

        handset_data = self.data[['Handset Manufacturer', 'Handset Type',]]
        top10_handet = handset_data["Handset Type"][handset_data["Handset Type"] != "undefined"].value_counts()
        print(">> top 10 handsets used by customers")
        print(tabulate(top10_handet.to_frame(), tablefmt= "grid"))

        top3_manufacturers = handset_data["Handset Manufacturer"][handset_data["Handset Manufacturer"] != "undefined"].value_counts().head(3)
        print(">> top 3 handsets manufacturers patronized by customers")
        print(tabulate(top3_manufacturers.to_frame(), tablefmt= "grid"))

        






    def get_aggregate_data(self):
        pass

    def analyse_aggregates(self):
        pass