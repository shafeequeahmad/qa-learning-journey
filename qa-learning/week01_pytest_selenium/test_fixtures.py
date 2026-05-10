import pytest

# Without fixture — you repeat setup in every test (bad):
def test_one():
    """Test case for one."""
    data = {'bucket': 'test', 'size': 100}
    assert data['bucket'] == 'test'
    print(data)
    data.clear()

# With fixture — setup runs automatically (good):
@pytest.fixture
def bucket():
    """Fixture that returns a dictionary representing a storage bucket."""
    data = {'bucket': 'test', 'size': 100}
    print("1:",data)
    yield data
    data.clear()  # runs after test automatically
    print("2:",data)

def test_bucket_name(bucket):
    """Test case for bucket name."""
    print(" --> test_bucket_name")
    assert bucket['bucket'] == 'test'

def test_bucket_size(bucket):
    """Test case for bucket size."""
    print(" --> test_bucket_size")
    assert bucket['size'] == 100


