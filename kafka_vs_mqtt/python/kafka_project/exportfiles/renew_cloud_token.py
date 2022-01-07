from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
from pathlib import Path

folder_path = Path(__file__).parent.absolute()

def gdrive_upload(path_to_file= str(folder_path) + '/file.txt'):
    gauth = GoogleAuth()
    gdrive = GoogleDrive(gauth)

    gfile = gdrive.CreateFile({'parents':[{'id': '1PTDF7G8Aiw4vQ_TgrjjPztuEfA-OiZeb'}]})
    gfile.SetContentFile(path_to_file)
    gfile.Upload()

if __name__ == '__main__':
    gdrive_upload()

