##############################################################################
# Import necessary modules and files
##############################################################################


import pandas as pd
import os
import sqlite3
from sqlite3 import Error
#from constants import *
#from city_tier_mapping import *
#from significant_categorical_level import *






###############################################################################
# Define the function to build database
###############################################################################

def build_dbs(db_file_name,db_path):
    '''
    This function checks if the db file with specified name is present 
    in the /Assignment/01_data_pipeline/scripts folder. If it is not present it creates 
    the db file with the given name at the given path. 


    INPUTS
        db_file_name : Name of the database file 'utils_output.db'
        db_path : path where the db file should be '   


    OUTPUT
    The function returns the following under the conditions:
        1. If the file exsists at the specified path
                prints 'DB Already Exsists' and returns 'DB Exsists'

        2. If the db file is not present at the specified loction
                prints 'Creating Database' and creates the sqlite db 
                file at the specified path with the specified name and 
                once the db file is created prints 'New DB Created' and 
                returns 'DB created'


    SAMPLE USAGE
        build_dbs()
    '''
    if os.path.isfile(db_path+db_file_name):
        print("DB Already exists")
    else:
        print("Creating Database")
        conn = None
        try:
            conn = sqlite3.connect(db_path+db_file_name)
            print("New DB Created")
        except Error as e:
            print(e)
            return "Error"
        finally:
            if conn:
                conn.close()
                return "DB created"
            
    
