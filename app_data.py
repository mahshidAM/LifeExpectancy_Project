""" Dashboard data prepration"""
import pandas as pd
import numpy as np
import json

conv_dict = {
    'Bahamas': 'Bahamas, The',
    'Brunei': 'Brunei Darussalam',
    'Bosnia and Herz.': 'Bosnia and Herzegovina',
    'Central African Rep.': 'Central African Republic',
    'Congo': 'Congo, Dem. Rep.',
    "Côte d'Ivoire": "Cote d'Ivoire",
    'Czech Rep.':  'Czech Republic',
    'N. Cyprus': 'Cyprus',
    'Dem. Rep. Congo': 'Congo (Brazzaville)',
    'Dominican Rep.':'Dominican Republic',
    'Eq. Guinea':'Equatorial Guinea',
    'Egypt': 'Egypt, Arab Rep.',
    'Gambia': 'Gambia, The',
    'Guinea': 'Papua New Guinea',
    'Iran': 'Iran, Islamic Rep.',
    'Korea': 'Korea, Rep.',
    'Kyrgyzstan': 'Kyrgyz Republic', 
    'Dem. Rep. Korea': 'Korea, Dem. People’s Rep.',
    'Lao PDR':'Lao PDR',
    'Macedonia': 'North Macedonia',
    'Myanmar':'Myanmar',
    'Russia': 'Russian Federation',
    'S. Sudan':'South Sudan',
    'Slovakia': 'Slovak Republic',
    'Solomon Is.': 'Solomon Islands',
    'Syria': 'Syrian Arab Republic',
    'Somaliland':'Somalia',
    'Taiwan':'Taiwan*',
    'Venezuela':'Venezuela, RB', 
    'Yemen': 'Yemen, Rep.'
}

def get_DataFrame():
    """
    Returns cleaned dataframe     
    """
    df = pd.read_csv('data/API_SP.csv', sep=',', encoding='utf8', engine='python')
    df.drop('Country Code',axis=1,inplace=True)
    df.drop('Indicator Name',axis=1,inplace=True)
    df.drop('Indicator Code',axis=1,inplace=True)
    
    cleaned_df = df.melt(id_vars=["Country Name"], var_name="year")
    cleaned_df.rename({'Country Name':'country'},axis=1,inplace=True)
    cleaned_df.dropna(inplace=True)
    cleaned_df.value = cleaned_df.value.astype(int)
    cleaned_df.year = cleaned_df.year.astype(int)
    
    return cleaned_df

def get_countries_geo(df):
    """
    Returns countries geojson for plotly map   
    Inputs - dataframe=df
    """
    world_path = 'data/data.geo.json'
    with open(world_path) as f:
        geo_world = json.load(f)
    geo_world
    
    found = []
    missing = []
    countries_geo = []
    # Instanciating necessary lists
    # For simpler acces, setting "zone" as index in a temporary dataFrame
    tmp = df.set_index('country')

    # Looping over the custom GeoJSON file
    for country in geo_world['features']:

        # Country name detection
        country_name = country['properties']['name']

        # Eventual replacement with our transition dictionnary
        country_name = conv_dict[country_name] if country_name in conv_dict.keys() else country_name
        go_on = country_name in tmp.index

        # If country is in original dataset or transition dictionnary
        if go_on:

            # Adding country to our "Matched/found" countries
            found.append(country_name)

            # Getting information from both GeoJSON file and dataFrame
            geometry = country['geometry']

            # Adding 'id' information for further match between map and data 
            countries_geo.append({
                'type': 'Feature',
                'geometry': geometry,
                'id':country_name
            })

        # Else, adding the country to the missing countries
        else:
            missing.append(country_name)

    geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}
    return geo_world_ok