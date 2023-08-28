"""
Description:    This module is used in verifying data and logic of core
                functionalities. 

Author:         Khamis Buol (c) 2023
"""
import requests
import platform
import os

def validate_url_exists(url: str) -> bool:
    """
    This function is used to validate a webpage denoted by a URL string. 

    :param str url: webpage url
    :return bool:   true if the page exists, otherwise false
    """
    http_request = requests.get(url)
    if http_request.status_code == 200:
        return True
    else:
        return False
    

def validate_file_exists(file_path: str) -> bool:
    output = os.path.exists(file_path)
    return output

#
# Might include in a different module
#
def get_platform() -> str:
    return platform.uname()[0]

