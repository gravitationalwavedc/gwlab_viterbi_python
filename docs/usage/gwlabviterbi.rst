Using the GWLabViterbi class
============================

The GWLabViterbi class will be used to handle all requests to the GWLab server.
The public methods of the GWLab class are focused on searching for and obtaining information for specific Viterbi jobs.
Below we will walk through some of the more common use cases.

Instantiating
-------------

As discussed in the previous section, we must first instantiate the class with our API token, to authenticate with the GWLab service:

::

    from gwlab_viterbi_python import GWLabViterbi

    gwl = GWLabViterbi(token='my_unique_gwlab_api_token')

Searching the public job list
-----------------------------

While the preferred job list is often a good starting place to search for a desired job sample, there is often a need to search for other jobs available to the public.
To this end, the GWLabViterbi class has another method, :meth:`~gwlab_viterbi_python.gwlab.GWLabViterbi.get_public_job_list`.
We are able to use this method to search the public jobs. For example, if we wish to find the jobs submitted by Thomas Reichardt at any time in the past, we can run:

::

    from gwlab_viterbi_python import TimeRange
    jobs = gwl.get_public_job_list(search="Thomas Reichardt", time_range=TimeRange.ANY)

The fields in this method operate exactly the same as on the website. We recommend using the :class:`.TimeRange` enum class to set the `time_range` field, though strings are still accepted.

Obtaining a single specific job
-------------------------------

If we have a list of ViterbiJob instances, as above, we are able to use the list index to reference a specific job from that list.
For example, if we want to work with a job from the above list, we can just grab the job by list index:

::

    job = jobs[0]

However, we are also able to obtain single jobs from the database if we know their job ID, using the :meth:`~gwlab_viterbi_python.gwlab.GWLabViterbi.get_job_by_id` method:

::

    job = gwl.get_job_by_id('Vml0ZXJiaUpvYk5vZGU6NTI=')

Both of these methods for getting a job yield equivalent results, but may be used in different ways.