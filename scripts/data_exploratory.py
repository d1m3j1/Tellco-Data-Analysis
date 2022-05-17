import numpy as np
import pandas as pd 
import os, sys

sys.path.append(os.path.abspath(os.path.join('../')))

data = pd.read_csv('data/Tellco-Data-Source.csv')

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

    def convert_to_datetime(self, cols) -> pd.DataFrame:
        self.df = pd.to_datetime(self.df[cols])
        return self.df
    
    def drop_duplicates(self) -> pd.DataFrame:
        old = df.shape[0]
        dropped = self.df[self.df.duplicated()].index
        self.df.drop(index = dropped, inplace = True)
        new = df.shape[0]
        count =  new - old
        if count == 0:
            print('There are no duplicates')
        else: 
            print(f'There are {count} numbers of duplicates')
        return self.df

    def convert_to_numbers(self) -> pd.DataFrame:
        self.df = self.df.apply(lambda x : pd.to_numeric(x, errors = 'coerce'))
        return self.df
    
    def convertByteMB(self, col1) -> pd.DataFrame:
        megabyte = 1*10e+5
        try:
            for col in col1: 
                self.df[col] = self.df[col] / megabyte
                self.df.rename(columns = {col : f'{col[:-7]}(Megabyte)'}, inplace = True)
            print('Byte conversion completed')
        except Exception as err: 
            print(f'Error encountered "{err}"')

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

    def drop_col_with_nul_values(self, threshold = 30) -> pd.DataFrame:
        null_present_df = pd.DataFrame(columns =['column', 'null_precent'])
        columns  = self.df.columns.values.tolist()

        null_precent_df['column'] = columns
        null_percent_df['null_percent'] = null_percent['column'].map(
                                        lambda x: percentage_missing_values(self, x))

        columns_subset = null_percent_df[null_percent_df['null_percent']
                                         < threshold_in_percent]['column'].to_list()

        self.df = self.df.dropna(subset=columns_subset)
        return self.df         
    def missing_values_table(df) ->pd.DataFrame:
        mis_val = df.isnull().sum()  # Total missing values
        mis_val_percent = 100 * mis_val / len(df) # Percentage of missing values
        mis_val_dtype = df.dtypes # dtype of missing values
        mis_val_table = pd.concat([mis_val, mis_val_percent, mis_val_dtype], axis=1) # Make a table with the results
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values', 2: 'Dtype'}) # Rename the columns
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,0] != 0].sort_values(
        '% of Total Values', ascending=False).round(2) # Sort the table by percentage of missing descending and remove columns with no missing values

        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
            " columns that have missing values.")

        if mis_val_table_ren_columns.shape[0] == 0:
            return

        return mis_val_table_ren_columns # Return the dataframe with missing information
        
    def handling_missing_quantitative_data_with_mean(self, df : pd.DataFrame, method = 'mean'):
        numeric_data =  ['int16', 'int32', 'int64',
                        'float16', 'float32', 'float64']
        
        all_cols = df.columns.to_list()
        num_cols = [i for i in all_cols if self.df[i].dtypes in numeric_data] 

        if (method == 'mean'): 
            for col in num_cols:
                self.df[col] = self.df[col].fillna(self.df[col].mean())
        elif (method =='ffil'):
            for col in num_cols:
                self.df[col] = self.df[col].fillna(method = 'ffill')
        elif (method =='bfil'):
            for col in num_cols:
                self.df[col] = self.df[col].fillna(method = 'bfill')
        else :
            print('Unknown Method')
            return self.df

    def handle_missing_categorical_data_with(self, df: pd.DataFrame, method="ffill"):
        numeric_data = ['int16', 'int32', 'int64',
                        'float16', 'float32', 'float64']
        
        all_cols = self.df.columns.to_list()
        num_cols = [i for i in all_cols if not self.df[i].dtypes in numeric_data]     
        
        if method == "ffill":
            for col in num_cols:
                self.df[col] = self.df[col].fillna(method='ffill')
            return self.df
        elif method == "bfill":
            for col in num_cols:
                self.df[col] = self.df[col].fillna(method='bfill')
            return self.df
        else:
            print("Method unknown")
            return self.df
