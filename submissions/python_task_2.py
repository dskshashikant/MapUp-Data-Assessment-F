import pandas as pd

def calculate_distance_matrix(df):
    required_columns = ['ID', 'Latitude', 'Longitude']
    if not set(required_columns).issubset(df.columns):
        raise ValueError(f"Input DataFrame must have columns: {required_columns}")

    coordinates = df[['Latitude', 'Longitude']]

    distances = pdist(coordinates, metric='euclidean')

    distance_matrix = squareform(distances)

    result_df = pd.DataFrame(distance_matrix, index=df['ID'], columns=df['ID'])

    result_df.values[(result_df.index, result_df.columns)] = 0

    return result_df
result_dataframe = calculate_distance_matrix(df)
print(result_dataframe)


def unroll_distance_matrix(df):
    required_columns = df.columns.tolist()
    if 'ID' not in required_columns:
        raise ValueError("Input DataFrame must have 'ID' column")

    stacked_distance = df.stack()

    unrolled_df = stacked_distance.reset_index()

    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df
result_unrolled = unroll_distance_matrix(result_dataframe)
print(result_unrolled)


def find_ids_within_ten_percentage_threshold(df, reference_id):
    reference_rows = df[df['id_start'] == reference_id]

    reference_avg_distance = reference_rows['distance'].mean()

    percentage_threshold = 0.10

    lower_bound = reference_avg_distance - (reference_avg_distance * percentage_threshold)
    upper_bound = reference_avg_distance + (reference_avg_distance * percentage_threshold)

    result_df = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    return result_df
reference_id = 1  # Replace with the desired reference ID
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled, reference_id)
print(result_within_threshold)


def calculate_toll_rate(df):
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate in rate_coefficients.items():
        column_name = f'{vehicle_type}_rate'
        df[column_name] = df['distance'] * rate

    return df
result_with_toll_rates = calculate_toll_rate(result_within_threshold)
print(result_with_toll_rates)


    


def calculate_time_based_toll_rates(df):
    time_ranges = [
        {'start': datetime.time(0, 0, 0), 'end': datetime.time(10, 0, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start': datetime.time(10, 0, 0), 'end': datetime.time(18, 0, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start': datetime.time(18, 0, 0), 'end': datetime.time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    df['start_day'] = df['end_day'] = df['start_time'] = df['end_time'] = ''

    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time

    for time_range in time_ranges:
        weekday_mask = (df['start_time'] >= time_range['start']) & (df['end_time'] <= time_range['end']) & (df['start_day'] < 'Saturday')
        weekend_mask = (df['start_time'] >= time_range['start']) & (df['end_time'] <= time_range['end']) & (df['start_day'] >= 'Saturday')

        for vehicle_type in ['moto_rate', 'car_rate', 'rv_rate', 'bus_rate', 'truck_rate']:
            df[vehicle_type] *= time_range['weekday_factor']
            df.loc[weekend_mask, vehicle_type] *= time_range['weekend_factor']

    return df
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_based_toll_rates)