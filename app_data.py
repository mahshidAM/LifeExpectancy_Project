""" Dashboard data prepration"""
import pandas as pd
import numpy as np


def get_DataFrame():
    """
    Returns cleaned dataframe     
    """
    df = pd.read_csv('data/API_SP.csv', sep=',', encoding='utf8', engine='python')
    df.drop('Country Code',axis=1,inplace=True)
    df.drop('Indicator Name',axis=1,inplace=True)
    df.drop('Indicator Code',axis=1,inplace=True)
    
    cleaned_df = df.melt(id_vars=["Country Name"], var_name="year")
    cleaned_df.rename({'Country Name':'country'},axis=1,inplace=True)
    cleaned_df.dropna(inplace=True)
    cleaned_df.value = cleaned_df.value.astype(int)
    cleaned_df.year = cleaned_df.year.astype(int)
    
    return cleaned_df