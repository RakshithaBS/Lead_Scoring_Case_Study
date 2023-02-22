"""
Import necessary modules
############################################################################## 
"""

import pandas as pd
import sqlite3

###############################################################################
# Define function to validate raw data's schema
############################################################################### 

def raw_data_schema_check(db_file_name,db_path,raw_data_schema):
    '''
    This function check if all the columns mentioned in schema.py are present in
    leadscoring.csv file or not.

   
    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be   
        raw_data_schema : schema of raw data in the form oa list/tuple as present 
                          in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Raw datas schema is in line with the schema present in schema.py' 
        else prints
        'Raw datas schema is NOT in line with the schema present in schema.py'

    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    
    conn = sqlite3.connect(db_path+db_file_name)
    if conn:
        df = pd.read_sql("select * from loaded_data",conn)
        if(set(df.columns)==set(raw_data_schema)):
            print("Raw datas schema is in line with the schema present in schema.py")
        else:
            print("Raw datas schema is NOT in line with the schema present in schema.py")

###############################################################################
# Define function to validate model's input schema
############################################################################### 

     
def model_input_schema_check(db_file_name,db_path,model_input_schema):
    '''
    This function check if all the columns mentioned in model_input_schema in 
    schema.py are present in table named in 'model_input' in db file.

   
    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be   
        raw_data_schema : schema of models input data in the form oa list/tuple
                          present as in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Models input schema is in line with the schema present in schema.py'
        else prints
        'Models input schema is NOT in line with the schema present in schema.py'
    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    
    conn = sqlite3.connect(db_path+db_file_name)
    if conn:
        df = pd.read_sql("select * from model_input",conn)
        if(set(df.columns)==set(model_input_schema)):
            print("Models input schema is in line with the schema present in schema.p")
        else:
            print("Models input schema is NOT in line with the schema present in schema.py")
    
    
