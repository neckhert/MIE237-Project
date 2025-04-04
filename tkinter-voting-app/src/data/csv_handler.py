import csv
import os


def write_voting_data(file_path, user_id, media_path, vote, ground_truth):
    """Write voting data to a CSV file."""
    header = ["User ID", "Media Path", "Vote", "Ground Truth"]
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Write the header if the file is new
        writer.writerow([user_id, media_path, vote, ground_truth])


def read_voting_data(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)
