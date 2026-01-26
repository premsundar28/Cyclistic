
# Handling Outliers in Ride Duration (`ride_length_mins`)

## 1. Problem Identification

Exploratory Data Analysis (EDA) on the `ride_length_mins` column revealed the presence of extreme outliers. While the majority of rides are under a few hours, the maximum ride duration is approximately 1,500 minutes (~25 hours).

These outliers heavily skew summary statistics like the mean, providing a misleading picture of a "typical" ride. They also distort visualizations like histograms, making it difficult to analyze the distribution of common ride durations.

## 2. Interpretation of Outliers

From a business perspective, ride durations exceeding 24 hours are not considered normal customer behavior. They almost certainly represent:

- **Data Errors:** System failures that prevented a ride from being properly terminated in the system.
- **Lost or Stolen Bikes:** Bikes that were not returned and remained "active" until they were eventually recovered and checked in by staff.

Since the project goal is to understand and convert *typical* casual riders, these anomalous data points are noise and must be filtered out.

## 3. Strategy: Apply a Sanity Filter

The strategy is to define a "reasonable" range for ride durations and filter the dataset to include only those trips. This ensures the analysis focuses on genuine, representative user behavior.

We will set the following thresholds:
- **Minimum Duration:** 1 minute. Trips shorter than this are likely "false starts" or undocking errors and do not represent a real journey.
- **Maximum Duration:** 1440 minutes (24 hours). Any ride longer than a full day is considered an anomaly as per the interpretation above.

## 4. Implementation

The following Python code, using the `pandas` library, applies this filtering logic.

```python
import pandas as pd

# Assume 'df' is your pre-cleaned DataFrame
print(f"Original number of rows: {len(df)}")

# Apply the duration filter
df_filtered = df[(df['ride_length_mins'] >= 1) & (df['ride_length_mins'] <= 1440)]

print(f"Number of rows after filtering: {len(df_filtered)}")
print(f"Rows removed: {len(df) - len(df_filtered)}")

# --- Verification ---
# Compare statistics before and after
print("\n--- Ride Length Stats (Before) ---")
print(df['ride_length_mins'].describe())

print("\n--- Ride Length Stats (After) ---")
print(df_filtered['ride_length_mins'].describe())
```

## 5. Verification & Outcome

After applying the filter, the summary statistics for `ride_length_mins` will be more representative of typical user behavior. The `max` value will be 1440, and the `mean` will be a more accurate reflection of a standard trip, allowing for a fair and meaningful comparison between casual riders and annual members.

```
