# Case Study: Cyclistic Bike-Share Analysis

## Introduction
This case study focuses on Cyclistic, a fictional bike-share company in Chicago. As a junior data analyst, the goal is to follow the data analysis process (Ask, Prepare, Process, Analyze, Share, and Act) to answer key business questions that will help guide the company's marketing strategy.

## Scenario
The Director of Marketing at Cyclistic believes the company’s future success depends on maximizing the number of annual memberships. The marketing analyst team needs to understand how casual riders and annual members use Cyclistic bikes differently. Based on these insights, the team will design a new marketing strategy to convert casual riders into annual members.

## About the Company
In 2016, Cyclistic launched a successful bike-share offering. Since then, the program has grown to a fleet of 5,824 bicycles that are geotracked and locked into a network of 692 stations across Chicago. The bikes can be unlocked from one station and returned to any other station in the system anytime.

Cyclistic offers flexible pricing plans:
*   **Casual Riders:** Customers who purchase single-ride or full-day passes.
*   **Cyclistic Members:** Customers who purchase annual memberships.

Finance analysts have concluded that annual members are much more profitable than casual riders. Moreno, the Director of Marketing, believes there is a solid opportunity to convert casual riders into members, as they are already aware of the Cyclistic program and have chosen it for their mobility needs.

## Phase 1: Ask

### Key Business Task
The primary objective is to identify the behavioral differences between casual riders and annual members of Cyclistic. By analyzing historical trip data, we aim to uncover trends that will inform a targeted marketing strategy to convert casual riders into long-term annual members, thereby driving company growth and profitability.

### Stakeholders
*   **Lily Moreno:** Director of Marketing and your manager. Responsible for the development of campaigns and initiatives to promote the bike-share program.
*   **Cyclistic Marketing Analytics Team:** A team of data analysts responsible for collecting, analyzing, and reporting data to guide marketing strategy.
*   **Cyclistic Executive Team:** The notoriously detail-oriented team that decides whether to approve the recommended marketing program.

### Guiding Questions
1.  How do annual members and casual riders use Cyclistic bikes differently?
2.  Why would casual riders buy Cyclistic annual memberships?
3.  How can Cyclistic use digital media to influence casual riders to become members?

### Conclusion: Strategic Alignment

business objective: **profit maximization through the conversion of high-potential casual riders into annual members**.

I’m focusing my analysis on the commercial drivers that turn casual riders into annual members. Rather than just observing data, I am identifying the specific behaviors that distinguish our most profitable segments. This allows me to provide the marketing team with a data-backed roadmap for high-ROI growth and help leadership make more informed strategic decisions.

## Phase 2: Prepare & Process (Data Cleaning)

To ensure the data was reliable and ready for analysis, the following cleaning and preparation steps were performed:

### 1. Handling Missing Values
- **Station Information:** A large number of trips had missing `start_station_name` and `end_station_name`. Instead of deleting these records, the missing values were filled with the label `"off-network"`. This preserves these trips for analysis and treats the lack of a station as a behavioral insight (i.e., dockless rides).
- **End Coordinates:** A small number of trips (~5,500) were missing `end_lat` and `end_lng`. These rows were dropped as the ride distance could not be calculated and the volume was low enough not to impact overall trends.

### 2. Correcting Data Integrity Issues & Handling Outliers
- **Negative/Zero Duration Rides:** Trips with a duration of less than one minute (`ride_length_mins` < 1) were removed. These are considered data errors (`ended_at` before `started_at`) or "false starts" that do not represent a valid trip.
- **Zero-Distance Rides:** Trips with a calculated distance of 0 km but a duration greater than one minute were kept. These are interpreted as valid "round-trip" journeys where the rider returned to the same starting station.
- **Extreme Duration Outliers:** Trips with a duration longer than 24 hours (1,440 minutes) were removed. These are considered anomalies, likely representing stolen bikes or system errors, and do not reflect typical user behavior.

After these steps, the dataset was clean and ready for the analysis phase, providing a more accurate foundation for comparing the behavior of casual riders and annual members.