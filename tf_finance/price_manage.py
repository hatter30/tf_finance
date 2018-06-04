
import pandas as pd

from tf_finance.util import *

default_codes = ['KODEX 200', 'KODEX S&P500 Futures(H)', 'KODEX Gold Futures(H)', 'KOSEF KTB',
                 'KOSEF USD Futures', 'KODEX KRW CASH']

class PriceManager:
    def __init__(self, names=default_codes):
        self._etf_code = get_etf_code()

        self._price = {name: self.load_from_web_csv(name) for name in names}
        self.save_all_price()

    def load_csv_to_df(self, name):
        file_path = absolute_file_path + '\\price_data\\' + name + '.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            return df
        else:
            return None

    def load_from_web(self, name, load_pg_num=None):
        url = get_finance_url(name, self._etf_code)
        df = daily_sise(url, num_end=load_pg_num)
        return df

    def load_from_web_csv(self, name, load_pg_num=10):
        old_df = self.load_csv_to_df(name)
        if old_df is not None:
            updated_df = self.load_from_web(name, load_pg_num)
            return merge_sise_by_day(updated_df, old_df)
        else:
            return self.load_from_web(name)

    def save_price(self, name, df):
        file_path = absolute_file_path + '\\price_data\\' + name + '.csv'
        df.to_csv(file_path, sep='\t', encoding='utf-8')

    def save_all_price(self):
        for name, price in self._price.items():
            self.save_price(name, price)

    def daily_price(self, names=None):
        if names is not None:
            day = self._price[names[0]]['날짜']
            daily_price_list = [self._price[name]['종가'].rename(name) for name in names]
        else:
            new_names = list(self._price.keys())
            day = self._price[new_names[0]]['날짜']
            daily_price_list = [self._price[name]['종가'].rename(name) for name in new_names]

        merged = pd.concat([day] + daily_price_list, axis=1)

        format = '%Y.%m.%d'
        merged['date'] = pd.DatetimeIndex(pd.to_datetime(merged['날짜'], format=format))
        del merged['날짜']
        merged = merged.set_index('date')

        return merged

    def __getitem__(self, key):
        return self._price[key]