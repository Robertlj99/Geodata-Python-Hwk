import pandas as pd
from pathlib import Path

# We use relative path here. Since the "read_csv_file_into_dataframe.py" is in the "Midterm_Code" directory,
# We need "../Data" to access the "Data" directory. "../" means the upper level directory of the current directory.
# If "Data" is in the same directory as "read_csv_file_into_dataframe.py, we will use "./Data" here, in which
# "./" stands for the current or the same directory.
data_path = Path("../Data")
beaufort_voter_txt_file = data_path / "beaufort_voter.csv"

# call the read_csv function
voter_df = pd.read_csv(beaufort_voter_txt_file)

# print header information
print("table headers:\n", voter_df.columns)

# print the voter status
# set function: convert any of the iterable to a sequence of iterable elements with distinct elements
print("voter status: ", set(voter_df["voter_status_desc"]))

# select "REMOVED" voters
removed_voter_flags = voter_df["voter_status_desc"] == "REMOVED"
removed_voter_df = voter_df[removed_voter_flags]

# count the number of removed voters
print("Total number of removed voters: ", len(removed_voter_df))

# save "REMOVED" voters into a CSV file
removed_voter_df.to_csv("./removed_voters.csv")

