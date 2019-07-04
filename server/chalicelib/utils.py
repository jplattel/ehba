import pandas as pd

def _read_dict(data):
    # TODO: support OV-Chipkaart exports (no check-in time in the same row... ugh)
    # if file.name.endswith('.csv'):
    
    df = pd.DataFrame.from_dict(data.get('data'))
    print(df.dtypes)
    # print(data.get('meta'))

    # We are dealign with NS Zakelijke
    if 'Prijs (excl. btw)' in data.get('meta').get('fields'):
    #     # Rename columns to match calculations
        df.rename(columns={
            'Datum': 'datum',
            'Check in': 'check_in',
            'Check uit': 'check_out',
            'Vertrek': 'place_from',
            'Bestemming': 'place_to',
            'Prijs (excl. btw)': 'bedrag',
            'Product': 'product',
        }, inplace=True) # rename inplace (save memory)
        
        # Filter only on train rides
        df = df[df['product'] == 'Treinreizen']
        df['bedrag'] = pd.to_numeric(df['bedrag'].str.replace('€ ', ''))

    # We are dealing with OV-Chipkaart export
    else:
        df.rename(columns={
            'Datum': 'datum',
            'Check-in': 'check_in',
            'Check-uit': 'check_out',
            'Vertrek': 'place_from',
            'Bestemming': 'place_to',
            'Bedrag': 'bedrag',
            'Product': 'product',
        }, inplace=True) # rename inplace (save memory)
        df['bedrag'] = df['bedrag'].str.replace(',', '.')
        df['bedrag'] = pd.to_numeric(df['bedrag'])

    # Drop the last row (empty from blank line from CSV parser)
    df = df[:-1]

    # Reindex
    df = df.reindex(['datum', 'check_in', 'check_out', 'place_from', 'place_to', 'bedrag', 'product'], axis=1)
    df = df.replace({pd.np.nan: None}) 
    
    # df['bedrag'] = df['bedrag'].astype(float)
    
    # df = df.dropna() # Drop empty rows
    return df

def parsed_json_files_to_dataframe(files):
    data = pd.concat(list(map(lambda data: _read_dict(data), files)), sort=True)
    data = data.reset_index(drop=True)

    results = get_results(data)
    return data, results

def get_results(df):
    return {
        'totals': {
            'count': df.shape[0],
            'sum': int(df['bedrag'].sum())
        },
        'months': [

        ],
        'years': [

        ],
    }