import pandas as pd
import utils

class Instrument:
    def __init__(self, ob):
        self.name = ob['name'] # EUR_USD
        self.instr_type = ob['type']
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['pipLocation'])
        self.marginRate = ob['marginRate']
    
    def __repr__(self):
        return str(vars(self))
    
    # Returns a df of the tradable pairs
    @classmethod
    def get_instruments_df(cls):
        filename = utils.get_instruments_data_filename()
        return pd.read_pickle(filename)
    

    # Provide all the details specified in __init__, of all the tradable pairs
    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]
    
    # Returns a dict of each tradable pair as the key and its details as the value
    @classmethod
    def get_instruments_dict(cls):
        i_list = cls.get_instruments_list()
        i_keys = [x.name for x in i_list]
        return { k:v for (k,v) in zip(i_keys, i_list)}
    
    # Return a single pair and its details
    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instruments_dict()
        if pairname in d:
            return d[pairname]
        else:
            return None
    

    
if __name__ == "__main__":
    print(Instrument.get_instrument_by_name("EUR_USD"))

