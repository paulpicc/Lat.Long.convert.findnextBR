# lat_long_convert.py

import re
import streamlit as st

def parse_coordinates(coord_str):
    """Parses coordinates from various formats (decimal or DMS) to decimal degrees."""
    coord_str = coord_str.strip("[]").replace("°", " ").replace("'", " ").replace('"', ' ')  # Clean up

    try:
        return float(coord_str)  # Decimal format
    except ValueError:
        try:
            parts = coord_str.split()
            degrees = float(parts[0])
            minutes = float(parts[1]) if len(parts) > 1 else 0
            seconds = float(parts[2]) if len(parts) > 2 else 0
            direction = parts[-1].upper() if parts[-1].upper() in ('N', 'S', 'E', 'W') else ''

            decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
            if direction in ('S', 'W'):
                decimal_degrees *= -1
            return decimal_degrees
        except (ValueError, IndexError):
            return None

def decimal_to_dms(decimal_degrees):
    """Converts decimal degrees to DMS (degrees, minutes, seconds)."""
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = (decimal_degrees - degrees - minutes / 60) * 3600
    return degrees, minutes, seconds

def format_dms(degrees, minutes, seconds, direction=""):
    """Formats DMS coordinates for display."""
    return f"{degrees}°{minutes}'{seconds:.2f}\"{direction}"

def main():
    """Main function to handle coordinate conversion."""
    st.title("Convert Lat/Long between Degree-Decimal")

    latitude_decimal = st.text_input("Enter latitude (e.g., 37.7749 or 37°47'29.6\"N): ")
    longitude_decimal = st.text_input("Enter longitude (e.g., -122.4194 or 122°25'10.1\"W): ")

    if latitude_decimal and longitude_decimal:
        latitude_decimal = parse_coordinates(latitude_decimal)
        longitude_decimal = parse_coordinates(longitude_decimal)

        if latitude_decimal is not None and longitude_decimal is not None:
            # Display in other formats
            lat_degrees, lat_minutes, lat_seconds = decimal_to_dms(latitude_decimal)
            long_degrees, long_minutes, long_seconds = decimal_to_dms(longitude_decimal)

            st.write("Decimal Degrees:")
            st.write(f"Latitude: {latitude_decimal:.6f}")
            st.write(f"Longitude: {longitude_decimal:.6f}")
            st.write(f"Lat, Long: {latitude_decimal:.6f}, {longitude_decimal:.6f}")

            st.write("Degrees, Minutes, Seconds (DMS):")
            st.write(f"Latitude: {format_dms(lat_degrees, lat_minutes, lat_seconds, 'N' if latitude_decimal >=0 else 'S')}")
            st.write(f"Longitude: {format_dms(long_degrees, long_minutes, long_seconds, 'E' if longitude_decimal >=0 else 'W')}")

if __name__ == "__main__":
    main()
