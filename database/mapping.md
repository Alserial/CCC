### Air Index Mapping
```json
{
  "mappings": {
    "properties": {
      "Date": {"type": "date"},
      "HealthAdvice": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "Latitude": {"type": "float"},
      "Longitude": {"type": "float"},
      "ParameterCode": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "SA2_Code": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "SA2_Name": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "State": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "Value": {"type": "float"},
      "siteName": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      }
    }
  }
}
```
### Feature Importance Index Mapping
```json
{
  "mappings": {
    "properties": {
      "importance": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      }
    }
  }
}
```

### Prediction Index Mapping

```json
{
  "mappings": {
    "properties": {
      "count": {"type": "long"},
      "illness": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "percentage": {"type": "float"},
      "sa2_code": {"type": "long"},
      "sa2_name": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "tot_people": {"type": "long"}
    }
  }
}
```
### Sudo Index Mapping
```json
{
  "mappings": {
    "properties": {
      "data": {"type": "text"}
    }
  }
}
```

### Weather Index Mapping

```json
{
  "mappings": {
    "properties": {
      "SA2_Code": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "SA2_Name": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "air_temp": {"type": "float"},
      "apparent_t": {"type": "float"},
      "delta_t": {"type": "float"},
      "gust_kmh": {"type": "long"},
      "lat": {"type": "float"},
      "local_date_time_full": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "lon": {"type": "float"},
      "name": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "press": {"type": "float"},
      "rain_trace": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "rel_hum": {"type": "long"},
      "site": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "time": {"type": "date"},
      "vis_km": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword", "ignore_above": 256}
        }
      },
      "wind_spd_kmh": {"type": "long"}
    }
  }
}
```

