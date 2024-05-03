##/QOpenSys/pkgs/bin/python3
##/usr/bin/python3
#------------------------------------------------
# FastAPI Main script name: main.py
#
# Description: 
# This is a sample FastAPI JSON Mock REST service for 
# reading JSON and CSV content and returning back as JSON 
# output. 
# It supports reading entire JSON and CSV files or querying 
# the JSON results using JMESPath JSON query language. 
# 
# FastAPI Setup How To:
# https://github.com/richardschoen/howtostuff/blob/master/installpythonfastapi.md
#
# pip packages needed:
## Install fastapi
# pip3 install fastapi
## Install uvicorn (The lightning fast ASGI server). This will be our web 
## Note: Dont install with the [standard] option. This will possibly cause errors when trying to build some of the wheels.
## app server component
# pip3 install uvicorn
# Install JMESPath JSON Query Language
# pip3 install jmespath
#
# TODO: ?
#
# Modifications
# 5/2/2024 - RJS - Updated to use parameter classes instead of processing the request body itself. 
#                  The old way worked, but the body entry would not show up in the OpenAPI docs which
#                  means the POST operations could not be tested with OpenAPI. Now they can.
#
# Links:
# https://fastapi.tiangolo.com/advanced/response-directly/
# https://fastapi.tiangolo.com/#installation
# https://www.uvicorn.org/
# https://stackoverflow.com/questions/60715275/fastapi-logging-to-file
# https://fastapi.tiangolo.com/tutorial/handling-errors/
# https://www.geeksforgeeks.org/convert-csv-to-json-using-python/
# https://www.linkedin.com/pulse/how-convert-csv-json-array-python-rajashekhar-valipishetty-/ 
# JMESPath JSON Query Language Tutorial
# https://jmespath.org/tutorial.html#filter-projections
#------------------------------------------------

# Declare imports
import configparser
import sys
from sys import platform
import os
import time
import traceback
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Union
from fastapi import FastAPI, Request,Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import jmespath
from fastapi.openapi.docs import get_swagger_ui_html

#--------------------------------------------------------------------------
# Function: csvtojson
# Desc: Function to convert a CSV file to Dictionary for return as JSON.
# Parameters:
# csvFilePath - Path to existing CSv file.
# dictionaryName - Dictionary/JSON array name. Default=data
# contentTypeRaw - Content type for return header with non CSV or JSON data. 
#                  Default=application/text
#--------------------------------------------------------------------------
def csvtojson(csvFilePath,dictionaryName="data"):

    # Create a new empty dictionary
   json_dictionary={}
  
   #------------------------------------------------
   # Let's do the work
   #------------------------------------------------
   try:  

      # Open the given csv file using open() function
      with open(csvFilePath) as csvfile:
       
          # Pass the given csv file as an argument to the DictReader() function of the csv module
          # to Convert the given cs file data into dictionary
       
          # Store it in a variable
          csvfiledata = csv.DictReader(csvfile)
          json_dictionary[dictionaryName]=[]
       
          # Loop in the rows of the above csv file data using the for loop
          for row_data in csvfiledata:

              # Print the row data. Enable for debug
              # print (row_data)
      
              # Append all the row data to the above created json dictionary.
              json_dictionary[dictionaryName]. append (row_data)

          return json_dictionary

   #------------------------------------------------
   # Handle Exceptions
   #------------------------------------------------
   except Exception as ex: # Catch and handle exceptions

      # Print exception to STDOUT for debugging
      traceback.print_exc()        

      # Init empty dictionary on error
      json_dictionary={}

      return json_dictionary

#--------------------------------------------------------------------------
# Read settings from config.py file
#--------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('config.cfg')
mockfiledirectory=config['settings']['mockfiledirectory']
debug=config['settings']['debug']
allowrawfiles=config['settings']['allowrawfiles']
contenttyperaw=config['settings']['contenttyperaw']

# Create POST parameter classes so body field entry shows up in OpenAPI Docs.
# It looks like these will auto-parse the JSON body to its parts automatically.
class PostParamsJsonGetFile(BaseModel):
    jsonfile: str

