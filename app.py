"""Main Streamlit authentication app"""

import streamlit as st
from config import initialize_firebase, get_google_authenticator
from auth_service import is_user_authenticated, get_user_info, logout
from ui_components import (
    render_user_dashboard,
    render_authentication_forms,
    render_protected_content,
)
from auth_debug import display_auth_debug_info

# Initialize Firebase
initialize_firebase()

# Initialize Google Authenticator
authenticator = get_google_authenticator()


def main():
    """Main application entry point"""
    st.title("🔐 Streamlit Authentication App")
    st.markdown("---")

    # Debug mode (only for development)
    if st.sidebar.button("🐛 Debug Mode"):
        display_auth_debug_info()

    # Check Google authentication
    try:
        authenticator.check_authentification()
    except Exception as e:
        # Log the error but don't show it to the user immediately
        # to prevent disruption of the UI
        error_str = str(e)
        if "invalid_grant" in error_str or "Invalid JWT" in error_str:
            # Handle JWT/credential issues gracefully
            if st.session_state.get("google_auth_error"):
                if st.sidebar.button("🔄 Retry Google Login"):
                    st.session_state.google_auth_error = False
                    st.rerun()
            else:
                st.session_state.google_auth_error = True
        else:
            # For other errors, log them
            st.error(f"Authentication error: {error_str}")

    # Initialize session state for email/password auth
    if "email_user" not in st.session_state:
        st.session_state.email_user = None

    # Check if user is authenticated
    if is_user_authenticated():
        # User is authenticated - show dashboard
        user_info = get_user_info()

        if user_info and user_info.get("connected"):
            render_user_dashboard(user_info)

            # Logout button
            if st.button("🚪 Logout"):
                if user_info.get("type") == "google":
                    authenticator.logout()
                else:
                    logout()
                st.rerun()

            # Protected content
            render_protected_content()
    else:
        # User is not authenticated - show login options
        render_authentication_forms(authenticator)


if __name__ == "__main__":
    main()
