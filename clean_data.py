import os
import re
import shutil

import pandas as pd
from util.env import data_path, repo_path


def processed_data_path(*args):
    return repo_path("clean", *args)


def process_fig4_data(df: pd.DataFrame = None):
    if df is None:
        df = pd.read_csv(data_path("youth-rtc", "fig4.csv"))

    df = df.rename(columns={"year": "state"})

    df = df.astype({"2010": "int", "2024": "int"})

    df["pct_chg"] = (((df["2024"] - df["2010"]) / df["2010"]) * 100).astype(float)

    states_to_keep = [
        "Illinois",
        "Indiana",
        "Kansas",
        "Montana",
        "Nebraska",
        "New Mexico",
        "New York",
        "Oklahoma",
        "Pennsylvania",
        "South Carolina",
        "West Virginia",
        "Wyoming",
        "National",
    ]

    processed_df = df[df["state"].isin(states_to_keep)]

    processed_df.to_csv(processed_data_path("clean_fig4_data.csv"), index=False)
    print(f"Fig 4 summary CSV file has been saved in {repo_path('clean')}")

    return None


def process_fig8_data():
    year_counts = {}

    for filename in os.listdir(data_path("WISQARS-data")):
        if any(str(year) in filename for year in range(2001, 2025)):
            year = filename.split("-")[-1].split(".")[0]

            df = pd.read_csv(os.path.join(data_path("WISQARS-data"), filename))

            suicide_df = df[df["Cause Category"] == "Suicide"]

            total_deaths = suicide_df["Deaths"].sum()

            year_counts[year] = total_deaths

    summary_df = pd.DataFrame(list(year_counts.items()), columns=["Year", "Count"])

    summary_df.to_csv(repo_path("clean", "clean_fig8_data.csv"), index=False)

    print(f"Fig 8 summary CSV file has been saved in {repo_path('clean')}")

    return None


def process_fig9_data():
    df = pd.read_csv(data_path('youth-rtc', 'fig9.csv'), skipinitialspace=True)
    
    df.columns = df.columns.str.replace('\xa0', '', regex=True).str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace({',': ''}, regex=True)
    for col in df.columns[1:]:  # Convert numeric columns; skip the first 'year' column
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    def_per_prtf = (
        df[df['year'].str.contains('prft_total_def', regex=False)].iloc[0, 1:] /
        df[df['year'].str.contains('prtf_count', regex=False)].iloc[0, 1:] 
    )
    def_per_sth =  (
        df[df['year'].str.contains('sth_total_def', regex=False)].iloc[0, 1:] / 
        df[df['year'].str.contains('sth_count', regex=False)].iloc[0, 1:]
    )

    clean_df = pd.DataFrame(
        {'year': def_per_prtf.index, 
         'def_per_prtf': def_per_prtf.values, 
         'def_per_sth': def_per_sth.values}
         )
    clean_df.to_csv(repo_path('clean', 'clean_fig9_data.csv'), index=False)
    
    return None


def convert_tsv_to_csv():
    """
    Convert a TSV file to a CSV file.

    Parameters:
    - tsv_filepath: str, path to the input TSV file
    - csv_filepath: str, path to the output CSV file
    """
    tsv_filepath = data_path("NMHSS", "N-MHSS-2010-DS0001-data-excel.tsv")
    csv_filepath = data_path("NMHSS", "N-MHSS-2010-DS0001-data-excel.csv")
    # Open the TSV file for reading and the CSV file for writing
    with open(tsv_filepath, "r") as tsv_file, open(csv_filepath, "w") as csv_file:
        # Read the TSV file line by line
        for line in tsv_file:
            # Replace tabs with commas and write to the CSV file
            csv_file.write(line.replace("\t", ","))

    return None


def rename_files(source_dir, target_dir):
    """
    Rename files to contain only the year in their filename and convert TSV to CSV if needed,
    then save a copy in the new folder. Includes logging for unmatched files.

    Parameters:
    - source_dir: Directory containing the original files.
    - target_dir: Directory where the renamed/converted files will be saved.
    """
    year_pattern = re.compile(r"\b(20\d{2})\b")
    processed_files = 0
    unmatched_files = []

    for file in os.listdir(source_dir):
        match = year_pattern.search(file)
        if match:
            year = match.group()
            file_path = os.path.join(source_dir, file)

            file_extension = os.path.splitext(file)[
                1
            ].lower()  # Normalize extension to lower case
            new_file_name = f"{year}{file_extension}"
            new_file_path = os.path.join(target_dir, new_file_name)

            if file_extension == ".tsv":
                df = pd.read_csv(file_path, sep="\t")
                new_file_path = new_file_path.replace(".tsv", ".csv")  # Convert to .csv
                df.to_csv(new_file_path, index=False)
            else:
                shutil.copy(file_path, new_file_path)
            processed_files += 1
        else:
            unmatched_files.append(file)

    return None


