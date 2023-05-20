import numpy as np

delta = 0.2


def find_closest_row(df, ws, wd, prev_values, ASC):
    # calculate distances
    df['distance'] = np.sqrt((df['wind_speed']-ws) **
                             2 + (df['wind_direction_true']-wd)**2)

    # sort dataframe by distance
    df = df.sort_values(by=['distance'])

    # filter rows with prev_values
    for prev_ws, prev_wd in prev_values:
        df = df[(df['wind_speed'] != prev_ws) | (
            df['wind_direction_true'] != prev_wd)]

    # check if dataframe is empty
    if df.empty:
        return None

    # select the first row with the correct tendency
    if ASC:
        mask = df['wind_speed'] > ws + delta
    else:
        mask = df['wind_speed'] < (ws - delta if ws - delta > 0 else 0)

    # select the first row that matches the tendency
    df = df[mask].head(1)
    if df.empty:
        return None

    # return the wind speed and wind direction values
    # df['wind_speed'].values[0], df['wind_direction_true'].values[0]
    return df
