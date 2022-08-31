import argparse
from base64 import encode
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories, get_df
import random
from  src.utils.data_mgmt import process_posts
import numpy as np


STAGE = "Two"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

def main(config_path, params_path):
    ## converting XML data tsv
    config = read_yaml(config_path)
    params = read_yaml(params_path) 

    # stage 1

    artifacts = config["artifacts"]

    prepare_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"],artifacts["PREPARED_DATA"])
    train_data_path = os.path.join(prepare_data_dir_path,artifacts["TRAIN_DATA"])
    test_data_path = os.path.join(prepare_data_dir_path,artifacts["TEST_DATA"])

    # stage 2

    featurized_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"],artifacts["PREPARED_DATA"])
    create_directories([featurized_data_dir_path])
    featurized_train_data_path = os.path.join(prepare_data_dir_path,artifacts["FEATURIZED_OUT_TRAIN"])
    featurized_test_data_path = os.path.join(prepare_data_dir_path,artifacts["FEATURIZED_OUT_TEST"])

    # stage -3

    max_features = params["featurize"]["max_params"]
    ngrams = params["featurize"]["ngrams"]

    df_train = get_df(train_data_path)
    
    train_words = np.array(df_train.text.str.lower().values.astype("U"))
    print(train_words[:20])












if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e