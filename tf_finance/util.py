import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

def get_corp_code(from_url=False, file_name='corp_code.xlsx'):
    if from_url:
        code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    else:
        file_path = os.path.dirname(os.path.realpath(__file__)) + '\\raw_data\\' + file_name
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
    if not item_name in code_df.name.values:
        raise ValueError('Invalid item name %s' % item_name)
    code = int(code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False))
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code:06d}'.format(code=code)
    return url

def daily_sise(url, num_start, num_end):
    df = pd.DataFrame()
    for page in range(num_start, num_end):
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


if __name__ == '__main__':
    folder_path = os.path.dirname(os.path.realpath(__file__))
    print(folder_path)


