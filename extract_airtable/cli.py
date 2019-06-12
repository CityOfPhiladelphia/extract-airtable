import csv
from typing import List, Type, Optional, Dict
import sys
import os
import json

import requests
import click
import boto3


def to_snake_case(text: str) -> str:
    return text.replace(' ', '_').lower()

def get_fieldnames(app_id: str, 
                   api_key: str, 
                   table_name: str, 
                   n_rows: int = 1000) -> List[Type]:
    
    response = requests.get(
        'https://api.airtable.com/v0/{app_id}/{table_name}?maxRecords={max_records}'.format(
            app_id=app_id, 
            table_name=table_name, 
            max_records=n_rows,
        ),
        headers={
            'Authorization': 'Bearer {api_key}'.format(api_key=api_key)
        }
    )
    
    data = response.json()

    fieldnames = []

    for record in data['records']:
        record_fieldnames = list(record['fields'].keys())

        for fieldname in record_fieldnames:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
                
    return [to_snake_case(fieldname) for fieldname in fieldnames]

def get_records(app_id: str, 
                api_key: str, 
                table_name: str, 
                offset: Optional[int] = None, 
                rows_per_page: int = 1000) -> Type:
    
    response = requests.get(
        'https://api.airtable.com/v0/{app_id}/{table_name}?maxRecords={max_records}'.format(
            app_id=app_id, 
            table_name=table_name, 
            max_records=rows_per_page
        ),
        headers={
            'Authorization': 'Bearer {api_key}'.format(api_key=api_key)
        },
        params={
            'offset': offset
        }
    )
    
    data = response.json()
    
    yield data['records']
    
    if 'offset' in data:
        yield from get_records(app_id, api_key, table_name, offset=data['offset'], rows_per_page=1000)

def load_to_s3(s3_bucket: str, s3_key: str, file_path: str) -> None:
    s3 = boto3.resource('s3')
    s3.Object(s3_bucket, s3_key).put(Body=open(file_path, 'rb'))

def clean_up(file_path: str) -> None:
    if os.path.isfile(file_path):
        os.remove(file_path)

def extract_records_inner(app_id: str, 
                          api_key: str, 
                          table_name: str, 
                          offset: Optional[int] = None, 
                          rows_per_page: int = 1000,
                          s3_bucket: Optional[str] = None,
                          s3_key: Optional[str] = None) -> None:
    
    fieldnames = get_fieldnames(app_id, api_key, table_name)

    if (s3_bucket and s3_key):

        file_path = '{}.csv'.format(table_name)

        # On Linux, save to tmp folder
        if os.name != 'nt':
            file_path = '/tmp/{}'.format(file_path)

        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            snake_case_fieldnames = [to_snake_case(fieldname) for fieldname in fieldnames]
            writer.writerow(snake_case_fieldnames)

            for records_batch in get_records(app_id, api_key, table_name):
                for record in records_batch:
                    writer.writerow(record['fields'])

        load_to_s3(s3_bucket, s3_key, file_path)
        clean_up(file_path)

    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

        snake_case_fieldnames = [to_snake_case(fieldname) for fieldname in fieldnames]
        writer.writerow(snake_case_fieldnames)

        for records_batch in get_records(app_id, api_key, table_name):
            for record in records_batch:
                writer.writerow(record['fields'])
        
        sys.stdout.flush()

@click.group()
def main():
    pass

@main.command('extract-records')
@click.argument('app_id')
@click.argument('api_key')
@click.argument('table_name')
@click.option('--rows-per-page', default=1000, help='The number of rows to load per page')
@click.option('--s3-bucket', default=None, help='Optional S3 bucket to upload to')
@click.option('--s3-key', default=None, help='Optional S3 key to upload to')
def extract_records(app_id: str, 
                    api_key: str, 
                    table_name: str, 
                    rows_per_page: int = 1000,
                    s3_bucket: Optional[str] = None,
                    s3_key: Optional[str] = None) -> None:
                    
    extract_records_inner(
        app_id=app_id, 
        api_key=api_key, 
        table_name=table_name, 
        rows_per_page=rows_per_page, 
        s3_bucket=s3_bucket, 
        s3_key=s3_key)

if __name__ == '__main__':
    main()