def check_if_table_has_value(cnx,table_name):
    check_table = pd.read_sql(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';", cnx).shape[0]
    if check_table == 1:
        return True
    else:
        return False
###############################################################################
# Define function to load the csv file to the database
###############################################################################

def load_data_into_db(db_file_name,db_path,data_dictionary):
    '''
    Thie function loads the data present in datadirectiry into the db
    which was created previously.
    It also replaces any null values present in 'toal_leads_dropped' and
    'referred_lead' with 0.


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        data_directory : path of the directory where 'leadscoring.csv' 
                        file is present
        

    OUTPUT
        Saves the processed dataframe in the db in a table named 'loaded_data'.
        If the table with the same name already exsists then the function 
        replaces it.


    SAMPLE USAGE
        load_data_into_db()
    '''
    conn = sqlite3.connect(db_path+db_file_name)
    data = pd.read_csv(data_dictionary, index_col=[0])
    data['total_leads_droppped'] = data['total_leads_droppped'].fillna(0)
    data['referred_lead']= data['referred_lead'].fillna(0)
    if not check_if_table_has_value(conn,'loaded_data'):
        data.to_sql(name="loaded_data",con=conn,if_exists='replace',index=False)
    conn.close()
    

###############################################################################
# Define function to map cities to their respective tiers
###############################################################################

    
def map_city_tier(db_file_name,db_path,city_tier_mapping):
    '''
    This function maps all the cities to their respective tier as per the
    mappings provided in /mappings/city_tier_mapping.py file. If a
    particular city's tier isn't mapped in the city_tier_mapping.py then
    the function maps that particular city to 3.0 which represents
    tier-3.


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        city_tier_mapping : a dictionary that maps the cities to their tier

    
    OUTPUT
        Saves the processed dataframe in the db in a table named
        'city_tier_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_city_tier()

    '''
###############################################################################
# Define function to map insignificant categorial variables to "others"
###############################################################################
    conn = sqlite3.connect(db_path+db_file_name)
    if not check_if_table_has_value(conn,'city_tier_mapped'):
        df = pd.read_sql("select * from loaded_data" ,conn)
        df["city_tier"] = df["city_mapped"].map(city_tier_mapping)
        df['city_tier']=df['city_tier'].fillna(3.0)
        df=df.drop('city_mapped',axis=1)
        df.to_sql(name="city_tier_mapped",con=conn,if_exists='replace',index=False)
    conn.close()

def map_categorical_vars(db_file_name,db_path,list_platform,list_medium,list_source):
    '''
    This function maps all the unsugnificant variables present in 'first_platform_c'
    'first_utm_medium_c' and 'first_utm_source_c'. The list of significant variables
    should be stored in a python file in the 'significant_categorical_level.py' 
    so that it can be imported as a variable in utils file.
    

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        list_platform : list of all the significant platform.
        list_medium : list of all the significat medium
        list_source : list of all rhe significant source

        **NOTE : list_platform, list_medium & list_source are all constants and
                 must be stored in 'significant_categorical_level.py'
                 file. The significant levels are calculated by taking top 90
                 percentils of all the levels. For more information refer
                 'data_cleaning.ipynb' notebook.
  

    OUTPUT
        Saves the processed dataframe in the db in a table named
        'categorical_variables_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_categorical_vars()
    '''
    conn = sqlite3.connect(db_path+db_file_name)
    if conn:
        if not check_if_table_has_value(conn,"categorical_variables_mapped"):
            df = pd.read_sql("select * from city_tier_mapped",conn)
            new_df=df[~df['first_platform_c'].isin(list_platform)]
            new_df['first_platform_c']="others"
            old_df = df[df['first_platform_c'].isin(list_platform)]
            df = pd.concat([new_df,old_df])

            new_df=df[~df['first_utm_medium_c'].isin(list_medium)]
            new_df['first_utm_medium_c']="others"
            old_df = df[df['first_utm_medium_c'].isin(list_medium)]
            df = pd.concat([new_df,old_df])

            new_df=df[~df['first_utm_source_c'].isin(list_source)]
            new_df['first_utm_source_c']="others"
            old_df = df[df['first_utm_source_c'].isin(list_source)]
            df = pd.concat([new_df,old_df])
            
            df = df.drop_duplicates()
            df.to_sql("categorical_variables_mapped",con=conn,if_exists='replace',index=False)
    conn.close()
##############################################################################
# Define function that maps interaction columns into 4 types of interactions
##############################################################################
def interactions_mapping(db_file_name,db_path,interaction_mapping_file,index_columns,not_features):
    '''
    This function maps the interaction columns into 4 unique interaction columns
    These mappings are present in 'interaction_mapping.csv' file. 


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        interaction_mapping_file : path to the csv file containing interaction's
                                   mappings
        index_columns : list of columns to be used as index while pivoting and
                        unpivoting
        NOTE : Since while inference we will not have 'app_complete_flag' which is
        our label, we will have to exculde it from our index_columns. It is recommended 
        that you use an if loop and check if 'app_complete_flag' is present in 
        'categorical_variables_mapped' table and if it is present pass a list with 
        'app_complete_flag' in it as index_column else pass a list without 'app_complete_flag'
        in it.

    
    OUTPUT
        Saves the processed dataframe in the db in a table named 
        'interactions_mapped'. If the table with the same name already exsists then 
        the function replaces it.
        
        It also drops all the features that are not requried for training model and 
        writes it in a table named 'model_input'

    
    SAMPLE USAGE
        interactions_mapping()
    '''
    conn = sqlite3.connect(db_path+db_file_name)
    if conn:   
        if not check_if_table_has_value(conn,'interactions_mapped'):
            df = pd.read_sql("select * from categorical_variables_mapped",conn)
            df = df.drop_duplicates()
            df_event_mapping = pd.read_csv(interaction_mapping_file,index_col=[0])
            # check if app_complete_flag is in df.columns
            df_unpivot=pd.melt(df,id_vars=index_columns,var_name='interaction_type',value_name='interaction_value')
            df_unpivot['interaction_value'] = df_unpivot['interaction_value'].fillna(0)
            df=pd.merge(df_unpivot,df_event_mapping,how='left',on='interaction_type')
            df = df.drop('interaction_type',axis=1)
            df_pivot = df.pivot_table(values='interaction_value', index=index_columns, columns='interaction_mapping', aggfunc='sum')
            df_pivot = df_pivot.reset_index()
            df_pivot.to_sql('interactions_mapped',con=conn,if_exists='replace',index=False)     
            #df_model_input = df_pivot.drop(not_features,axis=1)
            #print("saving into model_input")
            #df_model_input.to_sql('model_input',con=conn,if_exists='replace',index=False)
            
            
    conn.close()                              
            
            
def drop_features(db_file_name,db_path,drop_feature_list):
    conn = sqlite3.connect(db_path+db_file_name)
    interaction_mapping = pd.read_sql("select * from interactions_mapped",conn)
    interaction_mapping= interaction_mapping.drop(drop_feature_list,axis=1)
    interaction_mapping.to_sql('model_input',con=conn,if_exists='replace',index=False)
    conn.close()
    