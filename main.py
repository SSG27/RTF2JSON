import json
from striprtf.striprtf import rtf_to_text
import os
from datetime import datetime
import uuid
import re

def convert():
    url = 'sample.rtf'
    file_uuid = uuid.uuid4()
    uuid_string = str(file_uuid)

    with open(url, 'r') as rtf_file:
        rtf_data = rtf_file.read()

    text = rtf_to_text(rtf_data)
    metadata_list = metadata(url)
    structured_text = format_structured_text(text, rtf_data)
    subfiles = format_subfiles(uuid_string)

    output_json = format_text(text, metadata_list, uuid_string, structured_text, subfiles)

    json_data = json.dumps(output_json, indent=2)

    with open('file.json', 'w') as json_file:
        json_file.write(json_data)

def metadata(url):
    file_info = {
        "type": "filename",
        "value": os.path.basename(url),
        "size": os.path.getsize(url),
        "creation_time": datetime.fromtimestamp(os.path.getctime(url)).isoformat(),
        "modification_time": datetime.fromtimestamp(os.path.getmtime(url)).isoformat(),
    }
    return [file_info]

def format_structured_text(text, rtf_data):
    font_pattern = re.compile(r'\\f\d+\\fnil\\fcharset0 ([^\\]+)')
    font_match = font_pattern.search(rtf_data)
    font = font_match.group(1) if font_match else "Default Font"

    font_size_pattern = re.compile(r'\\fs(\d+)')
    font_size_match = font_size_pattern.search(rtf_data)
    font_size = int(font_size_match.group(1)) if font_size_match else 12  # Default font size

    structured_text = [
        {
            "text": text,
            "metadata": [
                {"type": "font", "value": font},
                {"type": "font-size", "value": font_size}
            ]
        }
    ]

    return structured_text

def format_subfiles(uuid_string):
    subfiles = [
        {
            "uuid": uuid_string
        }
    ]

    return subfiles


def format_text(text, metadata, uuid_string, structured_text, subfiles):
    json_schema_list = []
    json_schema = {
        "text": text,
        "uuid": uuid_string,
        "metadata": metadata,
        "structuredtext": structured_text,
        "subfiles": subfiles
    }
    json_schema_list.append(json_schema)
    json_schema_files = {"files": json_schema_list}
    return json_schema_files

convert()
