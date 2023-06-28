import pandas as pd
import datetime
import re
import time
import pytz
import numpy as np
import os
class Log_Reader:
    def __init__(self, log_path, output_path):
        self.log_path = log_path
        self.output_path = output_path

    def __str__(self):
        return f"Here is the path to the output log file: {self.output_path} \n" \
               f"You can use log_rewrite() for transfer your file into the csv format \n" \
               f"Main method for reading log is log_read() \n" \
               f"If there is no file that exists in output path - it creates one \n"
    def UTC_timestamp(self, time_str):
        time_format = "%d/%b/%Y:%H:%M:%S %z"

        offset_hours = int(time_str[-5:-3])
        offset_minutes = int(time_str[-3:-1])

        total_offset_minutes = offset_hours * 60 + offset_minutes
        dt = datetime.datetime.strptime(time_str, time_format)

        timezone = pytz.FixedOffset(total_offset_minutes)

        dt_utc = dt.astimezone(pytz.utc) - timezone.utcoffset(dt)

        timestamp = (dt_utc - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        return timestamp


    def log_rewrite(self):
        # Read the log file into a DataFrame
        df = pd.read_csv(self.log_path, header=None)
        new_df = pd.DataFrame()
        df.columns = ['Text']

        # Extract the info from the log file
        new_df['client IP'] = df['Text'].apply(lambda x: re.findall(r'(.*?)' + re.escape(' - - '), x)[0])
        new_df['time_local'] = df['Text'].apply(lambda x: re.findall(r'\[(.*?)\]', x)[0])

        # Apply the 'UTC_timestamp' function to convert 'time_local' to a timestamp
        new_df['timestamp'] = new_df['time_local'].apply(self.UTC_timestamp)

        new_df['status'] = df['Text'].apply(lambda x: re.findall(re.escape('" ') + '(.*?)' + re.escape(' '), x)[0])
        new_df['request'] = df['Text'].apply(lambda x: re.findall(re.escape('"') + '(.*?)' + re.escape('/?'), x)[0])
        new_df['gtName'] = df['Text'].apply(lambda x: re.findall(re.escape('gtName=') + '(.*?)' + re.escape('&'), x)[0])
        new_df['majorIOV'] = df['Text'].apply(lambda x: re.findall(re.escape('majorIOV=') + '(.*?)' + re.escape('&'), x)[0])
        new_df['minorIOV'] = df['Text'].apply(lambda x: re.findall(re.escape('minorIOV=') + '(.*?)' + re.escape(' '), x)[0])
        new_df['HTTP_version'] = df['Text'].apply(lambda x: re.findall(re.escape('HTTP/') + '(.*?)' + re.escape('"'), x)[0])
        new_df['byte size'] = df['Text'].apply(lambda x: re.findall(re.escape('" 200 ') + '(.*?)' + re.escape(' "-"'), x)[0])
        new_df['additional info'] = df['Text'].str.extract(r'HTTP(.*)')
        new_df['additional info'] = new_df['additional info'].str.replace('"', '')

        file_path = self.output_path
        # Write the new DataFrame to a CSV file with tab-separated values
        new_df.to_csv(file_path, sep='\t', index=False)

    def log_read(self):
        if os.path.exists(self.output_path):
            print('file exists')
        else:
            self.log_rewrite()
        df = pd.read_csv(self.output_path, delimiter='\t')
        return df
