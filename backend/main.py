import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# TODO dont mantain order
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



class FilePost(BaseModel):
    name: str
    content: str

@app.get("/open_project")
async def open_project():
    try:
        os.chdir("./tests/")
    except Exception:
        # Note: we are already in the tests folder
        pass
    try:
        file = open('.dict', 'r')
    except Exception as e:
        print (e)
        file = open('.dict', 'w')
    try:
        data = file.read()
        print (data)
        file.close()
        return {'raw': data}
    except Exception as e:
        print (e)
        return {'raw': data}


@app.post("/save_filepost/")
async def save_file(filepost: FilePost):
    
    print (filepost.name)
    print (filepost.content)
    try:
        file = open(filepost.name, 'w')
        file.write(filepost.content)
        file.close()
        return {'raw': True}
    except Exception as e:
        print (e)
        return {'raw': False}

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
    return res

@app.get("/open_file/{file_path:path}")
def open_file(file_path: str):
    open_files.add(file_path)
    return {'res': True}

@app.get('/get_file/{file_path:path}')
def get_file(file_path: str):
    data = ""
    print ("get_file ", file_path)
    try:
        file = open(file_path)
        data = file.read()
        file.close()
        return {'raw': data}
    except FileNotFoundError:
        file = open(file_path, 'w+')
        data = file.read()
        open_files.add(file_path)
        file.close()
        return {'raw': data}
    except Exception as e:
        print (e)
        return {'raw': data}

@app.get('/create_file/{file_path:path}')
def create_file(file_path: str):
    data = ""
    print ("create_file ", file_path)
    try:
        if not os.path.isfile(file_path):
            file = open(file_path, "w+")
            data = file.read()
            open_files.add(file_path)
            file.close()
            return {'raw': data}
    except Exception as e:
        print (e)
        return {'raw': data}

@app.get('/create_directory/{file_path:path}')
def create_directory(file_path: str):
    print ("create_directory ", file_path)
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            return {'result': True}
    except OSError as error: 
        print(error)
        return {'result': False}


#TODO: allow links in the data str
@app.get('/save_file/{filename}/{data}')
def save_file(filename: str, data:str):
    try:
        file = open(filename)
        file.write(data)
        file.close()
        return {'raw': True}
    except Exception:
        return {'raw': False}

@app.get("/close_file/{file_path:path}")
def close_file(file_path: str):
    open_files.remove(file_path)
    return {'res': True}

@app.get('/opened_files')
def opened_files():
    return {'files': open_files}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}