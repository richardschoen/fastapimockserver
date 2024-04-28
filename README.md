# Python FastAPI Mock Server
This project contains a Python FastAPI Mock Server for Serving JSON and CSV Files as JSON API Responses

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
### Access the API for initial testing
Enter one of the following URLs to access a sample JSON file.

Sample states.csv file served up as JSON:  
```http://1.1.1.1:3001/api/jsongetfile/states.csv```

Sample weather.json file served up as raw JSON content:  
```http://1.1.1.1:3001/api/jsongetfile/weather.json```

