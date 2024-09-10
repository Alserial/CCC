"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""


from Utils import Utils
import json
import requests
from flask import current_app
from datetime import datetime
from elasticsearch8 import Elasticsearch
from elasticsearch8.helpers import bulk


def main():
    """Harvest weather data from BOM, and write the data into Elastic Search
       the script is called every 72hrs, matching the frequency of update of the website
    """
    current_app.logger.info("Start harvesting weather")

    site_apis = Utils.get_weather_api()
    site_sa2 = Utils.get_site_sa2()

    weather = []
    for site, url in site_apis.items():
        current_app.logger.info(f"Starting harvest weather observations from {site}")

        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                current_app.logger.info("Harvest succeed")
                
                data = response.json()
                sa2_code = None
                sa2_name = None
                lon, lat = (0, 0)
                for dic in site_sa2:
                    if dic['site'] == site:
                        sa2_code = dic['sa2_code']
                        sa2_name = dic['sa2_name']
                        lon, lat = dic['location']
                weather.extend(process_data(data, site, lat, lon, sa2_code, sa2_name))
             
        except requests.exceptions.Timeout:
            current_app.logger.info("Request time out")
        except requests.exceptions.RequestException as e:
            current_app.logger.info(f"Request error: {e}")
    client = Utils.get_es_client()
    # Bulk index operation
    response = bulk(client, weather)
    current_app.logger.info(f"Data upload response: {response}")
    # for res in response:
    #     print(str(res))
    
    response = bulk(client, impute_data(weather))
    current_app.logger.info(f"Imputed data upload response: {response}")
    
    # for res in response:
    #     print(str(res))

    return "OK"

def process_data(data, site, lat, lon, sa2_code, sa2_name):
    for d in data["observations"]["data"]:
        utc_time = d["aifstime_utc"]
        time = datetime.strptime(utc_time, "%Y%m%d%H%M%S")
        iso_date_time_str = time.isoformat()
        id = f"{site}_{utc_time}"

        cleaned_observation = {
            "_index": "weather",
            "_id": id,
            "time": iso_date_time_str,
            "site": site,
            "name": d.get("name", ""),
            "local_date_time_full": d.get("local_date_time_full", ""),
            "lat": lat,
            "lon": lon,
            "SA2_Code": sa2_code,
            "SA2_Name": sa2_name, 
            "gust_kmh": d.get("gust_kmh", ""),
            "apparent_t": d.get("apparent_t"),
            "delta_t": d.get("delta_t", ""),
            "air_temp": d.get("air_temp", ""),
            "press": d.get("press", ""),
            "rain_trace": d.get("rain_trace",""),
            "rel_hum": d.get("rel_hum", ""), 
            "vis_km": d.get("vis_km", ""), 
            "wind_spd_kmh": d.get("wind_spd_kmh", "")
        }
        yield cleaned_observation
        
        
def impute_data(data):
    # ROOT = 'https://object-store.rc.nectar.org.au/v1/AUTH_cee2b7b252db404282a2beb9fb689e86/cloud-volume'
    ROOT = Utils.config("MRC_OBJ_STORE_URL")
    nearest_sa2 = requests.get(f'{ROOT}/nearest_sa2.json').json()
    unseen = requests.get(f'{ROOT}/need_weather_imp_sa2.json').json()
    all_sa2 = requests.get(f'{ROOT}/All_SA2.json').json()
    imputed = []
    for k, v in nearest_sa2.items():
        print(f"start imputing data for {k}")
        if len(v) == 1:
            continue
        neighbours = [d[0] for d in v]
        all_dist = [1/d[1] for d in v]
        weights = [d / sum(all_dist) for d in all_dist]
        neighbour_observations = [[], [], [], [], []]
        for observation in data:
            for i in range(len(neighbours)):
                if observation["SA2_Code"] == neighbours[i]:
                    neighbour_observations[i].append(observation)     
                
        for i in range(160):
            now = [neighbour_observations[j][int(i%len(neighbour_observations[j]))] for j in range(5)]
            imputed_data = {
                '_index': 'weather',
                '_id': f"{find_sa2_name(k, all_sa2)}-{now[0]['time']}",
                'time': now[0]['time'],
                'site': "Imputation", 
                'name': "Imputation", 
                'local_date_time_full': now[0]['local_date_time_full'], 
                'lat': unseen[k][1],
                'lon': unseen[k][0],
                "SA2_Code": k,
                "SA2_Name": find_sa2_name(k, all_sa2), 
                "gust_kmh": weighted_average(now, weights, "gust_kmh"),
                "apparent_t": weighted_average(now, weights, "apparent_t"),
                "delta_t": weighted_average(now, weights, "delta_t"),
                "air_temp": weighted_average(now, weights, "air_temp"),
                "press": weighted_average(now, weights, "press"),
                "rain_trace": weighted_average(now, weights, "rain_trace"),
                "rel_hum": weighted_average(now, weights, "rel_hum"),
                "vis_km": weighted_average(now, weights, "vis_km"),
                "wind_spd_kmh": weighted_average(now, weights, "wind_spd_kmh")
            }
            imputed.append(imputed_data)
    return imputed
            
            
def weighted_average(observations, weight, target):
    total = [observations[i][target] for i in range(len(observations))]
    avg = []
    for i in range(len(weight)):
        if isinstance(total[i], float):
            avg.append(weight[i]*total[i])
    return sum(avg)

def find_sa2_name(code, all_sa2):
    for s in all_sa2:
        if s['sa2_code'] == code:
            return s["sa2_name"]
    return "Imputation"