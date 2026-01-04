from pandas import DataFrame
import numpy as np
from pandas.io.formats import printing

def get_num_dups(df:DataFrame):
    """
    Returns the number of duplicated rows in the DataFrame

    args:
        df: Pandas DataFrame

    return:
        Number of duplicated rows
    """
    return df.duplicated().sum()

def get_cols_with_none(df:DataFrame):
    """
    Return columns with at least one None value

    args:
        df: Pandas DataFrame

    return:
        Columns with at least one None value
    """
    return df.isnull().any()

def get_cols(df: DataFrame):
    """
    Return the column names in the DataFrame
    """
    return list(df.columns)


def get_info(df:DataFrame):
    return df.info()

def get_numeric_cols(df:DataFrame):
    """
    Returns the list of numeric cols in the dataframe filtering the IDs
    
    args:
        df: Pandas Dataframe 
    """
    
    #get numeric cols from the DataFrame
    numeric_cols = list(df.select_dtypes(include='number'))

    #filter the columns that contains _id or seq
    filtered_id = list(filter(lambda el: "_id" not in el, numeric_cols))
    filtered = list(filter(lambda el: "seq" not in el, filtered_id))
    
    return filtered

def get_basic_stats(df: DataFrame):
    """
    Return the basic stats for only the numeric values without the IDs
    args:
        df: Pandas DataFrame
    """
    #take the numeric cols
    numeric_cols = get_numeric_cols(df)

    #if no numeric cols return 
    if len(numeric_cols) == 0:
        return 
    
    #create the filtered dataframe
    filtered_df = df[numeric_cols]

    return filtered_df.describe()


def get_correlation(df:DataFrame, method:str = "kendall"): 
    """
    args:
        df: DataFrame containing numeric or ordinal variables to be correlated.
        method: correlation method to use ('kendall', 'pearson', or 'spearman').
            - kendall (default): measures the degree of agreement between the orderings (rankings) of two variables.
            - spearman: measures the strength and direction of a monotonic relationship (based on rank correlation).
            - pearson: measures the strength and direction of a linear relationship between continuous variables.
    return:
        Correlation between columns in the DataFrame
    """

    #get the numeric cols 
    numeric_cols = get_numeric_cols(df)

    #if no cols or just one return
    if len(numeric_cols) == 0 or len(numeric_cols) == 1:
        return 
    
    #create the filtered DataFrame
    filtered_df = df[numeric_cols]

    return filtered_df.corr(method=method) #pyright:ignore

#ghetti i types
def get_types(df:DataFrame):
    return df.dtypes


def get_ICD_groups(df:DataFrame):
    """
    Returns a new dataframe containing, for each ICD code, 
    the number of Female, Male, and the Total (F + M) with that ICD code

    args:
        df: Pandas DataFrame
    return:
        grouped: Pandas dataframe having for each ICD code, 
        the number of Female, Male, and the Total (F + M) with that ICD code
    """

    # create the new dataframe
    # grouped by the ICD code and the gender
    # calculate the number of uniques genders with that ICD code
    grouped = df.groupby(['icd_code', 'gender'])['subject_id'].nunique().unstack()

    # calculate the sum of the number of patient having that ICD code
    grouped["total"] = grouped.sum(axis=1) 
    
    return grouped

def get_nums_of_abnormal(df:DataFrame):

    """
    Returns, for each hadm_id, the number of abnormal values encountered during the tests 

    args:
        df: Pandas DataFrame

    return:
        df_abnormal: Pandas dataframe with, for each hadm_id, the number of abnormal values encountered during the tests
    """
    # calculate the number of abnormal test values for each hadm_id
    df_abnormal = df.groupby("hadm_id")[['valuenum', 'ref_range_lower', 'ref_range_upper']].apply(
    lambda args: ((args['valuenum'] < args['ref_range_lower']) | 
                   (args['valuenum'] > args['ref_range_upper'])).sum()
    )

    return df_abnormal
