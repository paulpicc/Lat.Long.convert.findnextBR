import streamlit as st
import math
import re

def deg_min_sec_to_dec(deg, min=None, sec=None, direction=None):
    if min is None and sec is None:
        return deg
    else:
        if direction == "S" or direction == "W":
            return -((deg + min / 60 + sec / 3600))
        else:
            return (deg + min / 60 + sec / 3600)

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

        lat_deg = st.text_input("Enter Latitude (e.g., 40 26 46 N, 40.4462, 40 degrees 26 minutes 46 seconds N):")
        lon_deg = st.text_input("Enter Longitude (e.g., 79 56 55 W, -79.9486, 79 degrees 56 minutes 55 seconds W):")

        if st.button("Convert"):
            try:
                lat_deg = re.sub(r'[^\d\.\s-]', '', lat_deg)
                lon_deg = re.sub(r'[^\d\.\s-]', '', lon_deg)

                lat_deg_parts = lat_deg.split()
                lon_deg_parts = lon_deg.split()

                if len(lat_deg_parts) == 1:
                    lat_dec = float(lat_deg_parts[0])
                elif len(lat_deg_parts) == 3:
                    lat_dec = deg_min_sec_to_dec(float(lat_deg_parts[0]), float(lat_deg_parts[1]), float(lat_deg_parts[2]))
                else:
                    raise ValueError("Invalid latitude format")

                if len(lon_deg_parts) == 1:
                    lon_dec = float(lon_deg_parts[0])
                elif len(lon_deg_parts) == 3:
                    lon_dec = deg_min_sec_to_dec(float(lon_deg_parts[0]), float(lon_deg_parts[1]), float(lon_deg_parts[2]))
                else:
                    raise ValueError("Invalid longitude format")

                st.write(f"Latitude in Decimal Degrees: {lat_dec:.6f}")
                st.write(f"Longitude in Decimal Degrees: {lon_dec:.6f}")
            except Exception as e:
                st.write("An error occurred: ", e)

    elif tab == "Find Next with Bearing Range":
        st.title("Find Next with Bearing Range")

        lat1_deg = st.text_input("Enter Starting Latitude (e.g., 40 26 46 N, 40.4462, 40 degrees 26 minutes 46 seconds N):")
        lon1_deg = st.text_input("Enter Starting Longitude (e.g., 79 56 55 W, -79.9486, 79 degrees 56 minutes 55 seconds W):")
        bearing = st.text_input("Enter Bearing in Degrees:")
        distance = st.text_input("Enter Distance:")
        unit = st.selectbox("Select Unit", ["NM", "KM", "MI"], index=0)

        if st.button("Find Next"):
            try:
                lat1_deg = re.sub(r'[^\d\.\s-]', '', lat1_deg)
                lon1_deg = re.sub(r'[^\d\.\s-]', '', lon1_deg)

                lat1_deg_parts = lat1_deg.split()
                lon1_deg_parts = lon1_deg.split()

                if len(lat1_deg_parts) == 1:
                    lat1_dec = float(lat1_deg_parts[0])
                elif len(lat1_deg_parts) == 3:
                    lat1_dec = deg_min_sec_to_dec(float(lat1_deg_parts[0]), float(lat1_deg_parts[1]), float(lat1_deg_parts[2]))
                else:
                    raise ValueError("Invalid starting latitude format")

                if len(lon1_deg_parts) == 1:
                    lon1_dec = float(lon1_deg_parts[0])
                elif len(lon1_deg_parts) == 3:
                    lon1_dec = deg_min_sec_to_dec(float(lon1_deg_parts[0]), float(lon1_deg_parts[1]), float(lon1_deg_parts[2]))
                else:
                    raise ValueError("Invalid starting longitude format")

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
            except Exception as e:
                st.write("An error occurred: ", e)

if __name__ == "__main__":
    main()
