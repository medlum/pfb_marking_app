from twilio.rest import Client
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button


account_sid = st.secrets.twilio.account_sid

auth_token = st.secrets.twilio.auth_token
client = Client(account_sid, auth_token)

def send_sms_txt(body):
    try:
        client.messages.create(
            from_='+17087266912',
            body=body,
            to='+6594235231'
        )
    except Exception:
        st.warning("Twilio SMS limit reached")

import streamlit as st

# Custom CSS for floating button
floating_button_css = """
<link href="https://fonts.googleapis.com/css2?family=Cookie&display=swap" rel="stylesheet">
<style>
    .floating-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #ffdd00;
        color: #4B382A !important;
        padding: 5px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 550;
        font-size: 25px;
        font-family: 'Cookie', cursive;
        text-decoration: none !important;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
        display: inline-block;
    }
    .floating-button:hover {
        background-color: #ffcc00;
        transform: scale(1.1);
    }
    .floating-button a {
        color: inherit !important;
        text-decoration: none !important;
        display: inline-block;
        width: 100%;
        height: 100%;
    }
</style>
"""

# HTML for Buy Me a Coffee button
floating_button_html = """
<a class="floating-button" href="https://buymecoffee.streamlit.app" target="_blank">☕ Buy Me a Coffee</a>
"""

# Inject HTML and CSS
#st.markdown(floating_button_css, unsafe_allow_html=True)
#st.markdown(floating_button_html, unsafe_allow_html=True)


