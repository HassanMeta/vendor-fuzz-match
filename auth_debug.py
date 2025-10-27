"""Debug utilities for authentication issues"""

import streamlit as st
import json
from datetime import datetime
import sys


def display_auth_debug_info():
    """Display debug information for authentication issues"""
    with st.expander("🔍 Debug Information (for developers)"):
        st.write("### Configuration")
        st.write(f"**Python Version:** {sys.version}")
        st.write(f"**Current Time:** {datetime.now()}")

        # Check for environment
        if st.secrets.get("STREAMLIT_RUNTIME_ENV"):
            st.write(f"**Environment:** {st.secrets['STREAMLIT_RUNTIME_ENV']}")

        # Check session state
        st.write("### Session State")
        auth_keys = ["connected", "email_user", "google_auth_error"]
        for key in auth_keys:
            if key in st.session_state:
                st.write(f"**{key}:** {str(st.session_state[key])[:100]}")

        # Check if Google credentials are valid JSON
        try:
            google_creds = json.loads(st.secrets["google_credentials"])
            st.success("✅ Google credentials are valid JSON")
            st.write(
                f"**Client ID:** {google_creds.get('web', {}).get('client_id', 'Not found')}"
            )
        except Exception as e:
            st.error(f"❌ Google credentials JSON error: {str(e)}")

        # Check Firebase auth token
        try:
            fb_token = dict(st.secrets["firebase_auth_token"])
            st.success("✅ Firebase auth token is valid")
            st.write(f"**Project ID:** {fb_token.get('project_id', 'Not found')}")
        except Exception as e:
            st.error(f"❌ Firebase auth token error: {str(e)}")
