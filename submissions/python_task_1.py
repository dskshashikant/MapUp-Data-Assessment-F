import pandas as pd


def generate_car_matrix(df) -> pd.DataFrame:
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    matrix.values[[range(len(matrix))]*2] = 0 
    return matrix

def get_type_count(df) -> dict:
    bins = [-float('inf'), 15, 25, float('inf')]
    labels = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=bins, labels=labels)
    count_dict = df['car_type'].value_counts().to_dict()
    count_dict = {k: count_dict.get(k, 0) for k in labels}
    count_dict = dict(sorted(count_dict.items()))
    return count_dict   

def get_bus_indexes(df) -> list:
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)

def filter_routes(df) -> list:
    routes_above_7 = df.groupby('route')['truck'].mean() > 7
    return sorted(routes_above_7[routes_above_7].index.tolist())

def multiply_matrix(matrix) -> pd.DataFrame:
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    return modified_matrix.round(1)

def time_check(df) -> pd.Series:
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['time_difference'] = df['end_timestamp'] - df['start_timestamp']
    day_duration = pd.Timedelta(days=1)

    def check_time(row):
        return (row['time_difference'] == day_duration and
                row['start_timestamp'].dayofweek == 0 and
                row['end_timestamp'].dayofweek == 6)

    result_series = df.apply(check_time, axis=1)
    result_series.index = pd.MultiIndex.from_arrays([df['id'], df['id_2']])
    return result_series




