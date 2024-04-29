# Python FastAPI Mock Server
This mock server project contains a very simple Python FastAPI Mock Server for Serving JSON and CSV Files as JSON API Responses.   

A mock JSON and CSV server can be used for creating sample or test APIs or mocking up production APIs to test before they are fully defined. 

This server can be used as is to serve up static JSON and CSV files as JSON. Or you can extend it with your own API calls.

## Getting started

### Clone repository
Clone the respository to a local directory.  Ex: ```/fastapimockserver```

```
cd /
git clone https://github.com/richardschoen/fastapimockserver
```

### Edit the Config File 
Edit the config file ```config.py``` and make sure the ```mockdatadirectory``` setting matches the location where you cloned the project.   

The default location for mockjson data is: ```/fastapimockserver/mockjson```

### Start up the FastAPI server
The following script file will start the FastAPI server to monitor all IP addresses on port 3001.  

```
cd /fastapimockserver
./startapp.sh
```

## Initial API Test

### Access the API for initial testing
Enter one of the following URLs to serve up a sample CSV and JSON file repectively.   
CSV files are converted on-the-fly to JSON before serving up results.   

Sample states.csv file served up as JSON:  
```http://1.1.1.1:3001/api/jsongetfile/states.csv```

Sample weather.json file served up as raw JSON content:  
```http://1.1.1.1:3001/api/jsongetfile/weather.json```

Sample customers.json file served up as raw JSON content:  
```http://1.1.1.1:3001/api/jsongetfile/customers.json```

**If data is returned to yout browser as JSON, the server is working as expected.**

## API Routes

### Read CSV or JSON file and return as JSON via Get - /api/jsongetfile/{jsonfile}
This route is used to read and return a CSV or JSON file. 

Parameters:   
{jsonfile} - JSON or CSV file to serve up as JSON   

Sample URL for states.csv file served up as JSON after GET:  
```http://1.1.1.1:3001/api/jsongetfile/states.csv```

Sample URL for weather.json file served up as raw JSON content after GET:  
```http://1.1.1.1:3001/api/jsongetfile/weather.json```

Sample URL for customers.json file served up as raw JSON content after GET:  
```http://1.1.1.1:3001/api/jsongetfile/customers.json```

### Query CSV or JSON file and return as JSON via Get - /api/jsonqueryfile/{jsonfile}/{jmescriteria}
This route is used to read and return a CSV or JSON file. 

Parameters:   
{jsonfile} - JSON or CSV file to serve up as JSON.  Ex: ```states.csv```   
{jmescriteria} - JMES Query language criteria. ? encoded as ```%3F```    
Ex state abbreviation=MN: ```data[%3FAbbreviation=='MN']```   

Sample URL for states.csv file queried for state abbreviation = 'MN' served up as after GET:  
```http://1.1.1.1:3001/api/jsongetfile/states.csv/data[%3FAbbreviation=='MN']```  

### Read CSV or JSON file and return as JSON via Post - /api/jsongetfile
This route is used to read and return a CSV or JSON file. 

Parameters are posted via JSON in the request body.

Content type for post should be:   
```application/json```

Parameters:   
{jsonfile} - JSON or CSV file to serve up as JSON

Sample JSON post body:   
```
{
"jsonfile":"states.csv"
}
```

Sample URL for states.csv file served up as JSON after POST:  
```http://1.1.1.1:3001/api/jsongetfile```

### Query CSV or JSON file and return as JSON via Post - /api/jsonqueryfile
This route is used to query a CSV or JSON file and return results as JSON.  

Parameters are posted via JSON in the request body.

Content type for post should be:   
```application/json```

Parameters:   
{jsonfile} - JSON or CSV file to serve up as JSON.   
{jmescriteria} - JMES Query language criteria.   
Ex state abbreviation=MN: ```data[Abbreviation=='MN']```  

Sample JSON post body:   
```
{
"jsonfile":"states.csv",   
"jmescriteria":"data[?Abbreviation=='MN']"   
}
```

Sample URL for states.csv file queried for state abbreviation = 'MN' served up as JSON after POST:  
```http://1.1.1.1:3001/api/jsonqueryfile```

### Adding Additional JSON or CSV Files to the Mock Server   
If you have other JSON or CSV files you want to serve up with the mock server, place them in the correct mockdatadirectory.   
In our example the mockdatadirectory is: ```/fastapimockserver/mockjson```

### More info on FastAPI   
FastAPI Home Page   
https://fastapi.tiangolo.com

How to install Python FastAPI Web Framework and Get Started on IBM i   
https://github.com/richardschoen/howtostuff/blob/master/installpythonfastapi.md 



