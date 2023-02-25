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
### Pre-processing

### EDA

### Model Experimentation

Pycaret is an open-source, low-code machine learning library in Python that is designed to simplify the machine learning process. It allows users to perform several common machine learning tasks, such as data pre-processing, feature engineering, model selection, hyperparameter tuning, and model deployment, with minimal coding.. Based on the initial experiment results, it was found that there were a few irrelevant features. The second run of the experiment was done after removing the irrelevant features. Pycaret internally logs the model too mllflow registry based on the parameters passed in setup function. The model experimentation notebook can be found here [Model experimentation](https://github.com/RakshithaBS/Lead_Scoring_Case_Study/blob/master/notebooks/lead_scoring_model_experimentation.ipynb).

### Test Cases




## Setup
