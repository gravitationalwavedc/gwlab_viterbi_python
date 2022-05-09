import pytest
from gwlab_viterbi_python import ViterbiJob, FileReference, FileReferenceList


@pytest.fixture
def png_data_result():
    return FileReferenceList([
        FileReference(
            path='data/dir/test1.png',
            file_size='1',
            download_token='test_token_1',
            job_id='id'
        ),
        FileReference(
            path='data/dir/test2.png',
            file_size='1',
            download_token='test_token_2',
            job_id='id'
        ),
        FileReference(
            path='result/dir/test1.png',
            file_size='1',
            download_token='test_token_3',
            job_id='id'
        ),
        FileReference(
            path='result/dir/test2.png',
            file_size='1',
            download_token='test_token_4',
            job_id='id'
        ),
    ])


@pytest.fixture
def png_extra():
    return FileReferenceList([
        FileReference(
            path='test1.png',
            file_size='1',
            download_token='test_token_5',
            job_id='id'
        ),
        FileReference(
            path='test2.png',
            file_size='1',
            download_token='test_token_6',
            job_id='id'
        ),
        FileReference(
            path='arbitrary/dir/test1.png',
            file_size='1',
            download_token='test_token_7',
            job_id='id'
        ),
        FileReference(
            path='arbitrary/dir/test2.png',
            file_size='1',
            download_token='test_token_8',
            job_id='id'
        ),
    ])


@pytest.fixture
def corner():
    return FileReferenceList([
        FileReference(
            path='test1_corner.png',
            file_size='1',
            download_token='test_token_9',
            job_id='id'
        ),
        FileReference(
            path='test2_corner.png',
            file_size='1',
            download_token='test_token_10',
            job_id='id'
        ),
    ])


@pytest.fixture
def config():
    return FileReferenceList([
        FileReference(
            path='a_config_complete.ini',
            file_size='1',
            download_token='test_token_11',
            job_id='id'
        ),
    ])


@pytest.fixture
def json():
    return FileReferenceList([
        FileReference(
            path='result/dir/a_merge_result.json',
            file_size='1',
            download_token='test_token_12',
            job_id='id'
        ),
    ])


@pytest.fixture
def index():
    return FileReferenceList([
        FileReference(
            path='index.html',
            file_size='1',
            download_token='test_token_13',
            job_id='id'
        ),
    ])


@pytest.fixture
def png(png_data_result, png_extra, corner):
    return png_data_result + png_extra + corner


@pytest.fixture
def default(png_data_result, config, json, index):
    return png_data_result + config + json + index


@pytest.fixture
def full(png, config, json, index):
    return png + config + json + index


@pytest.fixture
def mock_viterbi_job(mocker):
    def viterbi_job(methods={}):
        config_dict = {f'{key}.return_value': value for key, value in methods.items()}
        return ViterbiJob(
            client=mocker.Mock(**config_dict),
            job_id='test_id',
            name='TestName',
            description='Test description',
            user='Test User',
            job_status={
                'name': 'Completed',
                'date': '2021-12-02'
            },
        )

    return viterbi_job


@pytest.fixture
def mock_viterbi_job_files(mock_viterbi_job, full):
    return mock_viterbi_job({'_get_files_by_job_id': full})


def test_viterbi_job_full_file_list(mock_viterbi_job_files, full):
    viterbi_job = mock_viterbi_job_files
    assert viterbi_job.get_full_file_list() == full

    viterbi_job.client._get_files_by_job_id.assert_called_once()


def test_viterbi_job_equality(mocker):
    job_data = {
        "client": mocker.Mock(),
        "job_id": 1,
        "name": "test_name",
        "description": "test description",
        "user": "Test User",
        "job_status": {
            "name": "Completed",
            "date": "2021-01-01"
        }
    }
    job_data_changed_id = {**job_data, "job_id": 2}
    job_data_changed_name = {**job_data, "name": "testing_name"}
    job_data_changed_user = {**job_data, "user": "Testing User"}

    assert ViterbiJob(**job_data) == ViterbiJob(**job_data)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_id)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_name)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_user)
