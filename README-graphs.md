# make-graphs.py overview

This Python script generates horizontal boxplots from CSV files located in a specified directory. It allows customization of the plot's heading, the sorting of boxplots by data average or filename alphabetically, and direction of sorting. The script outputs the plot as a PNG image file.

## Requirements

- Python 3.x
- Pandas library
- Matplotlib library

## Usage

```bash
./make-graphs.py [--directory DIR] [--heading HEADING] [--sort {data,alphabet}] [--reverse]
```

### Arguments

- `--directory DIR`  
  Specifies the directory path containing CSV files.  
  Default: `.` (current directory)

- `--heading HEADING`  
  Sets the heading for the boxplot graph.  
  Default: Empty

- `--sort {data,alphabet}`  
  Sorts boxplots by "data" (average value) or "alphabet" (filename).  
  Default: No sorting

- `--reverse`  
  When sorting by "data", sorts from low to high.  
  Default behavior without `--reverse` is high to low sorting.

## Examples

1. **Generate Boxplot with Default Settings**  
   Generates a boxplot for CSV files in the current directory without any sorting and with no heading.
   ```bash
   ./make-graphs.py
   ```

2. **Custom Directory and Heading**  
   Generates a boxplot for CSV files in `/path/to/csvs` with a custom heading.
   ```bash
   ./make-graphs.py --directory /path/to/csvs --heading "My Custom Heading"
   ```

3. **Sorting by Data Average**  
   Generates a boxplot, sorted by the average values in the CSV files, from low to high.
   ```bash
   ./make-graphs.py --sort data --reverse
   ```

4. **Sorting by Filename Alphabetically**  
   Generates a boxplot, sorted alphabetically by filename.
   ```bash
   ./make-graphs.py --sort alphabet
   ```

## Output

The script saves the generated boxplot as `boxplot_horizontal.png` in the specified directory. An error message will be printed if there are issues processing any CSV files or if there are no CSV files to process.

## Troubleshooting

- **Missing Libraries:** Ensure all required Python libraries are installed.
- **File Reading Errors:** Check if CSV files are correctly formatted and accessible.
- **Plotting Issues:** Verify that Matplotlib is correctly installed and working.


## TODO
Set up filename output and prevent program from stomping on files.
