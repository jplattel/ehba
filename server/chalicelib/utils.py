def _read_file(file):
    # TODO: support OV-Chipkaart exports (no check-in time in the same row... ugh)
    if file.name.endswith('.csv'):
        df = pd.read_csv(file.name)
        # Rename columns to match calculations
        df.rename(columns={
            'Datum': 'datum',
            'Check-in': 'check_in',
            'Check-uit': 'check_out',
            'Vertrek': 'place_from',
            'Bestemming': 'place_to',
            'Prijs (incl. btw)': 'bedrag',
        }, inplace=True) # rename inplace (save memory)
        
    # If excel, then its from NS, which offers better export
    if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
        df = pd.read_excel(file.name)

        # Rename columns to match calculations
        df.rename(columns={
            'Datum': 'datum',
            'Check in': 'check_in',
            'Check uit': 'check_out',
            'Vertrek': 'place_from',
            'Bestemming': 'place_to',
            'Prijs (incl. btw)': 'bedrag',
        }, inplace=True) # rename inplace (save memory)

        # Drop all other columns
        df.reindex(['datum', 'check_in', 'check_out', 'place_from', 'place_to', 'bedrag'], axis=1)
        return df

def _files_to_dataframe(files):
    return pd.concat(list(map(lambda file: _read_file(file), files)))