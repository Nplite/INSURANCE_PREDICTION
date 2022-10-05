from flask import Flask, request
import sys
import pip
from InsurancePremiumPrediction.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from InsurancePremiumPrediction.logger import logging
from InsurancePremiumPrediction.Exception import InsuranceException
import os, sys
import json
from InsurancePremiumPrediction.config.configuration import Configuration
from InsurancePremiumPrediction.constant import CONFIG_DIR, get_current_time_stamp
from InsurancePremiumPrediction.Pipeline.pipeline import Pipeline
from InsurancePremiumPrediction.entity.insurance_premium_predictor import InsurancePredictor, InsurancePremiumPredictionData
from flask import send_file, abort, render_template



ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "InsurancePremiumPrediction"
SAVED_MODELS_DIR_NAME = "saved_models"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "config.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "config.yaml")

from InsurancePremiumPrediction.logger import get_log_dataframe

INSURANCE_DATA_KEY = "Insurance_data"
EXPENSES_VALUE_KEY = "expenses"

app=Flask(__name__)

@app.route('/artifact', defaults={'req_path': 'InsurancePremiumPrediction'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("InsurancePremiumPrediction", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    pipeline = Pipeline(config=Configuration(CONFIG_FILE_PATH))
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)

@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        INSURANCE_DATA_KEY: None,
        EXPENSES_VALUE_KEY: None
    }

    if request.method == 'POST':
        age = int(request.form.get('age'))
        sex = request.form.get('sex')
        bmi = float(request.form.get('bmi'))
        children = int(request.form.get('children'))
        smoker = request.form.get('smoker')
        region = request.form.get('region')

        Insurance_data = InsurancePremiumPredictionData(age=age,
                                                        sex=sex,
                                                        bmi=bmi,
                                                        children=children,
                                                        smoker=smoker,
                                                        region=region,
                                                        )
        insurance_df = Insurance_data.get_insurance_input_data_frame()
        insurance_predictor = InsurancePredictor(model_dir=MODEL_DIR)
        folder_name = list(map(int, os.listdir(MODEL_DIR)))
        if folder_name==[]:
            context = {
                        INSURANCE_DATA_KEY: Insurance_data.get_insurance_data_as_dict(),
                        EXPENSES_VALUE_KEY: "TRAIN MODEL FIRST",
                        }
            return render_template('predict.html', context=context)          
        expenses = insurance_predictor.predict(insurance_df)
        logging.info(f"expenses :{float(expenses)}" )
        context = {
                    INSURANCE_DATA_KEY: Insurance_data.get_insurance_data_as_dict(),
                    EXPENSES_VALUE_KEY: float(expenses),
                    }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)

@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)

@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", debug=True,port=port)
