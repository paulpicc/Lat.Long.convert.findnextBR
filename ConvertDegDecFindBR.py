import streamlit as st

# Lat-Long Converter
st.header("Lat-Long Converter")
latitude_decimal = st.text_input("Enter latitude (e.g., 37.7749 or 37°47'29.6\"N): ")
longitude_decimal = st.text_input("Enter longitude (e.g., -122.4194 or 122°25'10.1\"W): ")

if latitude_decimal and longitude_decimal:
    # Your lat-long converter code goes here
    st.write("Decimal Degrees:")
    st.write(f"Latitude: {latitude_decimal:.6f}")
    st.write(f"Longitude: {longitude_decimal:.6f}")

    st.write("Degrees, Minutes, Seconds (DMS):")
    # Your DMS conversion code goes here
    st.write(f"Latitude: {format_dms(lat_degrees, lat_minutes, lat_seconds, 'N' if latitude_decimal >=0 else 'S')}")
    st.write(f"Longitude: {format_dms(long_degrees, long_minutes, long_seconds, 'E' if longitude_decimal >=0 else 'W')}")

# Bearing-Range Calculator
st.header("Bearing-Range Calculator")
bearing = st.text_input("Enter bearing (e.g., 45): ")
range = st.text_input("Enter range (e.g., 10): ")

if bearing and range:
    # Your bearing-range calculator code goes here
    st.write("Next Point:")
    st.write(f"Latitude: {next_lat:.6f}")
    st.write(f"Longitude: {next_long:.6f}")
