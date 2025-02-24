import streamlit as st
import re
import math

def deg_min_sec_to_dec(deg, min, sec):
    return deg + min / 60 + sec / 3600

def dec_to_deg_min_sec(dec, direction):
    deg = int(dec)
    min = int((dec - deg) * 60)
    sec = round(((dec - deg) * 60 - min) * 60)
    return f"{abs(deg)}\u00B0 {min}' {sec}\" {direction}"

def main():
    st.title("Convert Deg Dec Find BR")

    options = ["Convert Coordinates", "Find Next with Bearing Range"]
    tab = st.selectbox("Select an option", options)

    if tab == "Convert Coordinates":
        st.title("Convert Coordinates")

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

                st.write("### Converted Coordinates:")
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
        distance_unit = st.selectbox("Distance Unit", ["Nautical Miles (NM)", "Kilometers (KM)", "Miles (MI)"])
        distance = st.text_input("Enter Distance:")

        if distance_unit == "Nautical Miles (NM)":
            distance_factor = 1852
        elif distance_unit == "Kilometers (KM)":
            distance_factor = 1000
        else:
            distance_factor = 1609.34

        if st.button("Find Next"):
            try:
                lat_deg = re.sub(r'[^\d\.\s-]', '', lat_deg)
                lon_deg = re.sub(r'[^\d\.\s-]', '', lon_deg)

                lon_deg = lon_deg.replace(" ", "").replace("N", "").replace("S", "").replace("E", "").replace("W", "")

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
                distance = float(distance) * distance_factor

                lat1, lon1 = math.radians(lat_dec), math.radians(lon_dec)
                bearing = math.radians(bearing)

                lat2 = math.asin(math.sin(lat1) * math.cos(distance / 6371) + math.cos(lat1) * math.sin(distance / 6371) * math.cos(bearing))
                lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / 6371) * math.cos(lat1), math.cos(distance / 6371) - math.sin(lat1) * math.sin(lat2))

                lat2, lon2 = math.degrees(lat2), math.degrees(lon2)

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
