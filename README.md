# Python FastAPI Mock Server

This mock server project contains a very simple Python FastAPI Mock Server for Serving JSON and CSV Files as JSON API Responses.

The server can be used to serve up static JSON and CSV files as JSON responses. JSON and CSV files can also be queried using the JMESPath JSON query language. Or you can extend the server with your own API calls.

A mock JSON and CSV server can be used for retrieving and querying sample CSV and JSON data while developing mobile or other applications that need to receive data and the app APIs are not fully defined yet. Simply compose some CSV or JSON data, place the files on the server and start serving up your mocked up data.

There are other tools out there such as Mockaroo, but often it's nice to have your own mock data server. And this was an interesting project to showcase how easy it is to get new APIs off the ground with FastAPI and Python.

## Getting started

### Clone repository

Clone the respository to a local directory.  Ex: `/fastapimockserver`

```sh
cd / # or elsewhere
git clone https://github.com/richardschoen/fastapimockserver
```

### Edit the Config File

Edit the config file `config.cfg` and make sure the `mockdatadirectory` setting matches the location where you cloned the project.

The default location for mockjson data is: `/fastapimockserver/mockjson`

### Create a virtual environment and activate it (if you want to use venv)

```sh
python -m venv my_venv --system-site-packages
. my_venv/bin/activate
```

### Install the necessary support modules

```sh
pip install uvicorn fastapi jmespath
```

### Start up the FastAPI server

The following script file will start the FastAPI server to monitor all IP addresses on port 3001.  

```sh
cd /fastapimockserver
sh ./startapp.sh
```

## Initial API Test

### Access the API for initial testing via OpenAPI
`http://localhost:3001/api/docs`

This URL will display the OpenAPI documentation where APIs can also be tested.   

![image](https://github.com/richardschoen/fastapimockserver/assets/9791508/56712793-3322-40b6-ad59-80a5261b9ada)

### Access the API for initial testing with simple URL test 

Enter one of the following URLs to serve up a sample CSV and JSON file repectively.
CSV files are converted on-the-fly to JSON before serving up results.

Sample states.csv file served up as JSON:  
`http://localhost:3001/api/jsongetfile/states.csv`

Sample weather.json file served up as raw JSON content:  
`http://localhost:3001/api/jsongetfile/weather.json`

Sample customers.json file served up as raw JSON content:  
`http://localhost:3001/api/jsongetfile/customers.json`

**If data is returned to yout browser as JSON, the server is working as expected.**

## API Routes

### Read CSV or JSON file and return as JSON via Get - /api/jsongetfile/{jsonfile}

This route is used to read and return a CSV or JSON file.

Parameters:
```{jsonfile}``` - JSON or CSV file to serve up as JSON

Sample URL for states.csv file served up as JSON after GET:  
`http://localhost:3001/api/jsongetfile/states.csv`

Sample URL for weather.json file served up as raw JSON content after GET:  
`http://localhost:3001/api/jsongetfile/weather.json`

Sample URL for customers.json file served up as raw JSON content after GET:  
`http://localhost:3001/api/jsongetfile/customers.json`

### Query CSV or JSON file and return as JSON via Get - /api/jsonqueryfile/{jsonfile}/{jmescriteria}

This route is used to read and return a CSV or JSON file.

Parameters:
`{jsonfile}` - JSON or CSV file to serve up as JSON.  Ex: `states.csv`
`{jmescriteria}` - JMESPath Query language criteria. ? encoded as `%3F`
Ex state abbreviation=MN: `data[%3FAbbreviation=='MN']`

Sample URL for states.csv file queried for state abbreviation = 'MN' served up as after GET:  
`http://localhost:3001/api/jsonqueryfile/states.csv/data[%3FAbbreviation=='MN']`  

### Read CSV or JSON file and return as JSON via Post - /api/jsongetfile

This route is used to read and return a CSV or JSON file.

Parameters are posted via JSON in the request body.

Content type for post should be:
`application/json`

Parameters:
`{jsonfile}` - JSON or CSV file to serve up as JSON

Sample JSON post body:

```json
{
"jsonfile":"states.csv"
}
```

Sample URL for states.csv file served up as JSON after POST:  
`http://localhost:3001/api/jsongetfile`

### Query CSV or JSON file and return as JSON via Post - /api/jsonqueryfile

This route is used to query a CSV or JSON file and return results as JSON.  

Parameters are posted via JSON in the request body.

Content type for post should be:
`application/json`

Parameters:
`{jsonfile}` - JSON or CSV file to serve up as JSON.
`{jmescriteria}` - JMESPath Query language criteria.
Ex state abbreviation=MN: `data[Abbreviation=='MN']`

Sample JSON post body:

```json
{
"jsonfile":"states.csv",   
"jmescriteria":"data[?Abbreviation=='MN']"   
}
```

Sample URL for states.csv file queried for state abbreviation = 'MN' served up as JSON after POST:  
`http://localhost:3001/api/jsonqueryfile`

### Adding Additional JSON or CSV Files to the Mock Server

If you have other JSON or CSV files you want to serve up with the mock server, place them in the correct mockdatadirectory.
In our example the mockdatadirectory is: `/fastapimockserver/mockjson`

### More info on FastAPI

FastAPI Home Page  
<https://fastapi.tiangolo.com>

How to install Python FastAPI Web Framework and Get Started on IBM i  
<https://github.com/richardschoen/howtostuff/blob/master/installpythonfastapi.md>

JMESPath query language for JSON tutorial  
<https://jmespath.org/tutorial.html>
