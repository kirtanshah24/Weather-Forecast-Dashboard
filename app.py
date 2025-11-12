# app.py
import streamlit as st
from utils.api import get_current_weather

# Page config
st.set_page_config(
    page_title="Vayu - Weather Dashboard",
    page_icon="cloud",
    layout="centered"
)

# Title
st.title("cloud Vayu")
st.subheader("Real-time Weather Dashboard")

# Input
city = st.text_input("Enter city name:", placeholder="e.g., Mumbai, Delhi, London")

if city:
    with st.spinner(f"Fetching weather for **{city}**..."):
        weather_data = get_current_weather(city)

    if weather_data and "error" not in weather_data:
        # Success - Display weather
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(weather_data["icon"], width=100)
        
        with col2:
            st.markdown(f"""
            ### {weather_data['city']}, {weather_data['region']}
            #### {weather_data['condition']}
            """)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{weather_data['temp_c']}°C")
        with col2:
            st.metric("Feels Like", f"{weather_data['feels_like_c']}°C")
        with col3:
            st.metric("Humidity", f"{weather_data['humidity']}%")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Wind Speed", f"{weather_data['wind_kph']} kph")
        with col2:
            st.caption(f"Data from WeatherAPI • Updated just now")

    elif weather_data and "error" in weather_data:
        st.error(f"Error: {weather_data['error']}")
    else:
        st.warning("No data received. Please try again.")

else:
    st.info("Enter a city name above to see real-time weather!")

# Footer
st.markdown("---")
st.caption("Built with love using Streamlit | Powered by WeatherAPI")