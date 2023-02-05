import os

import yaml

# metadata

__version__ = "0.2.2"
last_update = "February 4, 2023"

# project data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "log")
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# load conf file

with open(os.path.join(DATA_DIR, "conf.yaml"), "r") as f:
    CONF = yaml.safe_load(f)

# data

MPC_NEOCP_URL = CONF["data"]["mcp_neocp_url"]

# observatory

OBS_COORDS = {
    "lat": CONF["observatory"]["lat"],
    "lon": CONF["observatory"]["long"]
}

# visibility

MIN_ALT = CONF["observatory"]["min_alt"]
OBS_TIME = CONF["observatory"]["obs_time"]
TIME_INCR = CONF["observatory"]["time_incr"]

# array columns

COLUMNS = CONF["keys"]
