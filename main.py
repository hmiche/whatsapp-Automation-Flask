# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import json
import requests
import re
import docker
import threading
import time

i =1 
app = Flask(__name__)
data = ""
client = docker.from_env()


def printer(container):
    time.sleep(30)
    for line in container.logs(stream=True):
        b = line.decode('utf8')
        print(str(b))

@app.route("/")
def hello():
    container = client.containers.run("allburov/whatsapp-http-api", detach=True, ports={"3000/tcp": "3000"})
    threading.Thread(target=printer , args=(container,)).start()
    for line in container.logs(stream=True):     
        if re.findall("code", str(line)):
            a= str(line)
            data = a.replace("b\' {\"code\":\"", "").replace("\"}\\n\'", "")    
            return render_template("index.html",data=data)
  
if __name__ == "__main__":
    app.run(debug=True)