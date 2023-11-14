# DSIP template repository

To set up builds for this report, run this command in the root directory of this repository (the directory containing this `README.md` file):

```bash
pip3 install -r build-requirements.txt
```

This will install all the prerequisites.

To fetch the data, run:

```bash
python3 fetch_data.py
```

To build the book, run:

```
jupyter-book build .
```

The book build appears in the `_build/html` directory.  You can open it with your browser.
