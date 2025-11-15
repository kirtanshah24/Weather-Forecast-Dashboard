# app.py
import streamlit as st
from utils.api import get_current_weather, search_cities

# Page config
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="cloud",
    layout="centered"
)

# Title
st.title("cloud Vayu")
st.subheader("Real-time Weather Dashboard")

# Session state to store selected city
if "selected_city" not in st.session_state:
    st.session_state.selected_city = ""

# Search input with autocomplete
search_query = st.text_input(
    "Search for a city:",
    placeholder="Type city name (e.g., Mumbai, Lon, New York)",
    key="search_input"
)

# Show suggestions only if typing
if search_query and len(search_query) >= 2:
    with st.spinner("Searching cities..."):
        suggestions = search_cities(search_query)
    
    if suggestions:
        city_names = [s["name"] for s in suggestions]
        selected = st.selectbox(
            "Did you mean:",
            options=city_names,
            index=None,
            placeholder="Select a city from suggestions",
            key="city_select"
        )
        if selected:
            st.session_state.selected_city = selected
            st.success(f"Selected: **{selected}**")
    else:
        st.warning("No cities found. Try another name.")
else:
    st.session_state.selected_city = ""

# Use selected city or fallback to manual input
final_city = st.session_state.selected_city or search_query

# Fetch weather if city is valid
if final_city and len(final_city) >= 2:
    with st.spinner(f"Fetching weather for **{final_city}**..."):
        weather_data = get_current_weather(final_city)

    if weather_data and "error" not in weather_data:
        # Success Display
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(weather_data["icon"], width=120)
        with col2:
            st.markdown(f"""
            ### {weather_data['city']}, {weather_data['region']}
            #### {weather_data['condition']}
            """)

        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Temperature", f"{weather_data['temp_c']}°C")
        with m2:
            st.metric("Feels Like", f"{weather_data['feels_like_c']}°C")
        with m3:
            st.metric("Humidity", f"{weather_data['humidity']}%")

        m4, m5 = st.columns(2)
        with m4:
            st.metric("Wind", f"{weather_data['wind_kph']} kph")
        with m5:
            st.caption("Data from WeatherAPI")

        # Refresh button
        if st.button("Refresh Data"):
            st.rerun()

    elif weather_data and "error" in weather_data:
        st.error(f"Error: {weather_data['error']}")
    else:
        st.warning("No data. Please try a valid city.")

else:
    st.info("Start typing a city name to see suggestions!")

# Footer
st.markdown("---")
st.caption("Built with love using Streamlit | Powered by WeatherAPI")