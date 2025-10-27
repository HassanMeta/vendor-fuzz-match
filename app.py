"""Main Streamlit authentication app"""

import streamlit as st
import pandas as pd
from config import initialize_firebase, get_google_authenticator
from auth_service import is_user_authenticated, get_user_info
from ui_components import (
    render_user_dashboard,
    render_authentication_forms,
)
from vendor_matching import process_vendor_dataframe

# Initialize Firebase
initialize_firebase()

# Initialize Google Authenticator
authenticator = get_google_authenticator()


def main():
    """Main application entry point"""
    st.title("🔐 Vendor Fuzz Match")
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

            # Main application content
            show_vendor_matcher()
    else:
        # User is not authenticated - show login options
        render_authentication_forms(authenticator)


def show_vendor_matcher():
    """Display vendor matching interface"""
    st.header("🔍 Vendor Matching Tool")
    st.markdown("Upload CSV files to identify and group similar vendor names")
    st.markdown("---")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file with vendor data",
        type=["csv"],
        help="CSV should have 'Vendor' and 'Amount' columns",
    )

    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)

            # Display preview
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # Check required columns
            if "Vendor" not in df.columns or "Amount" not in df.columns:
                st.error("⚠️ CSV must contain 'Vendor' and 'Amount' columns")
                return

            # Process data
            with st.spinner("Processing vendor data..."):
                result = process_vendor_dataframe(df)

            if "error" in result:
                st.error(result["error"])
                return

            # Display results
            st.markdown("---")
            st.subheader("📊 Matching Results")

            # Statistics
            stats = result["stats"]
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Vendors", stats["total_unique_vendors"])
            with col2:
                st.metric("Matched Groups", stats["matched_groups"])
            with col3:
                st.metric("Matched Vendors", stats["total_matched_vendors"])
            with col4:
                st.metric("Unmatched", stats["unmatched_vendors"])

            st.markdown("---")

            # Display matched groups
            if result["summary"]:
                st.subheader("🎯 Similar Vendor Groups")

                for idx, item in enumerate(result["summary"], 1):
                    with st.expander(f"Group {idx}: {item['Primary Name']}"):
                        st.write(f"**Primary Name:** {item['Primary Name']}")
                        st.write(f"**Variations Found:** {item['Variations']}")
                        if item["Total Amount"] != "N/A":
                            st.write(f"**Total Amount:** ${item['Total Amount']:,.2f}")
                        st.write("**All Variations:**")
                        st.code(item["Matched Names"], language="text")

            # Download results
            if result["summary"]:
                st.markdown("---")
                st.subheader("💾 Export Results")

                summary_df = pd.DataFrame(result["summary"])
                csv = summary_df.to_csv(index=False)

                st.download_button(
                    label="📥 Download Matched Groups CSV",
                    data=csv,
                    file_name="vendor_matches.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    else:
        # Show instructions
        st.info(
            "ℹ️ Upload a CSV file to get started. The file should contain 'Vendor' and 'Amount' columns."
        )

        # Show sample data
        if st.checkbox("Show sample data structure"):
            sample_df = pd.read_csv("vendor_transactions.csv")
            st.dataframe(sample_df.head(5), use_container_width=True)


if __name__ == "__main__":
    main()
