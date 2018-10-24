import numpy as np
import pandas as pd


# 数据文件路径设置
file_path = 'data\\'
source_file = file_path + '399300.csv'
target_file = file_path + '399300_new.csv'
# 以下是特征数据文件
usdx_file = file_path + 'USDX.csv'
usdcny_file = file_path + 'USDCNY.csv'
usdjpy_file = file_path + 'USDJPY.csv'
eurusd_file = file_path + 'EURUSD.csv'
gbpusd_file = file_path + 'GBPUSD.csv'
audusd_file = file_path + 'AUDUSD.csv'
xauusd_file = file_path + 'XAUUSD.csv'
xagusd_file = file_path + 'XAGUSD.csv'
bulkstock_file = file_path + 'BulkStock.csv'
industrialproducts_file = file_path + 'IndustrialProducts.csv'
sp500_file = file_path + 'SP500.csv'
dji_file = file_path + 'DJI.csv'
ixic_file = file_path + 'IXIC.csv'
gdaxi_file = file_path + 'GDAXI.csv'
ftse_file = file_path + 'FTSE.csv'
fchi_file = file_path + 'FCHI.csv'
n255_file = file_path + 'N225.csv'
hsi_file = file_path + 'HSI.csv'

global df

def get_stock_index_data(inp_file):
    """
    从csv文件读取沪深300股票指数数据
    """
    global df
    try:
        df = pd.read_csv(inp_file, index_col='trade_date')
        df.index = pd.to_datetime(df.index)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))


def add_usdx(inp_file):
    """
    将美元指数USDX收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_usdx = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdx.index = pd.to_datetime(df_usdx.index)
    df_usdx = pd.Series(df_usdx['close'], name='USDX')

    df = df.join(df_usdx)

    # 补全缺失值
    df['USDX'].fillna(method='ffill', inplace=True)


def add_usdcny(inp_file):
    """
    将人民币汇率USDCNY收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_usdcny = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdcny.index = pd.to_datetime(df_usdcny.index)
    df_usdcny = pd.Series(df_usdcny['close'], name='USDCNY')

    df = df.join(df_usdcny)

    # 补全缺失值
    df['USDCNY'].fillna(method='ffill', inplace=True)


def add_usdjpy(inp_file):
    """
    将USDJPY收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_usdjpy = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdjpy.index = pd.to_datetime(df_usdjpy.index)
    df_usdjpy = pd.Series(df_usdjpy['close'], name='USDJPY')

    df = df.join(df_usdjpy)

    # 补全缺失值
    df['USDJPY'].fillna(method='ffill', inplace=True)


def add_audusd(inp_file):
    """
    将AUDUSD收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_audusd = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_audusd.index = pd.to_datetime(df_audusd.index)
    df_audusd = pd.Series(df_audusd['close'], name='AUDUSD')

    df = df.join(df_audusd)

    # 补全缺失值
    df['AUDUSD'].fillna(method='ffill', inplace=True)


def add_eurusd(inp_file):
    """
    将EURUSD收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_eurusd = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_eurusd.index = pd.to_datetime(df_eurusd.index)
    df_eurusd = pd.Series(df_eurusd['close'], name='EURUSD')

    df = df.join(df_eurusd)

    # 补全缺失值
    df['EURUSD'].fillna(method='ffill', inplace=True)


def add_gbpusd(inp_file):
    """
    将GBPUSD收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_gbpusd = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_gbpusd.index = pd.to_datetime(df_gbpusd.index)
    df_gbpusd = pd.Series(df_gbpusd['close'], name='GBPUSD')

    df = df.join(df_gbpusd)

    # 补全缺失值
    df['GBPUSD'].fillna(method='ffill', inplace=True)


def add_xauusd(inp_file):
    """
    将XAUUSD收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_xauusd = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_xauusd.index = pd.to_datetime(df_xauusd.index)
    df_xauusd = pd.Series(df_xauusd['close'], name='XAUUSD')

    df = df.join(df_xauusd)

    # 补全缺失值
    df['XAUUSD'].fillna(method='ffill', inplace=True)


def add_xagusd(inp_file):
    """
    将XAGUSD收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_xagusd = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_xagusd.index = pd.to_datetime(df_xagusd.index)
    df_xagusd = pd.Series(df_xagusd['close'], name='XAGUSD')

    df = df.join(df_xagusd)

    # 补全缺失值
    df['XAGUSD'].fillna(method='ffill', inplace=True)


