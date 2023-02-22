# You can create more variables according to your project. The following are the basic variables that have been provided to you
DB_PATH = "/home/airflow/dags/Lead_scoring_data_pipeline/data/"
DB_FILE_NAME = "lead_scoring_data_cleaning_inference.db"
#DB_FILE_NAME = "lead_scoring_data_cleaning.db"
UNIT_TEST_DB_FILE_NAME = "test.db"
DATA_DIRECTORY = "/home/airflow/dags/Lead_scoring_data_pipeline/data/leadscoring_inference.csv"
#DATA_DIRECTORY = "/home/airflow/dags/Lead_scoring_data_pipeline/data/leadscoring.csv"

INTERACTION_MAPPING = "/home/airflow/dags/Lead_scoring_data_pipeline/mapping/interaction_mapping.csv"
#INDEX_COLUMNS = ['created_date', 'city_tier', 'first_platform_c',
#       'first_utm_medium_c', 'first_utm_source_c', 'total_leads_droppped',
#       'referred_lead', 'app_complete_flag']
INDEX_COLUMNS = ['created_date', 'city_tier', 'first_platform_c',
       'first_utm_medium_c', 'first_utm_source_c', 'total_leads_droppped',
       'referred_lead']
ORIGINAL_DATA="loaded_data"
CITY_TIER_MAPPED="city_tier_mapped"
CATAEGORICAL_VALUES_MAPPED="categorical_variables_mapped"
INTERACTIONS_MAPPED="interactions_mapped"
NOT_FEATURES=['created_date', 'assistance_interaction', 'career_interaction',
                'payment_interaction', 'social_interaction', 'syllabus_interaction']
