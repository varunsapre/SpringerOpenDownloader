import argparse
import json
import os

import wget
# ------------------------------------------------------------------------------------
def download_books(book_details):
    # check if the "compiled" key is present
    # this is done so that an uncompiled json is not mistakenly parsed in this function
    try:
        compiled = book_details["compiled"]
        book_details.pop("compiled") # remove this element for ease of parsing dict
    except Exception as ex:
        print ("JSON provided was not compiled, please verify that json file contents were compiled using the script!")
        return

    for isbn in book_details:
        if isbn != True:
            book = book_details[isbn]
            book_filename = f"{book['book_title']} - {book['author']} - {book['edition']}.pdf"
            print (f"downloading: {book['book_title']} by {book['author']}")
            wget.download(book["pdf_url"], out=book_filename)
            print("\n")

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to download and save springer books (from PDF/JSON)')
    parser.add_argument('source', help="Source file provided is a compiled json file")
    args = parser.parse_args()

    # check parser args
    if not os.path.isfile(args.source):
        # raise a parser error if it doesn't exist
        parser.error("{} does not exist".format(args.source))

    with open(args.source, "r") as fread:
        book_details = json.load(fread)

    download_books(book_details)
