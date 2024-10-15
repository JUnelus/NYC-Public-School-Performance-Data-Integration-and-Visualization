import pandas as pd
import json
import os


def clean_data(demographics_df, performance_df):
    """
    Cleans and preprocesses the dataframes.
    """
    # 1. Create a 'dbn' column in demographics_df:
    demographics_df['dbn'] = demographics_df['borough'] + ' ' + demographics_df['year']

    # 2. Ensure 'dbn' is uppercase in both dataframes for consistency:
    demographics_df['dbn'] = demographics_df['dbn'].str.upper()
    performance_df['dbn'] = performance_df['dbn'].str.upper()

    return demographics_df, performance_df


def merge_data(demographics_df, performance_df):
    """
    Merges the two dataframes on 'dbn'.
    """
    merged_df = pd.merge(demographics_df, performance_df, on='dbn')
    return merged_df


if __name__ == "__main__":
    # Load raw data from the data/raw directory
    with open("data/raw/school_demographics.json", "r") as f:
        demographics_data = json.load(f)

    with open("data/raw/school_performance.json", "r") as f:
        performance_data = json.load(f)

    demographics_df = pd.DataFrame(demographics_data)
    performance_df = pd.DataFrame(performance_data)

    demographics_df, performance_df = clean_data(demographics_df, performance_df)
    merged_df = merge_data(demographics_df, performance_df)

    # Ensure the processed data directory exists
    os.makedirs("data/processed", exist_ok=True)

    # Save the processed data to a new file in the data directory
    merged_df.to_csv("data/processed/merged_school_data.csv", index=False)