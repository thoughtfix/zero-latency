#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Generate a horizontal boxplot for CSV files.')
parser.add_argument('--directory', default='.', help='Directory path containing CSV files. Default is the current directory.')
parser.add_argument('--heading', default='', help='The heading for the boxplot graph. Default is empty.')
parser.add_argument('--sort', choices=['data', 'alphabet'], default=None, help='Sort boxplots by "data" (average value) or "alphabet" (filename). Default is no sorting.')
parser.add_argument('--reverse', action='store_true', help='When sorting by "data", sorts from low to high. Default is high to low.')

# Parse command line arguments
args = parser.parse_args()

# Use the directory path, heading, sort option, and reverse flag provided by the user
directory_path = args.directory
graph_heading = args.heading
sort_option = args.sort
reverse_sort = args.reverse

# Initialize a list to store the data from each CSV file and a list for labels
data_list = []
labels = []
averages = []

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
            # Calculate and store the average for sorting if needed
            averages.append(data[0].mean())
        except Exception as e:
            print(f'Failed to process {filename}: {e}')

# Apply sorting based on the user's choice
if sort_option == 'data':
    sorted_lists = sorted(zip(labels, data_list, averages), key=lambda x: x[2], reverse=not reverse_sort)
    labels, data_list, _ = zip(*sorted_lists)
elif sort_option == 'alphabet':
    labels, data_list = zip(*sorted(zip(labels, data_list), key=lambda x: x[0], reverse=reverse_sort))

if sort_option in ['data', 'alphabet']:
    labels = list(labels)
    data_list = list(data_list)

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
    plt.xticks(rotation=0)

    # Save the plot as a PNG image file in the same directory
    image_path = os.path.join(directory_path, 'boxplot_horizontal.png')
    plt.savefig(image_path)
    print(f'Boxplot saved as {image_path}')

    # Optionally, display the plot
    plt.show()
else:
    print("No data to plot.")
