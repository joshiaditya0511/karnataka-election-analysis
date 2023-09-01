from PIL import Image
import pytesseract
import os
from tempfile import TemporaryDirectory
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
import os
import time
from multiprocessing import Pool
import threading
import asyncio
import cv2
from math import floor, ceil

DIR = os.getenv('KEA_BASE_DIR')
DOWNLOAD_THRESHOLD = 5  # Number of remaining PDFs to trigger downloading
LOT_SIZE = 30  # The number of PDFs to call / download at once i.e. size of pdf lot
BATCH_SIZE = 25  # The number of pdf lots to dowload in a single loop

finished=[]

new_links = []
with open(r"new_links.txt",'r') as f:
    new_links = f.readlines()
new_links = list(map(str.strip,new_links))

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'}

path_to_poppler_exe = f"{DIR}/poppler-23.05.0/Library/bin"
pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")

error_log=[]

temp_path = f"{DIR}/pdfs for ocr"
if not os.path.exists(temp_path): os.mkdir(temp_path)

def http_get_sync(url: str):
    response = requests.get(url,headers=headers)
    return response.content

async def http_get(url: str):
    return await asyncio.to_thread(http_get_sync, url)

async def download_pdf(url:str):
    filename = url.split('/')[-1]
    try:
        response = await http_get(url)            
    except:
        error_log.append(f'Error raised for {filename}')
        finished.append(filename)
    else:
        if response.status_code >= 400:
            error_log.append(f'Bad request for {filename}')
            finished.append(filename)        
        else:
            file = open(f"{DIR}/pdfs for ocr/{filename}",'wb')
            file.write(response)
            file.close()
    

async def call_multiple_pdfs(batch_start):
    for i in range(batch_start,batch_start+BATCH_SIZE):
        if batch_start*LOT_SIZE > len(new_links):
            break
        start = i*LOT_SIZE
        end = start + LOT_SIZE
        if end > len(new_links):
            end = len(new_links)+1
        print(f"await called for {start} to {end} for batch start {batch_start}")
        await asyncio.gather(*[download_pdf(url) for url in new_links[start:end]])
        print(f"{start} to {end} finished for batch start: {batch_start} to batch end: {batch_start+BATCH_SIZE}")
        time.sleep(5)


def compare(text:str)->str:
    return (bool(re.search(r"\D",text)) or text=='')


def start_downloading(batch_start : int):
    thread = threading.Thread(target=asyncio.run,args=[call_multiple_pdfs(batch_start)])
    thread.start()


