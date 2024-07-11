import streamlit as st
import requests
from bs4 import BeautifulSoup

#css to beautify 
def inject_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }

        h1 {
            color: #FF6347;
            text-align: center;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .stSelectbox, .stSelectbox>div>div>div>div {
            color: #FF6347;
            background-color: #333333;
        }

        .stMarkdown, .stMarkdown>div>div>div>div {
            color: #FFFFFF;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

# Function to fetch the horoscope
def horoscope(zodiac_sign: int, period: str, day: str = None) -> str:
    base_url = "https://www.horoscope.com/us/horoscopes/"
    if period == "daily":
        url = f"{base_url}general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}"
    elif period == "weekly":
        url = f"{base_url}general/horoscope-general-weekly.aspx?sign={zodiac_sign}"
    elif period == "monthly":
        url = f"{base_url}general/horoscope-general-monthly.aspx?sign={zodiac_sign}"
    else:
        return "Invalid period specified."

    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return "Failed to retrieve horoscope. Please try again later."
    
    soup = BeautifulSoup(response.content, "html.parser")
    horoscope_div = soup.find("div", class_="main-horoscope")
    if horoscope_div and horoscope_div.p:
        return horoscope_div.p.text
    else:
        return "Could not find the horoscope. Please try again later."

# Mapping of zodiac signs to their numbers
zodiac_signs = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12,
}

# List of days
days = ["yesterday", "today", "tomorrow"]

#injecting the css before the streamlit ui
inject_css()

# Streamlit UI
st.title("Horoscope")

# Zodiac sign selection
zodiac_sign = st.selectbox("Select your Zodiac sign", list(zodiac_signs.keys()))

# Period selection
period = st.selectbox("Select the period", ["daily", "weekly", "monthly"])

# Day selection for daily horoscope
day = None
if period == "daily":
    day = st.selectbox("Select the day", days)

# Button to fetch horoscope
if st.button("Get Horoscope"):
    with st.spinner("Fetching your horoscope..."):
        horoscope_text = horoscope(zodiac_signs[zodiac_sign], period, day)
    st.write(horoscope_text)
