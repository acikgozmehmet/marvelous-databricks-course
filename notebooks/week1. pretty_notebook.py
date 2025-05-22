# Databricks notebook source
# Install in editable mode.
# COMMAND ----------
!pip install python-dotenv

# COMMAND ----------
from dotenv import load_dotenv
load_dotenv(override=True)
# COMMAND ----------

%pip install -e ..
%restart_python

# COMMAND ----------
from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent / 'src'))

# COMMAND ----------
# Install the whl file located in the notebooks folder 
%pip install house_prices-0.1.1-py3-none-any.whl
# %pip install git+https://github.com/end-to-end-mlops-databricks-3/marvelous.git
%restart_python

# COMMAND ----------
%pip install house_prices-0.1.1-py3-none-any.whl
%restart_python
# COMMAND ----------
from loguru import logger
import yaml
import sys
from pyspark.sql import SparkSession
import pandas as pd

# COMMAND ----------
from house_prices.config import ProjectConfig
from house_prices.data_processor import DataProcessor
from marvelous.logging import setup_logging
from marvelous.timer import Timer

config = ProjectConfig.from_yaml(config_path="../project_config.yml", env="dev")

setup_logging(log_file="logs/marvelous-1.log")

logger.info("Configuration loaded:")
logger.info(yaml.dump(config, default_flow_style=False))

# COMMAND ----------

# Load the house prices dataset
spark = SparkSession.builder.getOrCreate()

filepath = "../data/data.csv"

# Load the data
df = pd.read_csv(filepath)


# COMMAND ----------
# Load the house prices dataset
with Timer() as preprocess_timer:
    # Initialize DataProcessor
    data_processor = DataProcessor(df, config, spark)

    # Preprocess the data
    data_processor.preprocess()

logger.info(f"Data preprocessing: {preprocess_timer}")

# COMMAND ----------

# Split the data
X_train, X_test = data_processor.split_data()
logger.info("Training set shape: %s", X_train.shape)
logger.info("Test set shape: %s", X_test.shape)

# COMMAND ----------
# Save to catalog
logger.info("Saving data to catalog")
data_processor.save_to_catalog(X_train, X_test)

# Enable change data feed (only once!)
logger.info("Enable change data feed")
data_processor.enable_change_data_feed()
# COMMAND ----------
