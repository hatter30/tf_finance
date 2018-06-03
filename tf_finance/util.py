import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

absolute_file_path = os.path.dirname(os.path.realpath(__file__))

def get_corp_code(from_url=False, file_name='corp_code.xlsx'):
    if from_url:
        code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    else:
        file_path = absolute_file_path + '\\raw_data\\' + file_name
        code_df = pd.read_excel(file_path)

    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
    code_df = code_df[['회사명', '종목코드']]
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    return code_df

def get_etf_code(file_name = 'etf_code.xlsx'):
    file_path = os.path.dirname(os.path.realpath(__file__)) + '\\raw_data\\' + file_name
    code_df = pd.read_excel(file_path)
    return code_df


def get_finance_url(item_name, code_df):
    if not item_name in code_df.name_en.values:
        raise ValueError('Invalid item name %s' % item_name)
    code = int(code_df.query("name_en=='{}'".format(item_name))['code'].to_string(index=False))
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code:06d}'.format(code=code)
    return url

def daily_sise(url, num_start=1, num_end=None):
    if not num_end:
        last_pg_num = get_last_page_num(url)
    else:
        last_pg_num = num_end

    df = pd.DataFrame()
    for page in range(num_start, last_pg_num):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    df.dropna()
    return df

def get_last_page_num(url):
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(data, 'html.parser')
    text_attrs = bs.find_all('a')[-1].attrs['href']
    num_last_pg = int(text_attrs.split('=')[-1])
    return num_last_pg

def merge_sise_by_day(updated_df, old_df, day_column='날짜'):
    old_df_first_day = old_df.loc[0][day_column]
    index_matched_list = updated_df.index[updated_df[day_column] == old_df_first_day].tolist()
    assert len(index_matched_list) == 1, 'Invalid index list'
    index_matched = index_matched_list[0]

    sliced_update_df = updated_df.loc[:index_matched-1]
    merged = pd.concat([sliced_update_df, old_df])
    merged = merged.reset_index(drop=True)
    return merged


if __name__ == '__main__':
    folder_path = os.path.dirname(os.path.realpath(__file__))
    print(folder_path)


