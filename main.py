import json

from pandas import DataFrame

from base import DataFileInterface, NewItem


class CSVDataFile(DataFileInterface):
    def __init__(self, csv_file_name: str, json_output_name: str) -> None:
        self.csv_file_name: str = csv_file_name
        self.json_output_name: str = json_output_name

    def transform_data_to_json(self):
        results: list = []
        with open(self.json_output_name, "r") as data_open:
            for line in data_open:
                data = json.loads(line)
                data["date"], data["time"] = data.get("timestamp").split(" ")
                results.append(data)
        return results

    def filter_fields(self, df) -> DataFrame:
        filtered_data: DataFrame = df[
            (df["timestamp"].str.startswith("2018-04"))
            & (
                (df["sensor_07"] > 20) & (df["sensor_07"] < 30)
                | (df["sensor_47"] > 20) & (df["sensor_47"] < 30)
            )
        ]
        return filtered_data


class NewItemCSV:
    def create_dataframe(self, entries):
        item = NewItem(entries)
        return item.parser_to_dataframe()
