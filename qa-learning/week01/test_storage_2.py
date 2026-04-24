import pytest

@pytest.mark.storage
def test_get_storage_configuration(storage_config):
    print("--> host : ", storage_config['host'])
    print("--> port : ", storage_config['port'])
    print("--> access_key : ", storage_config['access_key'])
    print("--> secret_key : ", storage_config['secret_key'])
    