def add_bulkstock(inp_file):
    """
    将中国大宗商品BulkStock收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_bulkstock = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_bulkstock.index = pd.to_datetime(df_bulkstock.index)
    df_bulkstock = pd.Series(df_bulkstock['close'], name='BulkStock')

    df = df.join(df_bulkstock)

    # 补全缺失值
    df['BulkStock'].fillna(method='ffill', inplace=True)


def add_industrialproducts(inp_file):
    """
    将中国工业品IndustrialProducts收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_industrialproducts = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_industrialproducts.index = pd.to_datetime(df_industrialproducts.index)
    df_industrialproducts = pd.Series(df_industrialproducts['close'], name='IndustrialProducts')

    df = df.join(df_industrialproducts)

    # 补全缺失值
    df['IndustrialProducts'].fillna(method='ffill', inplace=True)


def add_sp500(inp_file):
    """
    将标准普尔SP500指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_sp500 = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_sp500.index = pd.to_datetime(df_sp500.index)
    df_sp500 = pd.Series(df_sp500['close'], name='SP500')

    df = df.join(df_sp500)

    # 补全缺失值
    df['SP500'].fillna(method='ffill', inplace=True)


def add_dji(inp_file):
    """
    将道琼斯DJI指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_dji = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_dji.index = pd.to_datetime(df_dji.index)
    df_dji = pd.Series(df_dji['close'], name='DJI')

    df = df.join(df_dji)

    # 补全缺失值
    df['DJI'].fillna(method='ffill', inplace=True)


def add_ixic(inp_file):
    """
    将纳斯达克IXIC指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_ixic = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_ixic.index = pd.to_datetime(df_ixic.index)
    df_ixic = pd.Series(df_ixic['close'], name='IXIC')

    df = df.join(df_ixic)

    # 补全缺失值
    df['IXIC'].fillna(method='ffill', inplace=True)


def add_gdaxi(inp_file):
    """
    将德国DAX指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_gdaxi = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_gdaxi.index = pd.to_datetime(df_gdaxi.index)
    df_gdaxi = pd.Series(df_gdaxi['close'], name='GDAXI')

    df = df.join(df_gdaxi)

    # 补全缺失值
    df['GDAXI'].fillna(method='ffill', inplace=True)


def add_ftse(inp_file):
    """
    将英国富时FTSE指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_fise = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_fise.index = pd.to_datetime(df_fise.index)
    df_fise = pd.Series(df_fise['close'], name='FTSE')

    df = df.join(df_fise)

    # 补全缺失值
    df['FTSE'].fillna(method='ffill', inplace=True)


def add_fchi(inp_file):
    """
    将法国CAC指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_fchi = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_fchi.index = pd.to_datetime(df_fchi.index)
    df_fchi = pd.Series(df_fchi['close'], name='FCHI')

    df = df.join(df_fchi)

    # 补全缺失值
    df['FCHI'].fillna(method='ffill', inplace=True)


def add_n225(inp_file):
    """
    将日经指数N225指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_n225 = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_n225.index = pd.to_datetime(df_n225.index)
    df_n225 = pd.Series(df_n225['close'], name='N225')

    df = df.join(df_n225)

    # 补全缺失值
    df['N225'].fillna(method='ffill', inplace=True)


def add_hsi(inp_file):
    """
    将恒生HSI指数收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_hsi = pd.read_csv(inp_file, index_col='trade_date')
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_hsi.index = pd.to_datetime(df_hsi.index)
    df_hsi = pd.Series(df_hsi['close'], name='HSI')

    df = df.join(df_hsi)

    # 补全缺失值
    df['HSI'].fillna(method='ffill', inplace=True)


def BBANDS(inp_ndays):
    """
    计算布林通道指标
    """
    global df

    MA = df['close'].rolling(inp_ndays).mean()
    SD = df['close'].rolling(inp_ndays).std()

    upper_BB = MA + 2 * SD
    upper_BB = pd.Series(upper_BB, name='Upper_BollingerBand')
    df = df.join(upper_BB)

    lower_BB = MA - 2 * SD
    lower_BB = pd.Series(lower_BB, name='Lower_BollingerBand')

    df = df.join(lower_BB)


