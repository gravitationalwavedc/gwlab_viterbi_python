from dataclasses import dataclass, field
from collections import UserList, OrderedDict
from pathlib import Path
from .utils import remove_path_anchor


@dataclass
class FileReference:
    """Object used to facilitate simpler downloading of files.
    """
    path: str
    file_size: int = field(repr=False)
    download_token: str = field(repr=False)
    job_id: int = field(repr=False)

    def __post_init__(self):
        self.path = remove_path_anchor(Path(self.path))
        self.file_size = int(self.file_size)


class FileReferenceList(UserList):
    """Used to store FileReference objects and provide simple methods with which to obtain their data.
    As a subclass of :class:`collections.UserList`, this class contains the same functionality as a regular list.
    It also contains several other useful methods.

    Parameters
    ----------
    initlist : list
        List of FileReference objects
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._check_items(self.data)

    def _check_items(self, items):
        for item in items:
            if not isinstance(item, FileReference):
                raise TypeError('All items in FileReferenceList must be a FileReference object')

    def append(self, item):
        """Use as you would list.append()

        Parameters
        ----------
        item : FileReference
            If this is not a FileReference instance, the method will fail

        Raises
        ------
        Exception
            Raised if item is not a FileReference
        """
        self._check_items([item])
        self.data.append(item)

    def get_total_bytes(self):
        """Sum the total size of each file represented in the list

        Returns
        -------
        int
            Total size of all files
        """
        total_bytes = 0
        for ref in self.data:
            total_bytes += ref.file_size

        return total_bytes

    def get_tokens(self):
        """Get all the download tokens in a list

        Returns
        -------
        list
            List of download tokens
        """
        return [ref.download_token for ref in self.data]

    def get_paths(self):
        """Get all the file paths in a list

        Returns
        -------
        list
            List of file paths
        """
        return [ref.path for ref in self.data]

    def get_output_paths(self, root_path, preserve_directory_structure=True):
        """Get all the file paths modified to give them a base directory.
        Can also optionally remove any existing directory structure

        Parameters
        ----------
        root_path : str or ~pathlib.Path
            Directory to add to the beginning of the file paths
        preserve_directory_structure : bool, optional
            Retain existing directory structure in the file paths, by default True

        Returns
        -------
        list
            List of output file paths
        """
        paths = []
        for ref in self.data:
            if preserve_directory_structure:
                paths.append(root_path / ref.path)
            else:
                paths.append(root_path / Path(ref.path.name))
        return paths

    def _batch_by_job_id(self):
        batched = OrderedDict()
        for ref in self.data:
            job_files = batched.get(ref.job_id, FileReferenceList())
            job_files.append(ref)
            batched[ref.job_id] = job_files

        return batched
