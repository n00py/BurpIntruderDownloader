import bs4
import base64
from bs4 import BeautifulSoup
# Import the Burp File
path = 'FILEPATH'
burp_file = open(path,'r')
xml = burp_file.read()
# Parse the XML with BeautifulSoup
parsed = BeautifulSoup(xml, "html.parser")


# Search through each item in the file
for document in parsed.find_all('item'):
    try:
        # Extract the CDATA content within an item response
        # https://stackoverflow.com/questions/2032172/how-can-i-grab-cdata-out-of-beautifulsoup
        based = document.response.find(text=lambda tag: isinstance(tag, bs4.CData)).string.strip()
        # Decode the base64 encoded response
        data = base64.b64decode(based)
        # Strip off the HTTP headers, leaving only the body
        content = data.split(b'\r\n\r\n')[1]
        # Extract the filename from the HTTP header, replace any slashes in filename
        stringed = str(data)
        filename = (stringed.split("filename=\"")[1].split("\"")[0]).replace("/", "-")
        # Write the body to a file using extracted filename
        f = open("/tmp/" + filename, "wb")
        f.write(content)
        f.close()
    # If something goes wrong, print the exception
    except Exception as e:
        print(e)

