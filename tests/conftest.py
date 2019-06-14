import sys
import os
import json

import pytest


@pytest.fixture(scope='module')
def response():
    os.chdir('tests')
    
    with open(os.path.join('fixtures_data', 'immigrant_services.json')) as f:
        return json.load(f)
