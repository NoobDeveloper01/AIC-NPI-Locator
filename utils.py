import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(address):
    geolocator = Nominatim(user_agent="aic_npi_locator")
    try:
        # Add country bias to the search
        location = geolocator.geocode(address, country_codes="us")
        
        if location:
            # Extract full address
            full_address = location.raw['display_name']
            
            # Verify if the result is in the USA
            if "United States" in full_address:
                return location.latitude, location.longitude, full_address
            else:
                return None, None, None
        else:
            return None, None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None, None

def get_coordinates_multiple(address, max_results=5):
    geolocator = Nominatim(user_agent="aic_npi_locator")
    try:
        # Get multiple results
        locations = geolocator.geocode(address, country_codes="us", exactly_one=False, limit=max_results)
        
        if locations:
            results = []
            for location in locations:
                full_address = location.raw['display_name']
                
                # Verify if the result is in the USA
                if "United States" in full_address:
                    results.append({
                        'latitude': location.latitude,
                        'longitude': location.longitude,
                        'address': full_address
                    })
            
            return results
        else:
            return []
    except (GeocoderTimedOut, GeocoderServiceError):
        return []
        
def set_page_config():
    st.set_page_config(page_title="AIC/NPI Locator", page_icon="🏥", layout="wide")

def apply_custom_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #2C2C2C;
            color: #FFFFFF;
        }
        .stSelectbox>div>div>select {
            background-color: #2C2C2C;
            color: #FFFFFF;
        }
        .stRadio>div {
            background-color: #2C2C2C;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 5px;
        }
        .stDataFrame {
            background-color: #2C2C2C;
            color: #FFFFFF;
        }
        .streamlit-expanderHeader {
            background-color: #2C2C2C;
            color: #FFFFFF;
        }
        .stPlotlyChart {
            background-color: #2C2C2C;
        }
    </style>
    """, unsafe_allow_html=True)