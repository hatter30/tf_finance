

def pct_change(df):
    pct_change = (1 - df / df.shift(1)).shift(-1)
    pct_change = pct_change.dropna()
    return pct_change