"""Authentication service for Google authentication"""

import streamlit as st


def is_user_authenticated():
    """Check if user is authenticated via Google

    Returns:
        bool: True if user is authenticated, False otherwise
    """
    return st.session_state.get("connected", False)


def get_user_info():
    """Get current user information

    Returns:
        dict: User information or None if not authenticated
    """
    if st.session_state.get("connected", False):
        return {
            "type": "google",
            "info": st.session_state["user_info"],
            "connected": True,
        }
    return None
