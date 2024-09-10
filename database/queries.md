### create index

```json
"create_index_query": {
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    },
    "mappings": {
        "properties": {
            "site": {
                "type": "text"
            },
            "time": {
                "type": "date"  
            },
            "data": {
                "type": "text"
            }
        }
    }
}
```

### search query

``` json
"query": {
    "size": 1000,
    "query": {
        "bool": {
            "must": [
            ]
        }
    }
}
```