def process_pdf(pdf,page=1,count=0,isEnglish=False):
    factor=0
    if isEnglish: factor=1
    temp_dic = {
        'const_num' : [],
        'page_num' : [],
        'male_voters':[],
        'female_voters':[],
        'other_voters':[],
        'total_voters':[]
    }
    if bool(re.search(r'ppm$',pdf)):
        return pd.DataFrame(temp_dic)
    elif count==2:
        return process_pdf(pdf,page=1,count=count+1,isEnglish=True)
        
    try:
        input_pdf = PdfReader(f"{DIR}/pdfs for ocr/{pdf}")
    except:
        finished.append(pdf)
        error_log.append(f'EOF error for {pdf}')
        print(f'EOF error for {pdf}')
        temp_path = f"{DIR}/pdfs for ocr/{pdf.strip('.pdf')}.ppm"
        if os.path.exists(temp_path): os.remove(temp_path)
        os.remove(f"{DIR}/pdfs for ocr/{pdf}")
        return pd.DataFrame(temp_dic)
        
    else:
        pdf_img = convert_from_path(f"{DIR}/pdfs for ocr/{pdf}",600,poppler_path = path_to_poppler_exe,fmt='ppm',grayscale=True,first_page=page,last_page=page)
        pdf_img[0].save(f"{DIR}/pdfs for ocr/{pdf.strip('.pdf')}.ppm")
        try:
            img = cv2.imread(f"{DIR}/pdfs for ocr/{pdf.strip('.pdf')}.ppm")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            width,height = Image.fromarray(edges).size
            lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
            y_cords = []
            for line in lines:
                x1,y1,x2,y2 = line[0]
                from_start = floor((0.33606557*width) - (0.0245901639*factor))
                to_end = ceil((0.339344*width) - (0.0229508*factor))
                if (x1 in range(from_start,to_end) or (x1<from_start<x2) and abs(x1-x2)>=0.5*width) and (y1==y2):
                    y_cords.append(y1)
            y = max(y_cords)
        except:
            os.remove(f"{DIR}/pdfs for ocr/{pdf}")
            os.remove(f"{DIR}/pdfs for ocr/{pdf.strip('.pdf')}.ppm")
            finished.append(pdf)
            error_log.append(f'Max args error for {pdf}')
            print(f'Max args error for {pdf}')
            return pd.DataFrame(temp_dic)
            
        male_dims = ((0.37868852459 - 0.02950819*factor)*width,(y-0.022016228*height),(0.45737704918 - 0.01311475409*factor)*width,y)
        female_dims = ((0.532786885 - 0.027868852*factor)*width,(y-0.022016228*height),(0.6081967213 - 0.032786885*factor)*width,y)
        other_dims = ((0.6737704918 - 0.037704918*factor)*width,(y-0.022016228*height),(0.74426229508 - 0.036065573*factor)*width,y)
        total_dims = ((0.813114754098 - 0.0311475409*factor)*width,(y-0.022016228*height),(0.8885245901639 - 0.0311475409*factor)*width,y)
        
        temp = re.search(r'^S10A([0-9]*)P([0-9]*)\.pdf$',pdf)
        temp_dic['const_num'].append(int(temp.group(1)))
        temp_dic['page_num'].append(int(temp.group(2)))
        
        male_votes_img =  pdf_img[0].crop(male_dims)
        temp_dic['male_voters'].append(str(pytesseract.image_to_string(male_votes_img,lang='eng',config='--psm 4 --oem 3 digits')).strip())
        
        female_votes_img =  pdf_img[0].crop(female_dims)
        temp_dic['female_voters'].append(str(pytesseract.image_to_string(female_votes_img,lang='eng',config='--psm 4 --oem 3 digits')).strip())
        
        other_votes_img =  pdf_img[0].crop(other_dims) #await cropped(pdf_img[0],other_dims)
        temp_dic['other_voters'].append(str(pytesseract.image_to_string(other_votes_img,lang='eng',config='--psm 4 --oem 3 digits')).strip())
        
        total_votes_img =  pdf_img[0].crop(total_dims) #await cropped(pdf_img[0],total_dims)
        temp_dic['total_voters'].append(str(pytesseract.image_to_string(total_votes_img,lang='eng',config='--psm 4 --oem 3 digits')).strip())
        
        if any(list(map(compare,[temp_dic['male_voters'][0],temp_dic['female_voters'][0],temp_dic['total_voters'][0]]))) and count!=3:
            [temp_dic[key].pop() for key in temp_dic.keys()]
            return process_pdf(pdf,page=2,count=count+1)
        finished.append(pdf)
        temp_path = f"{DIR}/pdfs for ocr/{pdf}"
        if os.path.exists(temp_path): os.remove(temp_path) 
        temp_path = f"{DIR}/pdfs for ocr/{pdf.strip('.pdf')}.ppm"
        if os.path.exists(temp_path): os.remove(temp_path)
        return pd.DataFrame(temp_dic)


def main():      
    file_list = os.listdir(f"{DIR}/pdfs for ocr/")
    counter = 0
    while len(finished)<len(new_links):
        # Check if the number of remaining PDFs is below the threshold
        if len(file_list) < DOWNLOAD_THRESHOLD:
            start_downloading((counter*BATCH_SIZE))
            print(f"Downloading started for batch start: {(counter*BATCH_SIZE)} with counter: {counter}")
            counter +=1
            time.sleep(240) 

        # Refresh the file list
        file_list = os.listdir(f"{DIR}/pdfs for ocr/")
        
        # Process the existing PDFs using multiprocessing
        with Pool(processes=6) as pool:
            results = pool.imap_unordered(process_pdf, file_list,chunksize=15)
            new_df = pd.DataFrame(columns=['const_num','page_num','male_voters','female_voters','other_voters','total_voters'])
            for df in results:
                new_df = pd.concat([df,new_df],ignore_index=True)
            if os.path.exists(r"eligible_voters_NEW.csv"):
                temp_df = pd.read_csv(r"eligible_voters_NEW.csv",index_col=0)
                new_df = pd.concat([temp_df,new_df],ignore_index = True)
            new_df.to_csv(r"eligible_voters_NEW.csv")
        
        read_error_logs=[]
        with open('error_log.txt','r') as file:
            read_error_logs = file.readlines()
            read_error_logs = list(map(str.strip,read_error_logs))

        with open('error_log.txt','a') as file:
            [file.write(log+'\n') for log in error_log if log not in read_error_logs]

        temp_path = f"{DIR}/pdfs for ocr"
        if os.path.exists(temp_path): os.remove(temp_path)
            

if __name__ == "__main__":
    main()
