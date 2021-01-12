import pandas as pd
import configparser


def get_mapBoxToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['mapbox']['secret_token']


def get_mapbox():
    return {
        'accesstoken': get_mapBoxToken(),
        'center': {"lat": 37.86, "lon": -98.00},
        'zoom': 4.0,
        'style': 'light',
    }


def get_sliders(months):
    return [{
        'transition': {'duration': 0},
        'x': 0.08,
        'len': 0.88,
        'currentvalue': {'font': {'size': 15}, 'prefix': '📅 ', 'visible': True, 'xanchor': 'center'},
        'steps': [
            {
                'label': str(pd.to_datetime(month, format='%Y-%m-%d').month_name()),
                'method': 'animate',
                'args': [
                    ['frame_{}'.format(month)],
                    {'mode': 'immediate', 'frame': {'duration': 1500,
                                                    'redraw': True}, 'transition': {'duration': 50}}
                ],
            } for month in months]
    }]


play_button = {
    'type': 'buttons',
    'showactive': True,
    'x': 0.045, 'y': -0.08,
    'buttons': [{
            'label': '▶',
            'method': 'animate',
            'args': [
                None,
                {
                    'frame': {'duration': 1500, 'redraw': True},
                    'transition': {'duration': 50},
                    'fromcurrent': True,
                    'mode': 'immediate',
                }
            ]
    }]
}
