"""Authentication service for email/password authentication"""

import requests
import streamlit as st
from firebase_admin import auth as firebase_auth
from config import get_rest_api_url, get_firebase_api_key


def sign_in_with_email_password(email, password):
    """Sign in user with email and password using Firebase

    Args:
        email: User email address
        password: User password

    Returns:
        dict: Response containing auth token or error
    """
    url = f"{get_rest_api_url()}:signInWithPassword?key={get_firebase_api_key()}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def create_user_with_email_password(email, password, display_name):
    """Create new user account with Firebase

    Args:
        email: User email address
        password: User password
        display_name: User display name

    Returns:
        dict: Response containing user ID or error
    """
    try:
        user = firebase_auth.create_user(
            email=email, password=password, display_name=display_name
        )
        return {"success": True, "uid": user.uid}
    except Exception as e:
        return {"error": str(e)}


def reset_password(email):
    """Send password reset email

    Args:
        email: User email address

    Returns:
        dict: Response from Firebase
    """
    url = f"{get_rest_api_url()}:sendOobCode?key={get_firebase_api_key()}"
    payload = {"requestType": "PASSWORD_RESET", "email": email}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def is_user_authenticated():
    """Check if user is authenticated (either via Google or Email/Password)

    Returns:
        bool: True if user is authenticated, False otherwise
    """
    return (
        st.session_state.get("connected", False)
        or st.session_state.get("email_user") is not None
    )


def get_user_info():
    """Get current user information

    Returns:
        dict: User information or None if not authenticated
    """
    if st.session_state.get("connected", False):
        # Google authentication
        return {
            "type": "google",
            "info": st.session_state["user_info"],
            "connected": True,
        }
    elif st.session_state.get("email_user"):
        # Email/Password authentication
        return {"type": "email", "info": st.session_state.email_user, "connected": True}
    return None


def logout():
    """Logout the current user"""
    if st.session_state.get("connected", False):
        st.session_state.email_user = None
        # Reset Google auth will be handled by authenticator.logout()
    else:
        st.session_state.email_user = None
