"""
Author: Álvar Ginés Legaz Aparicio
Mail: alvarlegaz@gmail.com

Briefly: Metacollectormetacollector is a tool designed for extracting metadata from PDF files, whether they reside locally on a machine or are accessible on the internet.

License: Creative Commons Legal Code
"""

import sys
import requests
import PyPDF2
import os
from datetime import datetime

# Program version
major_version = "1"
minor_version ="0"
pdf_reader = None

def get_pdf_metadata_from_url(url):
    # Descargar el archivo PDF desde la URL
    response = requests.get(url)
    with open("temp.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)

    # Extraer metadatos del PDF
    with open("temp.pdf", "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        metadatos = pdf_reader.metadata
    os.remove("temp.pdf")
    return metadatos

def get_pdf_metadata_from_local(path):
    with open(path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        metadatos = pdf_reader.metadata
        return metadatos
    
def remove_metadata(path, path_out):
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Make a PdfFileWriter object to write the new PDF
        pdf_writer = PyPDF2.PdfWriter() 
        for page_num in pdf_reader.pages:
            pdf_writer.add_page(page_num)

    pdf_writer.add_metadata({
        '/Title': '',
        '/Author': '',
        '/Subject': '',
        '/Producer': '',
        '/Keywords': '',
    }) 
    with open(path_out, 'wb') as out_pdf_file:
            pdf_writer.write(out_pdf_file)   

def show_metadata(metadata):
    print(f"Title: {metadata.title}")
    print(f"Author: {metadata.author}")
    print(f"Creator: {metadata.creator}")
    print(f"Producer: {metadata.producer}")
    print(f"Subject: {metadata.subject}")

#These lines will only be executed if the script is run directly.
if __name__ == "__main__":
    
    #print(f"bla {var}") to process sting var in brakes
    if len(sys.argv) < 2:
        print("Error: parameters not defined.")
        sys.exit(1) 

    if sys.argv[1] == "-h":
        print(f"MetaCollector v{major_version}.{minor_version}") 
        print("-l: get pdf from local file.")
        print("-w: get pdf from local url.") 
        print("-r: create new file with metadata removed")     
        sys.exit(0)

    elif sys.argv[1] == "-l":
        if len(sys.argv) != 3:
            print("Fail getting local file - Error: parameters not defined.")
            sys.exit(1)  
        path = sys.argv[2];     
        print(f"Getting pdf from local file:{path}")
        metadata = get_pdf_metadata_from_local(path)
        show_metadata(metadata)
        sys.exit(0)  

    elif sys.argv[1] == "-w":
        if len(sys.argv) != 3:
            print("Fail getting url file - Error: parameters not defined.")
            sys.exit(1) 
        url = sys.argv[2];  
        print(f"Getting pdf from url:{url}")
        metadata = get_pdf_metadata_from_url(url)  
        show_metadata(metadata)
        sys.exit(0)

    if sys.argv[1] == "-r":
        if len(sys.argv) < 3:
            print("Fail removing metadata - Error: parameters not defined.");
            sys.exit(1) 
        elif len(sys.argv) == 3:
            path = sys.argv[2]   
            out_path =  "out.pdf"
            print(f"Getting pdf from local file:{path}")
            print(f"Saving new pdf in local file:{out_path}")
            remove_metadata(path, out_path) 
            sys.exit(0)  
        elif len(sys.argv) == 4:
            path = sys.argv[2]
            out_path = sys.argv[3]    
            print(f"Getting pdf from local file:{path}")
            print(f"Saving new pdf in local file:{out_path}")
            remove_metadata(path, out_path) 
            sys.exit(0)  
    else:
        print("Error: Unknown parameter");
        sys.exit(1) 

