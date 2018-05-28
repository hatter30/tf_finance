import os
import pandas as pd

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
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    return url


if __name__ == '__main__':
    folder_path = os.path.dirname(os.path.realpath(__file__))
    print(folder_path)


