"""Main Streamlit authentication app"""

import streamlit as st
from config import initialize_firebase, get_google_authenticator
from auth_service import is_user_authenticated, get_user_info
from ui_components import (
    render_user_dashboard,
    render_authentication_forms,
    render_protected_content,
)

# Initialize Firebase
initialize_firebase()

# Initialize Google Authenticator
authenticator = get_google_authenticator()


def main():
    """Main application entry point"""
    st.title("🔐 Streamlit Authentication App")
    st.markdown("---")

    # Check Google authentication
    authenticator.check_authentification()

    # Check if user is authenticated
    if is_user_authenticated():
        # User is authenticated - show dashboard
        user_info = get_user_info()

        if user_info and user_info.get("connected"):
            render_user_dashboard(user_info)

            # Logout button
            if st.button("🚪 Logout"):
                authenticator.logout()
                st.rerun()

            # Protected content
            render_protected_content()
    else:
        # User is not authenticated - show login options
        render_authentication_forms(authenticator)


if __name__ == "__main__":
    main()
