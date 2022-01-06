import sys
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    
    '''Reads in and merges the messages and categories files
    
    INPUT:
    messages_filepath - string with file path for disasters_messages.csv
    categories_filepath - string with file path for disasters_categories.csv
        
    OUTPUT:
    df - a new dataframe that merges the messages and categories files          
    '''
    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, how='inner', on='id')
    return df
    
     
def clean_data(df):
    
    '''cleans the merged messages and categories data set
    
    INPUT:
          Single dataframe (df)   
    OUTPUT:
        df - a new dataframe after the following transformations:
            1. splitting the single categories column into 36 separate columns for each of the categories
            2. adding a column description to the newly created columns
            3. converting the category columns to integer values
            4. dropping duplicate rows
    '''
    
    # clean data
    categories = df['categories'].str.split(";", expand=True)
    row = categories.iloc[0]
    category_colnames = row.apply(lambda label: re.match(".+?(?=\-)", label).group())
    categories.columns = category_colnames
    
    for column in categories:
        categories[column] = categories[column].str[-1].astype(int) 
         
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    df = df.drop_duplicates()
    return df


def save_data(df, database_filename):
    
    '''loads cleaned data to an sqlite database   
    
    INPUT:
            dataframe with cleaned data (df)
            string with file path for database to store data in
    OUTPUT:
            None
    '''
    
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('Messages', engine, index=False, if_exists='replace')


def main():
    
    '''controls the ETL process flow by calling several functions in sequence    
    INPUT:
         System parameters incorporated via the function call when the package is run           
    OUTPUT:
         None    
    '''
        
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()