import pandas as pd
import datetime

def _read_dict(data):
    # Get data and transform into dataframe
    df = pd.DataFrame.from_dict(data.get('data'))
    
    # Drop the last row (empty from blank line from CSV parser)
    df = df[:-1]

    # We are dealing with NS Zakelijk
    if 'Prijs (excl. btw)' in data.get('meta').get('fields'):
        
        # Rename columns to match calculations
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

    # We are dealing with NS (persoonlijk)
    elif 'Check in' in data.get('meta').get('fields'):
        
        # Only select train rides
        df = df[df['Transactie'] == 'Reis']
    
        df.rename(columns={
            'Datum': 'datum',
            'Check in': 'check_in',
            'Check uit': 'check_out',
            'Vertrek': 'place_from',
            'Bestemming': 'place_to',
            'Af': 'bedrag',
            'Product': 'product',
        }, inplace=True) # rename inplace (save memory)

        # Convert monetary value
        df['bedrag'] = df['bedrag'].str.replace('€', '')
        df['bedrag'] = pd.to_numeric(df['bedrag'].str.replace(',', '.'))

        # Convert date
        df['datum'] = pd.to_datetime(df['datum'], format='%d-%m-%Y')

    # We are dealing with OV-Chipkaart export
    else:
        # Drop automatisch opladen 
        df = df[df['Transactie'] != 'Saldo automatisch opgeladen']

        # Drop product op kaart geladen
        df = df[df['Transactie'] != 'Product op kaart geladen']

        # Rename columns to match calculations
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
        
        # Get the index of the shifted rows (should now have an empty checkin & checkout)
        shifted_rows = df[(df['check_in'] == pd.np.nan) & (df['check_out'] == pd.np.nan)].index

        # Drop the actual shifted rows
        df = df.drop(shifted_rows)
        df = df.drop(df[df['place_to'] == ""].index) # And drop where we dont have a matching place to...

        # Convert monetary value
        df['bedrag'] = pd.to_numeric(df['bedrag'].str.replace(',', '.'))

        # Convert date
        df['datum'] = pd.to_datetime(df['datum'], format='%d-%m-%Y')

    # Reindex
    df = df.reindex(['datum', 'check_in', 'check_out', 'place_from', 'place_to', 'bedrag', 'product'], axis=1)
    df = df.replace({pd.np.nan: None})
    
    return df


def parsed_json_files_to_dataframe(files):
    if len(files) == 0:
        return [], {}

    data = pd.concat(list(map(lambda data: _read_dict(data), files)), sort=True)
    data = parse_times(data)
    data = data.reset_index(drop=True)
    results = get_results(data)
    data['datum'] = data['datum'].astype(str) # Convert date object back to str
    return data, results

def check_weekday_reduction_time(check_in):
    try:
        # Parse time if possible
        time = datetime.time.fromisoformat(check_in)
        
        # Before 6:30
        if time < datetime.time(hour=6, minute=30):
            return True
        # Between 9:00 and 16:30
        elif time > datetime.time(hour=9) and time < datetime.time(hour=16, minute=30):
            return True
        # Evening after 18:30
        elif time > datetime.time(hour=18, minute=30):
            return True
        else: 
            return False
    except:
        return False

def parse_times(df):
    print(df.dtypes)
    df['reduction_weekend'] = df['datum'].dt.day_name().isin(["Saturday", "Sunday"]) # Weekend
    df['reduction_hours'] = df['check_in'].apply(check_weekday_reduction_time)
    df['reduction'] = df['reduction_weekend'] | df['reduction_hours']
    return df

def get_results(df):
    
    # Sort by year
    years = df.groupby(df['datum'].dt.strftime('%Y'))['bedrag'].agg({'sum', 'count'}).fillna(0)

    # Sort by months of the year
    months = df.groupby(df['datum'].dt.strftime('%Y %m'))['bedrag'].agg({'sum', 'count'}).fillna(0)

    # Sort by weekday
    weekdays_catagories = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays = df.groupby(df['datum'].dt.strftime('%A'))['bedrag'].agg({'sum', 'count'}).reindex(weekdays_catagories).fillna(0)

    # Filter reduction
    reduction_df = df[df['reduction'] == True]
    reduction_months = reduction_df.groupby(reduction_df['datum'].dt.strftime('%Y %m'))['bedrag'].agg({'sum', 'count'}).fillna(0)
    reduction_years = reduction_df.groupby(reduction_df['datum'].dt.strftime('%Y'))['bedrag'].agg({'sum', 'count'}).fillna(0)

    # Filter for weekends
    weekend_df = df[df['reduction_weekend'] == True]
    weekend_months = weekend_df.groupby(weekend_df['datum'].dt.strftime('%Y %m'))['bedrag'].agg({'sum', 'count'}).fillna(0)
    weekend_years = weekend_df.groupby(weekend_df['datum'].dt.strftime('%Y'))['bedrag'].agg({'sum', 'count'}).fillna(0)

    return {
        'months': months.to_dict(orient='index'),
        'years': years.to_dict(orient='index'),
        'weekdays': weekdays.to_dict(orient='index'),
        'reduction': {
            'months': reduction_months.to_dict(orient='index'),
            'years': reduction_years.to_dict(orient='index')
        },
        'weekend': {
            'months': weekend_months.to_dict(orient='index'),
            'years': weekend_years.to_dict(orient='index')
        },
        'totals': {
            'total': {
                'count': df.shape[0],
                'sum': int(df['bedrag'].sum())
            },
            'reduction': {
                'count': reduction_df.shape[0],
                'sum': int(reduction_df['bedrag'].sum())
            },
            'weekend': {
                'count': weekend_df.shape[0],
                'sum': int(weekend_df['bedrag'].sum())
            }
        },
    }