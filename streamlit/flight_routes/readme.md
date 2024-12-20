## Flight Routes Project

This repository was developed to automate some functions for analyzing datasets. After creating static flight maps using QGIS and ArcGIS Pro, the use of python was explored to create this application.

## Project Overview

The objective of this project is to use flight data from OpenFlights.org (https://openflights.org/data) to plot connections routes between origin and destination airports based on country and origin airport.

## Key Technologies

- **Python**: The primary programming language used for the analysis.
- **Folium**: Data wrangling of the Python ecosystem and the mapping strengths of the Leaflet.js library.
- **Streamlit**: An open-source Python framework.

## How to Use

1. Choose Country by drop-down list or typing Country name.
2. Choose Airport by drop-down list or typing name of airport.
3. Map displays connecting routes between chosen airports and destination.
4. Clear selection button to restart.
Note: Because the dataset is full (over 6500 lines of data) in its initial session, it takes some time to load on initial run or clearing the query.

## Improvements

1. To optimize initial load times. 
2. To work on coding to facilitate polyline crossing date line issues. 

## Acknowledgement

This project was completed with the research of varying python methods but ultimately pulling from Folium Route Maps Builder by Kenneth Burchfiel.
