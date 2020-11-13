# eigen_takehome

## Getting Started

1. Install Requirements
With Pipenv
```bash
pipenv install 
```
With pip / requirements.txt
```bash
pip install -r requirements.txt
```

2. Enter the venv using whichever tool you chose. 

3. Run the parser / loader
```bash
# json is the only output-as option right now, others like yaml / csv were considered
# code has been left open for extension. 
python cli.py parse-documents --output-as json
```
This parser will parse any documents you place into the `docs` folder and *only* documents found there. 

4. Output files are contained in the `output` directory. The output decided on was JSON for this project submission, for simplicity. 

5. (OPTIONAL) Lookup words from the command line. 

```bash
python cli.py lookup-word frustration
```

If you haven't run the parser you'll get an error like `exceptions.NoDataAvailable: No data files exist yet, it's possible you haven't run the parser`.  
If the word doesn't exist in the text corpus you've provided, you'll get a `KeyError: 'foobas'`
