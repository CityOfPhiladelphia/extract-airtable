# extract-airtable

Command line tool to extract data from Airtable

## Requirements
- Python 3.5+
- Pip
- Airtable App ID and API Key

## Usage
```bash
# Extract records to stdout
extract-airtable extract-records \
                 your-airtable-app-id \
                 your-airtable-api-key \
                 airtable-table-name

# Extract records to S3
extract-airtable extract-records \
                 your-airtable-app-id \
                 your-airtable-api-key \
                 airtable-table-name \
                 --s3-bucket my-s3-bucket \
                 --s3-key my-s3-key
```

## Installation
```bash
pip install git+https://github.com/CityOfPhiladelphia/extract-airtable#egg=extract_airtable
```
