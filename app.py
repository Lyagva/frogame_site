#!/usr/bin/env python3.9

import os
import json
from flask import Flask, render_template, json, request, send_file
from src import commands
from pathlib import Path


current_path = str(Path(__file__).parent.resolve()) + "/"
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sendPrompt", methods=["GET", "POST"])
def get_prompt():
    prompt = str(request.json["prompt"])
    return_data = commands.processPrompt(prompt,
                                         kwargs={"path": request.json["path"],
                                                 "audioDuration": request.json["audioDuration"],
                                                 "audioPlayback": request.json["audioPlayback"],
                                                 "audioSrc": request.json["audioSrc"]})

    return json.dumps(return_data)


@app.route("/getFile/<file>", methods=["GET", "POST"])
def get_file(file):
    print(file)
    return send_file(current_path + "src/fileSys/files/" + file)

if __name__ == "__main__":
    commands.updateCommands()
    
    port = int(os.environ.get("PORT", 9000))
    print(port)
    app.run(host="0.0.0.0", port=port)
