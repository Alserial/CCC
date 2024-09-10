"""
Author: COMP90024 Group 32, 2024 May
    Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
    Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
    Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
    Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
    Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>
"""

from Utils import Utils
from elasticsearch8 import Elasticsearch
import json
from flask import current_app, request

# Gets the data from ES based on SA2 code
def by_area():
    sa2_code = request.headers["X-Fission-Params-Area"]

    current_app.logger.info(f"Getting data for the following SA2: {sa2_code} ")

    client = Utils.get_es_client()
    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {"term": {"sa2_code": int(sa2_code)}} 
                ]
            }
            }
    }
    response = client.search(body=query, index="prediction")
    
    current_app.logger.info(response)
    return json.dumps(response["hits"]["hits"])

def by_illness():
    illness = request.headers["X-Fission-Params-Illness"]

    current_app.logger.info(f"Getting data for the following illness: {illness} ")

    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {"term": {"illness": illness}} 
                ]
            }
            }
    }
    response = client.search(body=query, index="prediction")
    
    current_app.logger.info(response)
    return json.dumps(response["hits"]["hits"])

def by_area_and_illness():
    sa2_code = request.headers["X-Fission-Params-Area"]
    illness = request.headers["X-Fission-Params-Illness"]

    current_app.logger.info(f"Getting data for the following SA2: {sa2_code} and illness:  {illness}")

    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {"term": {"sa2_code": int(sa2_code)}},
                    {"term": {"illness": illness}} 
                ]
            }
        }
    }
    response = client.search(body=query, index="prediction")
    
    current_app.logger.info(response)
    return json.dumps(response["hits"]["hits"][0])


def get_most_frequency_illness():
    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    
                ]
            }
        }
    }

    index_name = "prediction"

    try:
        res = client.search(
            index=index_name,        
            body=query,
            scroll='1m'
        )

        scroll_id = res['_scroll_id']   
        all_docs = res['hits']['hits']

        while True:
            res = client.scroll(scroll_id=scroll_id, scroll='1m')
            if not res['hits']['hits']:
                break
            all_docs.extend(res['hits']['hits'])

        client.clear_scroll(scroll_id=scroll_id)

        json_data = [doc['_source'] for doc in all_docs]
        
        illness_counts = {}
        for item in json_data:
            illness = item['illness']
            if illness in illness_counts:
                illness_counts[illness] += int(item['count'])
            else:
                illness_counts[illness] = int(item['count'])


        sorted_illnesses = sorted(illness_counts.items(), key=lambda x: x[1], reverse=True)

        # illness name sorted list
        return json.dumps([x for x,_ in sorted_illnesses])

    except Exception as e:
        current_app.logger.info(f"An error occurred: {str(e)}")
        return None
    

def get_least_frequency_illness():
    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    
                ]
            }
        }
    }

    index_name = "prediction"

    try:
        res = client.search(
            index=index_name,        
            body=query,
            scroll='1m'
        )

        scroll_id = res['_scroll_id']   
        all_docs = res['hits']['hits']

        while True:
            res = client.scroll(scroll_id=scroll_id, scroll='1m')
            if not res['hits']['hits']:
                break
            all_docs.extend(res['hits']['hits'])

        client.clear_scroll(scroll_id=scroll_id)

        json_data = [doc['_source'] for doc in all_docs]
        
        illness_counts = {}
        for item in json_data:
            illness = item['illness']
            if illness in illness_counts:
                illness_counts[illness] += int(item['count'])
            else:
                illness_counts[illness] = int(item['count'])


        sorted_illnesses = sorted(illness_counts.items(), key=lambda x: x[1], reverse=False)
        # illness name sorted list
        return json.dumps([x for x,_ in sorted_illnesses])

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
def get_affected_percentage():
    illness_name = request.headers["X-Fission-Params-Illness"]
    percentage = float(request.headers["X-Fission-Params-Percentage"])
    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {"term": {"illness": illness_name}} 
                ]
            }
        }
    }

    index_name = "prediction"

    try:
        
        res = client.search(
            index=index_name,        
            body=query,
            scroll='1m'
        )

        scroll_id = res['_scroll_id']   
        all_docs = res['hits']['hits']

        while True:
            res = client.scroll(scroll_id=scroll_id, scroll='1m')
            if not res['hits']['hits']:
                break
            all_docs.extend(res['hits']['hits'])

        client.clear_scroll(scroll_id=scroll_id)


        json_data = [doc['_source'] for doc in all_docs]
        
        output = {}
        for item in json_data:
            
            sa2 = item["sa2_name"]
            p = item["percentage"]
            if p > percentage:
                if sa2 not in output:
                    output[sa2] = p

        # dict {sa2: percentage}
        return json.dumps(output)


            
        # print([x for x,_ in sorted_illnesses])

    except Exception as e:
        current_app.logger.info(f"An error occurred: {str(e)}")
        return None


