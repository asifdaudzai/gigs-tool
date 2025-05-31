import os

# API Keys (replace with your actual keys or set as environment variables)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY") # Example for a search tool

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD") # App password for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Other configurations
REPORT_TIME_HOUR = 18 # 6 PM
REPORT_TIME_MINUTE = 0 # 00 minutes
