import sys
from unittest.mock import patch

sys.path.append('../')
from extract_airtable.cli import get_fieldnames, get_records, process_row


APP_ID = 'fake_app_id'
API_KEY = 'fake_api_key'
TABLE_NAME = 'immigration_services'

@patch('requests.get')
def test_getfieldnames(mocked_request, response):
    mocked_request.return_value.json.return_value = response

    fieldnames = get_fieldnames(
        app_id=APP_ID,
        api_key=API_KEY,
        table_name=TABLE_NAME)

    expected_fieldnames = [
        'organization_name',
        'street_address',
        'phone_number',
        'email',
        'website',
        'services_offered',
        'tags',
        'hide_on_finder',
    ]

    assert fieldnames == expected_fieldnames

@patch('requests.get')
def test_get_records(mocked_request, response):
    mocked_request.return_value.json.return_value = response

    first_record = next(
        get_records(
            app_id=APP_ID,
            api_key=API_KEY,
            table_name=TABLE_NAME
        )
    )[0]

    expected_first_record = {
        'id': 'rec0pNEBObUtWbnT4',
        'fields': {
            'organization_name': 'Bethanna',
            'street_address': '2501 Reed Street, Philadelphia, PA 19146',
            'phone_number': '215-568-2435',
            'email': 'info@bethanna.org',
            'website': 'www.bethanna.org',
            'services_offered': [
                'Health/mental health services',
                'Immigrant focused youth programs'
            ],
            'tags': [
                'English',
                'Haitian-Creole',
                'Mandarin',
                'Spanish',
                'Swahili'
            ]
        },
        'createdTime': '2019-06-11T00:28:54.000Z'
    }

    assert first_record == expected_first_record

def test_process_row():
    row = {
        'website': 'www.bethanna.org',
        'services_offered': [
            'Health/mental health services',
            'Immigrant focused youth programs'
        ]
    }

    assert process_row(row) == {
        'website': 'www.bethanna.org',
        'services_offered': '["Health/mental health services", "Immigrant focused youth programs"]'
    }
