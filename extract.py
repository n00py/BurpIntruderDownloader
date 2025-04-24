#!/bin/python
import base64
import re
import xml.etree.ElementTree as ET
import sys
# Variables
#path = 'document-download.burp'
from pathlib import Path
output_path = Path()

def main():
    # Parse Burp file
    for path in sys.argv[1:]:
        mytree = ET.parse(path)
        myroot = mytree.getroot()

        # Search through each item in the file
        for item in myroot.findall('item'):
            try:
                # Retreive the response
                based = (item.find('response').text)
                req = (item.find('request').text)

                # Decode the response
                data = base64.b64decode(based)
                httpverb, reqpath, rest = base64.b64decode(req).decode('utf-8').split(' ',2)



                # Retrieve the headers from the response
                headers = data.split(b'\r\n\r\n')[0]

                # Retrieve the content from the response
                content = data.split(b'\r\n\r\n')[1]

                # Extract the filename from the response headers
                regex_expression = r'filename=(?:\")?([a-zA-Z0-9\-\_\.\_]*)(?:\")?'
                filenames = re.findall(regex_expression, headers.decode("utf-8"))
                if len(filenames) <= 0 :
                    filename=reqpath.split('/')[-1]
                    print(f'[+] not filename in response detected, falling back to requested: {filename}')
                else:
                    # Get the first match
                    filename = filenames[0]

                # Generate the output path

                with (output_path/filename).open("wb") as f:
                    # Write the body to a file using extracted filename
                    f.write(content)
                print (f"[+] Extracted : {filename}")

            # If something goes wrong, print the exception
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
