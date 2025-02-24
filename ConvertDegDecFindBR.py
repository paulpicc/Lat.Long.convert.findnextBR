import math
import re

def deg_min_sec_to_dec(deg, min, sec, direction):
    return (deg + min / 60 + sec / 3600) * (1 if direction in ['N', 'E'] else -1)

def dec_to_deg_min_sec(dec, direction):
    dec = abs(dec)
    deg = int(dec)
    min = int((dec - deg) * 60)
    sec = round((dec - deg - min / 60) * 3600)
    return f"{deg} {min} {sec} {direction}"

st.title("Latitude and Longitude Converter and Find Next with Bearing Range")

tab = st.selectbox("Choose an option", ["Convert Degrees, Minutes, Seconds to Decimal", "Convert Decimal to Degrees, Minutes, Seconds", "Find Next with Bearing Range"])

if tab == "Convert Degrees, Minutes, Seconds to Decimal":
    st.title("Convert Degrees, Minutes, Seconds to Decimal")

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
                lat_dec = deg_min_sec_to_dec(float(lat_deg_parts[0]), float(lat_deg_parts[1]), float(lat_deg_parts[2]), lat_deg_parts[3])
            else:
                raise ValueError("Invalid latitude format")

            if len(lon_deg_parts) == 1:
                lon_dec = float(lon_deg_parts[0])
            elif len(lon_deg_parts) == 3:
                lon_dec = deg_min_sec_to_dec(float(lon_deg_parts[0]), float(lon_deg_parts[1]), float(lon_deg_parts[2]), lon_deg_parts[3])
            else:
                raise ValueError("Invalid longitude format")

            st.write("### Converted Coordinates:")
            st.write(f"Latitude: {lat_dec:.6f}")
            st.write(f"Longitude: {lon_dec:.6f}")
            st.write(f"Coordinates (comma-separated): {lat_dec:.6f}, {lon_dec:.6f}")
        except Exception as e:
            st.write("An error occurred: ", e)

elif tab == "Convert Decimal to Degrees, Minutes, Seconds":
    st.title("Convert Decimal to Degrees, Minutes, Seconds")

    lat_dec = st.text_input("Enter Latitude (in decimal degrees):")
    lon_dec = st.text_input("Enter Longitude (in decimal degrees):")

    if st.button("Convert"):
        try:
            lat_dec = float(lat_dec)
            lon_dec = float(lon_dec)

            lat_dms = dec_to_deg_min_sec(lat_dec, "N" if lat_dec > 0 else "S")
            lon_dms = dec_to_deg_min_sec(lon_dec, "E" if lon_dec > 0 else "W")

            st.write("### Converted Coordinates:")
            st.write(f"Latitude: {lat_dms}")
            st.write(f"Longitude: {lon_dms}")
        except Exception as e:
            st.write("An error occurred: ", e)

elif tab == "Find Next with Bearing Range":
    st.title("Find Next with Bearing Range")

    lat_deg = st.text_input("Enter Starting Latitude (e.g., 40 26 46 N, 40.4462, 40 degrees 26 minutes 46 seconds N):")
    lon_deg = st.text_input("Enter Starting Longitude (e.g., 79 56 55 W, -79.9486, 79 degrees 56 minutes 55 seconds W):")
    bearing = st.text_input("Enter Bearing (in degrees):")
    distance = st.text_input("Enter Distance (in nautical miles):")

    if st.button("Find Next"):
        try:
            lat_deg = re.sub(r'[^\d\.\s-]', '', lat_deg)
            lon_deg = re.sub(r'[^\d\.\s-]', '', lon_deg)

            lat_deg_parts = lat_deg.split()
            lon_deg_parts = lon_deg.split()

            if len(lat_deg_parts) == 1:
                lat_dec = float(lat_deg_parts[0])
            elif len(lat_deg_parts) == 3:
                lat_dec = deg_min_sec_to_dec(float(lat_deg_parts[0]), float(lat_deg_parts[1]), float(lat_deg_parts[2]), lat_deg_parts[3])
            else:
                raise ValueError("Invalid latitude format")

            if len(lon_deg_parts) == 1:
                lon_dec = float(lon_deg_parts[0])
            elif len(lon_deg_parts) == 3:
                lon_dec = deg_min_sec_to_dec(float(lon_deg_parts[0]), float(lon_deg_parts[1]), float(lon_deg_parts[2]), lon_deg_parts[3])
            else:
                raise ValueError("Invalid longitude format")

            bearing = float(bearing)
            distance_km = float(distance) * 1.852

            lat1, lon1 = math.radians(lat_dec), math.radians(lon_dec)
            bearing = math.radians(bearing)

            lat2 = math.asin(math.sin(lat1) * math.cos(distance_km / 6371) + math.cos(lat1) * math.sin(distance_km / 6371) * math.cos(bearing))
            lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance_km / 6371) * math.cos(lat1), math.cos(distance_km / 6371) - math.sin(lat1) * math.sin(lat2))

            lat2, lon2 = math.degrees(lat2), math.degrees(lon2)

            lat_dms = dec_to_deg_min_sec(lat2, "N" if lat2 > 0 else "S")
            lon_dms = dec_to_deg_min_sec(lon2, "E" if lon2 > 0 else "W")

            st.write("### Next Coordinates:")
            st.write("#### Decimal Degrees:")
            st.write(f"Latitude: {lat2:.6f}")
            st.write(f"Longitude: {lon2:.6f}")
            st.write(f"Coordinates (comma-separated): {lat2:.6f}, {lon2:.6f}")
            st.write("#### Degrees, Minutes, Seconds:")
            st.write(f"Latitude: {lat_dms}")
            st.write(f"Longitude: {lon_dms}")
        except Exception as e:
            st.write("An error occurred: ", e)
