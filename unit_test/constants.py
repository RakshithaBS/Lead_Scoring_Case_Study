# You can create more variables according to your project. The following are the basic variables that have been provided to you
DB_PATH = "data/"
DB_FILE_NAME = "utils_output.db"
UNIT_TEST_DB_FILE_NAME = "test.db"
DATA_DIRECTORY = "data/leadscoring.csv"
INTERACTION_MAPPING = "interaction_mapping.csv"
INDEX_COLUMNS = ['created_date', 'city_tier', 'first_platform_c',
       'first_utm_medium_c', 'first_utm_source_c', 'total_leads_droppped',
       'referred_lead', 'app_complete_flag']
ORIGINAL_DATA="loaded_data"
CITY_TIER_MAPPED="city_tier_mapped"
CATAEGORICAL_VALUES_MAPPED="categorical_variables_mapped"
INTERACTIONS_MAPPED="interactions_mapped"
NOT_FEATURES=['created_date', 'assistance_interaction', 'career_interaction',
                'payment_interaction', 'social_interaction', 'syllabus_interaction']
