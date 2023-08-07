from abc import ABC, abstractmethod

import pandas
from pandas import DataFrame


class DataFileInterface(ABC):
    def load_data_from_csv(self, csv_file: str) -> DataFrame:
        """
        Load data from a CSV file and return it as a pandas DataFrame.

        Parameters:
            csv_file (str): The path to the CSV file.

        Returns:
            DataFrame: A pandas DataFrame containing the data from the CSV file.
        """
        print("[+] Reading csv file...")
        return pandas.read_csv(csv_file)

    def save_json(self, json_name_file: str, df: DataFrame) -> None:
        """
        Save a pandas DataFrame to a JSON file.

        Parameters:
            json_name_file (str): The path and name of the JSON file to be saved.
            df (DataFrame): The pandas DataFrame to be saved as JSON.
        """
        df.to_json(json_name_file, orient="records", lines=True)
        print("[+] Json file successfully saved!")

    def filter_fields(self, data: DataFrame) -> DataFrame:
        """
        Filter the data in the pandas DataFrame.

        This function can be overridden in subclasses to apply specific filtering logic.

        Parameters:
            data (DataFrame): The pandas DataFrame containing the data.

        Returns:
            DataFrame: The filtered pandas DataFrame.
        """
        # This function is used to filter the data in the json file
        return data

    @abstractmethod
    def transform_data_to_json(self):
        """
        Abstract method to transform the data to JSON.

        This method must be implemented in concrete subclasses.
        """
        pass

    def get_data_json(self, csv_file: str, json_name_output: str):
        """
        Load data from a CSV file, filter it, transform it to JSON, and save it to a file.

        Parameters:
            csv_file (str): The path to the CSV file.
            json_name_output (str): The path and name of the JSON file to be saved.

        Returns:
            The result of calling the transform_data_to_json() method.
        """
        data = self.load_data_from_csv(csv_file)
        filtered_data = self.filter_fields(data)
        self.save_json(json_name_output, filtered_data)
        return self.transform_data_to_json()


class NewItem:
    def __init__(self, entries: list) -> None:
        self.entries: list = entries

    def parser_to_dataframe(self) -> DataFrame:
        """
        Create a pandas DataFrame from a list of entries.

        Returns:
            DataFrame: The pandas DataFrame created from the list of entries.
        """
        return DataFrame.from_records(self.entries)
