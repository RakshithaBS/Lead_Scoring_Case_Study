##############################################################################
# Import the necessary modules
##############################################################################
import sqlite3
from constants import *
import pandas as pd

###############################################################################
# Write test cases for load_data_into_db() function
# ##############################################################################

def test_load_data_into_db():
    """_summary_
    This function checks if the load_data_into_db function is working properly by
    comparing its output with test cases provided in the db in a table named
    'loaded_data_test_case'
s

    SAMPLE USAGE
        output=test_get_data()

    """
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    loaded_data = pd.read_sql("select * from "+ORIGINAL_DATA,conn)
    
    conx = sqlite3.connect(TEST_DB_FILE_NAME)
    test_data = pd.read_sql("select * from loaded_data_test_case",conx)
    
    #print(loaded_data.head())
    #print(test_data.head())
    conn.close()
    conx.close()
    
    assert test_data.equals(loaded_data)

###############################################################################
# Write test cases for map_city_tier() function
# ##############################################################################
def test_map_city_tier():
    """_summary_
    This function checks if map_city_tier function is working properly by
    comparing its output with test cases provided in the db in a table named
    'city_tier_mapped_test_case'


    SAMPLE USAGE
        output=test_map_city_tier()

    """
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    city_mapped_data = pd.read_sql("select * from city_tier_mapped",conn)
    
    conx = sqlite3.connect(TEST_DB_FILE_NAME)
    test_data = pd.read_sql("select * from city_tier_mapped_test_case",conx)
    conn.close()
    conx.close()
    
    assert test_data.equals(city_mapped_data)

###############################################################################
# Write test cases for map_categorical_vars() function
# ##############################################################################    
def test_map_categorical_vars():
    """_summary_
    This function checks if map_cat_vars function is working properly by
    comparing its output with test cases provided in the db in a table named
    'categorical_variables_mapped_test_case'


    SAMPLE USAGE
        output=test_map_cat_vars()

    """    
    
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    categorical_mapped_data = pd.read_sql("select * from "+CATAEGORICAL_VALUES_MAPPED,conn)
    
    conx = sqlite3.connect(TEST_DB_FILE_NAME)
    test_data = pd.read_sql("select * from categorical_variables_mapped_test_case",conx)
    
    conn.close()
    conx.close()

    assert test_data.equals(categorical_mapped_data)

###############################################################################
# Write test cases for interactions_mapping() function
# ##############################################################################    
def test_interactions_mapping():
    """_summary_
    This function checks if test_column_mapping function is working properly by
    comparing its output with test cases provided in the db in a table named
    'interactions_mapped_test_case'


    SAMPLE USAGE
        output=test_column_mapping()

    """ 
    conn = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    interactions_mapped_data = pd.read_sql("select * from "+INTERACTIONS_MAPPED,conn)
    
    conx = sqlite3.connect(TEST_DB_FILE_NAME)
    test_data = pd.read_sql("select * from interactions_mapped_test_case",conx)
    
    conn.close()
    conx.close()
    
    assert test_data.equals(interactions_mapped_data)
    
if __name__ == "__main__":
    test_load_data_into_db()
    test_map_city_tier()
    test_map_categorical_vars()
    test_interactions_mapping()
    print("Everything passed")
