from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive 
from pathlib import Path

folder_path = Path(__file__).parent.absolute()

def gdrive_upload(path_to_file= str(folder_path) + '/file.txt'):
    '''
        this functionality requires you to configure a google drive API, and place the correct tokens and settings in files settings.yaml
    for more read: 

        https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf
        https://pythonhosted.org/PyDrive/oauth.html#automatic-and-custom-authentication-with-settings-yaml
    '''
    print(' -- > Exporting to google cloud ...')
    gauth = GoogleAuth()
    gdrive = GoogleDrive(gauth)

    gfile = gdrive.CreateFile({'parents':[{'id': '1PTDF7G8Aiw4vQ_TgrjjPztuEfA-OiZeb'}]})
    gfile.SetContentFile(path_to_file)
    gfile.Upload()
    print('Done ! !')

if __name__ == '__main__':
    gdrive_upload()

