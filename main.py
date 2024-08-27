from fastapi import FastAPI, File, UploadFile
import requests
import json

app = FastAPI()

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
item_list = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"data/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await uploaded_file.read())

    with open(file_location, "rb") as file_object:
        r = requests.post(receiptOcrEndpoint, data={
            'client_id': 'TEST',
            'recognizer': 'auto',
            'ref_no': 'ocr_python_123',
        }, files={"file": file_object})
        
        data = json.loads(r.text)

        if 'receipts' in data and len(data['receipts']) > 0 and 'items' in data['receipts'][0]:
            items = data['receipts'][0]['items']
            for item in items:
                item_list.append(item['description'])

    print(item_list)
    return {"item_list": item_list}
