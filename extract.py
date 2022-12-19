import base64
import re
import xml.etree.ElementTree as ET

# Variables
path = 'document-download.burp'
output_path = './extracted/'

def main():
    # Parse Burp file
    mytree = ET.parse(path)
    myroot = mytree.getroot()

    # Search through each item in the file
    for item in myroot.findall('item'):
        try:
            # Retreive the response
            based = (item.find('response').text)

            # Decode the response
            data = base64.b64decode(based)

            # Retrieve the headers from the response
            headers = data.split(b'\r\n\r\n')[0]

            # Retrieve the content from the response
            content = data.split(b'\r\n\r\n')[1]

            # Extract the filename from the response headers
            regex_expression = r'filename=(?:\")?([a-zA-Z0-9\-\_\.\_]*)(?:\")?'
            filenames = re.findall(regex_expression, headers.decode("utf-8"))
            if len(filenames) <= 0 :
                raise Exception("No filename was identified")

            # Get the first match
            filename = filenames[0]

            # Generate the output path
            output_name = output_path + filename
            print (f"[+] Extracted : {filename}")

            # Write the body to a file using extracted filename
            f = open(output_name, "wb")
            f.write(content)
            f.close()

        # If something goes wrong, print the exception
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
