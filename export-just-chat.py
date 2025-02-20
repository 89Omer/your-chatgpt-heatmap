import json
import pandas as pd
from datetime import datetime

# Load exported ChatGPT data
CHATGPT_EXPORT_FILE = "conversations.json"
OUTPUT_CSV = "chat_usage_log.csv"

def extract_user_messages():
    with open(CHATGPT_EXPORT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    extracted_data = []

    for convo in data:
        for msg in convo.get("mapping", {}).values():
            if msg.get("message") and msg["message"].get("author", {}).get("role") == "user":
                timestamp = msg["message"]["create_time"]
                dt_object = datetime.fromtimestamp(timestamp)  # Convert Unix timestamp
                
                extracted_data.append([
                    dt_object.strftime("%Y-%m-%d"),  # Date
                    dt_object.strftime("%H"),  # Hour
                    dt_object.strftime("%Y"),  # Year
                    dt_object.strftime("%m")   # Month
                ])

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(extracted_data, columns=["Date", "Hour", "Year", "Month"])
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Extracted data saved to {OUTPUT_CSV}")

# Run extraction
extract_user_messages()
