import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

from npi_functions import get_npi_details, parse_npi_data,blank_npi_data
from aic_functions import fetch_address, process_data
from utils import get_coordinates, set_page_config, apply_custom_css,get_coordinates_multiple

# Set page configuration
set_page_config()
apply_custom_css()

# Streamlit UI
st.title("🏥 AIC/NPI Locator")

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["NPI Address Locator", "AIC Address Locator"],
        icons=["hospital", "geo-alt"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#2C2C2C"},
            "icon": {"color": "#4CAF50", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#3E3E3E"},
            "nav-link-selected": {"background-color": "#3E3E3E"},
        }
    )

if selected == "NPI Address Locator":
    st.header("NPI Address Locator")
    st.write("Enter the NPI ID or upload a file to get the address.")
    
    # Option to upload file or enter NPI ID
    upload_option = st.radio("Choose input method:", ("Upload Excel/CSV file", "Enter single NPI ID"))

    npi_ids = []

    if upload_option == "Upload Excel/CSV file":
        uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["xlsx", "csv"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                npi_ids = df.iloc[:, 0].astype(str).tolist()
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    elif upload_option == "Enter single NPI ID":
        single_npi = st.text_input("Enter NPI ID")
        if single_npi:
            npi_ids = [single_npi]

    if st.button("🔍 Search"):
        if npi_ids:
            with st.spinner('Fetching NPI details...'):
                result_data = pd.DataFrame()
                for npi_id in npi_ids:
                    npi_details = get_npi_details(npi_id)

                    if 'created_epoch' in npi_details.keys():
                        parsed_data = parse_npi_data(npi_details)
                        result_data = pd.concat([result_data, parsed_data], ignore_index=True)
                    
                    else:
                        parsed_data = blank_npi_data(npi_details)
                        result_data = pd.concat([result_data, parsed_data], ignore_index=True)

            if not result_data.empty:
                st.success(f"Found {len(result_data)} NPI details.")
                
                # Display results in an interactive table
                st.write("NPI Details:")
                st.dataframe(result_data)

                # Create a map with all locations
                st.subheader("NPI Locations")
                
                # Filter out rows with status not found
                result_data = result_data[result_data['Status'] != 'Not Found']
                
                if not result_data.empty:
                    # Get coordinates for each address
                    with st.spinner('Generating map...'):
                        result_data['Full Address'] = result_data['Address_1_Address1'] + ', ' + result_data['Address_1_City'] + ', ' + result_data['Address_1_State'] + ' ' + result_data['Address_1_Postal Code']
                        result_data['Coordinates'] = result_data['Full Address'].apply(get_coordinates)
                        result_data['Latitude'] = result_data['Coordinates'].apply(lambda x: x[0] if x else None)
                        result_data['Longitude'] = result_data['Coordinates'].apply(lambda x: x[1] if x else None)
                        
                        # Filter out rows with no coordinates
                        map_data = result_data.dropna(subset=['Latitude', 'Longitude'])
                        
                        if not map_data.empty:
                            fig = px.scatter_mapbox(map_data, 
                                                    lat="Latitude", 
                                                    lon="Longitude", 
                                                    hover_name="NPI ID",
                                                    hover_data=["Address_1_Address1", "Address_1_City", "Address_1_State", "Address_1_Postal Code"],
                                                    zoom=3, 
                                                    mapbox_style="open-street-map")
                            fig.update_layout(
                                paper_bgcolor="rgba(0,0,0,0)", 
                                plot_bgcolor="rgba(0,0,0,0)",
                                mapbox=dict(
                                    center=dict(lat=map_data['Latitude'].mean(), lon=map_data['Longitude'].mean()),
                                    zoom=3
                                )
                            )
                            st.plotly_chart(fig)
                        else:
                            st.warning("Could not generate map due to missing location data.")
                else:
                    st.warning("Could not generate map due to missing location data.")

                # Download the results
                csv = result_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download data as CSV",
                    data=csv,
                    file_name='npi_details.csv',
                    mime='text/csv'
                )
            else:
                st.warning("No valid NPI details found for the given input(s).")
        else:
            st.warning("Please enter an NPI ID or upload a file before searching.")

elif selected == "AIC Address Locator":
    st.header("AIC Address Locator")
    st.write("Enter the AIC Name and Location/ZIP code or upload a file to get the address.")
    
    # Option to upload file or enter single search
    upload_option = st.radio("Choose input method:", ("Upload Excel/CSV file", "Enter single AIC Name and Location ZIP"))

    if upload_option == "Upload Excel/CSV file":
        uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["xlsx", "csv"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                search_texts = df.iloc[:, 0].astype(str).tolist()
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                search_texts = []
    else:
        search_text = st.text_input("AIC Name and Location/ZIP:")
        search_texts = [search_text] if search_text else []

    if st.button("🔍 Search"):
        if search_texts:
            results = []
            with st.spinner('Searching for addresses...'):
                for search_text in search_texts:
                    locations = get_coordinates_multiple(search_text)
                    if locations:
                        for location in locations:
                            results.append({
                                "AIC Name and Location/ZIP": search_text,
                                "Address": location['address'],
                                "Latitude": location['latitude'],
                                "Longitude": location['longitude'],
                                "Status": "Found"
                            })
                    else:
                        results.append({
                            "AIC Name and Location/ZIP": search_text,
                            "Address": "",
                            "Latitude": "",
                            "Longitude": "",
                            "Status": "Not Found"
                        })

            if results:
                results_df = pd.DataFrame(results)
                
                # Display results in tabular form
                st.subheader("Search Results")
                st.dataframe(results_df)

                # Filter out rows with status not found
                map_df = results_df[results_df['Status'] == 'Found']
                results_df = results_df[results_df['Status'] == 'Found']

                if not map_df.empty:
                    # Display interactive map
                    st.subheader("Location Map")
                    fig = px.scatter_mapbox(map_df, 
                                            lat="Latitude", 
                                            lon="Longitude", 
                                            zoom=3, 
                                            hover_name="AIC Name and Location/ZIP", 
                                            hover_data=["Address"], 
                                            mapbox_style="open-street-map")
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)",
                        mapbox=dict(
                            center=dict(lat=map_df['Latitude'].mean(), lon=map_df['Longitude'].mean()),
                            zoom=3
                        )
                    )
                    st.plotly_chart(fig)
                else:
                    st.warning("Could not generate map due to missing location data.")

                # Download button
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download results as CSV",
                    data=csv,
                    file_name='aic_addresses.csv',
                    mime='text/csv',
                )
            else:
                st.error("No addresses found for the given input(s).")
        else:
            st.warning("Please enter an AIC Name and Location/ZIP or upload a file.")
# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Cognizant")