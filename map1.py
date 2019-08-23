import folium
import pandas


def color_producer(value):
    if value < 1000:
        return 'green'
    elif 1000 <= value < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[37.252209, -121.978408], zoom_start=6)
data = pandas.read_csv('Volcanoes.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
name = list(data['NAME'])
elev = list(data['ELEV'])
status = list(data['STATUS'])

html = """
Name: %s <br>
Height: %s m<br>
Status: %s<br>
"""

feature_volc = folium.FeatureGroup(name='Volcanoes in NA')
feature_pop = folium.FeatureGroup(name='Country Population')

for latVal, lonVal, elevVal, nameVal, statVal in zip(lat, lon, elev, name, status):
    iframe = folium.IFrame(html=html % (nameVal, str(elevVal), statVal), width=200, height=100)
    feature_volc.add_child(folium.CircleMarker(location=[latVal, lonVal], radius=5,popup=folium.Popup(iframe), fill_color=color_producer(elevVal), color='gray', fill_opacity=0.7, fill=True))


feature_pop.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(feature_pop)
map.add_child(feature_volc)
map.add_child(folium.LayerControl())

map.save('Map1.html')

