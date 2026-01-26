# Project Context: Cyclistic Bike-Share Analysis

## 1. Business Objective

The primary goal of this project is to analyze the usage patterns of Cyclistic bike-share casual riders and annual members. The ultimate objective is to inform a marketing strategy designed to convert casual riders into annual members, thereby increasing company profitability and growth.

**Key Questions to Answer:**
*   How do annual members and casual riders use Cyclistic bikes differently?
*   Why would casual riders buy Cyclistic annual memberships?
*   How can Cyclistic use digital media to influence casual riders to become members?

## 2. Data Overview

The analysis is based on historical bike trip data stored in `master.csv`. Key columns include:
*   `ride_id`: Unique identifier for each trip.
*   `rideable_type`: Type of bike (e.g., electric_bike, classic_bike).
*   `started_at`, `ended_at`: Start and end timestamps of the ride.
*   `start_station_name`, `end_station_name`: Names of start/end stations (can be 'off-network').
*   `start_station_id`, `end_station_id`: IDs of start/end stations (can be 'off-network').
*   `start_lat`, `start_lng`, `end_lat`, `end_lng`: Geographical coordinates of start/end points.
*   `member_casual`: User type (member or casual).
*   `ride_length_mins`: Calculated duration of the ride in minutes.
*   `ride_distance`: Calculated distance of the ride in kilometers.

## 3. Data Cleaning and Preparation

The `master.csv` dataset underwent the following cleaning and preparation steps:

*   **Missing Values:**
    *   Missing station names/IDs (`start_station_name`, `end_station_name`, `start_station_id`, `end_station_id`) were imputed with `"off-network"` to capture behavior related to dockless bikes.
    *   Rows with missing `end_lat` or `end_lng` were dropped due to their small number and inability to calculate ride distance accurately.
*   **Data Integrity & Outliers:**
    *   Trips with `ride_length_mins` less than 1 minute were removed (considered "false starts" or errors).
    *   Trips with `ride_length_mins` greater than 1440 minutes (24 hours) were removed (considered anomalies like lost bikes or system errors).
    *   Zero-distance trips (`ride_distance` = 0) with `ride_length_mins` <= 3 minutes were removed (considered "false starts"). Zero-distance trips with `ride_length_mins` > 3 minutes were retained as "round trips".

## 4. Current State

The data is now cleaned and prepared, with `ride_length_mins` and `ride_distance` calculated, and is ready for in-depth exploratory data analysis (EDA) and visualization.

## 5. Next Steps

The next phase involves analyzing the cleaned data to:
*   Compare ride durations, distances, and patterns (e.g., day of week, time of day) between casual and annual members.
*   Identify popular stations and routes for each user type.
*   Generate visualizations to highlight key differences and trends.
*   Formulate actionable insights and recommendations for the marketing team to convert casual riders into members.
