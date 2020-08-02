import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import glob

app = FastAPI()

open_files = set()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

@app.get("/dir")
def dir():
    try:
        os.chdir("./tests/")
    except Exception:
        # Note: we are already in the tests folder
        pass
    #arr = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("~/files")) for f in fn]
    arr =  getListOfFiles(".")
    res = {'data': arr}
    open_files.add(arr[1])
    print(res)
    print(open_files)
    return res

@app.get("/open_file/{filename}")
def open_file(filename: str):
    print ("open ", filename)
    open_files.add(filename)
    return {'res': True}

@app.get('/get_file/{filename}')
def get_file(filename: str):
    data = ""
    try:
        file = open("./"+filename)
        data = file.read()
        file.close()
        return {'raw': data}
    except Exception:
        return {'raw': data}

#TODO: allow links in the data str
@app.get('/save_file/{filename}/{data}')
def save_file(filename: str, data:str):
    try:
        file = open("./"+filename)
        file.write(data)
        file.close()
        return {'raw': True}
    except Exception:
        return {'raw': False}

@app.get("/close_file/{filename}")
def close_file(filename: str):
    open_files.remove(filename)
    return {'res': True}

@app.get('/opened_files')
def opened_files():
    return {'files': open_files}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}