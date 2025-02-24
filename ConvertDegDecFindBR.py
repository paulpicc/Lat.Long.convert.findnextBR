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
            st.write(f"Lat, Long: {latitude_decimal:.6f}, {longitude_decimal:.6f}")  # <--- Added this line

            st.write("Degrees, Minutes, Seconds (DMS):")
            st.write(f"Latitude: {format_dms(lat_degrees, lat_minutes, lat_seconds, 'N' if latitude_decimal >=0 else 'S')}")
            st.write(f"Longitude: {format_dms(long_degrees, long_minutes, long_seconds, 'E' if longitude_decimal >=0 else 'W')}")
