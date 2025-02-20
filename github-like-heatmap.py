import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np
import calendar

# Load chat usage data
LOG_FILE = "chat_usage_log.csv"

def load_data():
    df = pd.read_csv(LOG_FILE, parse_dates=["Date"])  # Ensure "Date" is parsed as datetime
    df["Year"] = df["Date"].dt.year
    return df

def generate_github_heatmap(year):
    """Generate a GitHub-style heatmap for chat usage."""
    df = load_data()

    # Filter for the selected year
    df = df[df["Year"] == year]

    if df.empty:
        print(f"⚠️ No data for {year}.")
        return

    # Create a date range for the full year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    all_dates = pd.date_range(start=start_date, end=end_date)

    # Count interactions per day
    usage_count = df.groupby("Date").size().reindex(all_dates, fill_value=0)

    # Convert dates to week number & weekday format
    usage_df = pd.DataFrame({"Date": all_dates, "Count": usage_count.values})
    usage_df["Week"] = usage_df["Date"].dt.strftime("%U").astype(int)  # Week number
    usage_df["Weekday"] = usage_df["Date"].dt.weekday  # Monday=0, Sunday=6

    # Create pivot table (Weeks × Days)
    heatmap_data = usage_df.pivot(index="Weekday", columns="Week", values="Count")

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.heatmap(heatmap_data, cmap="Greens", linewidths=0.5, linecolor="gray", cbar=True, ax=ax)

    # Calculate month positions
    first_days = pd.date_range(start=start_date, end=end_date, freq='MS')
    month_weeks = [int(day.strftime("%U")) for day in first_days]

    # Format grid
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=10)
    
    # Set month labels at the correct week positions
    ax.set_xticks(month_weeks)
    ax.set_xticklabels([calendar.month_abbr[i] for i in range(1, 13)], fontsize=10)
    
    ax.set_title(f"GitHub-Style Chat Usage Heatmap ({year})", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.show()

# Run the heatmap for a given year
generate_github_heatmap(2024)