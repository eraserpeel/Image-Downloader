
import Queue
import threading
import re
import time
import urllib2
import os
from random import randint

class DownloadImages():
    """ 
    Instantiate DownloadManager in order to generate queues that can 
    be used with the DownloadThread class. 
    
    All methods are private, with the files being download upon
    instantiation of the class. The constructor takes in the 
    url_list and max_num_threads. The url_list should be sorted.
    
    """
    _list_of_queues = []
    
    #url_list is sorted using urlparser.py's urls_by_domain_list_ordered method
    def __init__(self, url_list, max_num_threads):
        self._create_queues(url_list, max_num_threads)
        #self._start_downloads()
        
    def _create_queues(self, url_list, max_num_threads):
        """
        Use url_list containing tuple of url, dir, and jpg to determine 
        number of threads and hence queues. 
        """
        domain_count, url_count = self._get_domain_url_count(url_list)
        urls_per_thread = self._get_url_per_thread_count(domain_count, url_count, max_num_threads)
        self._list_of_queues.append(Queue.Queue())
        current_queue = 0
        count = 0
        for domain in url_list:
            urls = domain[1]
            count = count + 1
            if(count > urls_per_thread):
                current_queue = current_queue + 1
                self._list_of_queues.append(Queue.Queue())
                count = 0
            for url in urls:
                self._list_of_queues[current_queue].put(url)
        
    def _get_url_per_thread_count(self, domain_count, url_count, max_num_threads):
        """Calculate the number of threads needed."""
        if(domain_count < max_num_threads):
            return domain_count
        return (url_count / max_num_threads)
        
    def _get_domain_url_count(self, url_list):
        """
        Calculate the number of unique domains and total number of urls from list.
        """
        url_count = 0
        domain_count = 0
        for domain, urls in url_list[0:-1]:     #This is a hack to exclude flickr which dominates the queue.
                                                #Remove the [0:-1] let it include flickr. 
            domain_count = domain_count + 1
            url_count = url_count + len(urls)
        url_count = url_count + len(url_list[len(url_list)-1])  #If including flickr in the count then remove this line 
                                                              #and the one above.
        return domain_count, url_count
            
    def _start_downloads(self):
        """Create threads, pass it the queues, and start threads."""
        threads = []
        print("Using: " + str(len(self._list_of_queues)) + " threads based on balancing thread load across domains.")
        for i in range(0,  len(self._list_of_queues)):
            threads.append(DownloadThread(i, self._list_of_queues[i]))
            threads[i].start()
        for thread in threads:
            thread.join()
            
        
class DownloadThread(threading.Thread):
    """
    Use download thread with DownloadManager in order to download jpgs
    using the queues initalized in DownloadManager.
    """
    _output_lock = threading.Lock()

    def __init__(self, threadID, queue, args = ""):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.args = args
    
    def _create_folder(self, folder_name):
        """Create folder in the instance that it doesn't exist."""
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            
    def _check_if_file_exists(self, directory, jpg_name):
        """Rename file if it already exists."""
        if(os.path.isfile("pic_dls\\" + directory + "\\" + jpg_name)):
            return str(randint(1000,100000)) + jpg_name
        return jpg_name
    
    def _download_image(self, url, dir, jpg_name):
        """
        Use for downloading jpg images to a specified directory.  
        All files are to be written within the sub-folder 'pic_dls'.
        Between downloads a wait of 1 second minimum is to be used in 
        order to not hit individual servers too hard. 
        """
        try:
            self._create_folder(dir)
            jpg_name = self._check_if_file_exists(dir, jpg_name)
            file_handle = open(dir + "\\" + jpg_name, 'wb')
            file_handle.write(urllib2.urlopen(url, timeout = 20).read())
            file_handle.close()
            print(self.name + "-Downloaded: " + jpg_name)
        except Exception, arg:
            with self._output_lock:
                print(self.name + "-Error download: " + jpg_name + " - " + str(arg))
        time.sleep(2)
            
    def run(self):
        """Pops next value off the queue and starts thread using download_image."""
        while not self.queue.empty():
            url, dir, jpg = self.queue.get(block = False)
            self._download_image(url, dir, jpg)
            