def CCI(inp_ndays):
    """
    计算CCI指标
    """
    global df

    typical_price = (df['close'] + df['high'] + df['low']) / 3
    CCI = pd.Series((typical_price - typical_price.rolling(inp_ndays).mean())
                    / (0.015 * typical_price.rolling(inp_ndays).std()), name='CCI')

    df = df.join(CCI)


def EMV(inp_ndays):
    """
    计算EMV指标
    """
    global df

    dm = ((df['high'] + df['low']) / 2) - \
         ((df['high'].shift(1) + df['low'].shift(1)) / 2)
    br = (df['vol'] / 100000000) / (df['high'] - df['low'])
    EMV = dm / br
    EMV_MA = pd.Series(EMV.rolling(inp_ndays).mean(), name='EMV')

    df = df.join(EMV_MA)


def ROC(inp_ndays):
    """
    计算ROC——波动率指标
    """
    global df

    N = df['close'].diff(inp_ndays)
    D = df['close'].shift(inp_ndays)

    ROC = pd.Series(N/D, name='ROC')

    df = df.join(ROC)


def ForceIndex(inp_ndays):
    """
    计算ForceIndex——强力指数指标
    """
    global df

    FI = pd.Series(df['close'].diff(inp_ndays) * df['vol'], name='ForceIndex')

    df = df.join(FI)


def KDJ(inp_N, inp_M1, inp_M2):
    """
    计算KDJ——随机指标
    """
    global df

    close = df.close
    high = df.high
    low = df.low
    date = df.index.to_series()
    ndate = len(date)
    periodHigh = pd.Series(np.zeros(ndate-(inp_N-1)),
                           index=date.index[(inp_N-1):], name='periodHigh')
    periodLow = pd.Series(np.zeros(ndate-(inp_N-1)),
                          index=date.index[(inp_N-1):], name='periodLow')
    RSV = pd.Series(np.zeros(ndate-(inp_N-1)),
                    index=date.index[(inp_N-1):], name='RSV')

    for i in range(inp_N-1, ndate):
        period = date[i-(inp_N-1):i+1]
        j = date[i]
        periodHigh[j] = high[period].max()
        periodLow[j] = low[period].min()
        RSV[j] = 100 * (close[j] - periodLow[j]) / (periodHigh[j] - periodLow[j])

    KValue = pd.Series(0.0, index=RSV.index, name='KValue')
    KValue[0] = 50
    for i in range(1, len(RSV)):
        KValue[i] = (inp_M1 - 1) / inp_M1 * KValue[i-1] + RSV[i] / inp_M1

    DValue = pd.Series(0.0, index=RSV.index, name='DValue')
    DValue[0] = 50
    for i in range(1, len(RSV)):
        DValue[i] = (inp_M2 - 1) / inp_M2 * DValue[i-1] + KValue[i] / inp_M2

    JValue = 3 * KValue - 2 * DValue
    JValue.name = 'JValue'

    df = df.join(KValue)
    df = df.join(DValue)
    df = df.join(JValue)


def SMA(inp_ndays):
    """
    计算SMA——简单移动平均线指标
    """
    global df

    ma_name = 'SMA_' + str(inp_ndays)
    SMA = pd.Series(df['close'].rolling(inp_ndays).mean(), name=ma_name)

    df = df.join(SMA)


def EMA(inp_ndays):
    """
    计算EMA——指数移动平均线指标
    """
    global df

    ma_name = 'EMA_' + str(inp_ndays)
    EMA = pd.Series(df['close'].ewm(inp_ndays).mean(), name=ma_name)

    df = df.join(EMA)


def RSI(inp_days):
    """
    计算RSI——相对强弱指标
    """
    global df

    date = df.index.to_series()
    ndate = len(date)
    RSI = pd.Series(np.zeros(ndate-inp_days),
                    index=date.index[inp_days:], name='RSI')

    for i in range(inp_days, ndate):
        A = 0
        B = 0
        for j in range(0, inp_days):
            if df['amt_change'][date[i-j]] > 0:
                A += df['amt_change'][date[i-j]]
            else:
                B += df['amt_change'][date[i-j]]

        RSI[date[i]] = A / (A - B) * 100

    df = df.join(RSI)


