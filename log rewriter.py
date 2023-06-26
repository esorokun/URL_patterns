import pandas as pd
import datetime
import re
import time
import pytz
import numpy as np


def UTC_timestamp(time_str):
    # Define the format of the input time string
    time_format = "%d/%b/%Y:%H:%M:%S %z"

    offset_hours = int(time_str[-5:-3])
    offset_minutes = int(time_str[-3:-1])

    # Calculate the total offset in minutes
    total_offset_minutes = offset_hours * 60 + offset_minutes
    dt = datetime.datetime.strptime(time_str, time_format)

    # Create a FixedOffset timezone object based on the total offset
    timezone = pytz.FixedOffset(total_offset_minutes)

    # Convert the datetime to UTC by subtracting the timezone offset
    dt_utc = dt.astimezone(pytz.utc) - timezone.utcoffset(dt)

    # Calculate the timestamp in seconds since the Unix epoch (January 1, 1970)
    timestamp = (dt_utc - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return timestamp


if __name__ == '__main__':
    # Read the log file into a DataFrame
    df = pd.read_csv('~/Desktop/log_file.txt', header=None)
    new_df = pd.DataFrame()
    df.columns = ['Text']

    # Extract the info from the log file
    new_df['remote_addr'] = df['Text'].apply(lambda x: re.findall(r'(.*?)' + re.escape(' - - '), x)[0])
    new_df['time_local'] = df['Text'].apply(lambda x: re.findall(r'\[(.*?)\]', x)[0])

    # Apply the 'UTC_timestamp' function to convert 'time_local' to a timestamp
    new_df['timestamp'] = new_df['time_local'].apply(UTC_timestamp)

    new_df['status'] = df['Text'].apply(lambda x: re.findall(re.escape('" ') + '(.*?)' + re.escape(' '), x)[0])
    new_df['request'] = df['Text'].apply(lambda x: re.findall(re.escape('"') + '(.*?)' + re.escape('/?'), x)[0])
    new_df['gtName'] = df['Text'].apply(lambda x: re.findall(re.escape('gtName=') + '(.*?)' + re.escape('&'), x)[0])
    new_df['majorIOV'] = df['Text'].apply(lambda x: re.findall(re.escape('majorIOV=') + '(.*?)' + re.escape('&'), x)[0])
    new_df['minorIOV'] = df['Text'].apply(lambda x: re.findall(re.escape('minorIOV=') + '(.*?)' + re.escape(' '), x)[0])
    new_df['HTTP_version'] = df['Text'].apply(lambda x: re.findall(re.escape('HTTP/') + '(.*?)' + re.escape('"'), x)[0])

    # Extract additional information from the log file (last info in the string)
    new_df['additional info'] = df['Text'].str.extract(r'HTTP(.*)')
    # Remove double quotes from the 'additional info' column
    new_df['additional info'] = new_df['additional info'].str.replace('"', '')

    file_path = "~/Desktop/output.csv"
    # Write the new DataFrame to a CSV file with tab-separated values
    new_df.to_csv(file_path, sep='\t', index=False)
