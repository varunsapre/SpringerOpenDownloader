# Downloader for Free SpringerOpen Books (PDF list)
This mini-project reads a PDF list of free Springer Books and downloads the files
___________________________
### Pre-requisites:
1) Py3 modules (downloader script)
-- wget

2) Py3 modules (data compiler script)
-- tabula
-- unicodedata
-- requests
___________________________
### Run downloader: `python3 download_books.py Books.json`
___________________________
### Converting Data from PDF to JSON (for `Books.json`):
1) `python3 compile_json.py <PDF_filename>` (Output is `raw.json` , `clean.json` )
2) open `clean.json` and make sure all entries in the JSON file are correct. If converting using the provided PDF, the last few entries in `clean.json` are corrupted due to tabula conversion error. Please manually clean these.
3) `python3 compile_json.py clean.json -C` (output is `Books.json`)
4) run downloader script after this
___________________________