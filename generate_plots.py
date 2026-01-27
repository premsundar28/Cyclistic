import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar

# Load and prepare data
master = pd.read_csv("./master.csv")
master["started_at"] = pd.to_datetime(master["started_at"])
master["ended_at"] = pd.to_datetime(master["ended_at"])
master['ride_length'] =  master['ended_at'] - master['started_at']
master['ride_length_mins'] = master['ride_length'].dt.total_seconds() / 60
master['day_of_the_week'] = master['started_at'].dt.day_name()
master['month'] = master['started_at'].dt.month
master['hour_of_day'] = master['started_at'].dt.hour

def calculate_ride_distance(df):
    R = 6371.0
    lat1, lon1 = np.radians(df['start_lat']), np.radians(df['start_lng'])
    lat2, lon2 = np.radians(df['end_lat']), np.radians(df['end_lng'])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

master['ride_distance'] = calculate_ride_distance(master)

station_cols = ['start_station_name' , 'start_station_id' , 'end_station_name' , 'end_station_id']
master[station_cols] = master[station_cols].fillna('off-network')
master.dropna(subset=['end_lat', 'end_lng'], inplace=True)
if 'Unnamed: 0' in master.columns:
    master.drop(columns=['Unnamed: 0'], inplace=True)

master_cleaned = master[master['ride_length_mins'] > 0].copy()
is_false_start = (master_cleaned['ride_distance'] == 0) & (master_cleaned['ride_length_mins'] <= 3)
master_cleaned = master_cleaned[~is_false_start]
master_cleaned_filtered = master_cleaned[(master_cleaned['ride_length_mins'] >= 1) & (master_cleaned['ride_length_mins'] <= 1440)]
master = master_cleaned_filtered

# --- Generate and Save Plots ---

# 1. Rideable Type Histogram
sns.histplot(master["rideable_type"])
plt.savefig('img/rideable_type_hist.png')
plt.close()

# 2. Ride Length Histogram
sns.histplot(data=master, x='ride_length_mins', binrange=(0, 200), bins=40)
plt.xlim(0, 200)
plt.savefig('img/ride_length_mins_hist.png')
plt.close()

# 3. Ride Duration vs. Distance
sns.jointplot(data=master, x='ride_length_mins', y='ride_distance', kind="hex", xlim=(0, 200), ylim=(0, 20))
plt.savefig('img/ride_duration_distance_hexbin.png')
plt.close()

# 4. Rides per Day
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
master['day_of_the_week'] = pd.Categorical(master['day_of_the_week'] , categories= day_order, ordered = True )
rides_per_day = master.groupby(['day_of_the_week' , 'member_casual'], observed = False)['ride_id'].count().reset_index()
plt.figure(figsize = (16,6))
sns.barplot(data = rides_per_day , x = 'day_of_the_week' , y = 'ride_id' , hue = 'member_casual')
plt.title('Rides per day')
plt.xlabel('Day of the week')
plt.ylabel('Number of rides')
plt.savefig('img/rides_per_day.png')
plt.close()

# 5. Rides per Month
month_map = {i: calendar.month_name[i] for i in range(1, 13)}
rides_per_month = master.groupby(['month', 'member_casual'], observed=False)['ride_id'].count().reset_index()
rides_per_month['month'] = rides_per_month['month'].map(month_map)
fig, ax = plt.subplots(figsize=(16, 6))
sns.barplot(data=rides_per_month, x='month', y='ride_id', hue='member_casual')
plt.title('Rides per Month')
plt.xlabel('Month')
plt.ylabel('Number of Rides')
plt.savefig('img/rides_per_month.png')
plt.close()

# 6. Rides per Hour
rides_per_hour = master.groupby(['member_casual' , 'hour_of_day'])['ride_id'].count().reset_index()
fig , ax = plt.subplots(figsize = (16,6))
sns.barplot(data = rides_per_hour , x = 'hour_of_day' , y = 'ride_id' , hue = 'member_casual')
plt.title('Rides per hour')
plt.xlabel('Hour of the day')
plt.ylabel('Number of rides')
plt.savefig('img/rides_per_hour.png')
plt.close()

# 7. Top Stations
valid_start_stations = master[master['start_station_name'] != 'off-network']
top_start_stations_member = (
    valid_start_stations.loc[valid_start_stations['member_casual'] == 'member', 'start_station_name']
    .value_counts()
    .head(10)
    .reset_index(name='count')
)
top_start_stations_casual = (
    valid_start_stations.loc[valid_start_stations['member_casual'] == 'casual', 'start_station_name']
    .value_counts()
    .head(10)
    .reset_index(name='count')
)

fig, ax = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
sns.barplot(x='count', y='start_station_name', data=top_start_stations_member, ax=ax[0], palette='viridis', hue='start_station_name', legend=False)
ax[0].set_title('Top Start Stations: Members', fontsize=14, fontweight='bold')
sns.barplot(x='count', y='start_station_name', data=top_start_stations_casual, ax=ax[1], palette='magma', hue='start_station_name', legend=False)
ax[1].set_title('Top Start Stations: Casual', fontsize=14, fontweight='bold')
ax[1].set_ylabel('')
plt.savefig('img/top_stations.png')
plt.close()

# 8. Bike Type Preference
plt.figure(figsize=(10, 6))
sns.barplot(x='member_casual', y='ride_id', hue='rideable_type', data=master.groupby(['member_casual', 'rideable_type'])['ride_id'].count().reset_index())
plt.title('Bike Type Preference by User Type')
plt.ylabel('Count')
plt.savefig('img/bike_type_preference.png')
plt.close()

print("All plots saved successfully.")
