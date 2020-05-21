=========
kubesplit
=========


.. image:: https://img.shields.io/pypi/v/kubesplit.svg
        :target: https://pypi.python.org/pypi/kubesplit

.. image:: https://circleci.com/gh/looztra/kubesplit.svg?style=svg
    :target: https://circleci.com/gh/looztra/kubesplit


Split multidoc yaml formatted kubernetes descriptors to a set of single resource files


* Free software: Apache Software License 2.0
* Documentation: https://github.com/looztra/kubesplit


Features
--------

- Invalid Kubernetes resources are ignored
- Empty resources are ignored
- Each resource found in the input is stored in a file with a name reflecting the name of the resource and its _kubernetes_ kind
- Cluster-wide resources (namespaces, clusterroles, clusterrolebindings) are stored in the root directory of the output, namespaced resources are stored in a subdirectory named like the namespace
- By default, resources are prefixed
- By default, quotes are preserved, use `--no-quotes-preserved` to disable quotes unless needed (for boolean and numbers if they were provided in the input as for the moment Kubesplit is not aware of the fact that only kubernetes annotations and environment variables require string)
- By default, dash elements in list are pushed inwards, you can disable this behaviour with the `-d`/`--no-dash-inwards` option
- Comments are preserved
- The output directory will be created if it doesn't exist (if the user running the command as sufficient rights)
- You can clean (delete files and directories existing before running `kubesplit`) the output directory with the `-c`/`--clean-output-dir` (**use at your own risks**)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Acknowledgements
----------------

- Dependencies scanned by `PyUp.io <https://pyup.io/>`_
