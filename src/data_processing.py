"""
Data Processing Module
Cleans, transforms, and merges NYC school demographics (borough-level) with
performance data (school-level) using district-to-borough mapping.
"""

import pandas as pd
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

# NYC school district number → borough mapping
DISTRICT_TO_BOROUGH = {
    "01": "Manhattan", "02": "Manhattan", "03": "Manhattan", "04": "Manhattan",
    "05": "Manhattan", "06": "Manhattan",
    "07": "Bronx", "08": "Bronx", "09": "Bronx", "10": "Bronx",
    "11": "Bronx", "12": "Bronx",
    "13": "Brooklyn", "14": "Brooklyn", "15": "Brooklyn", "16": "Brooklyn",
    "17": "Brooklyn", "18": "Brooklyn", "19": "Brooklyn", "20": "Brooklyn",
    "21": "Brooklyn", "22": "Brooklyn", "23": "Brooklyn", "32": "Brooklyn",
    "24": "Queens", "25": "Queens", "26": "Queens", "27": "Queens",
    "28": "Queens", "29": "Queens", "30": "Queens",
    "31": "Staten Island",
    "75": "Citywide", "79": "Citywide", "84": "Citywide",
}


def dbn_to_borough(dbn: str) -> str:
    """Extract district number from DBN and map to borough."""
    district = dbn[:2]
    return DISTRICT_TO_BOROUGH.get(district, "Unknown")


def review_date_to_school_year(date_str: str) -> str:
    """
    Convert a review date to the school year format used in demographics data.
    E.g., a review in April 2017 → school year '2016-17'.
    Reviews before August belong to the previous school year.
    """
    if not date_str or date_str == "No Data":
        return None
    try:
        dt = pd.to_datetime(date_str)
        # School year runs Sep-Aug. If review is Jan-Aug, it's the prior year's school year.
        if dt.month < 9:
            start_year = dt.year - 1
        else:
            start_year = dt.year
        end_year_short = str(start_year + 1)[-2:]
        return f"{start_year}-{end_year_short}"
    except Exception:
        return None


def clean_demographics(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the borough-level demographics data."""
    numeric_cols = [
        "total_enrollment", "grade_3k_pk_half_day_full", "grade_k",
        "grade_1", "grade_2", "grade_3", "grade_4", "grade_5",
        "grade_6", "grade_7", "grade_8", "grade_9", "grade_10",
        "grade_11", "grade_12", "female", "female_1", "male", "male_1",
        "asian", "asian_1", "black", "black_1", "hispanic", "hispanic_1",
        "multi_racial", "multi_racial_1", "native_american", "native_american_1",
        "white", "white_1", "missing_race_ethnicity_data", "missing_race_ethnicity_data_1",
        "students_with_disabilities", "students_with_disabilities_1",
        "english_language_learners", "english_language_learners_1",
        "poverty", "poverty_1", "economic_need_index",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    logger.info(f"Demographics: {len(df)} records, years: {sorted(df['year'].unique())}")
    return df


def clean_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the school-level performance data."""
    # Derive borough from DBN
    df["borough"] = df["dbn"].apply(dbn_to_borough)

    # Derive school year from review date
    df["year"] = df["dates_of_review"].apply(review_date_to_school_year)

    # Convert numeric columns
    numeric_cols = [
        "enrollment", "survey_pp_ri", "survey_pp_ct", "survey_pp_se",
        "survey_pp_es", "survey_pp_sf", "survey_pp_tr",
        "rating_ela_grade_8_pct_rs", "rating_mth_grade_8_pct_rs",
        "gender_female_pct", "gender_male_pct", "ell", "iep", "cap_sc_pct",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop schools with unknown borough or no year
    before = len(df)
    df = df[df["borough"].isin(["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"])]
    df = df.dropna(subset=["year"])
    logger.info(f"Performance: {before} → {len(df)} records after cleaning")
    return df


def merge_data(demographics_df: pd.DataFrame, performance_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge school-level performance with borough-level demographics on borough + year.
    This enriches each school with its borough's aggregate demographic data.
    """
    merged = pd.merge(
        performance_df,
        demographics_df,
        on=["borough", "year"],
        how="left",
        suffixes=("", "_borough"),
    )
    logger.info(f"Merged dataset: {len(merged)} records, {len(merged.columns)} columns")
    return merged


if __name__ == "__main__":
    logger.info("Starting data processing...")

    with open(os.path.join(RAW_DATA_DIR, "school_demographics.json"), "r") as f:
        demographics_data = json.load(f)
    with open(os.path.join(RAW_DATA_DIR, "school_performance.json"), "r") as f:
        performance_data = json.load(f)

    demographics_df = clean_demographics(pd.DataFrame(demographics_data))
    performance_df = clean_performance(pd.DataFrame(performance_data))

    merged_df = merge_data(demographics_df, performance_df)

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    output_path = os.path.join(PROCESSED_DATA_DIR, "merged_school_data.csv")
    merged_df.to_csv(output_path, index=False)
    logger.info(f"Saved merged data to {output_path}")

    # Print summary
    print("\n=== Dataset Summary ===")
    print(f"Total schools: {merged_df['dbn'].nunique()}")
    print(f"Boroughs: {sorted(merged_df['borough'].unique())}")
    print(f"School years: {sorted(merged_df['year'].dropna().unique())}")
    print(f"Columns: {list(merged_df.columns)}")
    print(f"\nSample data:\n{merged_df[['dbn', 'school_name', 'borough', 'year', 'rating_ela_grade_8_pct_rs', 'economic_need_index']].head(10)}")