def manually_rename_files(source_dir, target_dir):
    files_to_rename = {
        "NMHSS_2017_PUF_CSV.csv": "2017.csv",
        "nmhss_puf_2016.csv": "2016.csv",
    }

    for original_name, new_name in files_to_rename.items():
        original_path = os.path.join(source_dir, original_name)
        new_path = os.path.join(target_dir, new_name)

        file_extension = os.path.splitext(original_name)[1].lower()

        if file_extension == ".tsv":
            # Convert TSV to CSV
            df = pd.read_csv(original_path, sep="\t")
            new_path = new_path.replace(
                ".tsv", ".csv"
            )  # Ensure the new path has a .csv extension
            df.to_csv(new_path, index=False)
        elif file_extension == ".csv":
            # If it's already a CSV, just copy it over
            shutil.copy(original_path, new_path)
        else:
            print(f"Unsupported file format for manual renaming: {original_name}")

    return None


def get_nmhss_container() -> dict:

    df_container = dict()

    for filename in os.listdir(_dir_path()):
        print(f"{filename}")

    for filename in os.listdir(_dir_path()):
        df = pd.read_csv(_dir_path(filename))
        print(f"filename: {filename}")
        year = filename.split(".")[0]
        print(f"year: {year}")

        df.columns = df.columns.str.lower()
        df = df.astype(str)
        if year == 2010:
            df["caseid"] = df["caseid"].str.zfill(5)

            fips_col = fips_codes()
            df = pd.merge(df, fips_col, on="stfips")
            df = df.rename(columns={"stusps": "lst"})
        else:
            df["caseid"] = df["caseid"].str[4:]

        df = df.map(lambda x: x.lower().strip() if isinstance(x, str) else x)

        df_container[year] = df

    return df_container


def _dir_path(*args):
    return os.path.join(data_path("NMHSS", "renamed", *args))


def fips_codes() -> pd.DataFrame:

    df = pd.read_csv(data_path("us-state-ansi-fips.csv"))
    df = df.drop("stname", axis=1)
    df = df.rename(columns={" st": "stfips"})

    return df


def process_qcor_prtf_data():

    dir_path = data_path("qcor", "prtf")
    processed_dfs = []

    for file in os.listdir(dir_path):
        # get year of file from csv name
        year_match = re.search(r"(\d{4})", file)
        if year_match:
            year = year_match.group(1)

        df = pd.read_csv(os.path.join(dir_path, file))
        df = get_qcor_national_totals(df, year)

        processed_dfs.append(df)

    out_df = pd.concat(processed_dfs)
    #out_df = out_df.reset_index(drop=True)

    out_df.to_csv(processed_data_path("clean_fig10_data.csv"), index=False)

    return None


def get_qcor_national_totals(df: pd.DataFrame, year: str) -> pd.DataFrame:
    df = df.rename(
        columns={
            "Unnamed: 1": "std_surv_std",
            "Unnamed: 2": "std_surv_cop",
            "Unnamed: 3": "comp_surv_std",
            "Unnamed: 4": "comp_surv_cop",
            "Unnamed: 7": "total_surv"
        }
    ).drop(["Unnamed: 5", "Unnamed: 6"], axis=1)

    df = (
        df[df["Selection Criteria"] == "National Total"]
        .drop("Selection Criteria", axis=1)
        .copy()
    )

    df["std_surv_tot"] = df[["std_surv_std", "std_surv_cop"]].astype(int).sum(axis=1)
    df["comp_surv_tot"] = df[["comp_surv_std", "comp_surv_cop"]].astype(int).sum(axis=1)
    df["year"] = year

    return df


if __name__ == "__main__":
    #convert_tsv_to_csv()
    #rename_files(data_path("NMHSS"), data_path("NMHSS", "renamed"))
    #manually_rename_files(data_path("NMHSS"), data_path("NMHSS", "renamed"))
    #process_fig4_data()
    #process_fig8_data()
    #df_container = get_nmhss_container()

    process_qcor_prtf_data()
