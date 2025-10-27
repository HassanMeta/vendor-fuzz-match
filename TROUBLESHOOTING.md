# Troubleshooting Guide

## Invalid JWT Signature Error

If you encounter the error: `invalid_grant: Invalid JWT Signature`

This typically means there's an issue with your Google OAuth credentials or configuration.

### Common Causes and Solutions

#### 1. **Expired or Invalid Google OAuth Credentials**

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Navigate to "APIs & Services" → "Credentials"
- Verify your OAuth 2.0 Client ID is active
- Check if the credentials have expired

#### 2. **Redirect URI Mismatch**

The redirect URI in your `.streamlit/secrets.toml` must exactly match what's configured in Google Cloud Console.

**Current configuration in secrets.toml:**

```toml
REDIRECT_URI_GOOGLE="https://vendor-fuzz-match.streamlit.app/"
```

**To fix:**

1. Go to Google Cloud Console → Credentials → OAuth 2.0 Client
2. Add the exact URI (including trailing slash if present)
3. For local development, add: `http://localhost:8501/`
4. For production, add your Streamlit Cloud URL

#### 3. **JavaScript Origins Mismatch**

Make sure all origins are registered in Google Cloud Console:

- `http://localhost:8501` (for local development)
- `https://vendor-fuzz-match.streamlit.app` (for Streamlit Cloud)
- Any custom domain you're using

#### 4. **Credentials Not Properly Loaded**

If credentials are stored as a JSON string in secrets:

- Verify the JSON is properly escaped
- Check for any missing quotes or brackets
- Ensure the `google_credentials` secret is properly formatted

### Temporary Workaround

Until the JWT issue is resolved, users can still access the app using:

- **Email/Password authentication** (Login tab)

### Debug Mode

Click the "🐛 Debug Mode" button in the sidebar to view:

- Configuration details
- Session state information
- Credential validation status

### Regenerating Credentials

If you need to regenerate credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Credentials"
3. Click on your OAuth 2.0 Client ID
4. Download the new credentials JSON
5. Update the `google_credentials` secret in `.streamlit/secrets.toml`
6. Ensure all redirect URIs and JavaScript origins are properly configured

### Checking Current Configuration

Use the debug mode to check:

- ✅ Client ID is present
- ✅ Redirect URI matches your app URL
- ✅ Project ID matches between Firebase and Google OAuth

### Need More Help?

If the issue persists:

1. Check Streamlit logs for detailed error messages
2. Verify system time is synchronized (clock skew can cause JWT errors)
3. Ensure you're using the latest versions of authentication libraries
4. Contact support with error details from debug mode
