# google-drive-img-src-generator
Google Drive에 image 파일을 **업로드**하면서 **HTML img 태그의 src로 활용할 수 있는 값**을 바로 얻고 싶어 만들었습니다.

업로드 했을 때 얻게되는 링크 형태는 아래와 같습니다:
```
https://lh3.google.com/u/0/d/{file-id}
```

HTML img 태그에 다음처럼 활용이 가능합니다:
```html
<img src="https://lh3.google.com/u/0/d/{file-id}" title="test-img.png" alt="test-img.png"/>
```
<br>

## Prerequisites
- Python
  + google-api-python-client 패키지 (googleapiclient.discovery)
  + oauth2client 패키지
- Google Cloud Platform
  + 프로젝트 생성
  + 사용자 인증 정보 생성
  + 테스트 사용자 등록
  + OAuth 클라이언트 ID 만들기
  + `folder_id` 복사

<br>

### 0. Python

Python 설치 및 코드 편집 가능한 환경(Visual Studio Code, PyCharm 등) 세팅은 생략합니다.

만약 `googleapiclient.discovery`, `oauth2client`에 대해 **ModuleNotFoundError**가 발생한다면 terminal에서 아래 명령어를 입력해주세요.
```s
# googleapiclient.discovery
pip3 install google-api-python-client
# oauth2client
pip3 install --upgrade oauth2client
```

### 1. Google Cloud Platform 프로젝트 생성을 하지 않았다면 [여기](https://console.cloud.google.com/)를 클릭해주세요.

<img width="1066" alt="make-project-google-cloud-platform" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/51e71a0b-ca7d-472b-ba5e-745c627f99cd"><br>

### 2. 사용자 인증 정보 생성
   
<img width="1449" alt="make-user-information-for-auth" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/38da813b-7c36-431e-bf0e-f0d1741fe616"><br>

UserType `외부(external)` 설정 → 만들기 클릭 후, `테스트 사용자` 단계가 나올 때까지 **저장 후 계속** 버튼 클릭

<img width="450" alt="select-UserType" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/69c6a6ac-2224-4824-bce1-0fd7875ba43c"><br>

### 3. 테스트 사용자 등록

Google Drive API를 사용해 업로드하기 때문에, 사용할 계정이 필요합니다. 원하는 계정을 등록해주세요.

<img width="1051" alt="create-test-user" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/10ea1165-084e-4cd2-af3d-8f664036fdaa"><br>

### 4. OAuth 클라이언트 ID 만들기
- 애플리케이션 유형 : **데스크톱 앱**
- 이름 입력 후 `만들기` 버튼 클릭

<img width="1113" alt="create-oauth-client-id" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/57740578-10b1-4939-8e36-364afc9d751c"><br>

생성한 **클라이언트 ID/PW json 파일**을 다운로드해야 합니다. API 호출에 필요한 OAuth2 토큰 생성 시 필요한 파일입니다.

<img width="510" alt="download-oauth-client-information-json" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/aeceb951-0666-4e66-ba9a-b670b4a1b242">

### 5. `folder_id` 복사

Google Drive에서 파일을 업로드할 최종 경로 folder의 id가 필요합니다.<br>
복사 후 `google-drive-img-src-generator.py` 안에 붙여넣기 해주세요. (하단의 `코드 수정` 참조)

<img width="800" alt="image" src="https://github.com/yooniversal/google-drive-img-src-generator/assets/61930524/026e4366-514a-430d-8297-13b59a4ec9a4"><br>

<br>

## 코드 수정
git clone 후 `google-drive-img-src-generator.py`를 실행해주세요.
```
https://github.com/yooniversal/google-drive-img-src-generator.git
```
<br>

주석 표시한 부분을 확인해 다음 내용을 채운 뒤 run 해주세요. (참조할 파일들은 `google-drive-img-src-generator.py`와 **같은 경로에 있어야 합니다.**)
- OAuth 클라이언트 json 파일명
- 업로드 할 파일명 (여러개 가능)
- 업로드할 Google Drive 최종 경로 `folder-id`

```python
def main():
    # 생략

    if not creds or creds.invalid:
        oauth_client_json_file = '{json-file-name}' # OAuth 클라이언트 json 파일명 입력
        flow = client.flow_from_clientsecrets(oauth_client_json_file, SCOPES)
        creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    FILES = (
        # 업로드 할 파일명 입력
        ('upload-file-1.png'),
        ('upload-file-2.png'),
    )

    folder_id = '{folder-id}' # 업로드할 Google Drive 최종 경로 folder-id 입력

    for file_title in FILES:
        request_body = {'name': file_title, 'parents' : [folder_id], 'uploadType': 'multipart'}
        media = MediaFileUpload(file_title, mimetype=get_image_mimetype(file_title))

        res = DRIVE.files().create(body=request_body, media_body=media, fields='id,webViewLink').execute()
        if res:
            key = extract_key_from_uri(res.get('webViewLink'))
            print(f"[{file_title}] >> {get_upload_uri(key)}") # 최종 URI 출력
```
<br>

## 결과
```
[upload-file-1.png] >> https://lh3.google.com/u/0/d/{file-id}
[upload-file-2.png] >> https://lh3.google.com/u/0/d/{file-id2}
```

## References
- [YSY: [Python] 파이썬과 구글 드라이브 연동하고 파일 업로드/다운로드 하기 (Google Drive)](https://ysyblog.tistory.com/296)
- [pbj0812: [PYTHON] python을 사용한 Google Drive 에 파일 업로드](https://pbj0812.tistory.com/193)
- [JeeU147 : 구글 인증(Google Auth) 승인 오류 403 오류: access_denied](https://jeeu147.tistory.com/91)
