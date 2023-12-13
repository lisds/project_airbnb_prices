To set up builds for this report, run these commands in the root directory of this repository (the directory containing this `README.md` file):


STEP 1
Installing prerequisites libraries.
```bash
pip3 install -r build_requirements.txt
```


STEP 2
You will need to MANUALLY fetch the data:
Please Navigate to this link: 
https://www.kaggle.com/datasets/mrnabiz/detailed-airbnb-listing-data-london-sep-2022/

ENSURE you download "clean_df.csv" (Version 1 143.6MB)
This can be found half way down the page. IT IS NOT the 40mb download button at the top of the page.

The data will come compressed and should be unzipped in this directory:
"/project_airbnb_prices/data"

At this point you should have the file clean_df.csv in the "data" directory.

Please check you have this correctly by running:
check_data.py


STEP 3
To build the book, run:

```
jupyter-book build .
```

The book build appears in the `_build/html` directory.  You can open it with your browser.
