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
        direction = "S" if dec < 0 else "N"
    else:
        direction = "N" if dec > 0 else "S"
    dec = abs(dec)
    deg = math.floor(dec)
    min = math.floor((dec - deg) * 60)
    sec = round(((dec - deg) * 3600) % 60, 2)
    return f"{deg} {min} {sec} {direction}"

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

                st.write(f"Latitude in Decimal Degrees: {lat_dec:.6f}")
                st.write(f"Longitude in Decimal Degrees: {lon_dec:.6f}")
                st.write(f"Latitude in DMS: {lat_dms}")
                st.write(f"Longitude in DMS: {lon_dms}")
                st.write(f"Coordinates in Decimal Degrees (comma-separated): {lat_dec:.6f}, {lon_dec:.6f}")
            except Exception as e:
                st.write("An error occurred: ", e)

    elif tab == "Find Next with Bearing Range":
        st.title("Find Next with Bearing Range")

        # ... (rest of the code remains the same)

if __name__ == "__main__":
    main()
