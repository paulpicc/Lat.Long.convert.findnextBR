# lat_long_app.py

import re
import streamlit as st
import math

# ... (rest of the original code remains the same)

def main():
    st.title("Coordinate Converter and Navigator")

    tabs = ["Convert Lat/Long", "Find Next with Bearing Range"]
    tab = st.sidebar.selectbox("Select a tab", tabs)

    if tab == "Convert Lat/Long":
        # ... (rest of the original code remains the same)
    elif tab == "Find Next with Bearing Range":
        find_next_tab()

def find_next_tab():
    st.title("Find Next with Bearing Range")

    def decimal_degrees_to_dms(decimal_degrees):
        """Convert decimal degrees to (degrees, minutes, seconds)"""
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
        """Convert (degrees, minutes, seconds) to decimal degrees"""
        sign = -1 if degrees < 0 else 1
        degrees = abs(degrees)

        return sign * (degrees + (minutes / 60) + (seconds / 3600))

    def parse_coordinates(input_str, is_latitude=True):
        """Parse coordinate string in either decimal degrees or DMS format"""
        # ... (rest of the code remains the same)

    def calculate_destination(lat1, lon1, bearing_deg, distance_nm):
        """
        Calculate destination point given starting coordinates, bearing, and distance.
        Using the haversine formula.

        Args:
            lat1, lon1: Starting coordinates in decimal degrees
            bearing_deg: Bearing in degrees (0 = North, 90 = East, etc.)
            distance_nm: Distance in nautical miles

        Returns:
            tuple: (lat2, lon2) Destination coordinates in decimal degrees
        """
        # ... (rest of the code remains the same)

    def format_dd_output(decimal_degrees, is_latitude=True):
        """Format decimal degrees as a human-readable string"""
        if is_latitude:
            return f"{abs(decimal_degrees):.6f}° {'N' if decimal_degrees >= 0 else 'S'}"
        else:
            return f"{abs(decimal_degrees):.6f}° {'E' if decimal_degrees >= 0 else 'W'}"

    st.write("Enter coordinates in either decimal degrees (e.g., 40.7128 or 40.7128N) or DMS format (e.g., 40° 42' 46.08\" N)")

    lat_input = st.text_input("Enter starting latitude: ")
    lon_input = st.text_input("Enter starting longitude: ")
    bearing_input = st.text_input("Enter bearing in degrees (0-360): ")
    distance_input = st.text_input("Enter distance in nautical miles: ")

    if lat_input and lon_input and bearing_input and distance_input:
        try:
            lat = parse_coordinates(lat_input, is_latitude=True)
            lon = parse_coordinates(lon_input, is_latitude=False)
            bearing = float(bearing_input)
            distance = float(distance_input)
        except ValueError as e:
            st.error(f"Error: {e}. Please try again.")
        else:
            dest_lat, dest_lon = calculate_destination(lat, lon, bearing, distance)

            st.write("\nStarting Point:")
            st.write(f"  Latitude: {format_dd_output(lat, True)}")
            st.write(f"  Longitude: {format_dd_output(lon, False)}")
            st.write(f"Bearing: {bearing}°")
            st.write(f"Distance: {distance} nautical miles")
            st.write("\nDestination Point:")
            st.write(f"  Latitude: {format_dd_output(dest_lat, True)}")
            st.write(f"  Longitude: {format_dd_output(dest_lon, False)}")
            st.write(f"  Decimal coordinates: {dest_lat:.6f}, {dest_lon:.6f}")

if __name__ == "__main__":
    main()
