import csv
import os


def write_voting_data(file_path, user_id, media_path, vote, ground_truth, response_time):
    """Write voting data to a CSV file."""
    header = ["Name", "File", "Vote", "Truth", "Response Time"]
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the correct header if the file is new
            writer.writerow(header)
        writer.writerow([user_id, media_path, vote,
                        ground_truth, round(response_time, 2)])


def read_voting_data(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)
