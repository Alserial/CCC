import os
import logging
import requests
import socket
import json
import pandas as pd
from flask import current_app
import geopandas as gpd
from shapely import *
from bs4 import BeautifulSoup