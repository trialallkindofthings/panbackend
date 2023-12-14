##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : Phenix-G
# @File   : main.py
# @Time   : 2021/06/04 00:19:05
from pathlib import Path
from typing import List

import qrcode
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI()
# origins = ['*']  # 或者 ['http://wicos.me'] 可以自定义允许访问的地址
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = Path(__file__).resolve().parent
VIRUS_EXTENSION_NAME = [
    'exe', 'scr', 'com', 'vb', 'vbs', 'js', 'VBS',
    'VBE', 'JS', 'JSE', 'WSH', 'WSF', 'bat', 'sh', 'inf'
]
VIRUS = [virus for virus in map(lambda x: '.' + x, VIRUS_EXTENSION_NAME)]

FILE_PATH = BASE_DIR.joinpath('file')
TemplateResponse = templates.TemplateResponse


def get_files():
    files = [os.path.basename(str(path)) for path in FILE_PATH.iterdir()]
    yield files


def write_file(file):
    with open('./file/{}'.format(file.filename), 'wb')as f:
        for i in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
            f.write(i)


@app.post("/uploadfile/")
async def upload(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        if file.filename:
            extension_name = Path(file.filename).suffix
            if extension_name in VIRUS:
                return TemplateResponse('index.html', {'request': request, 'files': get_files(), 'fail': '上传失败'})
            else:
                write_file(file)
        else:
            return RedirectResponse('http://127.0.0.1:8000/')
    return TemplateResponse('index.html', {'request': request, 'files': get_files(), 'success': '上传成功'})


@app.get("/download/{file_name}")
async def download(file_name: str) -> FileResponse:
    path = str(FILE_PATH.joinpath(file_name))
    return FileResponse(path)


@app.get("/")
async def index(request: Request) -> TemplateResponse:
    return TemplateResponse('index.html', {'request': request, 'files': get_files()})


import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageSequence


def get_ewm(img_adds):
    """ 读取二维码的内容： img_adds：二维码地址（可以是网址也可是本地地址 """
    if os.path.isfile(img_adds):
        # 从本地加载二维码图片
        img = Image.open(img_adds)
    else:
        # 从网络下载并加载二维码图片
        rq_img = requests.get(img_adds).content
        img = Image.open(BytesIO(rq_img))

    # img.show()  # 显示图片，测试用
    # print(img.__dict__)

    txt_list = pyzbar.decode(img)
    print(type(txt_list))
    print(isinstance(txt_list, list))
    print(txt_list)
    # print(txt_list[0])
    # print(txt_list[0].rect)

    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        print(barcodeData)


from MyQR import myqr
import os,cv2

# words = "https://u.wechat.com/MPmqATs3sJz3ksX9aEVy2Ls"  # 解码出的地址
# myqr.run(
#     words,                                  # 可以是字符串，也可以是网址(前面要加http(s)://)
#     version=1,                              # 设置容错率为最高
#     level='H',                              # 控制纠错水平，范围是L、M、Q、H，从左到右依次升高
#     picture="a.gif",                        # 将二维码和图片合成
#     colorized=True,                         # True为彩色二维码，False为黑白
#     contrast=1.0,                           #用以调节图片的对比度，1.0 表示原始图片，更小的值表示更低对比度，更大反之。默认为1.0
#     brightness=1.0,                         #用来调节图片的亮度，其余用法和取值同上
#     save_name="2.gif",       # 保存文件的名字，格式可以是jpg,png,bmp,gif
#     save_dir=os.getcwd()                    #文件保存的位置，默认保存到和.py文件同级
# )
# qr = qrcode.QRCode(
#     version=1, #二维码的格子矩阵大小
#     error_correction=qrcode.constants.ERROR_CORRECT_Q,
#     box_size=10,
#     border=4,
# )
# qr.add_data("Hello World")#向二维码添加数据
# qr.make(fit=True)
# img = qr.make_image(fill_color="green", back_color="white")#更改QR的背景和绘画颜色
# img.show()# 显示二维码

if __name__ == '__main__':
    # import uvicorn
    #
    # uvicorn.run('main:app', port=8000, debug=True, reload=True)
    # get_ewm('code.jpg')  # 1080,2340
    get_ewm('0.png')  # 1080,2340
