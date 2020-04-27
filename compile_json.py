import argparse
import json
import os
import unicodedata
from pprint import pprint

import requests
import tabula

# CLEANING JSON FUNCTIONS ------------------------------------------------------------------------------
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

def get_pdfurl_isbn(sno, url):
    if "http" in url:
        pdf_replace_text = "content/pdf"
        isbn = url.split("/")[-1].split("?")[-1].split("&")[-1].split("=")[-1]
        r = requests.get(url)
        pdf_url = r.url.replace("book",pdf_replace_text)+".pdf"
        print(f"\t{sno} -> {pdf_url}                   ", end="\r")
        return [pdf_url,isbn]
    return [None, None]

def load_uncompiled_json(filename):
    jsondata = None
    clean_jsondata = []

    print ("cleaning json", end= " - ")
    try:
        # read and write out a human-friendly json with indents
        with open(filename, "r") as fread:
            jsondata = json.load(fread)
            for page_num in jsondata:
                for line_data in page_num["data"]:
                    # remove \r characters and strip accent chars
                    line = [ strip_accents(elem["text"].replace("\r", " ")) for elem in line_data ]
                    clean_jsondata.append(line)
        print ("done")
    except Exception as ex:
        print (f"failed! - {ex}")
        return "FAIL"

    print ("dumping cleaned json", end= " - ")
    try:
        with open("clean.json", "w") as fout:
            json.dump(clean_jsondata,fout, indent=4)
        print ("done")
    except Exception as ex:
        print (f"failed! - {ex}")
        return "FAIL"

    return "OK"


# COMPILE JSON FUNCTIONS -----------------------------------------------------------------------------
def compile_data(filename):
    print ("reading precleaned json", end= " - ")
    clean_jsondata = None
    try:
        # read and write out a human-friendly json with indents
        with open(filename, "r") as fread:
            clean_jsondata = json.load(fread)
        print ("done")
    except Exception as ex:
        print (f"failed! - {ex}")
        return "FAIL"

    book_details = {}
    headers = [ header.replace(" ","_").lower() for header in clean_jsondata[1]+["pdf_url", "isbn"] ] # add new parameters

    # books list removes 2 header lines
    books_list = clean_jsondata[2:]
    print (f"\ngetting URLs/ISBN  to each PDF (total: {len(books_list)}) - ")
    # single line pythonic way (not suitable to dumping data on every request) -
    # books_list = [ elem + get_pdfurl_isbn(elem[0], elem[-1]) for elem in books_list if "http" in elem[-1] ]

    # "compiled" key added to make sure that json dump was compiled from this function
    # check happens when downloading function receives this data
    book_details["compiled"] = True

    # non-pythonic way; but dumps book details immediately after retrieving
    for book in books_list:
        # if line has http, get the pdf url and isbn info
        if "http" in book[-1]:
            data = book + get_pdfurl_isbn(book[0], book[-1])
            book_details[data[-1]] = {headers[i] : data[i] for i in range(1,len(headers))}
            with open("Books.json", "w") as fout:
                json.dump(book_details,fout, indent=4)

    print ("\ndone") #no exception handling, if it fails, needs to exit
    return book_details

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to download and save springer books (from PDF/JSON)')
    parser.add_argument('source', help="PDF/JSON filepath (add '-C' option for precleaned JSON)")
    parser.add_argument('-C', '--precleaned_json', action='store_true', dest="precleaned_json", help="Pre cleaned JSON file is provided")
    args = parser.parse_args()

    # check parser args
    if not os.path.isfile(args.source):
        # raise a parser error if it doesn't exist
        parser.error("{} does not exist".format(args.source))

    if not args.precleaned_json:
        tabula.convert_into(args.source, "raw.json", output_format="json", pages='all')
        clean_jsondata = load_uncompiled_json("raw.json")
    else:
        book_details = compile_data(args.source)