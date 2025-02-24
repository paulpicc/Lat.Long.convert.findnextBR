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

def dec_to_deg_min_sec(dec, direction=None):
    if dec < 0:
        direction = "S" if direction in ["S", "N"] else "W"
    else:
        direction = "N" if direction in ["S", "N"] else "E"
    dec = abs(dec)
    deg = math.floor(dec)
    min = math.floor((dec - deg) * 60)
    sec = round(((dec - deg) * 3600) % 60, 2)
    return f"{deg}° {min}' {sec}" {direction}"

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    bearing = math.degrees(math.atan2(y, x))
    return bearing

def calculate_destination(lat1, lon1, bearing, distance, unit):
    R = 6371  # Earth radius in km
    if unit == "nmi":
        R = 3440.069  # Earth radius in nautical miles
    elif unit == "mi":
        R = 3958.8  # Earth radius in miles
        
    lat1, lon1, bearing = map(math.radians, [lat1, lon1, bearing])
    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) + math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1), math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))
    return math.degrees(lat2), math.degrees(lon2)

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

                lat_dms = dec_to_deg_min_sec(lat_dec, "N" if lat_dec > 0 else "S")
                lon_dms = dec_to_deg_min_sec(lon_dec, "E" if lon_dec > 0 else "W")

                st.write("### Conversion Results:")
                st.write("#### Decimal Degrees:")
                st.write(f"Latitude: {lat_dec:.6f}")
                st.write(f"Longitude: {lon_dec:.6f}")
                st.write(f"Coordinates: {lat_dec:.6f}, {lon_dec:.6f}")
                st.write("#### Degrees, Minutes, Seconds:")
                st.write(f"Latitude: {lat_dms}")
                st.write(f"Longitude: {lon_dms}")
            except Exception as e:
                st.write("An error occurred: ", e)

    elif tab == "Find Next with Bearing Range":
        st.title("Find Next with Bearing Range")

        lat_deg = st.text_input("Enter Starting Latitude (e.g., 40 26 46 N, 40.4462, 40 degrees 26 minutes 46 seconds N):")
        lon_deg = st.text_input("Enter Starting Longitude (e.g., 79 56 55 W, -79.9486, 79 degrees 56 minutes 55 seconds W):")
        bearing = st.text_input("Enter Bearing (in degrees):")
        distance = st.text_input("Enter Distance:")
        unit = st.selectbox("Select Unit", ["nmi", "km", "mi"], index=0)  # Set default to "nmi"

        if st.button("Find Next"):
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

                bearing = float(bearing)
                distance = float(distance)

                lat2, lon2 = calculate_destination(lat_dec, lon_dec, bearing, distance, unit)

                lat_dms = dec_to_deg_min_sec(lat2, "N" if lat2 > 0 else "S")
                lon_dms = dec_to_deg_min_sec(lon2, "E" if lon2 > 0 else "W")

                st.write("### Next Coordinates:")
                st.write("#### Decimal Degrees:")
                st.write(f"Latitude: {lat2:.6f}")
                st.write(f"Longitude: {lon2:.6f}")
                st.write(f"Coordinates: {lat2:.6f}, {lon2:.6f}")
                st.write("#### Degrees, Minutes, Seconds:")
                st.write(f"Latitude: {lat_dms}")
                st.write(f"Longitude: {lon_dms}")
            except Exception as e:
                st.write("An error occurred: ", e)

if __name__ == "__main__":
    main()
