from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
from os import getcwd



current_directory_for_file_upload = getcwd()

def gdrive_upload(path_to_file= current_directory_for_file_upload + '/file.txt'):
    '''
    this functionality requires you to configure a google drive API, and place the correct tokens and settings in files settings.yaml
    for more read: 

     https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf
     https://pythonhosted.org/PyDrive/oauth.html#automatic-and-custom-authentication-with-settings-yaml
    '''
    gauth = GoogleAuth()
    gdrive = GoogleDrive(gauth)

    gfile = gdrive.CreateFile({'parents':[{'id': '1PTDF7G8Aiw4vQ_TgrjjPztuEfA-OiZeb'}]})
    gfile.SetContentFile(path_to_file)
    gfile.Upload()