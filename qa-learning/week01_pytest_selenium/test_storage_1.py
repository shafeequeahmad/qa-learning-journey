# run test using below cmd
# python -m pytest  -s  -v  -m storage

import pytest

@pytest.mark.storage
def test_post_storage_configuration(storage_config):
    # Simulate updating the storage configuration
    """Test case for post storage configuration."""
    storage_config['port'] = 9001
    storage_config['access_key'] = 'root'
    print(">>>>>", storage_config)

@pytest.mark.storage
def test_get_storage_configuration(storage_config):
    """Test case for get storage configuration."""
    print("--> host : ", storage_config['host'])
    print("--> port : ", storage_config['port'])
    print("--> access_key : ", storage_config['access_key'])
    print("--> secret_key : ", storage_config['secret_key'])
    
