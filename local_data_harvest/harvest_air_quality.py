"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""


# from Utils import Utils
# import os
# import logging
# import socket
import json
import requests
# import pandas as pd
from flask import current_app
from datetime import datetime, timedelta
import numpy as np

def determine_health_advice(value):
    if value < 40:
        return "Good"
    elif 40 <= value < 80:
        return "Fair"
    elif 80 <= value < 120:
        return "Poor"
    elif 120 <= value < 300:
        return "Very poor"
    else:
        return "Extremely poor"

def euler_dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    

def find_sa2(lon, lat):
    with open("../data/All_SA2.json", 'r') as f:
        data = json.load(f)
        
    min_dist = float('inf')
    sa2_code = None
    sa2_name = None
    for lst in data:
        dist = euler_dist(lon, lat, lst['lon'], lst['lat'])
        if dist < min_dist:
            min_dist = dist
            sa2_code = lst['sa2_code']
            sa2_name = lst['sa2_name']
    return sa2_code, sa2_name


def main():
    """Harvest air quality from EPA, and write the data into Elastic Search
       the script is called every 72hrs, matching the frequency of update of the website
    """

    harvested = {}
    User_Agent = 'curl/8.4.0'
    vic_url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites"
    params = {"environmentalSegment": "air"}
    headers = {'User-Agent': User_Agent,
               'Cache-Control': 'no-cache',
               'X-API-key': "96527bc2db05455097a52c8e89fa55dc"}
    current_app.logger.info(f"Starting harvest observations from air quality of VIC")
    
    
    try:
        merged_data = []
        response = requests.get(vic_url, params=params, headers=headers, timeout = 60)
        if response.status_code == 200:      
            current_app.logger.info(f"VIC Harvest succeed")
            data_mel = response.json()
            for row in data_mel.get('records'):
                site_health_advices = row.get('siteHealthAdvices')
                # make sure that there is details for air quality 
                if site_health_advices is not None and isinstance(site_health_advices, list) and len(site_health_advices) > 0:
                    air_detail = site_health_advices[0]
                    lat = row.get("geometry").get('coordinates')[0]
                    lon = row.get("geometry").get('coordinates')[1]
                    sa2_code, sa2_name = find_sa2(lon, lat)
                    observation_data = {
                        "siteName": row.get("siteName"),
                        "Longitude": lon,
                        "Latitude": lat,
                        "SA2_Code": sa2_code,
                        "SA2_Name": sa2_name,
                        "Date": air_detail.get("until")[:10],
                        "ParameterCode": air_detail.get("healthParameter"),
                        "Value": air_detail.get("averageValue"),
                        "HealthAdvice" : air_detail.get("healthAdvice")
                    }
                    merged_data.append(observation_data)
                    
        site_details_url = "https://data.airquality.nsw.gov.au/api/Data/get_SiteDetails"
        site_details_response = requests.get(site_details_url, headers={"accept": "application/json"})
        site_details_data = site_details_response.json()

        # link the site id with the site name and its location
        site_id_to_details = {site["Site_Id"]: {"SiteName": site["SiteName"], "Longitude": site["Longitude"], "Latitude": site["Latitude"]} for site in site_details_data}
        # calcualte the time
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        previous_date = previous_date.strftime("%Y-%m-%d")
        current_date = current_date.strftime("%Y-%m-%d")
        # get the observation information
        observations_url = "https://data.airquality.nsw.gov.au/api/Data/get_Observations"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {
            "Parameters": ["PM10"],
            "Sites": list(site_id_to_details.keys()),
            "StartDate": previous_date,
            "EndDate": current_date,
            "Categories": ["Averages"],
            "SubCategories": ["Hourly"],
            "Frequency": ["24h rolling average derived from 1h average"]
            }
        observations_response = requests.post(observations_url, headers=headers, json=data)
        observations_data = observations_response.json()
        for observation in observations_data:
            site_id = observation["Site_Id"]
            site_details = site_id_to_details.get(site_id, {})
            lat = site_details.get("Latitude")
            lon = site_details.get("Longitude")
            sa2_code, sa2_name = find_sa2(lon, lat)
            site_id = observation["Site_Id"]
            site_details = site_id_to_details.get(site_id, {})
            if observation["Value"]:
                observation_data = {
                    "siteName": site_details.get("SiteName"),
                    "Longitude": lon,
                    "Latitude": lat,
                    "SA2_Code": sa2_code,
                    "SA2_Name": sa2_name,
                    "Date": observation["Date"],
                    "ParameterCode": observation["Parameter"]["ParameterCode"],
                    "Value": observation["Value"],
                    "HealthAdvice" : determine_health_advice(observation["Value"])
                }
                merged_data.append(observation_data)
                
    except Exception as e:
        print()
        
        
    with open("../data/air_quality_demo.json", 'w') as f:
        json.dump(merged_data, f)

    return json.dumps(harvested)