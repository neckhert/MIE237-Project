import csv
import os

def write_voting_data(file_path, user_id, video_id, vote, ground_truth):
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['User ID', 'Data ID', 'Vote', 'Ground Truth'])
        
        writer.writerow([user_id, video_id, vote, ground_truth])

def read_voting_data(file_path):
    if not os.path.isfile(file_path):
        return []
    
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)