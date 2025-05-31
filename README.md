# Freelance Gig Scraper App

Developed by Asif Ullah

---

## Overview

This is an open-source Streamlit application designed to help users find relevant freelance gigs from various platforms such as Fiverr, Freelancer, Upwork, and Guru. The app leverages AI agents powered by CrewAI and Langchain's Google Generative AI to simulate scraping and analyzing freelance gig data, providing users with concise and useful gig reports.

Users can configure their search preferences, select platforms to scrape from, and opt to receive daily email reports with gig summaries.

---

## Features

- Search for freelance gigs by keyword across multiple platforms.
- AI-powered scraping simulation and gig analysis.
- Daily email reports with gig summaries.
- Scheduling of daily scraping and report sending.
- Easy-to-use Streamlit interface.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/asifdaudzai/gigs-tool.git
   cd gigs-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for API keys and email credentials (e.g., in a `.env` file or your system environment):
   - `GOOGLE_API_KEY`
   - `SENDER_EMAIL`
   - `SENDER_EMAIL_PASSWORD`

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## Contributing

This project is open source and welcomes contributions from the community. If you want to contribute, please feel free to:

- Report issues or bugs.
- Suggest new features or improvements.
- Submit pull requests with enhancements or fixes.

Please follow standard GitHub contribution guidelines.

---

## Managing Secrets

This project uses Streamlit's secrets management to securely handle sensitive information such as API keys, email credentials, and database connection details.

To set up your secrets, create a file named `secrets.toml` inside a `.streamlit` directory at the root of the project:

```
.streamlit/secrets.toml
```

Example contents of `secrets.toml`:

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
SENDER_EMAIL = "your-email@example.com"
SENDER_EMAIL_PASSWORD = "your-email-app-password"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "gigsdb"
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"
```

Replace the placeholder values with your actual credentials.

Streamlit will automatically load these secrets and make them available via `st.secrets` in the app.

---

## License

This project is licensed under the MIT License.

---

## Contact

For any questions or feedback, please reach out to Asif Ullah.


