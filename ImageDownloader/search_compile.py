
import re
from urlparser import Parser
import urlparser
import os

def search(search_term):
    """
    Return a list of all files in which the search_term is
    found in the file name.
    """
    search_term = clean_str(search_term)
    found_files = []
    for line in open("search_terms.txt", 'r'):
        term, file = line.split(",")
        if(search_term.lower() in term.lower()):
           found_files.append(clean_str(file))
    return found_files

def compile_search(files, directory_base):
    """
    Takes in a list of files and compiles all links into a single ordered
    list sorted by the number of items in that domain.  
    """
    compiled_list = []
    for file in files:
        for line in open(clean_str(file), 'r'):
            jpg = clean_str(parse_jpg_name(line))
            if(jpg != ""): 
                dir = file.split("\\")
                dir = dir[len(dir) - 1].split(".")[0]
                url = clean_str(line)
                compiled_list.append((url, directory_base + "\\" + dir, jpg))
    urlParser = Parser(compiled_list)
    return urlParser.urls_by_domain_list_ordered()

def clean_str(str):
    """Simply used to clean the newlines, tabs and spaces from a string"""
    return str.strip("\n\t ")

def parse_jpg_name(url):
    """Parses the JPG from the url"""
    IMG_REGEX = "([a-zA-Z0-9\_\.]*(jpg|jpeg|gif|png))"
    try:
        jpg_name = re.search(IMG_REGEX, url, re.IGNORECASE).group(0)
        return jpg_name
    except: 
        return ""
    
