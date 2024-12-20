## Flight Routes Project

This repository was developed to automate some functions for analysing datasets. After creating static flight maps using QGIS and ArcGIS Pro, the use of python was explored to creat this application.

## Project Overview

The objective of this project is to use flight data from OpenFlights.org (https://openflights.org/data) to plot connections routes between origin and destination airports based on country and orgin airport.

## Key Technologies

- **Python**: The primary programming language used for the analysis.
- **Folium**: Data wrangling of the Python ecosystem and the mapping strengths of the Leaflet.js library.
- **Streamlit**: An open-source Python framework.

## How to Use

1. Choose Country by drop-down list or typing Country name.
2. Choose Airport by drop-down list or typing name of airport.
3. Map displays connecting routes between chosen airports and destination.
4. Clear selection button to restart.
Note: Because the dataset is full (over 6500 lines of data) in it's inital session, it takes some time to load on inital run or clearing the query. 

## Acknowledgement

This project was completed with the research of varying methods but ultimately pulling from Folium Route Maps Builder by Kenneth Burchfiel.
