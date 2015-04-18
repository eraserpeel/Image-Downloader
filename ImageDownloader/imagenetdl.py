
import download_images
import os
import re
import sys
import argparse
import search_compile

def main():
    """
    Where the program starts and takes in the command-line options 
    and compiles the necessary files.
    """
    print("Processing files...")
    parse_options()
    directory_base, thread_count, file_flag, search_term = parse_options()
    search_terms = get_search_list(file_flag, search_term) 
    file_list = []
    for term in search_terms: 
        file_list.extend(search_compile.search(term))
    if(len(file_list) > 0):
        url_list = search_compile.compile_search(file_list, directory_base)
    else:
       print("No links are found in these files.")
       sys.exit() 
    print_download_data(url_list)
    download_images.DownloadImages(url_list, int(thread_count))

def get_search_list(file_flag, search_term): 
    """
    If a file is being used then return all the contents. Otherwise just
    return the individual search_term
    """
    if(file_flag):
        try:
            return open(search_term, 'r').readlines()
        except Exception, arg:
            print("Error opening file: " + search_term + " - " + arg)
            sys.exit()
    else:
        return [search_term]
            
def print_download_data(dl_data):
    """Just used to give status on numbers of downloads"""
    domain_count = 0 
    url_count = 0
    for item in dl_data:
        domain_count = domain_count + 1
        url_count = url_count + len(item[1])
    print("Downloading: " + str(url_count) + " urls from " + str(domain_count) + " domains")
        
def parse_options():
    """
    Set the parser for handling files, directories, and the thread count.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action="store", dest="directory", default="pic_dls", 
                        help="Allows for a file of search terms to be used instead of a single term."
                              "The default directory is pic_dls.")
    parser.add_argument('-t', action="store", dest="threads", default=50,
                        help="Sets the max thread count, though doesn't guarantee that number of threads will be used."
                             "If nothing is set then the default will be 50")
    parser.add_argument('-f', '--file', action='store_true', 
                        help="Turns the search term into a file.")
    parser.add_argument("search_term", default = '',
                        help="Allows for a file of search terms to be used instead of a single term.")
    args = parser.parse_args()
    return (args.directory, args.threads, args.file, args.search_term) 
    
if __name__ == '__main__':
    main()
