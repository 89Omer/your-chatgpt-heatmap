import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import pandas as pd

def generate_yearly_heatmap(year):
    """Generate a heatmap for a given year."""
    LOG_FILE = "chat_usage_log.csv"  # Ensure this is the correct path
    df = pd.read_csv(LOG_FILE)  # Read data
    
    # Convert Year column to string for filtering
    df["Year"] = df["Year"].astype(str)
    
    # Filter data for the selected year
    yearly_data = df[df["Year"] == str(year)]
    
    if yearly_data.empty:
        print(f"⚠️ No interactions found for {year}. Try another year.")
        return
    
    print("✅ Data found for the year:", year)
    print(yearly_data.head())

    # Add missing "Day" column
    yearly_data["Day"] = yearly_data["Date"].str[-2:]  # Extract day from "YYYY-MM-DD"
    yearly_data["Day"] = yearly_data["Day"].astype(int)

    # Pivot data
    heatmap_data = yearly_data.pivot_table(index="Day", columns="Month", values="Hour", aggfunc="count", fill_value=0)

    # Plot heatmap
    plt.figure(figsize=(12, 7))
    sns.heatmap(
        heatmap_data, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5,
        cbar_kws={'label': 'Interactions Count'}
    )

    plt.title(f"ChatGPT Usage Heatmap ({year})", fontsize=16, fontweight="bold")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Day of Month", fontsize=12)
    plt.xticks(ticks=range(1, 13), labels=[calendar.month_abbr[i] for i in range(1, 13)], rotation=45)
    plt.yticks(fontsize=10)
    plt.show()

# Run the heatmap
generate_yearly_heatmap(2024)
