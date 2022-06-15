Importing and Authenticating
============================

Almost any script you can write involving the GWLab Viterbi API will require authenticating with the GWLab service first.

::

    from gwlab_viterbi_python import GWLabViterbi

    gwl = GWLabViterbi(token='my_unique_gwlab_api_token')

An instance of the GWLabViterbi class initialised with your token will provide an interface to the GWLab service, enabling you to manipulate jobs and their results as you might with the GWLab UI.
Remember not to share this token with others!