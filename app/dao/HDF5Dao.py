import pandas


def save(path, key, df, data_format='table', data_columns=True):
    df.to_hdf(path, key, table=True)
    # hdf = HDFStore(path)
    # hdf.put(key, df, data_format, data_columns)
    return True


def get(path, key):
    return pandas.read_hdf(path, key)
