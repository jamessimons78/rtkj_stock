import os
import pandas as pd


# 数据文件路径设置
file_path = os.getcwd() + '\\data\\'
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
        df = pd.read_csv(inp_file)
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df.set_index('trade_date', inplace=True)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))


def add_usdx(inp_file):
    """
    将美元指数USDX收盘价加到沪深300指数价格数据中
    """
    global df

    try:
        df_usdx = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdx['trade_date'] = pd.to_datetime(df_usdx['trade_date'])
    df_usdx.set_index('trade_date', inplace=True)
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
        df_usdcny = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdcny['trade_date'] = pd.to_datetime(df_usdcny['trade_date'])
    df_usdcny.set_index('trade_date', inplace=True)
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
        df_usdjpy = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_usdjpy['trade_date'] = pd.to_datetime(df_usdjpy['trade_date'])
    df_usdjpy.set_index('trade_date', inplace=True)
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
        df_audusd = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_audusd['trade_date'] = pd.to_datetime(df_audusd['trade_date'])
    df_audusd.set_index('trade_date', inplace=True)
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
        df_eurusd = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_eurusd['trade_date'] = pd.to_datetime(df_eurusd['trade_date'])
    df_eurusd.set_index('trade_date', inplace=True)
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
        df_gbpusd = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_gbpusd['trade_date'] = pd.to_datetime(df_gbpusd['trade_date'])
    df_gbpusd.set_index('trade_date', inplace=True)
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
        df_xauusd = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_xauusd['trade_date'] = pd.to_datetime(df_xauusd['trade_date'])
    df_xauusd.set_index('trade_date', inplace=True)
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
        df_xagusd = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_xagusd['trade_date'] = pd.to_datetime(df_xagusd['trade_date'])
    df_xagusd.set_index('trade_date', inplace=True)
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
        df_bulkstock = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_bulkstock['trade_date'] = pd.to_datetime(df_bulkstock['trade_date'])
    df_bulkstock.set_index('trade_date', inplace=True)
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
        df_industrialproducts = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_industrialproducts['trade_date'] = pd.to_datetime(df_industrialproducts['trade_date'])
    df_industrialproducts.set_index('trade_date', inplace=True)
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
        df_sp500 = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_sp500['trade_date'] = pd.to_datetime(df_sp500['trade_date'])
    df_sp500.set_index('trade_date', inplace=True)
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
        df_dji = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_dji['trade_date'] = pd.to_datetime(df_dji['trade_date'])
    df_dji.set_index('trade_date', inplace=True)
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
        df_ixic = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_ixic['trade_date'] = pd.to_datetime(df_ixic['trade_date'])
    df_ixic.set_index('trade_date', inplace=True)
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
        df_gdaxi = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_gdaxi['trade_date'] = pd.to_datetime(df_gdaxi['trade_date'])
    df_gdaxi.set_index('trade_date', inplace=True)
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
        df_fise = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_fise['trade_date'] = pd.to_datetime(df_fise['trade_date'])
    df_fise.set_index('trade_date', inplace=True)
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
        df_fchi = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_fchi['trade_date'] = pd.to_datetime(df_fchi['trade_date'])
    df_fchi.set_index('trade_date', inplace=True)
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
        df_n225 = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_n225['trade_date'] = pd.to_datetime(df_n225['trade_date'])
    df_n225.set_index('trade_date', inplace=True)
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
        df_hsi = pd.read_csv(inp_file)
        print('\n基础数据文件 %s 已经读取！' % inp_file)
    except Exception as err:
        print('\n读取文件时出现问题：%s' % str(err))

    df_hsi['trade_date'] = pd.to_datetime(df_hsi['trade_date'])
    df_hsi.set_index('trade_date', inplace=True)
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


def EVM(inp_ndays):
    """
    计算EVM指标
    """
    global df

    dm = ((df['high'] + df['low']) / 2) - \
         ((df['high'].shift(1) + df['low'].shift(1)) / 2)
    br = (df['vol'] / 100000000) / (df['high'] - df['low'])
    EVM = dm / br
    EVM_MA = pd.Series(EVM.rolling(inp_ndays).mean(), name='EVM')

    df = df.join(EVM_MA)


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


if __name__ == "__main__":
    global df
    # 读取沪深300股票指数的价格数据
    get_stock_index_data(source_file)

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
    BBANDS(20)
    CCI(20)
    EVM(14)
    ForceIndex(1)
    ROC(5)


    # 删除空值行
    # df = df.dropna()

    try:
        df.to_csv(target_file)
        print('\n新的特征数据文件 %s 已经生成！' % target_file)
    except Exception as err:
        print('\n新的特征数据文件存储时出现问题：%s' % str(err))

