# Lead_Scoring_Case_Study

## Topics Covered

* Overview
* Motivation
* Setup
* Technical Aspect


## Overview

The objective of this project is to predict whether a customer/ lead will purchase the product or not. In this project the focus is mostly on the process of creating pipelines for data pre-processing, model training and inference using Airflow. The project also covers model experiment tracking using MLFlow. Pycaret module which is an opensource framework for auto ML is used to find the best fit model. During pycaret experimentation it is found that lightgbm, which is an xgboost classfication algorithm gives the best performance.The model was evaluated based on accuracy.The project also covers unit test cases using pytest. 

## Motivation

The project is a case study on an ed-tech startup which is finding ways to utilize it's marketing spends efficiently. The company has spent extensively on aquiring customers /leads and is now looking to reduce the CAC(customer acquisition cost). High CAC could be due to the following reasons:

1. Incorrect targeting.
2. High Competition.
3. Inefficient conversion

The business metric addressed here is Leads to Application Completion which resolves the third issue.
A lead is generated when any person visits the website and enters their contact details on the platform. A junk lead is generated when a person who shares their contact details has no interest in the product/service. Having junk leads in the pipeline creates significant inefficiency in the sales process. Thus, the goal of the project is to build a system that categorises leads based on the likelihood of their purchasing the course. This system will help remove the inefficiency caused by junk leads in the sales process.

## Techincal Aspect

### Pipelines

1. Data Pipeline: processes the raw data 
2. Training pipeline : preprocessing & model training
3. Inference pipeline: pre-processing , model prediction 
### Pre-processing & EDA
The dataset primarity focuses on the variables/features describing the origin of the lead(e.g: referred_leads,city_mapped) and the interaction of the lead with the website(1_on_1_mentorship, whatsapp_chat_click). The Exploratory Data Analysis was done using pandas profiling.
#### EDA Observations
* The dataset consists a lot of missing values
* There are only a few categories which are significant in first_platform_c, first_utm_source_c,first_utm_medium_c.
* There are few interaction columns which have 99% missing values 
#### Data Pre-processing
* Reducing the high cardinality in city_mapping column: the city is mapped to tier1 , tier2 and tier 3.
* The first_platform_c, first_utm_medium_c and first_utm_source_c columns contained only a few significant categories. To sort this problem, we can pick up the categories that covered 90% of the data. The smaller contributing categories can be classified as ‘others’. To do this, we must calculate the cumulative frequency of each category to filter them out on 90% criteria. 
* Replaced the null values with 0 for total_leads_dropped and referred_leads column.
* There are 37 interaction columns which have to be classified into four categories namely assistance interaction, career interaction, payment interaction and syllabus interaction. 

The notebook for data preprocessing and EDA can be found here [Data Preprocessing&EDA](https://github.com/RakshithaBS/Lead_Scoring_Case_Study/blob/master/Lead_scoring_data_pipeline/data_cleaning_template.ipynb)

### Model Experimentation

Pycaret is an open-source, low-code machine learning library in Python that is designed to simplify the machine learning process. It allows users to perform several common machine learning tasks, such as data pre-processing, feature engineering, model selection, hyperparameter tuning, and model deployment, with minimal coding.. Based on the initial experiment results, it was found that there were a few irrelevant features. The second run of the experiment was done after removing the irrelevant features. Pycaret internally logs the model too mllflow registry based on the parameters passed in setup function. The model experimentation notebook can be found here [Model experimentation](https://github.com/RakshithaBS/Lead_Scoring_Case_Study/blob/master/notebooks/lead_scoring_model_experimentation.ipynb).

### Test Cases

The project covers basic unit test cases to check the pre-processing functionalities.

1. Check load_data_to_db function.
2. Check mapping city to tiers functionality
3. Test case to check the correct mapping of categorical variables.
4. Test case to check interaction mapping schema

Test cases can be found here [Test cases](https://github.com/RakshithaBS/Lead_Scoring_Case_Study/tree/master/unit_test)



## Setup

1. Install necessary dependencies using the below command.

```
pip install -r requirements.txt
```
2. Install airflow locally
3. Airflow Setup
* Create airflow user for the UI login
```
airflow users create \
    --username rakshitha\
    --firstname rakshitha\
    --lastname bs\
    --role Admin \
    --email rakshitha@gmail.com\
    --password 123
```

* Run airflow webserver
```
airflow webserver -p 8080
```

* Start airflow scheduler
```
airflow scheduler
```
4. MLflow setup
* Starting mlflow tracking server
```
mlflow serve --model-uri <path_to_sqilte_db> --port <port_number> --host <host_address>

```
