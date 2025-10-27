"""UI components for authentication forms"""

import streamlit as st
from auth_service import (
    sign_in_with_email_password,
    create_user_with_email_password,
    reset_password,
)


def render_user_dashboard(user_info):
    """Render the authenticated user dashboard

    Args:
        user_info: Dictionary containing user information
    """
    auth_type = user_info.get("type")
    info = user_info.get("info")

    if auth_type == "google":
        st.success("✅ Logged in with Google")

        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(info.get("picture"), width=80)
        with col2:
            st.write(f"**Name:** {info.get('name')}")
            st.write(f"**Email:** {info.get('email')}")
    else:
        st.success("✅ Logged in with Email")
        st.write(f"**Name:** {info.get('displayName', 'User')}")
        st.write(f"**Email:** {info.get('email')}")


def render_login_tab():
    """Render the login form tab"""
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if email and password:
                result = sign_in_with_email_password(email, password)
                if "idToken" in result:
                    st.session_state.email_user = result
                    st.success("Login successful!")
                    st.rerun()
                else:
                    error_msg = result.get("error", {}).get("message", "Login failed")
                    st.error(f"❌ {error_msg}")
            else:
                st.warning("Please enter both email and password")


def render_register_tab():
    """Render the registration form tab"""
    with st.form("register_form"):
        name = st.text_input("Display Name")
        email = st.text_input("Email Address", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if not all([name, email, password, confirm_password]):
                st.warning("Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords don't match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                result = create_user_with_email_password(email, password, name)
                if result.get("success"):
                    st.success("✅ Account created! Please login.")
                else:
                    st.error(f"❌ {result.get('error', 'Registration failed')}")


def render_reset_password_tab():
    """Render the password reset form tab"""
    with st.form("reset_form"):
        email = st.text_input("Enter your email address", key="reset_email")
        submit = st.form_submit_button("Send Reset Link")

        if submit:
            if email:
                result = reset_password(email)
                if "email" in result:
                    st.success("✅ Password reset email sent! Check your inbox.")
                else:
                    st.error(f"❌ {result.get('error', 'Failed to send reset email')}")
            else:
                st.warning("Please enter your email address")


def render_authentication_forms(authenticator):
    """Render all authentication forms (Google and Email/Password)

    Args:
        authenticator: Google authenticator instance
    """
    st.subheader("Please login to continue")

    # Google Login Button
    st.markdown("### 🔵 Login with Google")

    # Show warning if there's a Google auth error
    if st.session_state.get("google_auth_error"):
        st.warning(
            "⚠️ Google authentication is currently unavailable. "
            "Please use email/password login or contact support if this persists."
        )

    try:
        authenticator.login()
    except Exception as e:
        error_str = str(e)
        # Only show non-JWT errors
        if "invalid_grant" not in error_str and "Invalid JWT" not in error_str:
            st.error(f"Google login error: {str(e)}")

    st.markdown("---")

    # Email/Password Login
    st.markdown("### 📧 Login with Email")

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Reset Password"])

    with tab1:
        render_login_tab()

    with tab2:
        render_register_tab()

    with tab3:
        render_reset_password_tab()


def render_protected_content():
    """Render content that is only visible to authenticated users"""
    st.markdown("---")
    st.subheader("🎉 Welcome to Your App!")
    st.write("This content is only visible to authenticated users.")
