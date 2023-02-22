##############################################################################
# Import necessary modules
# #############################################################################


from airflow import DAG
from airflow.operators.python import PythonOperator
import importlib.util
from datetime import datetime, timedelta

###############################################################################
# Define default arguments and DAG
###############################################################################

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

utils = module_from_file("utils", "/home/airflow/dags/Assignment/01_data_pipeline/scripts/utils.py")
constants = module_from_file("constants", "/home/airflow/dags/Assignment/01_data_pipeline/scripts/constants.py")
schema = module_from_file("schema", "/home/airflow/dags/Assignment/01_data_pipeline/scripts/schema.py")
significant_categorical_level=module_from_file("significant_categorical_level", "/home/airflow/dags/Assignment/01_data_pipeline/scripts/significant_categorical_level.py")
data_validation_checks=module_from_file("data_validation_checks","/home/airflow/dags/Assignment/01_data_pipeline/scripts/data_validation_checks.py")
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022,7,30),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


ML_data_cleaning_dag = DAG(
                dag_id = 'Lead_Scoring_Data_Engineering_Pipeline',
                default_args = default_args,
                description = 'DAG to run data pipeline for lead scoring',
                schedule_interval = '@daily',
                catchup = False
)

###############################################################################
# Create a task for build_dbs() function with task_id 'building_db'
###############################################################################

building_db = PythonOperator(task_id='building_db',python_callable=utils.build_dbs,dag=ML_data_cleaning_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH})
###############################################################################
# Create a task for raw_data_schema_check() function with task_id 'checking_raw_data_schema'
###############################################################################

checking_raw_data_schema= PythonOperator(task_id='checking_raw_data',python_callable=data_validation_checks.raw_data_schema_check,dag = ML_data_cleaning_dag,op_kwargs=
                                         {'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'raw_data_schema':schema.raw_data_schema})
###############################################################################
# Create a task for load_data_into_db() function with task_id 'loading_data'
##############################################################################
loading_data = PythonOperator(task_id='loading_data',python_callable=utils.load_data_into_db,dag = ML_data_cleaning_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'data_dictionary':DATA_DIRECTORY})

###############################################################################
# Create a task for map_city_tier() function with task_id 'mapping_city_tier'
###############################################################################

mapping_city_tier = PythonOperator(task_id='mapping_city_tier',python_callable=utils.map_city_tier,dag = ML_data_cleaning_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'city_tier_mapping':city_tier_mapping})
###############################################################################
# Create a task for map_categorical_vars() function with task_id 'mapping_categorical_vars'
###############################################################################

mapping_categorical_vars = PythonOperator(task_id='mapping_categorical_vars',python_callable=utils.map_categorical_vars,dag = ML_data_cleaning_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'list_platform':list_platform,'list_medium':list_medium,'list_source':list_source})
############bui###################################################################
# Create a task for interactions_mapping() function with task_id 'mapping_interactions'
###############################################################################

mapping_interactions = PythonOperator(task_id='mapping_interactions',python_callable=utils.interactions_mapping,dag=ML_data_cleaning_dag,
                                      op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'interacation_mapping_file':INTERACTION_MAPPING,'index_columns':INDEX_COLUMNS})

###############################################################################
# Create a task for model_input_schema_check() function with task_id 'checking_model_inputs_schema'
###############################################################################

checking_model_inputs_schema=PythonOperator(task_id='checking_model_inputs_schema',python_callable=data_validation_checks.model_input_schema_check,dag=ML_data_cleaning_dag,
                                             op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'model_input_schema':schema.model_input_schema})
###############################################################################
# Define the relation between the tasks
###############################################################################


building_db.set_downstream(loading_data)
loading_data.set_downstream(checking_raw_data_schema)
checking_raw_data_schema.set_dowstream(mapping_city_tier)
mapping_city_tier.set_downstream(mapping_categorical_vars)
mapping_categorical_vars.set_downstream(mapping_interactions)
mapping_interactions.set_downstream(checking_model_inputs_schema)

