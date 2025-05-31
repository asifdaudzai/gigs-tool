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

## License

This project is licensed under the MIT License.

---

## Contact

For any questions or feedback, please reach out to Asif Ullah.


