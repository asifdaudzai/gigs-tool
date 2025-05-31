import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from config import SMTP_SERVER, SMTP_PORT, REPORT_TIME_HOUR, REPORT_TIME_MINUTE
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# Set Google API Key as environment variable for langchain
google_api_key = st.secrets.get("GOOGLE_API_KEY", None)
if not google_api_key:
    st.error("Google API key is not set in Streamlit secrets. Please add GOOGLE_API_KEY.")
else:
    os.environ["GOOGLE_API_KEY"] = google_api_key

# --- Streamlit UI ---
st.set_page_config(page_title="Gig Scraper App", layout="wide")
st.title("Freelance Gig Scraper")

st.markdown("""
This application helps you find relevant freelance gigs from various platforms.
Configure your preferences below and let the AI do the work!
""")

# User inputs for gig search
search_query = st.text_input("Enter your desired gig (e.g., 'Python Developer', 'UI/UX Designer'):")
platforms = st.multiselect(
    "Select platforms to scrape from:",
    ["Fiverr", "Freelancer", "Upwork", "Guru"],
    default=["Fiverr", "Freelancer"]
)
daily_report = st.checkbox("Send daily report to email?", value=True)
report_time = st.time_input("Report time (24-hour format):", value="18:00")
recipient_email = st.text_input("Recipient Email for daily reports:")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="models/chat-bison-001", temperature=0.7)

def simulate_scraping(query, platforms):
    # Simulate scraping with dummy data
    results = []
    if "Fiverr" in platforms:
        results.append(f"Found a Python gig on Fiverr: 'Build a web scraper' - Budget: $100-200. Skills: Python, BeautifulSoup.")
    if "Freelancer" in platforms:
        results.append(f"Found a UI/UX design project on Freelancer: 'Design a mobile app UI' - Budget: $500-1000. Skills: Figma, Adobe XD.")
    if not results:
        results.append("No gigs found for the given criteria.")
    return "\n".join(results)

def analyze_gigs(raw_text):
    prompt = f"""
You are an expert analyst. Analyze the following gig listings and summarize key details like title, description, estimated pay, and required skills in a bulleted list:

{raw_text}

Summary:
"""
    try:
        response = llm.predict(prompt)
    except Exception as e:
        st.error(f"Error during AI analysis: {e}")
        return "Analysis failed due to an error with the AI service. Please check your API key and configuration."
    return response

def run_gig_scraping_and_analysis(query, platforms):
    raw_gigs = simulate_scraping(query, platforms)
    analysis = analyze_gigs(raw_gigs)
    return analysis

# --- Email Sending Function ---
def send_email_report(recipient_email, report_content):
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_email_password = st.secrets["SENDER_EMAIL_PASSWORD"]

    if not sender_email or not sender_email_password:
        st.error("Sender email credentials are not configured. Please set SENDER_EMAIL and SENDER_EMAIL_PASSWORD in Streamlit secrets.")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily Freelance Gig Report"

    msg.attach(MIMEText(report_content, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_email_password)
            server.send_message(msg)
        st.success(f"Daily report sent to {recipient_email}!")
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        st.warning("Please ensure your sender email and app password are correct and that less secure app access is enabled for your Gmail account if you are not using an app password.")
        return False

# --- Scheduling Function ---
def schedule_daily_report(query, platforms, recipient_email, report_hour, report_minute):
    def job():
        st.info(f"Running scheduled scraping for '{query}' on {', '.join(platforms)}...")
        report = run_gig_scraping_and_analysis(query, platforms)
        send_email_report(recipient_email, report)

    schedule.every().day.at(f"{report_hour:02d}:{report_minute:02d}").do(job)
    st.success(f"Daily report scheduled for {report_hour:02d}:{report_minute:02d} to {recipient_email}.")
    st.info("The scheduler will run in the background. Keep this Streamlit app running for the scheduler to work.")

# --- Streamlit UI Logic ---
if st.button("Start Scraping"):
    if not search_query:
        st.error("Please enter a search query.")
    elif not platforms:
        st.error("Please select at least one platform.")
    elif daily_report and not recipient_email:
        st.error("Please enter a recipient email for daily reports.")
    else:
        st.info("Starting the gig scraping process...")

        with st.spinner("Running AI analysis..."):
            gig_report = run_gig_scraping_and_analysis(search_query, platforms)
        st.success("Scraping and analysis complete!")
        st.subheader("Scraping Results:")
        st.write(gig_report)

        if daily_report:
            schedule_daily_report(search_query, platforms, recipient_email, report_time.hour, report_time.minute)
        else:
            st.info("Daily report not scheduled.")

# --- Footer ---
st.sidebar.header("About")
st.sidebar.info("This app is a prototype for a freelance gig scraper using Streamlit and Google Generative AI.")
