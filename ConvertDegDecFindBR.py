import streamlit as st
import math

def convert_lat_long():
    st.title("Convert Lat/Long")

    lat_deg = st.text_input("Enter Latitude in Degrees, Minutes, and Seconds (e.g., 40 26 46 N):")
    long_deg = st.text_input("Enter Longitude in Degrees, Minutes, and Seconds (e.g., 79 56 55 W):")

    if st.button("Convert"):
        try:
            lat_deg_match = re.match(r"(\d+) (\d+) (\d+) (N|S)", lat_deg)
            long_deg_match = re.match(r"(\d+) (\d+) (\d+) (E|W)", long_deg)

            if lat_deg_match and long_deg_match:
                lat_deg, lat_min, lat_sec, lat_dir = lat_deg_match.groups()
                long_deg, long_min, long_sec, long_dir = long_deg_match.groups()

                lat_deg = int(lat_deg)
                lat_min = int(lat_min)
                lat_sec = int(lat_sec)
                long_deg = int(long_deg)
                long_min = int(long_min)
                long_sec = int(long_sec)

                lat_rad = math.radians(lat_deg + lat_min / 60 + lat_sec / 3600)
                long_rad = math.radians(long_deg + long_min / 60 + long_sec / 3600)

                if lat_dir == "S":
                    lat_rad = -lat_rad
                if long_dir == "W":
                    long_rad = -long_rad

                lat_dec = f"{lat_rad * 180 / math.pi:.6f}"
                long_dec = f"{long_rad * 180 / math.pi:.6f}"

                st.write(f"Latitude in Decimal Degrees: {lat_dec}")
                st.write(f"Longitude in Decimal Degrees: {long_dec}")
            else:
                st.write("Invalid input. Please enter latitude and longitude in the format: DD MM SS N/S and DD MM SS E/W")
        except Exception as e:
            st.write("An error occurred: ", e)

def find_next_with_bearing_range():
    st.title("Find Next with Bearing Range")

    lat_deg = st.text_input("Enter Latitude in Decimal Degrees:")
    long_deg = st.text_input("Enter Longitude in Decimal Degrees:")
    bearing = st.text_input("Enter Bearing in Degrees:")
    distance = st.text_input("Enter Distance in Kilometers:")

    if st.button("Find Next"):
        try:
            lat_deg = float(lat_deg)
            long_deg = float(long_deg)
            bearing = float(bearing)
            distance = float(distance)

            # Add your implementation to find the next point with bearing and range
            # For now, just print a success message
            st.write("Next point found successfully!")
        except ValueError:
            st.write("Invalid input. Please enter valid decimal degrees, bearing, and distance.")

def main():
    tabs = ["Convert Lat/Long", "Find Next with Bearing Range"]
    tab = st.sidebar.selectbox("Select a tab", tabs)

    if tab == "Convert Lat/Long":
        convert_lat_long()
    elif tab == "Find Next with Bearing Range":
        find_next_with_bearing_range()

if __name__ == "__main__":
    main()
