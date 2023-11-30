import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import datetime

def get_access_token():
    with open("creds.json", "r") as f:
        creds = eval(f.read())

    token = requests.post(
        "http://digital.iservices.rte-france.com/token/oauth/",
        auth=(creds["client_id"], creds["client_secret"])
    )

    if token.status_code != 200:
        print("Error accessing OAuth2")
    else:
        token = eval(str(token.content.decode('utf-8')))["access_token"]
        return token


def get_tempo_like_calendars(start_date, end_date, fallback_status=False, access_token=None):
    if not access_token:
        access_token = get_access_token()

    api_url = "https://digital.iservices.rte-france.com/open_api/tempo_like_supply_contract/v1/tempo_like_calendars"
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'fallback_status': fallback_status
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        # Add any other headers required by the API
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_today():
    tdy = datetime.date.today().strftime("%Y-%m-%dT%H:%M:%S+01:00")
    tmr = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S+01:00")
    response = get_tempo_like_calendars(tdy, tmr)
    if response:
        for item in response["tempo_like_calendars"]["values"]:
            if item["start_date"] == tdy:
                return item["value"]


def get_tomorrow():
    tmr = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S+01:00")
    after_tmr = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S+01:00")
    response = get_tempo_like_calendars(tmr, after_tmr)
    if response:
        for item in response["tempo_like_calendars"]["values"]:
            if item["start_date"] == tmr:
                return item["value"]
        else:
            # Likely not yet defined tomorrow's Tempo
            return None


if __name__ == "__main__":


    get_today()
    # TODO: make sure I am getting the proper day


    exit()
    # Example usage:
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    token_url = "https://authorization-server.com/token"
    username = "your_username"
    password = "your_password"
    scope = "your_requested_scopes"

    # Get the access token
    access_token = get_access_token(client_id, client_secret, token_url, username, password, scope)

    # Make the API request
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    fallback_status = "true"
    result = get_tempo_like_calendars(start_date, end_date, fallback_status, access_token)

    if result:
        print("API Response:")
        print(result)
    else:
        print("Failed to retrieve data from the API.")
