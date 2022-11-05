import os

def delete_files():
    print("crontab started")
    if(os.path.exists("../media/images/")):
        print("media file exists!")
        for file in os.scandir(("../media/images")):
            os.remove(file.path)