import requests
import json
import pandas as pd
import datetime
import calendar

def get_nomina(by_codigo_nivel: str ="all",by_codigo_entidad: str ="all",by_mes: str = "1"):

    api_url = "https://datos.hacienda.gov.py:443/odmh-api-v1/rest/api/v1/nomina/cabecera"
    with open('./access_token.json') as json_file:
        access_token = json.load(json_file)['accessToken']
    # Query parameters
    params = {
        "page": 1,
        "by_anho": 2024,
        "by_mes": by_mes,
        "by_codigo_nivel": by_codigo_nivel,
        "by_codigo_entidad": by_codigo_entidad
    }
    # Set headers
    headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['results'])

            if data['meta']['totalPages'] != 1: 
                for page in range(2,data['meta']['totalPages']):
                    params['page']=page
                    response = requests.get(api_url, params=params, headers=headers)
                    data = response.json()
                    df2 = pd.DataFrame(data['results'])
                    df = pd.concat([df, df2], ignore_index=True)    

            return df
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Request error: {e}")


def get_accessToken():

    api_url = "https://datos.hacienda.gov.py:443/odmh-api-v1/rest/api/v1/auth/token"  
    payload = {
    "clientSecret": "1a316111294da9e941b18a1ff72f98dc0ad6a1a90d87997926669f759add90b3"
    }
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "ed6ae92c-3a33-4b75-adbf-ce802893fb33"
    }

    try:
        access_token = requests.post(api_url, json=payload, headers=headers)

        if access_token.status_code == 200:

            print("API response:", access_token.json())

            with open("access_token.json", "w") as json_file:
                json.dump(access_token.json(), json_file, indent=4)
            return access_token.json()
        
        else:
            print(f"Error: {access_token.status_code} - {access_token.text}")
    except requests.RequestException as e:
        print(f"Request error: {e}")



def get_projects():
    url = "https://datos.congreso.gov.py/opendata/api/data/proyecto?offset=3&limit=10"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = df = pd.DataFrame(data.result.json())
        return df
    else:
        return None
    

if __name__ == "__main__":
    accessToken = get_accessToken()
    if accessToken is not None: print("Access token successfully obtained!!")

    # Current month 
    today_date = datetime.date.today()
    last_month = today_date.replace(day=1) - datetime.timedelta(days=1)
    #! Please, descomment after we found the correct date to update the csv.
    #previous_month_number = str(last_month.month) 
    #previous_month_name = calendar.month_name[last_month.month]
    previous_month_number = '2'
    previous_month_name = 'February'
    nomina = get_nomina(by_mes = previous_month_number)
   
    if nomina is not None:
        nomina.to_csv(f"./Data/{previous_month_name}.csv")
        print(nomina)


