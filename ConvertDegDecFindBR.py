import streamlit as st
import math
import re

def deg_min_sec_to_dec(deg, min, sec, direction):
    if direction == "S" or direction == "W":
        return -((int(deg) + int(min) / 60 + int(sec) / 3600))
    else:
        return (int(deg) + int(min) / 60 + int(sec) / 3600)

def find_bearing(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    y = math.sin(dlon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    bearing = math.degrees(math.atan2(y, x))

    if bearing < 0:
        bearing = 360 + bearing

    return bearing

def find_distance(lat1, lon1, lat2, lon2, unit):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # radius of the Earth in kilometers

    if unit == "NM":
        distance = r * c / 1.852  # in nautical miles
    elif unit == "KM":
        distance = r * c  # in kilometers
    elif unit == "MI":
        distance = r * c / 1.609344  # in miles

    return distance

def main():
    st.title("Coordinate Converter and Navigator")

    tabs = ["Convert Lat/Long", "Find Next with Bearing Range"]
    tab = st.sidebar.selectbox("Select a tab", tabs)

    if tab == "Convert Lat/Long":
        st.title("Convert Lat/Long")

        lat_deg = st.text_input("Enter Latitude in Degrees, Minutes, and Seconds (e.g., 40 26 46 N):")
        lon_deg = st.text_input("Enter Longitude in Degrees, Minutes, and Seconds (e.g., 79 56 55 W):")

        if st.button("Convert"):
            try:
                lat_deg_match = re.match(r"(\d+) (\d+) (\d+) (N|S)", lat_deg)
                lon_deg_match = re.match(r"(\d+) (\d+) (\d+) (E|W)", lon_deg)

                if lat_deg_match and lon_deg_match:
                    lat_deg, lat_min, lat_sec, lat_dir = lat_deg_match.groups()
                    lon_deg, lon_min, lon_sec, lon_dir = lon_deg_match.groups()

                    lat_dec = deg_min_sec_to_dec(lat_deg, lat_min, lat_sec, lat_dir)
                    lon_dec = deg_min_sec_to_dec(lon_deg, lon_min, lon_sec, lon_dir)

                    st.write(f"Latitude in Decimal Degrees: {lat_dec:.6f}")
                    st.write(f"Longitude in Decimal Degrees: {lon_dec:.6f}")
                else:
                    st.write("Invalid input. Please enter latitude and longitude in the format: DD MM SS N/S and DD MM SS E/W")
            except Exception as e:
                st.write("An error occurred: ", e)

    elif tab == "Find Next with Bearing Range":
        st.title("Find Next with Bearing Range")

        lat1_deg = st.text_input("Enter Starting Latitude in Degrees, Minutes, and Seconds (e.g., 40 26 46 N):")
        lon1_deg = st.text_input("Enter Starting Longitude in Degrees, Minutes, and Seconds (e.g., 79 56 55 W):")
        bearing = st.text_input("Enter Bearing in Degrees:")
        distance = st.text_input("Enter Distance:")
        unit = st.selectbox("Select Unit", ["NM", "KM", "MI"], index=0)

        if st.button("Find Next"):
            try:
                lat1_deg_match = re.match(r"(\d+) (\d+) (\d+) (N|S)", lat1_deg)
                lon1_deg_match = re.match(r"(\d+) (\d+) (\d+) (E|W)", lon1_deg)

                if lat1_deg_match and lon1_deg_match:
                    lat1_deg, lat1_min, lat1_sec, lat1_dir = lat1_deg_match.groups()
                    lon1_deg, lon1_min, lon1_sec, lon1_dir = lon1_deg_match.groups()

                    lat1_dec = deg_min_sec_to_dec(lat1_deg, lat1_min, lat1_sec, lat1_dir)
                    lon1_dec = deg_min_sec_to_dec(lon1_deg, lon1_min, lon1_sec, lon1_dir)

                    bearing = float(bearing)
                    distance = float(distance)

                    lat2_rad = math.radians(lat1_dec)
                    lon2_rad = math.radians(lon1_dec)
                    bearing_rad = math.radians(bearing)

                    lat2_rad = math.asin(math.sin(lat2_rad) * math.cos(distance / 6371) + math.cos(lat2_rad) * math.sin(distance / 6371) * math.cos(bearing_rad))
                    lon2_rad = lon2_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance / 6371) * math.cos(lat2_rad), math.cos(distance / 6371) - math.sin(lat2_rad) * math.sin(lat2_rad))

                    lat2_dec = math.degrees(lat2_rad)
                    lon2_dec = math.degrees(lon2_rad)

                    st.write(f"Latitude of Next Point: {lat2_dec:.6f}")
                    st.write(f"Longitude of Next Point: {lon2_dec:.6f}")
                else:
                    st.write("Invalid input. Please enter starting latitude and longitude in the format: DD MM SS N/S and DD MM SS E/W")
            except Exception as e:
                st.write("An error occurred: ", e)

if __name__ == "__main__":
    main()
