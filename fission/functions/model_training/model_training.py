"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""

import pandas as pd
from Utils import Utils
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from flask import current_app
from sklearn.model_selection import train_test_split
import json
from elasticsearch8 import Elasticsearch
from elasticsearch8.helpers import bulk


def main():
    # TODO import data sudo and weather from es
    df_sudo = pd.read_json(f'{Utils.config("MRC_OBJ_STORE_URL")}/total.json').T
    df_weather = pd.read_json(f'{Utils.config("MRC_OBJ_STORE_URL")}/weather.json')

    # get all sudo information having existed weather sa2 region then combine the data into one dataframe
    value_counts_weather = df_weather['SA2_Code'].value_counts()
    df_sudo_new = df_sudo[df_sudo[' sa2_code_2021'].isin(list(value_counts_weather.index))]
    df_total = pd.merge(df_sudo_new,df_weather,how='inner',left_on=' sa2_code_2021', right_on='SA2_Code')

    # deleted all label cols and irrelavant feataures
    deleted_lst = [' sa2_code_2021', 'lat', 'lon', 'SA2_Code', 'SA2_Name', 'site', 'name','local_date_time_full', 'time']
    zeros_count = (df_sudo_new == 0).sum()
    label_lst = []
    for index, _ in zeros_count.items():
        if 'age_tot' in index and 'per_age' not in index:
            label_lst.append(index)
    
    X = df_total.drop(label_lst, axis = 1)
    X_new = X.drop(deleted_lst, axis = 1)
    # fill missing values
    X = X.fillna(0)
    X = X.replace('-', 0)
    X_new = X_new.fillna(0)
    X_new = X_new.replace('-', 0)

    prediction_data = []
    feature_data = []
    added_observations = {}

    # training models and save as model files
    for label in label_lst:
        y = df_total[label]

        # train the model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_new, y)
        feature_names = list(X_new.columns)
        feature_importances_df = pd.DataFrame({'Feature': feature_names, 'Importance': model.feature_importances_})
        feature_importances_df = feature_importances_df.set_index("Feature").to_dict()
        feature_data.append({
                "_id": label,
                "_index": "feature_importance",
                "importance": json.dumps(feature_importances_df["Importance"])
                }
            )
        # predict the amount of people who will have this illness
        y_pred = model.predict(X_new)
        for sa2_code, sa2_name, tot, count in zip(df_total['SA2_Code'], df_total['SA2_Name'], df_total[' tot_p'], y_pred):
            if (label, sa2_code) not in added_observations:
                id = f"{label}_{sa2_code}"
                observation = {
                    "_id": id,
                    "_index": "prediction",
                    "sa2_code": sa2_code,
                    "sa2_name": sa2_name,
                    "illness": label,
                    "count": count,
                    "tot_people": tot,
                    "percentage": count/tot
                }
                added_observations[(label, sa2_code)] = True
                prediction_data.append(observation)

    client = Utils.get_es_client()
    current_app.logger.info("Start inserting into ES")

    current_app.logger.info(f"There are {len(prediction_data)} prediction data and {len(feature_data)} feature data")

    # Bulk index operation
    response = bulk(client, prediction_data)
    current_app.logger.info(f"Prediction data upload response: {response}")

    response = bulk(client, feature_data)
    current_app.logger.info(f"Feature data upload response: {response}")
    # for res in response:
    #     current_app.logger.info(f"Processed: {res}")
    
    current_app.logger.info("Finished")
    return "OK"