def get_importances():
    illness_name = request.headers["X-Fission-Params-Illness"]
    client = Utils.get_es_client()

    index_name = "feature_importance"
    doc_id = f" {illness_name}"

    try:
        res = client.get(index=index_name, id=doc_id)
        document = res['_source']
        importance_dict = json.loads(document["importance"])
        sorted_importance = sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)

        # dict(feature:importance)
        return json.dumps(sorted_importance)
    except Exception as e:
        current_app.logger.info(f"An error occurred: {str(e)}")
        return None

def get_most_healthy_SA2():
    client = Utils.get_es_client()
    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    
                ]
            }
        }
    }

    index_name = "prediction"

    try:
        res = client.search(
            index=index_name,        
            body=query,
            scroll='1m'
        )

        scroll_id = res['_scroll_id']   
        all_docs = res['hits']['hits']

        while True:
            res = client.scroll(scroll_id=scroll_id, scroll='1m')
            if not res['hits']['hits']:
                break
            all_docs.extend(res['hits']['hits'])

        client.clear_scroll(scroll_id=scroll_id)

        json_data = [doc['_source'] for doc in all_docs]
        
        sa2_illness_counts = {}
        for item in json_data:
            sa2 = item['sa2_name']
            if sa2 in sa2_illness_counts:
                sa2_illness_counts[sa2] += int(item['count'])
            else:
                sa2_illness_counts[sa2] = int(item['count'])


        sorted_sa2 = sorted(sa2_illness_counts.items(), key=lambda x: x[1], reverse=True)
        # illness name sorted list
        return json.dumps([x for x,_ in sorted_sa2])

    except Exception as e:
        current_app.logger.info(f"An error occurred: {str(e)}")
        return None
    
def get_least_healthy_SA2():    
    client = Utils.get_es_client()

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    
                ]
            }
        }
    }

    index_name = "prediction"

    try:
        res = client.search(
            index=index_name,        
            body=query,
            scroll='1m'
        )

        scroll_id = res['_scroll_id']   
        all_docs = res['hits']['hits']

        while True:
            res = client.scroll(scroll_id=scroll_id, scroll='1m')
            if not res['hits']['hits']:
                break
            all_docs.extend(res['hits']['hits'])

        client.clear_scroll(scroll_id=scroll_id)

        json_data = [doc['_source'] for doc in all_docs]
        
        sa2_illness_counts = {}
        for item in json_data:
            sa2 = item['sa2_name']
            if sa2 in sa2_illness_counts:
                sa2_illness_counts[sa2] += int(item['count'])
            else:
                sa2_illness_counts[sa2] = int(item['count'])


        sorted_sa2 = sorted(sa2_illness_counts.items(), key=lambda x: x[1], reverse=False)
        # illness name sorted list
        return json.dumps([x for x,_ in sorted_sa2])

    except Exception as e:
        current_app.logger.info(f"An error occurred: {str(e)}")
        return None