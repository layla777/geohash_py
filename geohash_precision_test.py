"""
Script Name: Geohash Precision Test

Purpose:
This script analyzes the precision of geohashes by observing how the latitude
and longitude intervals shrink with increasing geohash resolution. The analysis
is further visualized using a plot, showing the shrinking rates (on a logarithmic
scale) for latitude and longitude intervals as the geohash string length increases.

Usage Instructions:
1. Ensure you have Python 3.12.8 installed.
2. Install the required dependencies using pip:
   pip install matplotlib numpy
3. Execute the script in your IDE or terminal.
   python geohash_precision_test.py
4. The script outputs the shrinking rates and geohash ranges for each substring
   in the terminal and plots a graph showing the shrinking rates of geohash intervals.

Dependencies:
- matplotlib
- numpy
- A Python geohash library

Expected Output:
- The script will print geohash intervals (latitude and longitude) and their shrinking rates.
- A plot visualizing the shrinking rates will be displayed.

Why It's Useful:
This script is useful for understanding the mechanics of geohash precision and
how geohash resolution improves geographic encoding accuracy. It provides insights
for educational purposes as well as practical applications in geospatial data analysis.
"""
import matplotlib.pyplot as plt

# Import required modules
from geohash import *

# Define the Geohash string to test precision
geohash = 'ezs42e44yxpy'

# Initialize arrays to store shrinking lat/lng intervals and labels for visualization
lat_ranges = []
lng_ranges = []
labels = []

# Loop through each substring of the Geohash (from 1 character up to the full string)
for i in range(len(geohash)):
    # Generate a substring of the Geohash up to the current length
    test_geohash = geohash[0:i + 1]

    # Initialize the Geohash object
    gh = Geohash.init_with_geohash(geohash=test_geohash)

    # Decode intervals (latitude and longitude ranges)
    lat, lng = gh.decode_to_interval()

    # Store ranges for later visualization
    lat_ranges.append(lat[1] - lat[0])  # Latitude interval size
    lng_ranges.append(lng[1] - lng[0])  # Longitude interval size
    labels.append(f'{i + 1}-char')  # For labeling in the graph

    # Print the results for the current Geohash substring
    print(f'{i + 1:02} char(s) Geohash range: Latitude = {lat}, Longitude = {lng}')
    print(f'{i + 1:02} char(s) shrinking rate: Latitude range = {lat[1] - lat[0]}, Longitude range = {lng[1] - lng[0]}')
    print(f'{i + 1:02} char(s) Geohash bitstream: {Geohash._geohash_to_bits(test_geohash):b}')

# Plot results with matplotlib
plt.figure(figsize=(10, 6))

# Plot latitude and longitude shrinking rates using logarithmic scaling
plt.plot(range(1, len(geohash) + 1), lat_ranges, marker='o', label='Latitude range (shrinking rate)')
plt.plot(range(1, len(geohash) + 1), lng_ranges, marker='o', label='Longitude range (shrinking rate)')

# Set y-axis to log scale
plt.yscale('log')

# Add labels, grid, and title
plt.title('Geohash Accuracy: Latitude and Longitude Shrinking Rates (Log Scale)')
plt.xlabel('Number of Geohash Characters')
plt.ylabel('Range Width (log scale)')
plt.xticks(range(1, len(geohash) + 1), labels, rotation=45)
plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)  # Enhance grid for log scale
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
