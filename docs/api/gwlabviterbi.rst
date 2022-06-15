GWLabViterbi class
===================

The GWLabViterbi object class can be thought of as the link to Viterbi module of the GWLab service, though they are primarily used as a means by which to manipulate Bilby jobs. 
It can used for submitting a new job to the queue, obtaining the information for a single specific job, or even obtaining lists of jobs matching certain search criteria.
Indeed, :class:`~gwlab_viterbi_python.viterbi_job.ViterbiJob` objects also use a reference to the GWLabViterbi class to request their own files and information.

.. automodule:: gwlab_viterbi_python.gwlab_viterbi
   :members:
   :undoc-members:
   :show-inheritance:
