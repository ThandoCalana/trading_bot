import requests
import pandas as pd
import defs
import utils

class OandaAPI():

    def __init__(self):
        self.session = requests.Session()

    # Fecthes all instruments that can be traded
    # Returns a response code and response json with all the data of the instruments ('intruments' is the key)
    def fecth_instruments(self):

        url = f'{defs.OANDA_URL}/instruments'
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)

        return response.status_code, response.json()
    

    # Converts the response json of the instruments into a dataframe
    # Returns only the specific columns from the DF that we are looking for
    def get_instruments_df(self):
        code, data = self.fecth_instruments()

        if code == 200:
            df = pd.DataFrame(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None
        
        
    # Takes the dataframe from get_instruments_df()
    # Saves the dataframe as a pkl file
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())


    # Fetched the candle info on each pair that is passed to the function
    # Returns the status code and the reponse json, containing the information related to the pair
    def fetch_candles(self, pair_name, count, granularity):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        params = {
            'count': count,
            'granularity': granularity,
            'price': 'MBA'
        }
        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)

        return response.status_code, response.json()


if __name__ == "__main__":
    api = OandaAPI()
    api.save_instruments()
