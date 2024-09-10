# import os
# import logging
# import socket
import json
import requests
# import pandas as pd
from flask import current_app
# import geopandas as gpd

def config(k):
        with open(f'/configs/default/parameters/{k}', 'r') as f:
            return f.read()

def main():
    BOM_SITES = [
      {
        "site": "MOP",
        "site_name": "Melbourne Olypic Park",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
      },
      {
        "site": "MbA",
        "site_name": "Melbourne Airport",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94866.json"
      },
      {
        "site": "Ava",
        "site_name": "Avalon",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94854.json"
      },
      {
        "site": "Cbs",
        "site_name": "Cerberus",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94898.json"
      },
      {
        "site": "Cdsm",
        "site_name": "Coldstream",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94864.json"
      },
      {
        "site": "EA",
        "site_name": "Essendon Airport",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95866.json"
      },
      {
        "site": "Fwkn",
        "site_name": "Fawkner Beacon",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95872.json"
      },
      {
        "site": "FC",
        "site_name": "Ferny Creek",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94872.json"
      },
      {
        "site": "Frk",
        "site_name": "Frankston",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94876.json"
      },
      {
        "site": "Frkb",
        "site_name": "Frankston Beach",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94871.json"
      },
      {
        "site": "GR",
        "site_name": "Geelong Racecourse",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94857.json"
      },
      {
        "site": "Lav",
        "site_name": "Laverton",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94865.json"
      },
      {
        "site": "MrA",
        "site_name": "Moorabbin Airport",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94870.json"
      },
      {
        "site": "PnC",
        "site_name": "Point Cook",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95941.json"
      },
      {
        "site": "PnW",
        "site_name": "Point Wilson",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94847.json"
      },
      {
        "site": "Rhy",
        "site_name": "Rhyll",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94892.json"
      },
      {
        "site": "Scsb",
        "site_name": "Scoresby",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95867.json"
      },
      {
        "site": "She",
        "site_name": "Sheoaks",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94863.json"
      },
      {
        "site": "SCI",
        "site_name": "South Channel Island",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.94853.json"
      },
      {
        "site": "SKHR",
        "site_name": "St Kilda Harbour RMYS",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95864.json"
      },
      {
        "site": "Vb",
        "site_name": "Viewbank",
        "api": "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95874.json"
      }
    ]
    """Harvest weather data from BOM, and write the data into Elastic Search
       the script is called every 72hrs, matching the frequency of update of the website
    """

    sites = BOM_SITES

    # return json.dumps(sites)
    harvested = {}

    for s in sites:
        site = s["site"]
        site_name = s["site_name"]
        api = s["api"]

        print(f"Starting harvest {site} observations from {site_name}")

        try:
            response = requests.get(api, timeout=60)
            if response.status_code == 200:
                print("Harvest succeed")
                
                data = response.json()
                
                create_index_query = {
                    "settings": {
                        "index": {
                            "number_of_shards": 3,
                            "number_of_replicas": 1
                        }
                    },
                    "mappings": {
                        "properties": {
                            "data": {
                                "type": "text"
                            }
                        }
                    }
                }
                create_index_url = f"https://127.0.0.1:9200/{site.lower()}"
                create_index_response = requests.put(create_index_url, json=create_index_query, auth=('elastic', 'elastic'),verify=False)
                create_index_response_data = create_index_response.json()
                print(f"Index creation response: {create_index_response_data}")
                data_str = json.dumps(data["observations"]["data"])    
                upload_data_query = {
                    "data": data_str
                }
                upload_data_url = f"https://127.0.0.1:9200/{site.lower()}/_doc/1"
                upload_data_response = requests.put(upload_data_url, json=upload_data_query, auth=('elastic', 'elastic'),verify=False)
                upload_data_response_data = upload_data_response.json()
                print(f"Data upload response: {upload_data_response_data}")
                
        except requests.exceptions.Timeout:
            print("Request time out")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")


    return json.dumps(harvested)

if __name__ == "__main__":
    main()
    