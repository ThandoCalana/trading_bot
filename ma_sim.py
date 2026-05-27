import pandas as pd
import utils
import instrument


# ==========================
# THIS SCRIPT SIMULATES EVERY COMBINATION OF THE MAs and outputs 
# the best performing combination of any given tradable pair
# ==========================

# Trade signal is when diff and diff_prev have opposite signs => 
# They are crossing/ touching
def is_trade(row):
    if row['DIFF'] >= 0 and row['DIFF_prev'] < 0:
        return 1
    if row['DIFF'] <= 0 and row['DIFF_prev'] > 0:
        return -1
    else:
        return 0
    
# Calculating the difference in MAs in order to find crossing points
def evaluate_pair(i_pair, mashort, malong, price_data):
    price_data['DIFF'] = price_data['MA_16'] - price_data['MA_64']
    price_data['DIFF_prev'] = price_data['DIFF'].shift(1) # similar to LAG() window function (-1 for LEAD())
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis=1) 

    df_trades = price_data[price_data['IS_TRADE'] != 0].copy()
    # Calculating diff between next - current mid_c price
    df_trades['DELTA'] = (df_trades['mid_c'].diff() / i_pair.pipLocation).shift(-1)
    df_trades['GAIN'] = df_trades["DELTA"] * df_trades['IS_TRADE']

    print(f"{i_pair.name} {mashort} {malong} trades:{df_trades.shape[0]} gain:{df_trades['GAIN'].sum():.0f}")
    
    return df_trades['GAIN'].sum()

def get_price_data(pairname, granularity):
    # Reading in a pair's historical data, from pickle to df, using utils module
    df = pd.read_pickle(utils.get_hist_data_filename(pairname, granularity))

    non_price_cols = ['time', 'volume']
    price_cols = [x for x in df.columns if x not in non_price_cols] # Using list comprehension to isolate the price columns
    df[price_cols] = df[price_cols].apply(pd.to_numeric)

    # Creating df for moving average strategy using mid prices
    return df[['time', 'mid_c']] # only returning columns we are interested in

def get_ma_col(ma):
    return f"MA_{ma}"

def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_short + ma_long)

    # Looping through MA list, calculating and adding each MA to the DF
    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data['mid_c'].rolling(window=ma).mean()

    return price_data

def run():
    pairname = "EUR_USD"
    granularity = "H1"
    ma_short = [8, 16, 32, 64] # Sell when crossing down
    ma_long = [32, 64, 96, 128, 256] # Buy when crossing up
    i_pair = instrument.Instrument.get_instrument_by_name(pairname)

    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    best = -1000000.0
    b_mashort = 0
    b_malong = 0

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong: # ensures we don't sell when we should be buying
                continue
            res = evaluate_pair(i_pair, _mashort, _malong, price_data.copy())
            if res > best:
                best = res
                b_masshort = _mashort
                b_malong = _malong

    print(f"Best: {best:.0f} MA_SHORT: {b_masshort:.0f} MA_LONG: {b_malong:.0f}")
if __name__ == '__main__':
    run()