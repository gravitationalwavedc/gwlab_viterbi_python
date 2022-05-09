import logging

from gwdc_python import GWDC

from .viterbi_job import ViterbiJob
from .file_reference import FileReference, FileReferenceList
from .helpers import TimeRange
from .utils import convert_dict_keys
from .settings import GWLAB_VITERBI_ENDPOINT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class GWLabViterbi:
    def __init__(self, token, endpoint=GWLAB_VITERBI_ENDPOINT):
        self.client = GWDC(token=token, endpoint=endpoint)
        self.request = self.client.request

    def _get_job_model_from_query(self, query_data):
        if not query_data:
            return None

        return ViterbiJob(
            client=self,
            **convert_dict_keys(
                query_data,
                {'id': 'job_id'}
            )
        )

    def get_public_job_list(self, search="", time_range=TimeRange.ANY, number=100):
        """Obtains a list of public Viterbi jobs, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        search : str, optional
            Search terms by which to filter public job list, by default ""
        time_range : .TimeRange or str, optional
            Time range by which to filter job list, by default TimeRange.ANY
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
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
        """

        variables = {
            "search": search,
            "timeRange": time_range.value if isinstance(time_range, TimeRange) else time_range,
            "first": number
        }

        data = self.request(query=query, variables=variables)

        if not data['publicViterbiJobs']['edges']:
            logger.info('Job search returned no results.')
            return []

        return [self._get_job_model_from_query(job['node']) for job in data['publicViterbiJobs']['edges']]

    def get_job_by_id(self, job_id):
        """Get a Viterbi job instance corresponding to a specific job ID

        Parameters
        ----------
        job_id : str
            ID of job to obtain

        Returns
        -------
        ViterbiJob
            ViterbiJob instance corresponding to the input ID
        """
        query = """
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
        """

        variables = {
            "id": job_id
        }

        data = self.request(query=query, variables=variables)

        if not data['viterbiJob']:
            logger.info('No job matching input ID was returned.')
            return None

        return self._get_job_model_from_query(data['viterbiJob'])

    def get_user_jobs(self, number=100):
        """Obtains a list of Viterbi jobs created by the user, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
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
        """

        variables = {
            "first": number
        }

        data = self.request(query=query, variables=variables)

        return [self._get_job_model_from_query(job['node']) for job in data['viterbiJobs']['edges']]

    def _get_files_by_job_id(self, job_id):
        query = """
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
        """

        variables = {
            "jobId": job_id
        }

        data = convert_dict_keys(self.request(query=query, variables=variables))

        file_list = FileReferenceList()
        for file_data in data['viterbi_result_files']['files']:
            if file_data['is_dir']:
                continue
            file_data.pop('is_dir')
            file_list.append(
                FileReference(
                    **file_data,
                    job_id=job_id,
                )
            )

        return file_list
