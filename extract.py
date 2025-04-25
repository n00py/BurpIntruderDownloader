#!/bin/python
import base64
import re
import xml.etree.ElementTree as ET
import sys 
from urllib.parse import unquote
from pathlib import Path

output_path = Path()
# should match e.g.
# Content-Disposition: attachment; filename*=UTF-8''myfile.txt
# Content-Disposition: attachment; filename="myfile.txt"
# Content-Disposition: attachment; filename=myfile.txt
regex_expression = re.compile(r"filename(?:=\"?|\*=[\w\d\-]*'')(.+)\"?")

def main():
    # Parse Burp file
    for path in sys.argv[1:]:
        mytree = ET.parse(path)
        myroot = mytree.getroot()

        # Search through each item in the file
        for item in myroot.findall('item'):
            try:
                # Retreive the request and response
                based = (item.find('response').text)
                req = (item.find('request').text)

                # Decode the response
                data = base64.b64decode(based)
                    
                # Decode request and extract the requested path
                _, reqpath, _ = base64.b64decode(req).decode('utf-8').split(' ',2)

                # Retrieve the headers from the response
                headers, content = data.split(b'\r\n\r\n',1)

                # Extract the filename from the response headers
                filenames = regex_expression.findall(headers.decode("utf-8"))
                if len(filenames) <= 0 : 
                    # if the response does not contain a filename, use the requested file
                    filename=reqpath.split('/')[-1]
                else:
                    # Get the first match, parse %xx encoding
                    filename = Path(unquote(filenames[0]))
                    # remove any parent paths and surrounding whitespaces
                    filename = filename.name.strip()

                # Generate the output path
                with (output_path/filename).open("wb") as f:
                    # Write the body to a file using extracted filename
                    f.write(content)
                print (f"[+] Extracted : {filename}")

            # If something goes wrong, print the exception
            except Exception as e:
                print(e, file=sys.stderr)

if __name__ == "__main__":
    main()