class PostParamsJsonQueryFile(BaseModel):
    jsonfile: str
    jmescriteria: str    
    
#--------------------------------------------------------------------------
# Initialize app
#--------------------------------------------------------------------------
app = FastAPI()

#--------------------------------------------------------------------------
# Route function: root function route
# Desc: Handle URL routing if nothing passed - default route
#--------------------------------------------------------------------------
@app.get("/")
def readroot():
    return {"Status ": "FastAPI JSON Mock Service is active"}

#--------------------------------------------------------------------------
# Route function: jsongetfile
# Desc: Read CSV or JSON file and return as JSON via Get
# Parameters:
# jsonfile - JSON file name without path.  Ex: states.csv or weather.json
#--------------------------------------------------------------------------
@app.get("/api/jsongetfile/{jsonfile}")
async def jsongetfile(jsonfile):

 #------------------------------------------------
 # Let's do the work
 #------------------------------------------------
 try:  

   jsondata=""
   
   # Build full path to CSV/JSON file 
   fullpath=f"{mockfiledirectory}/{jsonfile}"

   # this will return a tuple of root and extension
   split_tup = os.path.splitext(jsonfile) 
   # extract the file name and extension
   file_name = split_tup[0].lower()
   file_extension = split_tup[1].lower()

   # See if mock data directory exists. if not, bail out
   if (os.path.isdir(mockfiledirectory)==False):
      raise Exception(f"Directory {mockfiledirectory} not found.") 

   # See if file exists. if not, bail out
   if (os.path.exists(fullpath)==False):
      raise Exception(f"File {jsonfile} not found.") 

   # Read JSON file if file is json
   if (file_extension==".json"):
      # Read entire JSON file contents as string
      json_text = Path(fullpath).read_text()
      # Convert string to Dictionary for JSON return
      json_data = json.loads(json_text)             
   elif (file_extension==".csv"):
      # Read entire file CSV contents and convert to JSON 
      json_data=csvtojson(fullpath)
   else: 
      # Return raw contents if returning raw contents enabled  
      if (allowrawfiles=="1"):
         json_data = Path(fullpath).read_text()
      else:   
         raise Exception(f"File {jsonfile} type not supported.") 
   
   # Use JSONResponse to convert array list to true JSON and return 
   if (file_extension==".csv" or file_extension==".json"):
      json_compatible_data = jsonable_encoder(json_data)
      return JSONResponse(content=json_compatible_data,media_type="application/json")
   else:
      return Response(content=json_data, media_type=contenttyperaw)   

 #------------------------------------------------
 # Handle Exceptions
 #------------------------------------------------
 except Exception as ex: # Catch and handle exceptions

   # Print exception to STDOUT for debugging
   traceback.print_exc()        

   # Return error info. If debug enabled, return actual exception
   # otherwise return a general message
   if (debug=="1"):
      returnstr="{\"error\":" + str(traceback.format_exception(None, ex, ex.__traceback__)) + "}"
   else:
      returnstr="{\"error\":" + "Error occurred during getjsonfile" + "}"

   return JSONResponse(status_code=404,content=returnstr,media_type="application/json")   

