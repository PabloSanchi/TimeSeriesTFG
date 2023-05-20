import pandas as pd
import numpy as np
import schedule
from FirebaseController import update_weather
from DataGenerator import find_closest_row


def load_data(filename, colums):
    global df
    df = pd.read_csv(filename, colums)


def init_weather():
    global df
    return df.sample()


def get_next_value():
    global ws, wd, prev_values, ASC
    print('----------------------------------------')

    data = find_closest_row(df.copy(), ws, wd, prev_values, ASC)

    if data is None:
        print('\n\n>> Change wind tendency <<', end='\n\n\n')
        ASC = not ASC
        data = find_closest_row(df, ws, wd, prev_values, ASC)

    if data is None:
        print('All rows have been repeated')
        return

    # Get the wind speed and direction values from the selected row
    ws = data['wind_speed'].values[0]
    wd = data['wind_direction_true'].values[0]
    wh = data['wave_height'].values[0]
    sh = data['swell_height'].values[0]
    sd = data['swell_direction'].values[0]

    # Add the index and values to prev_values
    prev_values.append((ws, wd))

    # If prev_values has more than 100k elements, remove the oldest one
    if len(prev_values) > 100_000:
        prev_values.pop(0)

    print('Current Wind speed: ', ws)
    print('Current Wind direction: ', wd)

    if np.random.choice([True, False], p=[0.2, 0.8]):
        ASC = not ASC
        _dir = 'UPWARDS' if ASC else 'DOWNWARDS'
        print(f'>> Wind tendency changed ({_dir}) <<')

    # update weather Firebase real time database
    update_weather({
        'wind_direction': wd,  # Local->wind_direction
        'wind_speed': ws,  # Local->wind_speed
        'wave_height': wh,  # Local->scale
        'swell_height': sh,  # Swell->scale
        'swell_direction': sd,  # Swell->wind_direction
    })


if __name__ == '__main__':
    filename = 'Data/synthetic_data.csv'
    df = pd.read_csv(filename)

    row = init_weather()

    # Get the wind speed and direction values from the row
    ws = row['wind_speed'].values[0]
    wd = row['wind_direction_true'].values[0]

    print('Starting Wind speed: ', ws)
    print('Starting Wind direction: ', wd)

    prev_values = [(ws, wd)]  # add the index to prev_values
    ASC = True

    schedule.every(2).seconds.do(get_next_value)

    while True:
        schedule.run_pending()
