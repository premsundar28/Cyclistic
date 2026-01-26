import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_ride_distance(df):
    # Earth's radius in kilometers
    R = 6371.0 

    # Convert degrees to radians for all coordinate columns
    lat1, lon1 = np.radians(df['start_lat']), np.radians(df['start_lng'])
    lat2, lon2 = np.radians(df['end_lat']), np.radians(df['end_lng'])

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Calculate final distance
    return R * c

def load_and_prepare_data(filepath):
    print("Loading data...")
    master = pd.read_csv(filepath)
    
    print("Preprocessing...")
    master["started_at"] = pd.to_datetime(master["started_at"])
    master["ended_at"] = pd.to_datetime(master["ended_at"])
    
    # Feature Engineering
    master['ride_length'] =  master['ended_at'] - master['started_at'] 
    master['ride_length_mins'] = master['ride_length'].dt.total_seconds() / 60
    master['day_of_the_week'] = master['started_at'].dt.day_name()
    master['month'] = master['started_at'].dt.month
    master['hour_of_day'] = master['started_at'].dt.hour
    master['ride_distance'] = calculate_ride_distance(master)
    
    # Cleaning
    station_cols = ['start_station_name' , 'start_station_id' , 'end_station_name' , 'end_station_id']
    master[station_cols] = master[station_cols].fillna('off-network')
    master.dropna(subset=['end_lat', 'end_lng'], inplace=True)
    if 'Unnamed: 0' in master.columns:
        master.drop(columns=['Unnamed: 0'], inplace=True)
        
    print(f"Initial rows: {len(master)}")
    
    # Filtering
    # Rule 1: Remove rides with negative or zero duration
    master_cleaned = master[master['ride_length_mins'] > 0].copy()
    
    # Rule 2: Remove 0-distance "False Starts" (duration <= 3 mins)
    is_false_start = (master_cleaned['ride_distance'] == 0) & (master_cleaned['ride_length_mins'] <= 3)
    master_cleaned = master_cleaned[~is_false_start]
    
    # Create master_cleaned_filtered (duration between 1 and 1440 mins)
    master_cleaned_filtered = master_cleaned[(master_cleaned['ride_length_mins'] >= 1) & (master_cleaned['ride_length_mins'] <= 1440)].copy()
    
    print(f"Final rows after filtering: {len(master_cleaned_filtered)}")
    return master_cleaned_filtered

def analyze_ride_duration(df):
    print("\n--- 1. Ride Duration Analysis ---")
    
    # Statistics
    stats = df.groupby('member_casual')['ride_length_mins'].agg(['mean', 'median', 'max', 'count'])
    print(stats)
    
    # Visualizations
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='member_casual', y='ride_length_mins', data=df)
    plt.title('Distribution of Ride Durations by User Type')
    plt.savefig('img/ride_duration_boxplot.png')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='ride_length_mins', hue='member_casual', element="step", stat="density", common_norm=False, log_scale=True)
    plt.title('Distribution of Ride Durations (Log Scale)')
    plt.savefig('img/ride_duration_hist_log.png')
    plt.close()
    print("Ride duration plots saved.")

def analyze_time_based(df):
    print("\n--- 2. Time-based Analysis ---")
    
    # Day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_the_week'] = pd.Categorical(df['day_of_the_week'], categories=day_order, ordered=True)
    
    # Analysis
    rides_per_day = df.groupby(['day_of_the_week', 'member_casual'], observed=False)['ride_id'].count().reset_index()
    rides_per_month = df.groupby(['month', 'member_casual'])['ride_id'].count().reset_index()
    rides_per_hour = df.groupby(['hour_of_day', 'member_casual'])['ride_id'].count().reset_index()
    
    # Plots
    plt.figure(figsize=(12, 6))
    sns.barplot(x='day_of_the_week', y='ride_id', hue='member_casual', data=rides_per_day)
    plt.title('Number of Rides by Day of the Week')
    plt.ylabel('Count')
    plt.savefig('img/rides_per_day.png')
    plt.close()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='month', y='ride_id', hue='member_casual', data=rides_per_month)
    plt.title('Number of Rides by Month')
    plt.ylabel('Count')
    plt.savefig('img/rides_per_month.png')
    plt.close()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='hour_of_day', y='ride_id', hue='member_casual', data=rides_per_hour)
    plt.title('Number of Rides by Hour of the Day')
    plt.ylabel('Count')
    plt.savefig('img/rides_per_hour.png')
    plt.close()
    print("Time-based plots saved.")

