from dataclasses import dataclass, field
from collections import UserList
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
