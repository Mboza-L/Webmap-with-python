# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 03:47:52 2020

@author: lukin

Interactive map showing Canada Parks boundaries, place names, campsites, 
facilities and interest points

Data from Government of Canada open governtment portal
https://open.canada.ca/data/en/dataset?q=name%3A%22e1f0c975-f40c-4313-9be2-beb951e35f4e%22+OR+name%3A%2274054d44-68cf-41af-8919-5f09f80dcd02%22+OR+name%3A%228e27e2d0-b265-47d0-8fa5-3237854c7a08%22+OR+name%3A%22cf5c266c-3a6a-4a3b-aed1-2ddd6e49d5e6%22+OR+name%3A%223969368d-33b5-47c8-8953-f31b15d8e007%22+&sort=metadata_modified+desc#


"""


import pandas
import folium
import geopandas as gpd
import requests
import fiona

def interetPoints():
    #convert csv data to dataframes, and into lists for easy manipulation
    iData = pandas.read_csv("Data/Interest_Point_Interet_vw.csv")
    iLat = list(iData["Y"])
    iLon = list(iData["X"])
    iName = list(iData["Name_e"])
    iType =list(iData["Principal_type"])
    
    #create empty list of feature groups
    prinTypes=[]
    for pt in iType:
        if pt not in prinTypes:
            prinTypes.append(pt)
            
    #Create feature group according to Principle type
    fgs=[]
    for pt in prinTypes:
        fgs.append(folium.FeatureGroup(name=pt))
    
    #assigning location features to individual points 
    for fgi in fgs:
        for lt, ln, nm in zip(iLat, iLon, iName):
            fgi.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup = nm, fill_color ='black', color= 'grey',fill = True, fill_opacity = 0.7))
            parkMap.add_child(fgi)
            
def parkBounds(yourMap):
    #convert data to geopandas data frame

    #website source url for .shp data
    url = 'http://ftp.maps.canada.ca/pub/pc_pc/National-parks_Parc-national/national_parks_boundaries/national_parks_boundaries.shp.zip'
    
    request = requests.get(url, verify=False)
    #find better solution to verification issue
    
    b = bytes(request.content)
    with fiona.BytesCollection(b) as f:
        crs = f.crs
        bound_gdf = gpd.GeoDataFrame.from_features(f, crs=crs)
        #print(bound_gdf.head())
    
    #writing a file to json using geopandas
    bound_gdf.to_file("parkBound.geojson", driver='GeoJSON')
    
    #used to add the geoJson polygon layer to demarkate country boundaries
    fgb = folium.FeatureGroup(name="Boundaries")
    #fileName = r'parkBound.geojson'
    #folium.GeoJson(fileName, name='geojson').add_to(yourMap)
    fgb.add_child(folium.GeoJson(open("parkBound.geojson").read()))
    #fgb.add_child(folium.GeoJson(r"parkBound.geojson"))
    #fgb.add_child("parkBound.geojson")
    yourMap.add_child(fgb)

def placeNames(yourMap):
    
    #convert csv data to dataframes, and into lists for easy manipulation
    pData = pandas.read_csv("Data/Place_Names_Noms_Lieux_APCA_vw.csv")
    pLat = list(pData["Y"])
    pLon = list(pData["X"])
    pName = list(pData["Name_e"])
    
    #First feature group: place names
    fgp = folium.FeatureGroup(name="Place Names")
    #assigning location features to individual points 
    for lat, lon, pname in zip(pLat, pLon, pName):
        #print(lt, ln, name)
        fgp.add_child(folium.CircleMarker(location=[lat, lon], radius = 3, popup = pname, fill_color ='yellow', color= 'grey',fill = True, fill_opacity = 0.7))
    yourMap.add_child(fgp)

#Map features including location on world map, default zoom settings and backgroud graphics
parkMap = folium.Map(location = [60, -80], zoom_start=4, tiles= 'Stamen Terrain')
#to do : find  a custom tile (Geo gratis Canada base map) that is more plain so all features reflected are those added
   
        
#add   boundary layer   
# fgb = folium.FeatureGroup(name="Boundaries")
# fgb.add_child(folium.GeoJson(data=open('national_parks_boundaries.json','r', encoding='utf-8-sig').read()))
# # for coordinates in [[38.2, -99.1],[39.2, -97.1]]:


#adding the feature groups, and layer control to choose to remove or display different features

parkBounds(parkMap)
placeNames(parkMap)
interetPoints()


#parkMap.add_child(fgb)
parkMap.add_child(folium.LayerControl())


#launch map
parkMap.save("CanadaNationalParks.html")