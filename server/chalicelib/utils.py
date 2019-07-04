import pandas as pd

def _read_dict(data):
    # TODO: support OV-Chipkaart exports (no check-in time in the same row... ugh)
    # if file.name.endswith('.csv'):
    
    df = pd.DataFrame.from_dict(data.get('data'))
    # print(df.dtypes)
    # print(data.get('meta'))

    # Drop the last row (empty from blank line from CSV parser)
    df = df[:-1]

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

        # Parse date
        df['datum'] = pd.to_datetime(df['datum'], format='%d-%m-%y')

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
        # Shift check once, align it with checkout
        df['check_in'] = df['check_in'].shift(1)

        # Convert monetary value
        df['bedrag'] = pd.to_numeric(df['bedrag'].str.replace(',', '.'))

        # Convert date
        df['datum'] = pd.to_datetime(df['datum'], format='%d-%m-%Y')

    
    # Reformat dates
    

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
    data['datum'] = data['datum'].astype(str) # Convert date object back to str
    return data, results

def get_results(df):

    months = df.groupby(df['datum'].dt.strftime('%Y %m'))['bedrag'].agg({'sum', 'count'})
    years = df.groupby(df['datum'].dt.strftime('%Y'))['bedrag'].agg({'sum', 'count'})

    # Sort by weekday
    weekdays_catagories = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays = df.groupby(df['datum'].dt.strftime('%A'))['bedrag'].agg({'sum', 'count'}).reindex(weekdays_catagories)

    return {
        'months': months.to_dict(orient='index'),
        'years': years.to_dict(orient='index'),
        'weekdays': weekdays.to_dict(orient='index'),
        'totals': {
            'total': {
                'count': df.shape[0],
                'sum': int(df['bedrag'].sum())
            }
        },
    }