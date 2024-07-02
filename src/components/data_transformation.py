'''
Here, I will be cleaning raw data so that I have a ready data for my model.
'''
import sys
import os
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file = os.path.join("artifacts", 'preprocessor.pickle')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_features = ['reading_score', 'writing_score']
            categorical_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                     ("one_hot_encoder", OneHotEncoder()),
                     ("scaler", StandardScaler(with_mean=False))
                    
                ]
            )

            logging.info("Pipeline Created")

            preprocessor = ColumnTransformer(
                [
                ("num_pipeline", num_pipeline,numerical_features),
                ("cat_pipline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reaing train and test data - Done")

            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_features = ['reading_score', 'writing_score']

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessing_obj.transform(input_feature_test_df)

            train_array = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]

            test_array = np.c_[
                input_feature_test_array, np.array(target_feature_test_df)
            ]

            save_object (
                file_path = self.data_transformation_config.preprocessor_obj_file,
                obj = preprocessing_obj
            )

            return (train_array, test_array, self.data_transformation_config.preprocessor_obj_file)


            
        except Exception as e:
            raise CustomException(e,sys)