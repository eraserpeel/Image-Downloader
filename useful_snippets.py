#===============================================================================
# file_listing = []
# for dir, set, files in os.walk("pic_links"):
#     for file in files:
#         fileread = open(dir + "\\" + file, 'r')
#         lines = fileread.readlines()
#         filewrite = open(dir + "\\" + file, 'w')
#         print file
#         for line in lines:
#             line = line.split(" ")
#             filewrite.write(line[1])
# 
# 
# 
# file_listing = []
# filewrite = open("search_terms.txt", 'w')
# 
# for dir, set, files in os.walk("pic_links"):
#     for file in files:
#         search_name = file.split("_")[0]
#         filewrite.write(search_name + "," + dir + "\\" + file + "\n")
#     
# filewrite.close()
#===============================================================================



#===============================================================================
# 
# #Test to parse out the urls. 
# #############################################
# filename = "engine_3287733.txt"
# fileread = open(filename, 'r')
# directory_name = filename.split(".txt")[0]
# create_directory(directory_name)
# urls = fileread.readlines()
# fileread.close()
# url_listing = []    
#  
#  
# for url in urls:
#     url = url.split(' ')
#     url_listing.append(url[1])
# ############################################    
#  
#===============================================================================
#===============================================================================
# urlParser = Parser(url_listing)
# dict = urlParser.urls_by_domain_dict()
# listy = urlParser.urls_by_domain_list_ordered()
# 
# d = downloadermanager.DownloadManager(listy, directory_name, 20)
#===============================================================================
#d.print_queue()


#===============================================================================
# for key, urls in listy:
#     print key
#===============================================================================
        
 