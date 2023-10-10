import boto3
from datetime import datetime, timedelta, timezone
import json

# Define the date threshold, for example here search for snapshots created before 06 Oct 2023
threshold_date = datetime(2023, 10, 6, tzinfo=timezone.utc)

# Create a Boto3 EC2 client
ec2_client = boto3.client('ec2')

# Define the search parameters : Here for example search for all snapshots having the word "bs-scratch" in their description

filters = [
    {'Name': 'description', 'Values': ['*bs-scratch*']},
]

# Retrieve all snapshots matching the filters
response = ec2_client.describe_snapshots(Filters=filters)

# Filter snapshots created before the specified date
snapshots = [snapshot for snapshot in response['Snapshots'] if snapshot['StartTime'] < threshold_date]


description  = "bs-scratch"
tag_1 = {"Key":"application","Value":"cgmqs-pixelhub" }
tag_2 = {"Key":"type","Value":"singleuser-storage" }


# Filter snapshots created before the specified date
snapshots = [snapshot for snapshot in response['Snapshots'] if snapshot['StartTime'] < threshold_date]


output_snapshots = {}
i = 1
for snap in snapshots :
    if description in snap["Description"] and "Tags" in snap :
        if tag_1 in snap['Tags'] and tag_2 in snap['Tags'] :    
            print (snap)
            output_snapshots[i] = {'Description':snap['Description'],"SnapshotId":snap["SnapshotId"],"StartTime":str(snap["StartTime"]), "Tags":snap["Tags"]}
            i = i+1

# Extract the result as a json file 
with open("snapshots.json", "w") as json_file:
    json.dump(output_snapshots, json_file, indent=2 )
            
