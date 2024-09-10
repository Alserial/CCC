"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""


from environment import *
from Utils import Utils

def config(site, k):
    with open(f"/configs/default/{site}/{k}", 'r') as f:
        return f.read()
    
def main():
    """Harvest weather data from BOM, and write the data into Elastic Search
       the script is called every 72hrs, matching the frequency of update of the website
    """
    site_apis = Utils.get_weather_api()
    site_sa2 = Utils.get_site_sa2()
    
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
                        
                cleaned_data = []
                for observation in data["observations"]["data"]:
                    cleaned_observation = {
                        "name": observation.get("name", ""),
                        "local_date_time_full": observation.get("local_date_time_full", ""),
                        "Longitude": lon,
                        "Latitude": lat,
                        "SA2_Code": sa2_code,
                        "SA2_Name": sa2_name,
                        "gust_kmh": observation.get("gust_kmh", ""),
                        "apparent_t": observation.get("apparent_t"),
                        "delta_t": observation.get("delta_t", ""),
                        "air_temp": observation.get("air_temp", ""),
                        "press": observation.get("press", ""),
                        "rain_trace": observation.get("rain_trace",""),
                        "rel_hum": observation.get("rel_hum", ""), 
                        "vis_km": observation.get("vis_km", ""), 
                        "wind_spd_kmh": observation.get("wind_spd_kmh", "")
                    }
                    cleaned_data.append(cleaned_observation)
                try:
                    store_res = requests.post(url=config(site, "DATA_PATH"),
                                              headers={'Content-Type': 'application/json'},
                                              data=json.dumps(cleaned_data),
                                              timeout = 60)
                    if store_res.status_code == 200:
                        current_app.logger.info("Write into database succeed")
                    else:
                        current_app.logger.info("Failed to write")
                except requests.exceptions.Timeout:
                    current_app.logger.info("Request time out")
                except requests.exceptions.RequestException as e:
                    current_app.logger.info(f"Request error: {e}")
                return "NICE!"    
            else:
                current_app.logger.info(f"Harvest failed with error code {response.status_code}")
                return response.status_code
        except requests.exceptions.Timeout:
            current_app.logger.info("Request time out")
        except requests.exceptions.RequestException as e:
            current_app.logger.info(f"Request error: {e}")