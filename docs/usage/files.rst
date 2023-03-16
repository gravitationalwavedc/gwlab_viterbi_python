Working with FileReferences and FileReferenceLists
==================================================

A completed Viterbi job will have a list of files associated with it.
With an instance of the :class:`.ViterbiJob` class, we are able to obtain the result files stored in the database.


.. _results-files:

Obtaining a job file list
-------------------------

If we want to examine which files are associated with a Viterbi job, we can obtain a list of file paths, sizes and download tokens as follows:

::

    files = job.get_full_file_list()

This will return a :class:`~gwdc_python.files.file_reference.FileReferenceList`, which contains FileReference instances for all files associated with the job:

::

    FileReference(path=PosixPath('archive.tar.gz'))
    FileReference(path=PosixPath('atoms/188-0/atoms-0'))
    FileReference(path=PosixPath('atoms/188-0/atoms-1'))
    ...
    FileReference(path=PosixPath('viterbi/results_a0_phase_loglikes_scores.dat'))
    FileReference(path=PosixPath('viterbi/results_path.dat'))
    FileReference(path=PosixPath('viterbi/results_scores.dat'))

Note that a FileReferenceList does not contain any of the actual data contained within the files. Browsing a FileReferenceList is effectively equivalent to browsing the list of files in the UI.
Obtaining the full file list is rarely required, hence there are several convenient methods by which we can obtain sensible subsets of the file list instead.
For example, to obtain just the list of candidates files we can use the method :meth:`~.ViterbiJob.get_candidates_file_list`.


Saving job files
----------------

There are a couple of ways that we are able to actually obtain the data from desired job files.
In general, we recommend streaming the files and saving them straight to disk. This is especially important for large files, or large numbers of files.
Hence, another set of methods, such as :meth:`~.ViterbiJob.save_candidates_files`, has been provided to download and save a subset of the results files.
For example, we can save all the candidates files, keeping the directory structure intact, by running:

::

    job.save_candidates_files('directory/to/store/files')

which should give output for the download in the form of a progress bar:

::

    100%|██████████████████████████████████████| 1.17k/1.17k [00:00<00:00, 3.36kB/s]
    All 1 files saved!

.. _get-file-label:

Obtaining job file data
-----------------------

If we want to just obtain the contents of some files, we can also download the files and store them in memory using methods such as :meth:`~.ViterbiJob.get_candidates_files`.
For example, if we wish to obtain the ini file of a job so that we can programmatically modify and resubmit it, we could use :meth:`~.ViterbiJob.get_ini_files`:

::

    file_data = job.get_ini_files()

which returns a list of all the contents of the ini files available for download.

.. warning::
    We recommend only using these methods when dealing with small total file sizes, as storing many MB or GB in memory can be detrimental to the performance of your machine.


Filtering files by path
-----------------------

If none of the provided methods return the desired subset of files, the full :class:`~gwdc_python.files.file_reference.FileReferenceList` can be filtered by using the more custom :meth:`~.FileReferenceList.filter_list_by_path` method.
This enables us to pick only the files we want based on the directories, the file name or the file extension.
For example, if we want to find all JSON files in the 'result' directory, we can can run:

::

    files = job.get_full_file_list()
    atoms_txt_files = files.filter_list_by_path(directory='atoms', extension='txt')

This returns a new :class:`~gwdc_python.files.file_reference.FileReferenceList` with contents like:

::

    FileReference(path=PosixPath('atoms/188-0/sfts_used.txt'))

We are able to save or obtain the files for this custom :class:`~gwdc_python.files.file_reference.FileReferenceList` using the :meth:`~.GWLabViterbi.save_files_by_reference` and :meth:`~.GWLabViterbi.get_files_by_reference` methods.
For example, to save the above :code:`atoms_txt_files`, we run:

::

    gwl.save_files_by_reference(atoms_txt_files, 'directory/to/store/files')

Note that a :class:`~gwdc_python.files.file_reference.FileReferenceList` object can contain references to files from many different Viterbi Jobs.
The :meth:`~.GWLabViterbi.save_files_by_reference` and :meth:`~.GWLabViterbi.get_files_by_reference` methods are able to handle such cases.