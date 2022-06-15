Starting a job
==============

The gwlab-viterbi-python API can also be used to start a Viterbi job, as we can using the Viterbi user interface.
However, instead of filling out the online forms, we use helper input classes.
Along with these inputs, each job requires a name, description and privacy setting.

Using input classes
-------------------

We have provided some helpful classes :mod:`gwlab_viterbi_python.utils.inputs` with the required inputs to start a job, prefilled with default values:

::

    from gwlab_viterbi_python.utils import DataInput, DataParametersInput, SearchParametersInput
    data_input = DataInput()
    data_params_input = DataParametersInput()
    search_params_input = SearchParametersInput()

    job = gwc.start_viterbi_job(
        job_name="a_meaningful_name",
        job_description="This job will usher in a new age of learning",
        private=True,
        data_input=data_input,
        data_params=data_params_input,
        search_params=search_params_input
    )

This method returns a ViterbiJob instance containing information on your new job.

Alternatively, you can override the default values in the input classes. For example, we can set the frequency band start and width as follows:

::

    data_parameters_input = DataParametersInput(
        start_frequency_band="200",
        freq_band="2"
    )


Monitoring job status
---------------------

While :class:`.ViterbiJob` instances only show the job name and ID when printed, they store more useful attributes, such as the description, the job status and others.
To observe the status of a job, we can just print the :attr:`.ViterbiJob.status` attribute. This attribute stores a dictionary containing the status name and the date when this status began.
For example, if we run:

::
    
    print(job.status)

we are shown that the job has been completed, and hence will have an associated list of result files:

::

    {'name': 'Completed', 'date': '2021-05-31T03:16:36+00:00'}
