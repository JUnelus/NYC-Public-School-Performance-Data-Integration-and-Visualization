# NYC Public School Performance Data Integration and Visualization

This project demonstrates the integration of publicly available NYC public school performance data from multiple sources, its transformation, and visualization using Python. It showcases skills in data acquisition, API interaction, data manipulation with Pandas, and visualization with Plotly, all within a Linux environment.

## Project Structure
````
nyc-school-performance/
├── data/
│   ├── raw/
│   │   ├── school_demographics.json
│   │   └── school_performance.json
│   └── processed/
│       └── merged_school_data.csv
├── notebooks/
│   └── data_integration_and_visualization.ipynb
├── src/
│   ├── data_acquisition.py
│   └── data_processing.py
├── requirements.txt
└── README.md
````

## Data Sources

- **NYC Open Data API:**
    - School demographics data: https://data.cityofnewyork.us/resource/vquv-pjuh.json
    - School performance data: https://data.cityofnewyork.us/resource/ci36-d7ea.json

## Setup and Execution

1. **Environment Setup (Linux):**
    - Create a new project directory: `mkdir nyc-school-performance`
    - Navigate to the directory: `cd nyc-school-performance`
    - Create a virtual environment (recommended): `python3 -m venv .venv`
    - Activate the virtual environment: `source .venv/bin/activate`

2. **Install Dependencies:**
    - Install the required packages: `pip install -r requirements.txt`

3. **Data Acquisition:**
    - Run the `data_acquisition.py` script to fetch and save the raw data: `python src/data_acquisition.py`

4. **Data Processing:**
    - Run the `data_processing.py` script to process and merge the data: `python src/data_processing.py`

5. **Data Visualization:**
    - Open and run the `data_integration_and_visualization.ipynb` Jupyter Notebook to generate the visualizations.

## Skills Demonstrated

- Data acquisition from APIs
- Data manipulation and transformation with Pandas
- Data visualization with Plotly
- Python programming
- Linux environment
- Version control with Git

## Visualizations

The Jupyter Notebook generates the following visualizations:

- Scatter plot of ELA Performance vs. Economic Need Index, colored by borough.
- Bar chart of Average ELA Performance by Borough.
- Box plot of the distribution of Economic Need Index across boroughs.

## Further Exploration

This project can be extended by:

- Adding more data sources (e.g., school quality reports, attendance data).
- Performing more in-depth data analysis and exploration.
- Creating interactive visualizations.
- Building a web application to display the data and visualizations.
