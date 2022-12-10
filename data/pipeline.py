import pandas as pd 
import numpy as np 
import warnings

warnings.filterwarnings('ignore')

FILE_PATH = 'D:\Coding\Python\game-recommendation-system\games.csv'

def drop_columns(df, cols):
    df.drop(cols, axis=1, inplace=True)
    return df

def drop_duplicates_on_name(df, col):
    df.drop_duplicates(subset=col, inplace=True)
    return df

def fix_sales_format(df, col1, col2):
    df.loc[:,col1] = df.loc[:,col1].apply(lambda val: str(val).replace('m',''))
    df.loc[:,col2] = df.loc[:,col2].apply(lambda val: str(val).replace('m',''))
    return df

def fix_na_format(df, cols):

    for col in cols:
        df.loc[:,col] = df.loc[:,col].apply(lambda val: np.NaN if val.strip() =='N/A' or val.strip() =='nan' else val)
    return df

def strip_objects(df, cols):

    for col in cols:
        df.loc[:,col] = df.loc[:,col].apply(lambda val: val.strip())
    return df

def convert_to_float(df, cols):

    for col in cols:
        df.loc[:,col] = df.loc[:,col].astype(np.float32)
    return df

def convert_to_datetime(df, col):
    
    df.loc[:,col] = df.loc[:,col].apply(pd.to_datetime)
    return df

def remove_datena_records(df, col):
    
    df.dropna(subset=col, inplace=True)
    return df

def fill_na_records_with_mean(df, cols):

    for col in cols:
        df.loc[:,col].fillna(np.mean(df[col]), inplace=True)
    return df

def fix_name(df, col):

    df.loc[:,col] = df.loc[:,col].apply(lambda val: val.replace('    Read the review',''))
    return df

def shuffle_dataframe(df):

    df = df.sample(frac=1)
    df = df.reset_index(drop=True)
    return df


dataframe = pd.read_csv(FILE_PATH)

preprocessed = dataframe.pipe(drop_columns, ['id', 'last_updated']).pipe(
                              drop_duplicates_on_name, 'name').pipe(
                              fix_sales_format, col1='total_shipped', col2='total_sales').pipe(
                              fix_na_format, ['vgchartz_score',
                                              'critic_score',
                                              'user_score',
                                              'total_shipped',
                                              'total_sales',
                                              'release_date']).pipe(
                              strip_objects, ['name','publisher','genre']).pipe(
                              convert_to_float, ['vgchartz_score',
                                                 'critic_score',
                                                 'user_score',
                                                 'total_shipped',
                                                 'total_sales']).pipe(
                              convert_to_datetime, col='release_date').pipe(
                              remove_datena_records, col='release_date').pipe(
                              fill_na_records_with_mean, ['vgchartz_score',
                                                          'critic_score',
                                                          'user_score',
                                                          'total_shipped',
                                                          'total_sales']).pipe(
                              fix_name, col='name').pipe(shuffle_dataframe)

print(preprocessed.head())
preprocessed.to_csv('finaldata.csv', index=False)