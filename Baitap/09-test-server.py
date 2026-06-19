from fastapi import FastAPI

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Chào Nhung! Mạng IoT kết nối thành công rồi nha!"}