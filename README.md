Application URL : [InsurancePremiumPredictor](https://insuranceprediction09.herokuapp.com/)

## Table of contents
* [About project](#about-project)
* [Technologies](#technologies)
* [Software and account requirement](#software-and-account-requirement)
* [Setup](#setup)
* [Project Pipeline](#project-pipeline)
<!-- * [License](#license) -->

## About project
This app predicts Insurance premium price based on some data.


## Technologies
This project is created with below technologies/tools/resorces:
* Python: 3.7
* Machine Learning
* Jupyter Notebook
* HTML/CSS
* Docker
* Git
* CI/CD Pipeline
* Heroku


## Software and account Requirement
1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT cli](https://git-scm.com/downloads)
5. [GIT Documentation](https://git-scm.com/docs/gittutorial)


## Setup
Create a conda environment
```
conda create -p venv python==3.7 -y
```

activate conda environment
```
conda activate venv/
```

To install requirement file
```
pip install -r requirements.txt
```

* Add files to git  `git add .` or  `git add <file_name>`    
* To check the git status  `git status`    
* To check all version maintained by git  `git log`    
* To create version/commit all changes by git  `git commit -m "message"`    
* To send version/changes to github  `git push origin main`    



To setup CI/CD pipeline in heroku we need 3 information
1. HEROKU_EMAIL = 76342ns@gmail.com
2. HEROKU_API_KEY = <>
3. HEROKU_APP_NAME = insuranceprediction

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```
> Note: Image name for docker must be lowercase


To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```

To check running container in docker
```
docker ps
```

Tos stop docker conatiner
```
docker stop <container_id>
```



```
python setup.py install
```


Install ipykernel

```
pip install ipykernel
```


Data Drift:
When your datset stats gets change we call it as data drift


## Project Pipeline
1. [Data Ingestion](#1-data-ingestion)
2. [Data Validation](#2-data-validation)
3. [Data Transformation](#3-data-transformation)
4. [Model Training](#4-model-training)
5. [Model Evaluation](#5-model-evaluation)
6. [Model Deployement](#6-model-deployement)

### 1. Data Ingestion: 
* Data ingestion is the process in which unstructured data is extracted from one or multiple sources and then prepared for training machine learning models.

### 2. Data Validation:
* Data validation is an integral part of ML pipeline. It is checking the quality of source data before training a new mode
* It focuses on checking that the statistics of the new data are as expected (e.g. feature distribution, number of categories, etc). 

### 3. Data Transformation 
* Data transformation is the process of converting raw data into a format or structure that would be more suitable for model building.
* It is an imperative step in feature engineering that facilitates discovering insights.

### 4. Model Training
* Model training in machine learning is the process in which a machine learning (ML) algorithm is fed with sufficient training data to learn from.

### 5. Model Evaluation
* Model evaluation is the process of using different evaluation metrics to understand a machine learning model’s performance, as well as its strengths and weaknesses.
* Model evaluation is important to assess the efficacy of a model during initial research phases, and it also plays a role in model monitoring.

### 6. Model Deployement
* Deployment is the method by which we integrate a machine learning model into production environment to make practical business decisions based on data. 




## Problem Statement :
The goal of this project to give people an estimate of how much they need based on their individual health situation. After that, customers can work with any health insurance carrier and its plans and perks whilwe keeping the projected cost from our study in mind. This can assist a person in concentrating on the health side of an insurance policy rather than the ineffective part.

## Dataset :
The dataset is taken from a Kaggle. You can download the dataset from [here](https://www.kaggle.com/noordeen/insurance-premium-prediction)

## Approach :
Applying machine learing tasks like Data Exploration, Data Cleaning, Feature Engineering, Model Building and model testing to build a solution that should able to predict the premium of the personal for health insurance.

- **Data Exploration :** Exploring the dataset using pandas, numpy, matplotlib, plotly and seaborn.
- **Exploratory Data Analysis :** Plotted different graphs to get more insights about dependent and independent variables/features.
- **Feature Engineering :** Numerical features scaled down and Categorical features encoded.
- **Model Building :** In this step, first dataset Splitting is done. After that model is trained on different Machine Learning Algorithms such as:
    1) Linear Regression
    2) Decision Tree Regressor
    3) Random Forest Regressor
    4) Gradient Boosting Regressor
 
- **Model Selection :** Tested all the models to check the R-squared and best R-squared model selected for GridSearchCV and best parameters to be find out.
- **Pickle File** : Selected model as per best R-squared and GridSearchCv best parameters,and created pickle file using pickle library.
- **Webpage &Deployment :** Created a web application that takes all the necessary inputs from the user & shows the output. Then deployed project on the Heroku Platform.

## Deployment Link :
Heroku Deployment : https://insuranceprediction09.herokuapp.com/



