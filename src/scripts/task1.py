from tabulate import tabulate
import pandas as pd
import numpy as np

class Task1:
    def __init__(self, data):
        self.data = data

    def user_overview_analysis(self):
        # stripping out the column names for easy parsing
        new_data_col = [i.strip() for i in list(self.data.columns)]
        self.data.columns = new_data_col

        handset_data = self.data[['Handset Manufacturer', 'Handset Type', ]]
        top10_handset = handset_data["Handset Type"][handset_data["Handset Type"] != "undefined"].value_counts()[:10]
        print(">> top 10 handsets used by customers")
        print(tabulate(top10_handset.to_frame(), tablefmt="grid"))

        top3_manufacturers = handset_data["Handset Manufacturer"][
            handset_data["Handset Manufacturer"] != "undefined"].value_counts().head(3)
        print("\n>> top 3 handsets manufacturers patronized by customers")
        print(tabulate(top3_manufacturers.to_frame(), tablefmt="grid"))

        handsets_by_top3_manufacturers = handset_data.set_index(keys=["Handset Manufacturer"]).loc[
            top3_manufacturers.keys()]
        top5_of_top3_manufacturers_dict = dict()
        for i in top3_manufacturers.keys():
            top5_of_top3_manufacturers_dict[i] = handsets_by_top3_manufacturers.loc[
                i, "Handset Type"].value_counts().head(5)

        top5_of_top3_manufacturers = pd.DataFrame.from_dict(top5_of_top3_manufacturers_dict, orient="index").stack()
        top5_of_top3_manufacturers.name = "count"
        top5_of_top3_manufacturers = top5_of_top3_manufacturers.to_frame()

        print("\n>> top 5 handsets produced by the top 3 handset manufacturers patronized by customers")
        print(tabulate(top5_of_top3_manufacturers, tablefmt="grid"))

    def get_aggregate_data(self):
        self.data["MSISDN/Number"] = self.data["MSISDN/Number"].fillna(-999).astype("int")

        no_of_xdr_sessions = self.data["MSISDN/Number"].fillna("median").value_counts()

        total_sessions_duration = (self.data[["MSISDN/Number", "Dur. (ms)"]]
                                   .fillna("median").groupby(["MSISDN/Number"])["Dur. (ms)"]
                                   .sum()
                                   ) / (60 * 60)

        total_dl_ul_data = (self.data[["MSISDN/Number", "Total DL (Bytes)", "Total UL (Bytes)"]]
                            .fillna("median").groupby(["MSISDN/Number"])[["Total DL (Bytes)", "Total UL (Bytes)"]]
                            .sum()
                            ) / (2 ** 20)

        total_dl_ul_data["total_data"] = total_dl_ul_data.sum(1)

        apps = ['Social Media DL (Bytes)', 'Social Media UL (Bytes)',
                'Google DL (Bytes)', 'Google UL (Bytes)', 'Email DL (Bytes)',
                'Email UL (Bytes)', 'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
                'Netflix DL (Bytes)', 'Netflix UL (Bytes)', 'Gaming DL (Bytes)',
                'Gaming UL (Bytes)', 'Other DL (Bytes)', 'Other UL (Bytes)', ]
        total_dl_ul_data_per_app = (self.data[apps + ["MSISDN/Number"]].fillna("mean")
                                    .groupby(["MSISDN/Number"])[apps].sum()
                                    ) / (2 ** 20)

        total_data_per_app = pd.DataFrame()
        count = 0
        for i, j in zip(range(len(total_dl_ul_data_per_app.columns)), total_dl_ul_data_per_app.columns):
            if count != 1:
                total_data_per_app[j.split()[0]] = total_dl_ul_data_per_app.iloc[:, i] + total_dl_ul_data_per_app.iloc[
                                                                                         :, i + 1]
                count = (count + 1) % 2
            else:
                count = (count + 1) % 2
                continue

        aggregates = (no_of_xdr_sessions.to_frame()
                      .join(total_sessions_duration)
                      .join(total_data_per_app)
                      .join(total_dl_ul_data)
                      )

        aggregates.index.name = "MSISDN"
        aggregates.columns = ["tot number of session", "tot sessions duration (hrs)", "social media data usage (MBs)",
                              "google data usage (MBs)", "Email data usage (MBs)", "youtube data usage (MBs)",
                              "netflix data usage (MBs)", "gaming apps data usage (MBs)", "other apps data usage (MBs)",
                              "tot downloaded data (MBs)", "tot uploaded data (MBs)", "tot data usage (MBs)", ]
        aggregates = aggregates.drop(index=-999)

        outliers_index = \
            aggregates["tot sessions duration (hrs)"][aggregates["tot sessions duration (hrs)"] > (30 * 12)].keys()
        aggregates.loc[outliers_index] = np.nan
        aggregates.dropna(inplace=True)

        print(">> data usage by customers \n...top 10")
        print(tabulate(aggregates.head(10), tablefmt="grid"))
        print("\n...stats")
        print(tabulate(aggregates.describe().T, tablefmt="grid"))

    def analyse_aggregates(self):
        pass