def OBV():
    """
    计算OBV——能量潮指标
    """
    global df

    date = df.index.to_series()
    ndate = len(date)
    OBV = pd.Series(np.zeros(ndate),
                    index=date.index, name='OBV')

    OBV[date[0]] = df['vol'][date[0]] / 100000000
    for i in range(1, ndate):
        if df['close'][date[i]] > df['close'][date[i-1]]:
            OBV[date[i]] = (OBV[date[i-1]] + df['vol'][date[i]]) / 100000000
        else:
            OBV[date[i]] = (OBV[date[i-1]] - df['vol'][date[i]]) / 100000000

    df = df.join(OBV)


def _TARGET(x):
    """
    按照涨跌幅大小进行涨跌幅度的分级
    if x > 1.8:
        return 'A'
    elif x > 0.3 and x <= 1.8:
        return 'B'
    elif x > -0.3 and x <= 0.3:
        return 'C'
    elif x > -1.46 and x <= -0.3:
        return 'D'
    elif x < -1.46:
        return 'E'
    else:
        return np.nan
    """
    if x >= 0.03:
        return 1
    elif x < 0.03:
        return -1
    else:
        return np.nan


def next_pctchange(inp_ndays):
    """
    统计之后N个交易日的涨跌幅指标
    """
    global df

    # 当天涨跌点数
    AMT_CHANGE = pd.Series(df['close'] - df['close'].shift(1),
                           name='amt_change')
    df = df.join(AMT_CHANGE)

    # 当天涨跌幅(%)
    PCT_CHANGE = pd.Series(100 * (df['close']-df['close'].shift(1))
                           / df['close'].shift(1), name='pct_change')
    df = df.join(PCT_CHANGE)

    # 第二天的涨跌幅度(%)
    NEXT = pd.Series(df['pct_change'].shift(-inp_ndays), name='next_pctchange')
    df = df.join(NEXT)

    # 要预测的价格目标（第二天的收盘价）
    PRICE_TARGET = pd.Series(df['close'].shift(-1), name='price_target')
    df = df.join(PRICE_TARGET)

    # 要预测的第二天的涨跌
    TARGET = pd.Series(df['next_pctchange'], name='target')
    TARGET = TARGET.apply(_TARGET)
    df = df.join(TARGET)

    # 当天的收盘价
    CLOSE_SELF = pd.Series(df['close'], name='close_self')
    df = df.join(CLOSE_SELF)


def DATA_NORMAL():
    """
    数据归一化处理
    """
    global df

    cols = pd.Series.tolist(df.columns)
    # 排除特征数据中不需要进行归一化处理的列
    exclude_cols = ['open', 'high', 'low', 'close', 'vol', 'amt_change',
                    'pct_change', 'next_pctchange', 'price_target', 'target']
    for col in exclude_cols:
        cols.remove(col)

    # 数据归一化处理
    for col in cols:
        df[col] = df[[col]].apply(lambda x :
                                  (x - np.min(x)) / (np.max(x) - np.min(x)))


if __name__ == "__main__":
    global df
    # 读取沪深300股票指数的价格数据
    get_stock_index_data(source_file)

    # 生成目标数据，即预测今后N天的涨跌，按照涨跌幅大小进行涨跌幅度的分级
    next_pctchange(1)

    # 添加国际金融市场的价格数据
    add_usdx(usdx_file)
    add_usdcny(usdcny_file)
    add_usdjpy(usdjpy_file)
    add_audusd(audusd_file)
    add_eurusd(eurusd_file)
    add_gbpusd(gbpusd_file)
    add_xauusd(xauusd_file)
    add_xagusd(xagusd_file)
    add_bulkstock(bulkstock_file)
    add_industrialproducts(industrialproducts_file)
    add_sp500(sp500_file)
    add_dji(dji_file)
    add_ixic(ixic_file)
    add_gdaxi(gdaxi_file)
    add_ftse(ftse_file)
    add_fchi(fchi_file)
    add_n225(n255_file)
    add_hsi(hsi_file)

    # 添加技术分析指标特征数据
    SMA(5)
    SMA(20)
    SMA(50)
    EMA(200)
    BBANDS(20)
    CCI(20)
    EMV(14)
    ForceIndex(1)
    ROC(5)
    KDJ(9, 3, 3)
    RSI(6)
    OBV()

    # 数据归一化处理
    DATA_NORMAL()

    # 删除空值行
    df.dropna(inplace=True)
    df['target'] = df['target'].astype(int)

    try:
        df.to_csv(target_file)
        print('\n新的特征数据文件 %s 已经生成！' % target_file)
    except Exception as err:
        print('\n新的特征数据文件存储时出现问题：%s' % str(err))
