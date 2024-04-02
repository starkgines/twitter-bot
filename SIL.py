import requests
import json
import pandas as pd

## HERE SHOULD BE ALL LIST OF FUNCTIONS


def get_projects():
    url = "https://datos.congreso.gov.py/opendata/api/data/proyecto?offset=3&limit=10"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = df = pd.json_normalize(data)
        return df
    else:
        return None
    

if __name__ == "__main__":
    projects = get_projects()

    if projects is not None:
        print(projects)


