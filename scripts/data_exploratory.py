import numpy as np
import pandas as pd 
import os, sys
from datetime import datetime

class Data_Preprocessing:

    def __init__(self, df : pd.DataFrame) -> None: 
        self.df = df

################################################################################################################
# Data Information Script
################################################################################################################

    def show_datatypes(self) -> pd.DataFrame:
        return self.df.dtypes

    def show_stats_info(self) -> pd.DataFrame:
        return self.df.agg(['mean'])
    
    def show_correlation(self) -> pd.DataFrame:
        return self.df.corr()
    
    def show_data_desc(self) -> pd.DataFrame:
        return self.df.describe()
    
    def preprocess_view_na(self) -> pd.DataFrame:
        return self.df.isna().sum()

################################################################################################################
# Data Cleaning Script
################################################################################################################

    def convert_to_datetime(self) -> pd.DataFrame:
        self.df['Start'] = pd.to_datetime(self.df['Start'], errors = 'coerce')
        self.df['Start'] = self.df['Start'].apply(lambda x: x.strftime('%Y-%m-%d'))
        self.df['End'] = pd.to_datetime(self.df['End'], errors = 'coerce')
        self.df['End'] = self.df['End'].apply(lambda x: x.strftime('%Y-%m-%d'))
        return self.df
    
    def drop_duplicates(self) -> pd.DataFrame:
        old = self.df.shape[0]
        dropped = self.df[self.df.duplicated()].index
        self.df.drop(index = dropped, inplace = True)
        new = self.df.shape[0]
        count =  new - old
        if count == 0:
            print('There are no duplicates')
        else: 
            print(f'There are {count} numbers of duplicates')

    def convert_to_numbers(self) -> pd.DataFrame:
        self.df = self.df.apply(lambda x : pd.to_numeric(x, errors = 'coerce'))
        return self.df
    
    def convertByteMB(self, col1) -> pd.DataFrame:
        megabyte = 1*10e+4
        self.df[col1] = round((self.df[col1] / megabyte), 2)
        return self.df

    def renameCols(self, col1) -> pd.DataFrame:
        self.df.rename(columns = {col1 : f'{col1[:-7]}(MB)'}, inplace = True)
        return self.df

################################################################################################################
# Missing Data Manuipulation Script
################################################################################################################

    def percentage_missing_values(self) -> pd.DataFrame:
        missing_count = self.df.isna().sum()
        total_cell = np.product(self.df.shape)
        total_missing = missing_count.sum()
        print(f'The dataset contains {round(((total_missing / total_cell) * 100 ), 2)}% of missing values')

    def percentage_missing_rows(self) -> pd.DataFrame:
        missing_rows = sum([True for idx, rows in self.df.iterrows() if any(rows.isna())])
        total_rows = self.df.shape[0]
        print(f'The dataset has {round(((missing_rows / total_rows) * 100 ), 2)}% of missing values')

    def missing_values_table(self) ->pd.DataFrame:
        mis_val = self.df.isnull().sum()  # Total missing values
        mis_val_percent = 100 * mis_val / len(self.df) # Percentage of missing values
        mis_val_dtype = self.df.dtypes # dtype of missing values
        mis_val_table = pd.concat([mis_val, mis_val_percent, mis_val_dtype], axis=1) # Make a table with the results
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values', 2: 'Dtype'}) # Rename the columns
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,0] != 0].sort_values(
        '% of Total Values', ascending=False).round(2) # Sort the table by percentage of missing descending and remove columns with no missing values

        print ("Your selected dataframe has " + str(self.df.shape[1]) + " columns.\n"
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
            " columns that have missing values.")

        if mis_val_table_ren_columns.shape[0] == 0:
            return

        return mis_val_table_ren_columns # Return the dataframe with missing information
        
    def fix_missing_ffill(self, col):
        count = self.df[col].isna().sum()
        self.df[col] = self.df[col].fillna(method='ffill')
        print(f"{count} missing values in the column {col} have been replaced using the forward fill method.")
        return self.df[col]


    def fix_missing_bfill(self, col):
        count = self.df[col].isna().sum()
        self.df[col] = self.df[col].fillna(method='bfill')
        print(f"{count} missing values in the column {col} have been replaced using the backward fill method.")
        return self.df[col]

    def fix_missing_median(self, col):
        median = self.df[col].median()
        count = self.df[col].isna().sum()
        self.df[col] = self.df[col].fillna(median)
        print(f"{count} missing values in the column {col} have been replaced by its median value {median}.")
        return self.df[col]

    def drop_cols(self) ->pd.DataFrame:
        old = self.df.shape[0]
        self.df.dropna(inplace = True)
        new = self.df.shape[0]
        tot = old - new
        print(f'{tot} rows containing missing values were dropped from our dataframe.')
        return self.df


        