"""Visualizations(plotly) for dash."""

import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

def get_countries_geo(df):
    import json
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

    # Displaying metrics
    #print(f'Countries found    : {len(found)}')
    #print(f'Countries not found: {len(missing)}')
    geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}
    return geo_world_ok

def generate_table(df):
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
        ],
        page_size=16,
        style_cell={'padding': '5px',#'textAlign': 'right',
                   'fontSize':12,'whiteSpace': 'normal',
                   'height': 'auto'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=df.to_dict('records'),
        sort_action="native",
    )

def create_map(df):
    

    df1 = df.query("year == 2007")
    
    fig = px.choropleth(df,               
              height=630,
              geojson=get_countries_geo(df), 
              locations='country',
              color=df['value'],
              hover_name="country",  
              animation_frame="year",    
              color_continuous_scale='Inferno'            
    )

    '''
    fig.update_layout(
        margin={'r':0,'t':0,'l':0,'b':0}
    )'''
    return fig

def create_chart():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    
    return fig



