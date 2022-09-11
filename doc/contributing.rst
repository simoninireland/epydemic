Contributing
============

``epydemic`` is an open-source project, and we welcome comments, issue
reports, requests for new features, and (especially!) code for new
features.


To report an issue
------------------

Issue ("bug") reports are handled through ``epydemic``'s GitHub
repository. To report an issue, go to
https://github.com/simoninireland/epydemic/issues
and click the "New issue" button.

Please be as specific as possible about the problem. Code that
illustrates an issue is very welcome, but please make it as simple as
possible!


To request a feature
--------------------

If you simply want to suggest a feature, please open an issue report
as above.


To contribute a feature
-----------------------

If on the other hand you have proposed code for a new feature, please
create a pull request containing your proposal, with using ``git``
directly or through GitHub's `Pull requests manager <https://github.com/simoninireland/epydemic/pulls>`_.

In submitting a pull request, please include:

- a clear description of what the code does, and what it adds to
  ``epydemic`` for a general user;
- well-commented code, including docstrings for methods;
- types for all methods using Python's `type hints <https://docs.python.org/3/library/typing.html>`_;
- a tutorial and/or cookbook recipe to illustrate the new feature in
  use; and
- tests in the ``test/`` sub-directory that let us automatically test
  any new features.

Please don't neglect the tests. We use continuous integration for
``epydemic`` to keep everything working, so it's important that new
features provide automated unit tests. Please also don't neglect
documentation, and remember that docstrings aren't enough on their own.

We use the `Python Black coding style <https://pypi.org/project/black/>`_,
and it'd be helpful if any pulled code did the same. We use
`type annotations <https://docs.python.org/3/library/typing.html>`_ to
improve maintainability.


Installing the codebase
-----------------------

To get your own copy of the codebase, simply clone the repo from
GitHub and (optionally) create your own branch to work on

.. code-block:: sh

   # clone the repo
   git clone git@github.com:simoninireland/epydemic.git
   cd epydemic

   # create a new branch to work on
   git branch my-new-feature

The makefile has several targets that are needed for development:

- ``make env`` build a virtual environment with all the necessary
  libraries. This include both those that ``epyc`` needs to run
  (specified in ``requirements.txt``, and those that are simply needed
  when developing and testing (specified in ``dev-requirements.txt``)
- ``make test`` runs the test suite. This consists of a *lot* of
  tests, some of which do a lot of work, and so this may take some time
- ``make clean`` delete s a lo of constructed files for a clean build
- ``make reallyclean`` also deletes the venv

Calling ``make`` on its own prints all the available targets.


Copyrights on code
------------------

You retain copyright over any code you submit that's incorporated in
``epydemic``'s code base, and this will be noted in the source code
comments and elsewhere.

We will only accept code that's licensed with the same license as
``epydemic`` itself (currently `GPLv3
<https://www.gnu.org/licenses/gpl-3.0.en.html>`_). Please indicate
this clearly in the headers of *all* source files to avoid confusion.
Please also note that we may need an explicit declaration from your
employer that this work can be released under GPL: see
https://www.gnu.org/licenses/ for details.
