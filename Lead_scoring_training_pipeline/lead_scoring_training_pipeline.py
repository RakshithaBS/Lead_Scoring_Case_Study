##############################################################################
# Import necessary modules
# #############################################################################
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
import importlib.util


###############################################################################
# Define default arguments and DAG
# ##############################################################################
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022,7,30),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ML_training_dag = DAG(
                dag_id = 'Lead_scoring_training_pipeline',
                default_args = default_args,
                description = 'Training pipeline for Lead Scoring System',
                schedule_interval = '@monthly',
                catchup = False
)

utils = module_from_file("utils", "/home/airflow/dags/Lead_scoring_training_pipeline/utils.py")
constants= module_from_file("utils", "/home/airflow/dags/Lead_scoring_training_pipeline/constants.py")


###############################################################################
# Create a task for encode_features() function with task_id 'encoding_categorical_variables'
# ##############################################################################

encoding_categorical_variables = PythonOperator(task_id='encoding_categorical_variables',python_callable=utils.encode_features,
                                               dag=ML_training_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'one_hot_encoded_features':constants.ONE_HOT_ENCODED_FEATURES,'features_to_encode':constants.FEATURES_TO_ENCODE})
###############################################################################
# Create a task for get_trained_model() function with task_id 'training_model'
# ##############################################################################

training_model = PythonOperator(task_id='training_model',python_callable=utils.get_trained_model,
                                               dag=ML_training_dag,op_kwargs={'db_file_name':constants.DB_FILE_NAME,'db_path':constants.DB_PATH,'model_config':constants.model_config,'tracking_uri':constants.TRACKING_URI,
                                                                             'experiment_name':constants.EXPERIMENT_NAME})

###############################################################################
# Define relations between tasks
# ##############################################################################

encoding_categorical_variables.set_downstream(training_model)