def analyze_stations(df):
    print("\n--- 3. Station Analysis ---")
    
    # Top Start Stations
    # Filter out 'off-network' if desirable, or keep to show magnitude of undocked rides
    # Here we exclude off-network for specific station analysis
    valid_start_stations = df[df['start_station_name'] != 'off-network']
    
    top_start_casual = valid_start_stations[valid_start_stations['member_casual'] == 'casual']['start_station_name'].value_counts().head(10).reset_index()
    top_start_casual.columns = ['start_station_name', 'count']
    
    top_start_member = valid_start_stations[valid_start_stations['member_casual'] == 'member']['start_station_name'].value_counts().head(10).reset_index()
    top_start_member.columns = ['start_station_name', 'count']
    
    print("\nTop 10 Start Stations (Casual):")
    print(top_start_casual)
    print("\nTop 10 Start Stations (Member):")
    print(top_start_member)
    
    # Plot Casual
    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='start_station_name', data=top_start_casual, palette='Blues_d')
    plt.title('Top 10 Start Stations - Casual Riders')
    plt.xlabel('Number of Rides')
    plt.tight_layout()
    plt.savefig('img/top_stations_casual.png')
    plt.close()
    
    # Plot Member
    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='start_station_name', data=top_start_member, palette='Greens_d')
    plt.title('Top 10 Start Stations - Annual Members')
    plt.xlabel('Number of Rides')
    plt.tight_layout()
    plt.savefig('img/top_stations_member.png')
    plt.close()
    print("Station plots saved.")

def analyze_bike_type(df):
    print("\n--- 4. Bike Type Analysis ---")
    
    bike_type_stats = df.groupby(['member_casual', 'rideable_type'])['ride_id'].count().reset_index()
    print(bike_type_stats)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='member_casual', y='ride_id', hue='rideable_type', data=bike_type_stats)
    plt.title('Bike Type Preference by User Type')
    plt.ylabel('Count')
    plt.savefig('img/bike_type_preference.png')
    plt.close()
    print("Bike type plot saved.")

def analyze_conversion_opportunities(df):
    print("\n--- 5. Conversion Opportunity Analysis ---")

    # --- Pricing Assumptions ---
    single_ride_cost = 2.99
    day_pass_cost = 15.00
    annual_membership_cost = 149.00

    # --- 1. Identify Potential Commuters (Casual riders during peak hours) ---
    peak_hours = (df['hour_of_day'].isin(range(7, 10)) | df['hour_of_day'].isin(range(16, 19)))
    weekday = df['day_of_the_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    casual_riders = df['member_casual'] == 'casual'
    
    potential_commuters = df[casual_riders & weekday & peak_hours]
    
    print(f"\nFound {len(potential_commuters)} rides from casual riders during peak commute hours.")
    
    rides_per_work_week = 10 
    weekly_cost_single_rides = rides_per_work_week * single_ride_cost
    
    print(f"A casual commuter riding twice a day for a week would spend ${weekly_cost_single_rides:.2f} on single rides.")
    print(f"An annual membership costs ${annual_membership_cost:.2f}. This is equivalent to ~{annual_membership_cost/weekly_cost_single_rides:.1f} weeks of commuting.")
    
    # --- 2. Identify Frequent Weekenders (Casual riders on weekends) ---
    weekends = df['day_of_the_week'].isin(['Saturday', 'Sunday'])
    
    frequent_weekenders = df[casual_riders & weekends]
    
    avg_weekend_rides = len(frequent_weekenders) / len(df['started_at'].dt.to_period('W').unique())
    
    print(f"\nOn average, there are {avg_weekend_rides:.0f} casual rides each weekend.")
    
    weekend_rides = 4
    weekend_cost = weekend_rides * single_ride_cost
    
    print(f"A casual rider taking {weekend_rides} rides over a weekend would spend ${weekend_cost:.2f}.")
    print(f"This is close to the cost of a Day Pass (${day_pass_cost:.2f}), but a membership offers more flexibility.")

    # --- 3. Power Users (High volume casual riders) ---
    top_casual_station = df[df['member_casual'] == 'casual']['start_station_name'].value_counts().index[0]
    power_user_rides = df[(df['member_casual'] == 'casual') & (df['start_station_name'] == top_casual_station)]
    
    print(f"\nAnalyzing rides from the top casual station: '{top_casual_station}'")
    print(f"There are {len(power_user_rides)} rides from this station by casual users.")
    
    weekly_rides = 3
    power_user_weekly_cost = weekly_rides * single_ride_cost
    power_user_annual_cost = power_user_weekly_cost * 52
    
    print(f"A hypothetical power user riding {weekly_rides} times a week would spend ${power_user_weekly_cost:.2f} weekly, or an estimated ${power_user_annual_cost:.2f} annually.")
    print(f"This is significantly more than the annual membership cost of ${annual_membership_cost:.2f}.")

if __name__ == "__main__":
    file_path = "./master.csv"
    master_cleaned_filtered = load_and_prepare_data(file_path)
    
    analyze_ride_duration(master_cleaned_filtered)
    analyze_time_based(master_cleaned_filtered)
    analyze_stations(master_cleaned_filtered)
    analyze_bike_type(master_cleaned_filtered)
    analyze_conversion_opportunities(master_cleaned_filtered)
