import streamlit as st
from crewai import Agent, Task, Crew, Process
import os
from config import SMTP_SERVER, SMTP_PORT, REPORT_TIME_HOUR, REPORT_TIME_MINUTE
from langchain_google_genai import ChatGoogleGenerativeAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# Set Google API Key as environment variable for langchain
# For Streamlit Cloud, secrets are accessed via st.secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# --- Streamlit UI ---
st.set_page_config(page_title="Gig Scraper App", layout="wide")
st.title("Freelance Gig Scraper")

st.markdown("""
This application helps you find relevant freelance gigs from various platforms.
Configure your preferences below and let the AI agents do the work!
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

# --- CrewAI Agent Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7) # Using gemini-pro as flash is not directly available in langchain_google_genai

# Define a placeholder tool for scraping. Real scraping tools would be more complex.
# For now, this will simulate scraping.
from crewai_tools import BaseTool

class GigScraperTool(BaseTool):
    name: str = "Gig Scraper Tool"
    description: str = "Scrapes freelance gig information from specified platforms."

    def _run(self, query: str, platforms: list) -> str:
        st.write(f"Simulating scraping for '{query}' on {', '.join(platforms)}...")
        # In a real scenario, this would involve actual web scraping using requests/BeautifulSoup
        # For demonstration, return dummy data
        if "Fiverr" in platforms:
            return f"Found a Python gig on Fiverr: 'Build a web scraper' - Budget: $100-200. Skills: Python, BeautifulSoup."
        if "Freelancer" in platforms:
            return f"Found a UI/UX design project on Freelancer: 'Design a mobile app UI' - Budget: $500-1000. Skills: Figma, Adobe XD."
        return "No gigs found for the given criteria."

gig_scraper_tool = GigScraperTool()

def run_gig_scraping_crew(query, platforms):
    gig_scraper_agent = Agent(
        role='Gig Scraper',
        goal=f'Scrape relevant freelance gigs for "{query}" from {", ".join(platforms)} using the Gig Scraper Tool.',
        backstory='An expert in finding the best freelance opportunities online, capable of using specialized tools to extract gig information.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[gig_scraper_tool]
    )

    gig_analysis_agent = Agent(
        role='Gig Analyzer',
        goal='Analyze scraped gigs and identify key details like pay, skills, and deadlines, then summarize them into a concise report.',
        backstory='A meticulous analyst who can extract crucial information from job postings and format it into a readable report.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    scrape_task = Task(
        description=f"Scrape gigs related to '{query}' from {', '.join(platforms)} using the 'Gig Scraper Tool'.",
        agent=gig_scraper_agent,
        expected_output="Raw text output from the Gig Scraper Tool containing gig details."
    )

    analyze_task = Task(
        description="Analyze the raw gig data provided by the Gig Scraper and summarize key details for each gig, including title, description, estimated pay, and required skills. Format the output as a clear, bulleted list.",
        agent=gig_analysis_agent,
        context=[scrape_task],
        expected_output="A structured report of gigs with their titles, descriptions, estimated pay, and required skills, formatted as a bulleted list."
    )

    project_crew = Crew(
        agents=[gig_scraper_agent, gig_analysis_agent],
        tasks=[scrape_task, analyze_task],
        verbose=2,
        process=Process.sequential
    )

    result = project_crew.kickoff()
    return result

# --- Email Sending Function ---
def send_email_report(recipient_email, report_content):
    # Access secrets from Streamlit's st.secrets
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
        report = run_gig_scraping_crew(query, platforms)
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
        
        # Run immediate scraping
        with st.spinner("Running CrewAI agents..."):
            gig_report = run_gig_scraping_crew(search_query, platforms)
        st.success("Scraping complete!")
        st.subheader("Scraping Results:")
        st.write(gig_report)

        # Schedule daily report if checked
        if daily_report:
            schedule_daily_report(search_query, platforms, recipient_email, report_time.hour, report_time.minute)
        else:
            st.info("Daily report not scheduled.")

# Note on Scheduling:
# For persistent daily reports, a Streamlit app deployed on Streamlit Cloud
# would typically require an external scheduling mechanism (e.g., a cron job
# on a separate server, or a cloud function that triggers the scraping logic).
# The `schedule` library used here will only run as long as the Streamlit app
# is actively open and running in a browser session.
# For this prototype, the scheduling function `schedule_daily_report` will
# set up the job, but its execution depends on the Streamlit app's lifecycle.

# --- Footer ---
st.sidebar.header("About")
st.sidebar.info("This app is a prototype for a freelance gig scraper using Streamlit and CrewAI.")
