Starting a job
==============

The gwlab-viterbi-python API can also be used to start a Viterbi job, as we can using the Viterbi user interface.
However, instead of filling out the online forms, we use helper input classes.
Along with these inputs, each job requires a name, description and privacy setting.

Using input classes
-------------------

Viterbi jobs can be started using the :meth:`gwlab_viterbi_python.GWLabViterbi.start_viterbi_job` method.
Each job requires a name, a description and a privacy setting. To submit a job with the default settings, we can run:

::

    job = gwl.start_viterbi_job(
        job_name="a_meaningful_name",
        job_description="This job will usher in a new age of learning",
        private=True
    )

This method returns a ViterbiJob instance containing information on our new job, along with helpful methods for :ref:`obtaining results files <results-files>`.

In :mod:`.gwlab_viterbi_python.inputs`, we have provided some helpful classes with the required inputs to start a job.
These classes are prefilled with default values for each input field. Alternatively, the default values can be overridden to tailor a Viterbi job for our needs.
For example, we can set the frequency band start and width as follows:

::

    from gwlab_viterbi_python import DataParametersInput

    data_parameters_input = DataParametersInput(
        start_frequency_band="200",
        freq_band="2"
    )

    job = gwl.start_viterbi_job(
        job_name="a_meaningful_name",
        job_description="This job will usher in a new age of learning",
        private=True,
        data_params=data_parameters_input
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
