

<h1 align="center">
  <br>
  <br>
  Viewmyai
  <br>
</h1>

<h4 align="center">COVID 19 X RAY SCANNER
  
## CircleCI
[![CircleCI](https://circleci.com/gh/covidxray/covidxray.org.svg?style=svg)](https://circleci.com/gh/covidxray/covidxray.org)

## DATASETS
  Download the covid dataset and extract it under project folder [link](https://drive.google.com/file/d/1iCdBP6F7xfqQH77eeclTRkOimMRjv237/view?usp=sharing)
  
 Download the xray dataset and extract it under project folder [link](https://drive.google.com/file/d/1lLNaiPtQwMDvn2ON_7dZRX8XiQRqTW6C/view?usp=sharing)
## Backend
   - FLASK

## Build from sources

```bash
$ # Clone the sources
$ git clone https://github.com/covidxray/covidxray.org.git
$ cd covidxray.org
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv --no-site-packages covid-19
$ source covid-19/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv --no-site-packages env
$ # .\env\Scripts\activate
$ 
$ # Install requirements
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Run the application
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the app in browser: http://127.0.0.1:5000/
```
