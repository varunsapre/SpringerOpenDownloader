import argparse
import json
import os
from multiprocessing import Pool
import wget
# ------------------------------------------------------------------------------------
def download_books_worker(book):
    book = book_details[book]
    book_filename = f"Books/{book['book_title']} - {book['author']} - {book['edition']}.pdf"
    print (f"Proc:{os.getpid()} = downloading: {book['book_title']} by {book['author']}")
    wget.download(book["pdf_url"], out=book_filename)
    print ("\n")

def download_books(book_details, _async):
    # check if the "compiled" key is present
    # this is done so that an uncompiled json is not mistakenly parsed in this function
    try:
        compiled = book_details["compiled"]
        book_details.pop("compiled") # remove this element for ease of parsing dict
    except Exception as ex:
        print ("JSON provided was not compiled, please verify that json file contents were compiled using the script!")
        return
    os.makedirs("./Books", exist_ok=True)

    # by default async will be 1, so only 1 worker will download
    with Pool(_async) as p:
        print(p.map(download_books_worker, book_details))

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to download and save springer books (from PDF/JSON)')
    parser.add_argument('source', help="Source file provided is a compiled json file")
    parser.add_argument('-a', '--async',type=int, default=1, dest="num_async_workers", help="Source file provided is a compiled json file")
    args = parser.parse_args()

    # check parser args
    if not os.path.isfile(args.source):
        # raise a parser error if it doesn't exist
        parser.error("{} does not exist".format(args.source))

    with open(args.source, "r") as fread:
        book_details = json.load(fread)
    print (f"Downloading using the power of {args.num_async_workers} worker(s)..")
    download_books(book_details, args.num_async_workers)