#--------------------------------------------------------------------------
# Route function: jsonqueryfile
# Desc: Query CSV or JSON file and return as JSON using Get
# Parameters:
# jsonfile - JSON file name without path.  Ex: states.csv or weather.json
# jmescriteria - JMES query criteria. Ex for states.csv: data[?Abbreviation='MN']
#--------------------------------------------------------------------------
@app.get("/api/jsonqueryfile/{jsonfile}/{jmescriteria}")
async def jsonqueryfile(jsonfile,jmescriteria):

 #------------------------------------------------
 # Let's do the work
 #------------------------------------------------
 try:  

   jsondata=""
 
   # Build full path to CSV/JSON file 
   fullpath=f"{mockfiledirectory}/{jsonfile}"

   # this will return a tuple of root and extension
   split_tup = os.path.splitext(jsonfile) 
   # extract the file name and extension
   file_name = split_tup[0].lower()
   file_extension = split_tup[1].lower()

   # See if mock data directory exists. if not, bail out
   if (os.path.isdir(mockfiledirectory)==False):
      raise Exception(f"Directory {mockfiledirectory} not found.") 

   # See if file exists. if not, bail out
   if (os.path.exists(fullpath)==False):
      raise Exception(f"File {jsonfile} not found.") 

   # Read JSON file if file is json
   if (file_extension==".json"):
      # Read entire JSON file contents as string
      json_text = Path(fullpath).read_text()
      # Convert string to Dictionary for JSON return
      json_data = json.loads(json_text)             
   elif (file_extension==".csv"):
      # Read entire file CSV contents and convert to JSON 
      json_data=csvtojson(fullpath)
   else: 
      # Return raw contents if returning raw contents enabled  
      if (allowrawfiles=="1"):
         json_data = Path(fullpath).read_text()
      else:   
         raise Exception(f"File {jsonfile} type not supported.") 
   
   # Use JSONResponse to convert array list to true JSON and return 
   if (file_extension==".csv" or file_extension==".json"):
      jmesquerycriteria=f"{jmescriteria}"
      print(jmesquerycriteria)
      json_data2=jmespath.search(f"{jmesquerycriteria}", json_data)
      print(json_data2)
      json_compatible_data = jsonable_encoder(json_data2)
      ##json_compatible_data = jsonable_encoder(json_data)
      return JSONResponse(content=json_compatible_data,media_type="application/json")
   else:
      return Response(content=json_data, media_type=contenttyperaw)   

 #------------------------------------------------
 # Handle Exceptions
 #------------------------------------------------
 except Exception as ex: # Catch and handle exceptions

   # Print exception to STDOUT for debugging
   traceback.print_exc()        

   # Return error info. If debug enabled, return actual exception
   # otherwise return a general message
   if (debug=="1"):
      returnstr="{\"error\":" + str(traceback.format_exception(None, ex, ex.__traceback__)) + "}"
   else:
      returnstr="{\"error\":" + "Error occurred during getjsonfile" + "}"

   return JSONResponse(status_code=404,content=returnstr,media_type="application/json")   

#--------------------------------------------------------------------------
# Route function: jsongetfile
# Desc: Get CSV or JSON file and return as JSON using Post
# JSON body parameters:
# jsonfile - JSON file name without path.  Ex: states.csv or weather.json
#--------------------------------------------------------------------------
@app.post("/api/jsongetfile")
async def jsongetfilepost(params: PostParamsJsonGetFile):
#async def jsongetfilepost(request: Request):

 #------------------------------------------------
 # Let's do the work
 #------------------------------------------------
 try:  

   ##jsondata=""
 
   # Get the JSON post request data 
   ##jsonreqdata = await request.json()

   # Get fields from the posted JSON data
   ##jsonfile = jsonreqdata['jsonfile']

   # Get fields from the posted JSON data
   jsonfile = params.jsonfile

   # Build full path to CSV/JSON file 
   fullpath=f"{mockfiledirectory}/{jsonfile}"

   # this will return a tuple of root and extension
   split_tup = os.path.splitext(jsonfile) 
   # extract the file name and extension
   file_name = split_tup[0].lower()
   file_extension = split_tup[1].lower()

   # See if mock data directory exists. if not, bail out
   if (os.path.isdir(mockfiledirectory)==False):
      raise Exception(f"Directory {mockfiledirectory} not found.") 

   # See if file exists. if not, bail out
   if (os.path.exists(fullpath)==False):
      raise Exception(f"File {jsonfile} not found.") 

   # Read JSON file if file is json
   if (file_extension==".json"):
      # Read entire JSON file contents as string
      json_text = Path(fullpath).read_text()
      # Convert string to Dictionary for JSON return
      json_data = json.loads(json_text)             
   elif (file_extension==".csv"):
      # Read entire file CSV contents and convert to JSON 
      json_data=csvtojson(fullpath)
   else: 
      # Return raw contents if returning raw contents enabled  
      if (allowrawfiles=="1"):
         json_data = Path(fullpath).read_text()
      else:   
         raise Exception(f"File {jsonfile} type not supported.") 
   
   # Use JSONResponse to convert array list to true JSON and return 
   if (file_extension==".csv" or file_extension==".json"):
      json_compatible_data = jsonable_encoder(json_data)
      return JSONResponse(content=json_compatible_data,media_type="application/json")
   else:
      return Response(content=json_data, media_type=contenttyperaw)   

 #------------------------------------------------
 # Handle Exceptions
 #------------------------------------------------
 except Exception as ex: # Catch and handle exceptions

   # Print exception to STDOUT for debugging
   traceback.print_exc()        

   # Return error info. If debug enabled, return actual exception
   # otherwise return a general message
   if (debug=="1"):
      returnstr="{\"error\":" + str(traceback.format_exception(None, ex, ex.__traceback__)) + "}"
   else:
      returnstr="{\"error\":" + "Error occurred during getjsonfile" + "}"

   return JSONResponse(status_code=404,content=returnstr,media_type="application/json")   

