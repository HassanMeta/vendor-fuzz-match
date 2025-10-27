"""Configuration and initialization for Firebase and Google Auth"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials
from streamlit_google_auth import Authenticate
import json
import tempfile


def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized"""
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_auth_token"]))
        firebase_admin.initialize_app(cred)


def get_google_authenticator():
    """Initialize and return Google Authenticator"""
    # Parse Google credentials from secrets
    google_creds_dict = json.loads(st.secrets["google_credentials"])

    # Write Google credentials to a temporary file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".json"
    ) as temp_file:
        json.dump(google_creds_dict, temp_file)
        google_creds_path = temp_file.name

    # Initialize Google Authenticator
    authenticator = Authenticate(
        secret_credentials_path=google_creds_path,
        cookie_name="streamlit_auth_cookie",
        cookie_key=st.secrets["COOKIE_KEY"],
        redirect_uri=st.secrets["REDIRECT_URI_GOOGLE"],
        cookie_expiry_days=30,
    )

    return authenticator


def get_firebase_api_key():
    """Get Firebase API Key from secrets"""
    return st.secrets["FIREBASE_API_KEY"]


def get_rest_api_url():
    """Get Firebase REST API base URL"""
    return "https://identitytoolkit.googleapis.com/v1/accounts"
