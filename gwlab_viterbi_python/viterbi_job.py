import logging
from .utils import file_filters
from .helpers import JobStatus

from gwdc_python.jobs import JobBase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class ViterbiJob(JobBase):
    """
    ViterbiJob class is useful for interacting with the Viterbi jobs returned from a call to the GWCloud API.
    It is primarily used to store job information and obtain files related to the job.

    Parameters
    ----------
    client : ~gwlab_viterbi_python.gwlab_viterbi.GWLabViterbi
        A reference to the GWLabViterbi object instance from which the ViterbiJob was created
    job_id : str
        The id of the Viterbi job, required to obtain the files associated with it
    name : str
        Job name
    description : str
        Job description
    user : str
        User that ran the job
    job_status : dict
        Status of job, should have 'name' and 'date' keys corresponding to the status code and when it was produced
    kwargs : dict, optional
        Extra arguments, stored in `other` attribute
    """

    FILE_LIST_FILTERS = {
        'ini': file_filters.ini_filter,
        'candidates': file_filters.candidates_filter
    }

    def __init__(self, client, job_id, name, description, user, job_status, **kwargs):
        self.client = client
        self.job_id = job_id
        self.name = name
        self.description = description
        self.user = user
        self.status = JobStatus(status=job_status['name'], date=job_status['date'])
        self.other = kwargs

    def __eq__(self, other):
        if isinstance(other, ViterbiJob):
            return (
                self.job_id == other.job_id and
                self.name == other.name and
                self.user == other.user
            )
        return False

    def get_full_file_list(self):
        """Get information for all files associated with this job

        Returns
        -------
        ~gwdc_python.files.file_reference.FileReferenceList
            Contains :class:`~gwdc_python.files.file_reference.FileReference` instances
            for each of the files associated with this job
        """
        result = self.client._get_files_by_job_id(self.job_id)
        return result
