import streamlit as st
import math

# Your original code
def decimal_degrees_to_dms(decimal_degrees):
    is_negative = decimal_degrees < 0
    decimal_degrees = abs(decimal_degrees)
    degrees = int(decimal_degrees)
    decimal_minutes = (decimal_degrees - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60
    if is_negative:
        degrees = -degrees
    return (degrees, minutes, seconds)

def dms_to_decimal_degrees(degrees, minutes, seconds):
    sign = -1 if degrees < 0 else 1
    degrees = abs(degrees)
    return sign * (degrees + (minutes / 60) + (seconds / 3600))

def parse_coordinates(input_str, is_latitude=True):
    if "°" in input_str or "'" in input_str or '"' in input_str or ' ' in input_str:
        parts = input_str.strip().replace('"', '').replace("'", ' ').replace('°', ' ').split()
        degrees = float(parts[0])
        minutes = float(parts[1]) if len(parts) > 1 else 0
        seconds = float(parts[2]) if len(parts) > 2 else 0
        if len(parts) > 3:
            direction = parts[3].upper()
            if (is_latitude and direction == 'S') or (not is_latitude and direction == 'W'):
                degrees = -abs(degrees)
        return dms_to_decimal_degrees(degrees, minutes, seconds)
    else:
        try:
            value = float(input_str.strip())
            return value
        except ValueError:
            if input_str[-1].upper() in ['N', 'S', 'E', 'W']:
                try:
                    value = float(input_str[:-1].strip())
                    if input_str[-1].upper() in ['S', 'W']:
                        value = -abs(value)
                    return value
                except ValueError:
                    raise ValueError("Invalid coordinate format")
            else:
                raise ValueError("Invalid coordinate format")

def calculate_destination(lat1, lon1, bearing_deg, distance_nm, unit="nmi"):
    if unit == "nmi":
        R = 3440.07  # Approximately 3440.07 nautical miles
    elif unit == "km":
        R = 6371.0  # Earth's radius in km
    elif unit == "mi":
        R = 3959.0  # Earth's radius in miles
    else:
        raise ValueError("Invalid unit")

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    bearing_rad = math.radians(bearing_deg)

    d = distance_nm / R

    lat2 = math.asin(math.sin(lat1) * math.cos(d) +
                     math.cos(lat1) * math.sin(d) * math.cos(bearing_rad))

    lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(d) * math.cos(lat1),
                             math.cos(d) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    lon2 = (lon2 + 540) % 360 - 180

    return (lat2, lon2)

# Streamlit app
st.title("Latitude and Longitude Converter")

st.markdown("<br><br>", unsafe_allow_html=True)  # Add some space

tab1, tab2 = st.tabs(["Convert between DMS and Decimal Degrees", "Calculate Next Point"])

with tab1:
    st.header("Convert between DMS and Decimal Degrees")
    lat_lon_input = st.text_input("Enter latitude and longitude in either decimal degrees (e.g. 43.6532, -79.3832) or DMS (e.g. 43° 39' 12\", -79° 23' 0\") format, separated by a comma")
    if st.button("Convert"):
        try:
            lat_input, lon_input = lat_lon_input.split(',')
            lat_dd = parse_coordinates(lat_input.strip())
            lon_dd = parse_coordinates(lon_input.strip(), False)
            lat_dms = decimal_degrees_to_dms(lat_dd)
            lon_dms = decimal_degrees_to_dms(lon_dd)
            st.write(f"Latitude (Decimal Degrees): {lat_dd:.6f}")
            st.write(f"Latitude (DMS): {lat_dms[0]}° {lat_dms[1]}' {lat_dms[2]:.2f}\"")
            st.write(f"Longitude (Decimal Degrees): {lon_dd:.6f}")
            st.write(f"Longitude (DMS): {lon_dms[0]}° {lon_dms[1]}' {lon_dms[2]:.2f}\"")
        except ValueError as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("Calculate Next Point")
    lat_lon_input = st.text_input("Enter starting latitude and longitude in either decimal degrees (e.g. 43.6532, -79.3832) or DMS (e.g. 43° 39' 12\", -79° 23' 0\") format, separated by a comma")
    bearing_input = st.number_input("Enter bearing in degrees (0-360)", value=90)
    distance_input = st.number_input("Enter distance", value=50)
    unit_input = st.selectbox("Select unit", ["nmi", "km", "mi"])

    if st.button("Calculate"):
        try:
            lat_input, lon_input = lat_lon_input.split(',')
            lat = parse_coordinates(lat_input.strip())
            lon = parse_coordinates(lon_input.strip(), False)
            bearing = bearing_input
            distance = distance_input
            unit = unit_input
            dest_lat, dest_lon = calculate_destination(lat, lon, bearing, distance, unit)
            st.write(f"Starting Point: {lat_lon_input}")
            st.write(f"Bearing: {bearing}°")
            st.write(f"Distance: {distance} {unit}")
            st.write(f"Destination Point: {dest_lat:.6f}, {dest_lon:.6f}")
        except ValueError as e:
            st.error(f"Error: {e}")
