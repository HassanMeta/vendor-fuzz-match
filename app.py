import streamlit as st
from streamlit_google_auth import Authenticate
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase_auth_token"]))
    firebase_admin.initialize_app(cred)


# Initialize Google Authenticator
authenticator = Authenticate(
    secret_credentials_path=json.loads(st.secrets["google_credentials"]),
    cookie_name="streamlit_auth_cookie",
    cookie_key=st.secrets["COOKIE_KEY"],
    redirect_uri=st.secrets["REDIRECT_URI_GOOGLE"],
    cookie_expiry_days=30,
)

# Firebase REST API URL
REST_API_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


def sign_in_with_email_password(email, password):
    """Sign in user with email and password using Firebase"""
    url = f"{REST_API_URL}:signInWithPassword?key={st.secrets['FIREBASE_API_KEY']}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def create_user_with_email_password(email, password, display_name):
    """Create new user account with Firebase"""
    try:
        user = auth.create_user(
            email=email, password=password, display_name=display_name
        )
        return {"success": True, "uid": user.uid}
    except Exception as e:
        return {"error": str(e)}


def reset_password(email):
    """Send password reset email"""
    url = f"{REST_API_URL}:sendOobCode?key={st.secrets['FIREBASE_API_KEY']}"
    payload = {"requestType": "PASSWORD_RESET", "email": email}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    st.title("🔐 Streamlit Authentication App")
    st.markdown("---")

    # Check Google authentication
    authenticator.check_authentification()

    # Initialize session state for email/password auth
    if "email_user" not in st.session_state:
        st.session_state.email_user = None

    # Check if user is logged in (either Google or Email/Password)
    if st.session_state.get("connected", False) or st.session_state.email_user:
        # User is authenticated
        if st.session_state.get("connected", False):
            # Google authentication
            user_info = st.session_state["user_info"]
            st.success("✅ Logged in with Google")

            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(user_info.get("picture"), width=80)
            with col2:
                st.write(f"**Name:** {user_info.get('name')}")
                st.write(f"**Email:** {user_info.get('email')}")

            if st.button("🚪 Logout"):
                authenticator.logout()
                st.rerun()

        elif st.session_state.email_user:
            # Email/Password authentication
            st.success("✅ Logged in with Email")
            st.write(
                f"**Name:** {st.session_state.email_user.get('displayName', 'User')}"
            )
            st.write(f"**Email:** {st.session_state.email_user.get('email')}")

            if st.button("🚪 Logout"):
                st.session_state.email_user = None
                st.rerun()

        # Your protected app content goes here
        st.markdown("---")
        st.subheader("🎉 Welcome to Your App!")
        st.write("This content is only visible to authenticated users.")

    else:
        # User is not authenticated - show login options
        st.subheader("Please login to continue")

        # Google Login Button
        st.markdown("### 🔵 Login with Google")
        authenticator.login()

        st.markdown("---")

        # Email/Password Login
        st.markdown("### 📧 Login with Email")

        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Reset Password"])

        with tab1:
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
                            error_msg = result.get("error", {}).get(
                                "message", "Login failed"
                            )
                            st.error(f"❌ {error_msg}")
                    else:
                        st.warning("Please enter both email and password")

        with tab2:
            with st.form("register_form"):
                name = st.text_input("Display Name")
                email = st.text_input("Email Address", key="reg_email")
                password = st.text_input(
                    "Password", type="password", key="reg_password"
                )
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

        with tab3:
            with st.form("reset_form"):
                email = st.text_input("Enter your email address", key="reset_email")
                submit = st.form_submit_button("Send Reset Link")

                if submit:
                    if email:
                        result = reset_password(email)
                        if "email" in result:
                            st.success(
                                "✅ Password reset email sent! Check your inbox."
                            )
                        else:
                            st.error(
                                f"❌ {result.get('error', 'Failed to send reset email')}"
                            )
                    else:
                        st.warning("Please enter your email address")


if __name__ == "__main__":
    main()
