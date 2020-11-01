Requirements:
=========================================================================================================
- Python 3.7.9 to be installed on the system

Setting up:
=========================================================================================================
1) Navigate to SourceCode directory
2) Set up virtual environment using                     ```python -m virtualenv venv```
3) Activate virtual environment using                   ```. venv/Scripts/activate```
4) Install required libraries using                     ```pip install -r requirements.txt```
5) Install additional library required by SpaCy using   ```python -m spacy download en_core_web_sm```


Running the programs:
=========================================================================================================
For 3.1 & 3.2 analysis, usage of jupyter lab is required:
1) On the terminal, run the following command: ```jupyter lab```
2) A browser window should open with the jupyterlab environment.
3) To access the respective notebooks, use the file browser on the left hand side of the browser window.

For 3.3:
1) Without going into jupyter lab, run the following command to launch the application: 
	```python 3_3_Application.py```

Interpreting Results:
=========================================================================================================
For 3.1: Graphs are generated within the notebook (Will differ from report as data is scraped live).
For 3.2: The results of the pair ranking is output as phrase_rankings.csv.
For 3.3: A Search Engine to allow the user to search for reviews by entering a search query.