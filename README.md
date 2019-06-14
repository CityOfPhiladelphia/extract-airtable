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

## Tests
```bash
pytest tests/
```

## Deployment
When a commit is made to master or test, Travis CI builds a docker image with an installed version of this repo and pushes it to ECR.

For this reason you should make changes to the test branch, make sure they pass automated tests and manual QA testing before making any changes to master.