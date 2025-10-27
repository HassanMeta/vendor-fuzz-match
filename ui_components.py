"""UI components for authentication forms"""

import streamlit as st


def render_user_dashboard(user_info):
    """Render the authenticated user dashboard

    Args:
        user_info: Dictionary containing user information
    """
    info = user_info.get("info")

    st.success("✅ Logged in with Google")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(info.get("picture"), width=80)
    with col2:
        st.write(f"**Name:** {info.get('name')}")
        st.write(f"**Email:** {info.get('email')}")


def render_authentication_forms(authenticator):
    """Render authentication forms (Google only)

    Args:
        authenticator: Google authenticator instance
    """
    st.subheader("Please login to continue")

    # Google Login Button
    st.markdown("### 🔵 Login with Google")
    authenticator.login()


def render_protected_content():
    """Render content that is only visible to authenticated users"""
    st.markdown("---")
    st.subheader("🎉 Welcome to Your App!")
    st.write("This content is only visible to authenticated users.")
