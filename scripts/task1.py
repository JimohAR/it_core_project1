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
        print(tabulate(top10_handet.to_frame(), tablefmt= "grid"))
        



    def get_aggregate_data(self):
        pass

    def analyse_aggregates(self):
        pass