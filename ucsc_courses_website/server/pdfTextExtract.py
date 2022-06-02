import pdfplumber
import json
import sys


totalText = ""

with pdfplumber.open('./uploads/'+sys.argv[1]) as pdf:
    for x in pdf.pages:
        totalText += x.extract_text()
# totalText = ''.join(totalText.split())
print(totalText)

# # x = open(r"ucsc_courses_website\server\package.json")
# with open('./uploads/'+sys.argv[1]) as json_data:
#  for entry in json_data:
#   print(entry)

# print("DONE2")
