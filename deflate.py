import urllib.parse
import zlib
import base64
import xml.etree.ElementTree as ET
import json

def encode(data, encode_uri=False, deflate_raw=False, base64_encode=False):
    # URI encode if the flag is set
    if encode_uri:
        try:
            data = urllib.parse.quote(data)
        except Exception as e:
            print(f"encodeURIComponent failed: {e}")
            return None

    # Deflate using raw deflate if the flag is set
    if deflate_raw and len(data) > 0:
        try:
            # Compress the data using raw deflate (-zlib.MAX_WBITS)
            compressed_data = zlib.compress(data.encode('utf-8'), level=zlib.Z_DEFAULT_COMPRESSION, wbits=-zlib.MAX_WBITS)
            # Convert the compressed byte data to a string
            data = ''.join(chr(byte) for byte in compressed_data)
        except Exception as e:
            print(f"deflateRaw failed: {e}")
            return None

    # Base64 encode if the flag is set
    if base64_encode:
        try:
            data = base64.b64encode(data.encode('latin1')).decode('utf-8')
        except Exception as e:
            print(f"btoa failed: {e}")
            return None

    return data

newlib = []

def process_xml(file_path, encode_uri=False, deflate_raw=False, base64_encode=False):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Process each <shape> element
    for shape in root.findall('shape'):
        aspect = shape.get('aspect')
        h = shape.get('h')
        w = shape.get('w')
        name = shape.get('name')
        # Convert the entire <shape> element to a string, including its tags and children
        shape_str = ET.tostring(shape, encoding='unicode')
        
        # Encode the string
        encoded_shape_str = encode(shape_str, encode_uri=encode_uri, deflate_raw=deflate_raw, base64_encode=base64_encode)

        if encoded_shape_str:
            # Replace the original element with the encoded content
            # We create a new element <encoded> to hold the encoded data, as the encoded string is no longer valid XML
            encoded_elem = ET.Element('encoded')
            encoded_elem.text = encoded_shape_str
            #print(f"&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\"0\"/&gt;&lt;mxCell id=\"1\" parent=\"0\"/&gt;&lt;mxCell id=\"2\" value=\"\" style=\"shape=stencil({encoded_elem.text});whiteSpace=wrap;html=1;\" vertex=\"1\" parent=\"1\"&gt;&lt;mxGeometry width=\"120\" height=\"120\" as=\"geometry\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;")
            enc = {
            "xml": f"&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\"0\"/&gt;&lt;mxCell id=\"1\" parent=\"0\"/&gt;&lt;mxCell id=\"2\" value=\"\" style=\"shape=stencil({encoded_elem.text});whiteSpace=wrap;html=1;aspect=fixed\" vertex=\"1\" parent=\"1\"&gt;&lt;mxGeometry width=\"120\" height=\"120\" as=\"geometry\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;",
            "w": w,
            "h": h,
            "title": name
            }
            newlib.append(enc)
            #print(json.dumps(enc))
            # Replace the old <shape> element with the new <encoded> element
            #root.replace(shape, encoded_elem)

    # Save the modified XML back to the file
    #tree.write(file_path)

# Example usage
xml_file_path = 'no-circle.xml'
process_xml(xml_file_path, encode_uri=True, deflate_raw=True, base64_encode=True)
print(json.dumps(newlib))
