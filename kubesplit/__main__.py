# -*- coding: utf-8 -*-
"""Allow kubesplit to be executable through `python -m kubesplit`."""
from __future__ import absolute_import

from .kubesplit import main

if __name__ == "__main__":  # pragma: no cover
    main()
