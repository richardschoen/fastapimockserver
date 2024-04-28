##/QOpenSys/pkgs/bin/python3
##/usr/bin/python3
#------------------------------------------------
# FastAPI Main script name: main.py
#
# Description: 
# This is a sample FastAPI JSON Mock REST service for 
# reading JSON and CSV content and returning back as JSON 
# output.
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
#
# TODO: ?
#
# Modifications
# x/xx/xx - xxx - Desc
#
# Links:
# https://fastapi.tiangolo.com/advanced/response-directly/
# https://fastapi.tiangolo.com/#installation
# https://www.uvicorn.org/
# https://stackoverflow.com/questions/60715275/fastapi-logging-to-file
# https://fastapi.tiangolo.com/tutorial/handling-errors/
# https://www.geeksforgeeks.org/convert-csv-to-json-using-python/
# https://www.linkedin.com/pulse/how-convert-csv-json-array-python-rajashekhar-valipishetty-/ 
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
config.read('config.py')
mockfiledirectory=config['settings']['mockfiledirectory']
debug=config['settings']['debug']
allowrawfiles=config['settings']['allowrawfiles']
contenttyperaw=config['settings']['contenttyperaw']

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
# Desc: Read CSV or JSON file and return as JSON
#--------------------------------------------------------------------------
@app.get("/api/jsongetfile/{jsonfile}")
async def jsongetfile(jsonfile):

 #------------------------------------------------
 # Let's do the work
 #------------------------------------------------
 try:  

   jsondata=""
   tempfile="/tmp/jsontemp.json"
 
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
      return Response(content=jsondata, media_type=contenttyperaw)   

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
