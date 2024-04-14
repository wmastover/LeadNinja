from getLinks import getLinks
from getProduct import getProduct
from processJsonOutput import processJsonOutput
from uploadFile import uploadFile
from postLinkToFirebase import addUrlToFirebase
import json

ProductArray = getLinks('https://www.producthunt.com/')
jsonArray = []

for product in ProductArray:
    product_json = getProduct(product)
    jsonArray.append(product_json)


    from datetime import datetime

    # Get today's date and format it as YYYYMMDD
    date_today = datetime.now().strftime('%Y%m%d')
    output_file_name = f'{date_today}.json'

    with open(output_file_name, 'a') as outfile:
        json.dump(product_json, outfile)
        outfile.write('\n')  # write a newline character after each JSON object

processJsonOutput()
try:
    link = uploadFile()
    addUrlToFirebase(link)
except Exception as e:
    print(f"An error occurred: {e}")

