elif tab == "Find Next with Bearing Range":
    st.title("Find Next with Bearing Range")

    lat_deg = st.text_input("Enter Starting Latitude (e.g., 40 26 46 N, 40.4462, 40 degrees 26 minutes 46 seconds N):")
    lon_deg = st.text_input("Enter Starting Longitude (e.g., 79 56 55 W, -79.9486, 79 degrees 56 minutes 55 seconds W):")
    bearing = st.text_input("Enter Bearing (in degrees):")
    distance_unit = st.selectbox("Distance Unit", ["nmi", "km", "mi"])
    distance = st.text_input("Enter Distance:")

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

            if distance_unit == "nmi":
                distance_km = distance * 1.852
            elif distance_unit == "km":
                distance_km = distance
            elif distance_unit == "mi":
                distance_km = distance * 1.60934

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