#--------------------------------------------------------------------------
# Route function: jsonqueryfile
# Desc: Query CSV or JSON file and return as JSON using Post
# JSON body parameters:
# jsonfile - JSON file name without path.  Ex: states.csv or weather.json
# jmescriteria - JMES query criteria. Ex for states.csv: data[?Abbreviation='MN']
#--------------------------------------------------------------------------
@app.post("/api/jsonqueryfile")
async def jsonqueryfilepost(params: PostParamsJsonQueryFile):
##async def jsonqueryfilepost(request: Request):

 #------------------------------------------------
 # Let's do the work
 #------------------------------------------------
 try:  

   ##jsondata=""
 
   # Get the JSON post request data 
   ##jsonreqdata = await request.json()

   # Get fields from the posted JSON data
   ##jsonfile = jsonreqdata['jsonfile']
   ##jmescriteria = jsonreqdata['jmescriteria']
  
   # Get fields from the posted JSON data
   jsonfile = params.jsonfile 
   jmescriteria = params.jmescriteria

   # Build full path to CSV/JSON file 
   fullpath=f"{mockfiledirectory}/{jsonfile}"

   # this will return a tuple of root and extension
   split_tup = os.path.splitext(jsonfile) 
   # extract the file name and extension
   file_name = split_tup[0].lower()
   file_extension = split_tup[1].lower()

   # See if mock data directory exists. if not, bail out
   if (os.path.isdir(mockfiledirectory)==False):
      raise Exception(f"Directory {mockfiledirectory} not found.") 

   # See if file exists. if not, bail out
   if (os.path.exists(fullpath)==False):
      raise Exception(f"File {jsonfile} not found.") 

   # Read JSON file if file is json
   if (file_extension==".json"):
      # Read entire JSON file contents as string
      json_text = Path(fullpath).read_text()
      # Convert string to Dictionary for JSON return
      json_data = json.loads(json_text)             
   elif (file_extension==".csv"):
      # Read entire file CSV contents and convert to JSON 
      json_data=csvtojson(fullpath)
   else: 
      # Return raw contents if returning raw contents enabled  
      if (allowrawfiles=="1"):
         json_data = Path(fullpath).read_text()
      else:   
         raise Exception(f"File {jsonfile} type not supported.") 
   
   # Use JSONResponse to convert array list to true JSON and return 
   if (file_extension==".csv" or file_extension==".json"):
      json_data2=jmespath.search(f"{jmescriteria}", json_data)
      json_compatible_data = jsonable_encoder(json_data2)
      return JSONResponse(content=json_compatible_data,media_type="application/json")
   else:
      return Response(content=json_data, media_type=contenttyperaw)   

 #------------------------------------------------
 # Handle Exceptions
 #------------------------------------------------
 except Exception as ex: # Catch and handle exceptions

   # Print exception to STDOUT for debugging
   traceback.print_exc()        

   # Return error info. If debug enabled, return actual exception
   # otherwise return a general message
   if (debug=="1"):
      returnstr="{\"error\":" + str(traceback.format_exception(None, ex, ex.__traceback__)) + "}"
   else:
      returnstr="{\"error\":" + "Error occurred during getjsonfile" + "}"

   return JSONResponse(status_code=404,content=returnstr,media_type="application/json")   
