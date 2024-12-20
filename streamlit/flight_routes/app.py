import folium
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import pandas as pd
from pyproj import Geod


st.set_page_config(page_title='Flight Route Finder', layout='wide')
st.title('Flight Route Finder')

st.markdown('This app uses historical flight data to visualize Non-Stop Flight Routes from '
            'any Country and Airport in the database.')

data_url = 'https://raw.githubusercontent.com/CoderCpy/Python_projects/refs/heads/main/data/flightroute/'
csv_file = 'flight_routes.csv'

@st.cache_data
def read_csv(url):
    df = pd.read_csv(url)
    return df

csv_url = data_url + csv_file
df_routes = read_csv(csv_url)
 

# This .csv file was created within flights_table_builder.ipynb, by using python code 
#to download, convert file type, merge and clean the data. 

def value_change(category):
    st.session_state.df_routes = st.session_state.df_routes[st.session_state.df_routes[category]==st.session_state[category]]
        
if 'df_routes' not in st.session_state:
    st.session_state.df_routes=df_routes  
    
cols = st.columns(2)
country = cols[0].selectbox('Country', st.session_state.df_routes.origin_country.unique(), index=0, 
                            key='origin_country', placeholder="Choose a Country", 
                            on_change=value_change,
                            kwargs={'category': 'origin_country'})
airport = cols[1].selectbox('Airport', st.session_state.df_routes.Airport_name.unique(), index=0, 
                            key='Airport_name', placeholder="Choose an Airport", 
                            on_change=value_change,  kwargs={'category': 'Airport_name'})


def clear_state():
    st.session_state.df_routes=df_routes
    
st.button('Clear selection', on_click=clear_state)

# Defines a placeholder to display the distance and download button once computed.    
placeholder = st.empty()


# Center location based on Airport coordinates.
longitude_cutoff = 300
s_origin_latitude = st.session_state.df_routes.iloc[0]['origin_lat']
s_origin_longitude = st.session_state.df_routes.iloc[0]['origin_long']
if s_origin_longitude > longitude_cutoff:
    s_origin_longitude -= 360
coordinates = [s_origin_latitude, s_origin_longitude]


m = folium.Map(location=coordinates, zoom_start=3, tiles = "CartoDB Positron")


def generate_map(df_routes):
  longitude_cutoff = 300
  # add an input for map_name when it works.

  g = Geod(ellps="WGS84")
  # From https://pyproj4.github.io/pyproj/stable/api/geod.html
  

  for i in range(len(st.session_state.df_routes)):

      origin_latitude = st.session_state.df_routes.iloc[i]['origin_lat']
      origin_longitude = st.session_state.df_routes.iloc[i]['origin_long']
      if origin_longitude > longitude_cutoff:
        origin_longitude -= 360
        
    
      destination_latitude = st.session_state.df_routes.iloc[i]['dest_lat']
      destination_longitude = st.session_state.df_routes.iloc[i]['dest_long']
      if destination_longitude > longitude_cutoff:
        destination_longitude -= 360
     # This method of reducing far-east longitude points by 360 is from:
     # https://github.com/Leaflet/Leaflet/issues/82#issuecomment-1260488 
        
      route_color = '#3388ff' 

      gc_points = g.npts(origin_longitude, origin_latitude,
      destination_longitude, destination_latitude, 20)
        # Uses pyproj to create a list of great circle ('gc') points
        # that produce curvilinear airline routes. From:
        # https://pyproj4.github.io/pyproj/stable/api/geod.html?highlight=npts#pyproj.Geod.npts

      revised_gc_points = []
      revised_gc_points.append((origin_latitude, origin_longitude))
      for item in gc_points:
        if item[0] > longitude_cutoff:
          new_lon = item[0] - 360
        else:
          new_lon = item[0]
        revised_gc_points.append((item[1], new_lon))
        # The coordinates in gc_points are stored in (longitude, latitude)
        # format, so this append statement flips them back into
        # (latitude, longitude) format for plotting.
      revised_gc_points.append((destination_latitude, destination_longitude))

      folium.vector_layers.PolyLine(revised_gc_points, weight = 1, color = route_color).add_to(m)
      # Based on:
      # https://python-visualization.github.io/folium/modules.html#folium.vector_layers.PolyLine

  # The following set of code creates a list of all airports contained
  # within the map, along with their coordinates.
  origin_airports = st.session_state.df_routes.copy()[['s_airport', 'origin_lat', 'origin_long']]
  origin_airports.columns=['code', 'lat', 'long']
  destination_airports = st.session_state.df_routes.copy()[['d_airport', 'dest_lat', 'dest_long']]
  destination_airports.columns=['code', 'lat', 'long']
  df_airports = pd.concat([origin_airports, destination_airports])
  df_airports.drop_duplicates('code', inplace=True)
  df_airports.reset_index(drop=True,inplace=True)

  
# This for loop plots airport markers on the map. 
  for i in range(len(df_airports)):
    if df_airports.iloc[i]['long'] > longitude_cutoff:
      airport_long = df_airports.iloc[i]['long'] - 360
    else:
      airport_long = df_airports.iloc[i]['long']
    if airport == True:
      folium.CircleMarker(location=[df_airports.iloc[i]['lat'],
      airport_long], radius = 2, fill = False,
      color = 'blue', fill_color = 'black', fill_opacity = 1).add_to(m)
      folium.Marker([df_airports.iloc[i]['lat'],
                     airport_long],
      icon = folium.features.DivIcon(icon_anchor = (10, 20),
      html="<div><b>"+df_airports.iloc[i]['code']+"</b></div>")).add_to(m)
        # Tips on how to use Folium Markers.
        # https://python-visualization.github.io/folium/modules.html#folium.map.Marker
        # https://python-visualization.github.io/folium/modules.html#folium.features.DivIcon

    else:
      folium.CircleMarker(location=[df_airports.iloc[i]['lat'],
      df_airports.iloc[i]['long']], tooltip = df_airports.iloc[i]['code'],
      radius = 1, fill = True, color = 'grey', fill_color = 'black',
      fill_opacity = 1).add_to(m)
      folium.Marker([df_airports.iloc[i]['lat'],
                     airport_long],
      icon = folium.features.DivIcon(icon_anchor = (10, 20),
      html="<div><b>"+df_airports.iloc[i]['code']+"</b></div>")).add_to(m)

  return m

route_map = generate_map(df_routes)
  
m.save('Routes.html')
with open('Routes.html') as file:
    placeholder.download_button('Download Routes', data=file, file_name='Routes.html')
        
    
folium_static(m, width=1200, height=800)
