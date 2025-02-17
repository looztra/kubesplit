"""Allow kubesplit to be executable through `python -m kubesplit`."""


from .kubesplit import main

if __name__ == "__main__":  # pragma: no cover
    main()
