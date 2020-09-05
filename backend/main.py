import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import shutil

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

async def get_current_project():
    try:
        file = open(".frost", 'r')
        data = file.read()
        file.close()
        return data
    except Exception as e:
        print (e)
        file = open(".frost", 'w')
        return None
        


@app.get("/init/")
async def init():
    try:
        os.chdir("./projects")
    except Exception as e:
        print (e)
    project = await get_current_project()
    return {'raw': project}
    
@app.get("/list_projects/")
async def list_projects():
    listOfFile = os.listdir("./")
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        if os.path.isdir(entry):
            #allFiles = allFiles + getListOfFiles(fullPath)
            allFiles.append(entry)
    return {'projects' : allFiles}



async def save_current_project(project):
    try:
        file = open("/.frost", 'w')
        file.write(project)
        file.close()
    except Exception as e:
        print(e)
        file.close()

@app.get("/create_new_project/{new_project_name}")
async def create_new_project(new_project_name):
    try:
        if not os.path.exists(new_project_name):
            os.mkdir(new_project_name)
            file = open(new_project_name+'/.dict', 'w')
            file.close()
            return {'result': True}
        return {'result': False}
    except Exception as e:
        return {'result': False}


@app.get("/open_project/{project}")
async def open_project(project):
    if os.path.exists(project):
        print("path exists ", project)
        current_project = project
        await save_current_project(project)
        return open_dictionary(project)
    else:
        print("path doesnt exist", project)
        return {'result':False}

def open_dictionary(project):
    filename = project+'/.dict'
    try:
        file = open(filename, 'r')
    except Exception as e:
        print (e)
        file = open(filename, 'w')
    try:
        data = file.read()
        print (data)
        file.close()
        return {'raw': data}
    except Exception as e:
        print (e)
        return {'raw': None}


@app.post("/save_filepost/")
async def save_file(filepost: FilePost):
    
    print (filepost.name)
    print (filepost.content)
    try:
        if filepost.name:
            file = open(filepost.name, 'w')
            file.write(filepost.content)
            file.close()
            return {'raw': True}
        return {'raw': False}
    except Exception as e:
        print (e)
        return {'raw': False}

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
   
    listOfFile = os.listdir(dirName)
    allFiles = list()
    
    # Iterate over all the entries
    for entry in listOfFile:
        if entry != ".dict":                
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                #allFiles = allFiles + getListOfFiles(fullPath)
                allFiles.append({'title':entry, 'data':{'fullPath':fullPath } , 'isLeaf': False, 'children':getListOfFiles(fullPath)})
            else:
                allFiles.append({'title':entry, 'data':{'fullPath':fullPath } ,'isLeaf': True})         
    return allFiles

@app.get("/dir")
async def dir():
    current_project = await get_current_project()
    print ("Files from ", current_project)
    arr =  getListOfFiles(current_project)
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
    except Exception as e:
        print (e)
        return {'raw': data}

@app.get('/create_file/{file_path:path}')
async def create_file(file_path: str):
    data = ""
    current_project = await get_current_project()
    #file_path = "./projects/"+ file_path
    print ("create_file ", file_path)
    try:
        res = os.path.isfile(file_path)
        print (res)
    except Exception as e:
        print ("qwe", e)
    if not res:
        try:            
            file = open(file_path, "w+")
            data = file.read()
            open_files.add(file_path)
            file.close()
            return {'raw': data}
        except Exception as e:
            print ("create file exception ", e)
            return {'raw': data}
    else:
        print("whaa")
    

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


@app.get("/remove_file/{file_path:path}")
def remove_file(file_path: str):
    if file_path in open_files:
        open_files.remove(file_path)
    os.remove(file_path)
    return {'res': True}

@app.get("/remove_directory/{file_path:path}")
def remove_directory(file_path: str):
    #open_files.remove(file_path)
    shutil.rmtree(file_path)
    return {'res': True}