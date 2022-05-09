from gwlab_viterbi_python import GWLabViterbi, ViterbiJob, FileReference, JobStatus, TimeRange
from gwlab_viterbi_python.utils import convert_dict_keys
import pytest


@pytest.fixture
def setup_gwl_request(mocker):
    def mock_init(self, token, endpoint):
        pass

    mock_request = mocker.Mock()
    mocker.patch('gwlab_viterbi_python.gwlab_viterbi.GWDC.__init__', mock_init)
    mocker.patch('gwlab_viterbi_python.gwlab_viterbi.GWDC.request', mock_request)

    return GWLabViterbi(token='my_token'), mock_request


@pytest.fixture
def job_data():
    return [
        {
            "id": 1,
            "name": "test_name_1",
            "description": "test description 1",
            "user": "Test User1",
            "jobStatus": {
                "name": "Completed",
                "date": "2021-01-01"
            }
        },
        {
            "id": 2,
            "name": "test_name_2",
            "description": "test description 2",
            "user": "Test User2",
            "jobStatus": {
                "name": "Completed",
                "date": "2021-02-02"
            }
        },
        {
            "id": 3,
            "name": "test_name_3",
            "description": "test description 3",
            "user": "Test User3",
            "jobStatus": {
                "name": "Error",
                "date": "2021-03-03"
            }
        }
    ]


def multi_job_request(query_name, return_job_data):
    return {
        query_name: {
            "edges": [{"node": job_datum} for job_datum in return_job_data],
        }
    }


@pytest.fixture
def job_file_data():
    return [
        {
            "path": "path/to/test.png",
            "fileSize": "1",
            "downloadToken": "test_token_1",
            "isDir": False
        },
        {
            "path": "path/to/test.json",
            "fileSize": "10",
            "downloadToken": "test_token_2",
            "isDir": False
        },
        {
            "path": "path/to/test",
            "fileSize": "100",
            "downloadToken": "test_token_3",
            "isDir": True
        }
    ]


def test_get_job_model_from_query(setup_gwl_request, job_data):
    gwl, _ = setup_gwl_request
    single_job_data = job_data[0]

    assert gwl._get_job_model_from_query(None) is None

    expected = ViterbiJob(
        client=gwl,
        job_id=single_job_data["id"],
        name=single_job_data["name"],
        description=single_job_data["description"],
        user=single_job_data["user"],
        job_status=single_job_data["jobStatus"],
    )
    assert gwl._get_job_model_from_query(single_job_data) == expected


