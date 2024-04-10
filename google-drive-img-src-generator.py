from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import re

def get_image_mimetype(file_title):
    if file_title.endswith('.jpeg') or file_title.endswith('.jpg'):
        return 'image/jpeg'
    if file_title.endswith('.png'):
        return 'image/png'
    if file_title.endswith('.gif'):
        return 'image/gif'
    return 'image/png'
    
def extract_key_from_uri(uri):
    pattern = r"https://drive.google.com/file/d/([^/]+)/view\?usp=drivesdk"
    match = re.match(pattern, uri)
    if match:
        return match.group(1)
    return None
    
def get_upload_uri(key):
    return 'https://lh3.google.com/u/0/d/' + key

def main():
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        # OAuth 클라이언트 json 파일명 입력
        oauth_client_json_file = '{json-file-name}'
        flow = client.flow_from_clientsecrets(oauth_client_json_file, SCOPES)
        creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    FILES = (
        # 업로드 할 파일명 입력
        ('upload-file-1.png'),
        ('upload-file-2.png'),
    )

    # 업로드할 Google Drive 최종 경로 folder-id 입력
    folder_id = '{folder-id}'

    for file_title in FILES:
        request_body = {'name': file_title, 'parents' : [folder_id], 'uploadType': 'multipart'}
        media = MediaFileUpload(file_title, mimetype=get_image_mimetype(file_title))

        res = DRIVE.files().create(body=request_body, media_body=media, fields='id,webViewLink').execute()
        if res:
            key = extract_key_from_uri(res.get('webViewLink'))
            print(f"[{file_title}] >> {get_upload_uri(key)}")

if __name__ == "__main__":
    main()
