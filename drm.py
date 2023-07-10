#필요한 모듈 호출
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet
import os

#cryptography 라이브러리를 사용하여 임의의 암호화 키를 생성
#print(encryption_key)예시: b'NHkWXWHf51ljv21HN9NGe9n0-eKvrmTtKI-oulCg3Yg='
encryption_key = Fernet.generate_key()


#암호화 할 파일의 경로 설정 -> 나중에 storage 계정이랑 연결해서 파일 받아오기
file_path = os.path.expanduser("C:/Users/kbd11/OneDrive/바탕 화면/hello.txt")

#암호화 할 파일의 내용 읽기
with open(file_path, "rb") as file:
    file_data = file.read()


#암호화 키를 사용하여 파일 데이터 암호화
cipher_suite = Fernet(encryption_key)
encrypted_data = cipher_suite.encrypt(file_data)


#암호화된 데이터를 Azure Blob Storage에 업로드
#스토리지 계정 연결 문자열을 사용하여 Blob 서비스 클라이언트 초기화 (괄호안에 스토리지 계정 연결 문자열 입력)
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storageaccountdrm;AccountKey=BnRGP0i5ZL5N5oMzodFcsok9Ct4QkX7T9EDzKbmGLeS6vTK5JmFdnYZ1esjf9GWW/L2nTQKVzZXq+AStJRf1Ig==;EndpointSuffix=core.windows.net")


#Blob 컨테이너 클라이언트 가져오기
container_client = blob_service_client.get_container_client("containerdrm")

#암호화된 데이터를 blob으로 업로드
blob_client = container_client.get_blob_client("test_blob")
blob_client.upload_blob(encrypted_data, overwrite=True)


#Blob 파일 암호 해독, 다운로드

#Azure Key Vault에서 암호화 키를 검색
#DefaultAzureCredential 클래스의 인스턴스 만들기
credential = DefaultAzureCredential()

#자격 증명 및 Key Vault URL을 사용하여 비밀 클라이언트 만들기
secret_client = SecretClient(vault_url="https://keyvalutdrm.vault.azure.net/", credential=credential)

#Azure Key Vault에서 암호화 키 검색
#encryption_key = secret_client.get_secret("keydrm").value

#암호화된 Blob 데이터를 다운로드 -> Azure Blob Storage에서 Blob 데이터 가져오기
blob_client = container_client.get_blob_client("test_blob")
downloaded_blob = blob_client.download_blob()
encrypted_data = downloaded_blob.readall()

#Blob 데이터 복호화
cipher_suite = Fernet(encryption_key)
decrypted_data = cipher_suite.decrypt(encrypted_data)

#복호화 한 데이터를 로컬(client측)에 저장
with open("C:/Users/kbd11/OneDrive/바탕 화면/description.txt", "wb") as file:
    file.write(decrypted_data)

print(decrypted_data)





