#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Generate a horizontal boxplot for CSV files.')
parser.add_argument('--directory', default='.', help='Directory path containing CSV files. Default is the current directory.')
parser.add_argument('--heading', default='', help='The heading for the boxplot graph. Default is empty.')

# Parse command line arguments
args = parser.parse_args()

# Use the directory path and heading provided by the user (or defaults)
directory_path = args.directory
graph_heading = args.heading

# Initialize a list to store the data from each CSV file
data_list = []
labels = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Construct the full path to the file
        file_path = os.path.join(directory_path, filename)
        try:
            # Read the CSV file into a pandas DataFrame
            data = pd.read_csv(file_path, header=None)
            # Add the data to the list
            data_list.append(data[0])
            # Process the filename to use as a label
            label = filename[:-4].replace('-', ' ')  # Remove '.csv' and replace dashes
            labels.append(label)
        except Exception as e:
            print(f'Failed to process {filename}: {e}')

# Check if we have data to plot
if data_list:
    # Generate a horizontal boxplot
    plt.figure(figsize=(10, 6))
    plt.boxplot(data_list, labels=labels, vert=False, patch_artist=True)
    plt.title(graph_heading)
    plt.xlabel('Value')
    plt.tight_layout()

    # Improve readability of labels
    plt.tick_params(axis='y', which='major', labelsize=8)
    plt.xticks(rotation=0)  # Ensure the value labels are horizontal

    # Save the plot as a PNG image file in the same directory
    image_path = os.path.join(directory_path, 'boxplot_horizontal.png')
    plt.savefig(image_path)
    print(f'Boxplot saved as {image_path}')

    # Optionally, display the plot
    plt.show()
else:
    print("No data to plot.")
