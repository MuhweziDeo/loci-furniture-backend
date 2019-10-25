import os
from flask import request
from werkzeug.utils import secure_filename
from app.main import create_app

app = create_app("dev")

def save_image(file_name, target_folder="static/images"):
    target = os.path.join(app.root_path, target_folder)
    if not os.path.isdir(target):
        os.makedirs(target)
    file = request.files[file_name]
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    url = "{}{}/{}".format(request.host_url, target_folder, filename)
    file.save(destination)
    return url