def test_get_job_by_id(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = {"viterbiJob": None}
    assert gwl.get_job_by_id('job_id') is None

    single_job_data = job_data[0]
    mock_request.return_value = {"viterbiJob": single_job_data}

    job = gwl.get_job_by_id('job_id')

    mock_request.assert_called_with(
        query="""
            query ($id: ID!){
                viterbiJob (id: $id) {
                    id
                    name
                    user
                    description
                    jobStatus {
                        name
                        date
                    }
                }
            }
        """,
        variables={
            "id": "job_id"
        }
    )

    assert job.job_id == single_job_data["id"]
    assert job.name == single_job_data["name"]
    assert job.description == single_job_data["description"]
    assert job.status == JobStatus(
        status=single_job_data["jobStatus"]["name"],
        date=single_job_data["jobStatus"]["date"]
    )
    assert job.user == single_job_data["user"]


def test_get_user_jobs(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = multi_job_request('viterbiJobs', [])
    assert gwl.get_user_jobs() == []

    mock_request.return_value = multi_job_request('viterbiJobs', job_data)
    jobs = gwl.get_user_jobs(number=100)
    mock_request.assert_called_with(
        query="""
            query ($first: Int){
                viterbiJobs (first: $first){
                    edges {
                        node {
                            id
                            name
                            user
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """,
        variables={
            "first": 100
        }
    )

    assert jobs[0].job_id == job_data[0]["id"]
    assert jobs[0].name == job_data[0]["name"]
    assert jobs[0].description == job_data[0]["description"]
    assert jobs[0].status == JobStatus(
        status=job_data[0]["jobStatus"]["name"],
        date=job_data[0]["jobStatus"]["date"]
    )
    assert jobs[0].user == job_data[0]["user"]

    assert jobs[1].job_id == job_data[1]["id"]
    assert jobs[1].name == job_data[1]["name"]
    assert jobs[1].description == job_data[1]["description"]
    assert jobs[1].status == JobStatus(
        status=job_data[1]["jobStatus"]["name"],
        date=job_data[1]["jobStatus"]["date"]
    )
    assert jobs[1].user == job_data[1]["user"]

    assert jobs[2].job_id == job_data[2]["id"]
    assert jobs[2].name == job_data[2]["name"]
    assert jobs[2].description == job_data[2]["description"]
    assert jobs[2].status == JobStatus(
        status=job_data[2]["jobStatus"]["name"],
        date=job_data[2]["jobStatus"]["date"]
    )
    assert jobs[2].user == job_data[2]["user"]


def test_get_public_job_list(setup_gwl_request, job_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = multi_job_request('publicViterbiJobs', [])
    assert gwl.get_public_job_list() == []

    mock_request.return_value = multi_job_request('publicViterbiJobs', job_data)
    jobs = gwl.get_public_job_list(search="Test", time_range=TimeRange.DAY, number=100)

    mock_request.assert_called_with(
        query="""
            query ($search: String, $timeRange: String, $first: Int){
                publicViterbiJobs (search: $search, timeRange: $timeRange, first: $first) {
                    edges {
                        node {
                            id
                            user
                            name
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """,
        variables={
            "search": "Test",
            "timeRange": TimeRange.DAY.value,
            "first": 100
        }
    )

    assert jobs[0].job_id == job_data[0]["id"]
    assert jobs[0].name == job_data[0]["name"]
    assert jobs[0].description == job_data[0]["description"]
    assert jobs[0].status == JobStatus(
        status=job_data[0]["jobStatus"]["name"],
        date=job_data[0]["jobStatus"]["date"]
    )
    assert jobs[0].user == job_data[0]["user"]

    assert jobs[1].job_id == job_data[1]["id"]
    assert jobs[1].name == job_data[1]["name"]
    assert jobs[1].description == job_data[1]["description"]
    assert jobs[1].status == JobStatus(
        status=job_data[1]["jobStatus"]["name"],
        date=job_data[1]["jobStatus"]["date"]
    )
    assert jobs[1].user == job_data[1]["user"]

    assert jobs[2].job_id == job_data[2]["id"]
    assert jobs[2].name == job_data[2]["name"]
    assert jobs[2].description == job_data[2]["description"]
    assert jobs[2].status == JobStatus(
        status=job_data[2]["jobStatus"]["name"],
        date=job_data[2]["jobStatus"]["date"]
    )
    assert jobs[2].user == job_data[2]["user"]


def test_gwlloud_files_by_job_id(setup_gwl_request, job_file_data):
    gwl, mock_request = setup_gwl_request
    mock_request.return_value = {
        "viterbiResultFiles": {
            "files": job_file_data,
        }
    }

    file_list = gwl._get_files_by_job_id('arbitrary_job_id')

    mock_request.assert_called_with(
        query="""
            query ($jobId: ID!) {
                viterbiResultFiles (jobId: $jobId) {
                    files {
                        path
                        isDir
                        fileSize
                        downloadToken
                    }
                }
            }
        """,
        variables={
            "jobId": "arbitrary_job_id"
        }
    )

    for i, ref in enumerate(file_list):
        job_file_data[i].pop('isDir')
        assert ref == FileReference(
            **convert_dict_keys(job_file_data[i]),
            job_id='arbitrary_job_id',
        )
