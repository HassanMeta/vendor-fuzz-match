# Vendor Fuzz Match Application

A Streamlit application for matching vendor transactions with fuzzy string matching capabilities.

## Features

- ✅ Google OAuth authentication
- ✅ Vendor transaction data management
- ✅ Fuzzy matching to identify similar vendor names
- ✅ Modular codebase for easy maintenance

## Project Structure

```
.
├── app.py                 # Main application entry point
├── config.py             # Firebase & Google Auth configuration
├── auth_service.py       # Authentication service
├── ui_components.py      # UI components
├── vendor_transactions.csv # Sample transaction data
└── requirements.txt      # Python dependencies
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Secrets

Create `.streamlit/secrets.toml` with your Firebase and Google OAuth credentials.

### 3. Run the Application

```bash
streamlit run app.py
```

## Deployment

### Render.com

This project is optimized for deployment on Render.com with:

- Fast build times (1-2 minutes)
- Minimal dependencies
- Production-ready configuration

See `DEPLOYMENT_OPTIMIZATION.md` for deployment details.

## Sample Data

The `vendor_transactions.csv` file contains:

- **350+ transactions** from 2 years of data
- **116 unique vendor name variations**
- Includes real-world name variations (e.g., "John Doe", "Doe John", "JohnDoe")
- Transaction amounts ranging from $100 to $10,000

## License

MIT
