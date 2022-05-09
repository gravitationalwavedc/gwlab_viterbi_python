import pytest
from pathlib import Path
from gwlab_viterbi_python import FileReference, FileReferenceList
from gwlab_viterbi_python.utils import remove_path_anchor


@pytest.fixture
def setup_dicts():
    return [
        {
            'path': 'data/dir/test1.png',
            'file_size': '1',
            'download_token': 'test_token_1',
            'job_id': 'id1',
        },
        {
            'path': 'data/dir/test2.png',
            'file_size': '1',
            'download_token': 'test_token_2',
            'job_id': 'id1',
        },
        {
            'path': 'result/dir/test1.txt',
            'file_size': '1',
            'download_token': 'test_token_3',
            'job_id': 'id2',
        },
        {
            'path': 'result/dir/test2.txt',
            'file_size': '1',
            'download_token': 'test_token_4',
            'job_id': 'id2',
        },
        {
            'path': 'test1.json',
            'file_size': '1',
            'download_token': 'test_token_5',
            'job_id': 'id3',
        },
        {
            'path': 'test2.json',
            'file_size': '1',
            'download_token': 'test_token_6',
            'job_id': 'id3',
        },
    ]


def test_file_reference(setup_dicts):
    for file_dict in setup_dicts:
        ref = FileReference(**file_dict)
        assert ref.path == remove_path_anchor(Path(file_dict['path']))
        assert ref.file_size == int(file_dict['file_size'])
        assert ref.download_token == file_dict['download_token']
        assert ref.job_id == file_dict['job_id']


def test_file_reference_list(setup_dicts):
    file_references = [FileReference(**file_dict) for file_dict in setup_dicts]
    file_reference_list = FileReferenceList(file_references)

    for i, ref in enumerate(file_reference_list):
        assert ref.path == file_references[i].path
        assert ref.file_size == file_references[i].file_size
        assert ref.download_token == file_references[i].download_token
        assert ref.job_id == file_references[i].job_id


def test_file_reference_list_types(setup_dicts):
    file_references = [FileReference(**file_dict) for file_dict in setup_dicts]
    file_reference_list = FileReferenceList(file_references)
    file_reference_list_appended = FileReferenceList()
    for ref in file_references:
        file_reference_list_appended.append(ref)

    assert file_reference_list == file_reference_list_appended

    # Check that other types can't be appended or included in initial data
    with pytest.raises(TypeError):
        FileReferenceList().append(1)

    with pytest.raises(TypeError):
        FileReferenceList().append('string')

    with pytest.raises(TypeError):
        FileReferenceList([1])

    with pytest.raises(TypeError):
        FileReferenceList(['string'])
