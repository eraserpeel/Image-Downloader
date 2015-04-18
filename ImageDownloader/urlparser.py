
import re
from collections import defaultdict
import tldextract 

class Parser():
    """
    This class is used to parse the urls and get them ready to be used by the 
    download_images module. 
    """
    def __init__(self, url_list):
        num_urls = len(url_list)
        self.url_list = url_list
    
    def urls_by_domain_dict(self):
        """
        Sorts the urls by domain.
        """
        domain_dict = defaultdict(list)
        for url, dir, jpg in self.url_list: 
            domain_name = tldextract.extract(url).domain
            if(domain_name != ""):
                domain_dict[domain_name].append((url.strip("\n"), dir, jpg))
        return domain_dict
    
    def urls_by_domain_list(self):
        """
        Converts the dictionary from urls_by_domain_dict to to a list.
        """
        domain_dict = self.urls_by_domain_dict()
        domain_list = []
        for key, value in domain_dict.iteritems():
            domain_list.append((key, value))
        return domain_list
    
    def urls_by_domain_list_ordered(self):
        """
        This will use the dictionary file to sort domain list by number of 
        urls per domain. The lowest number per domain is first.
        """
        domain_dict = self.urls_by_domain_dict()
        domain_list = []
        domain_list_rtn = []
        for key, value in domain_dict.iteritems():
            domain_list.append((len(value), key))
        domain_list = sorted(domain_list, key = self._getSortOn)
        for count, key in domain_list:
            domain_list_rtn.append((key, domain_dict[key]))
        return domain_list_rtn
        
    def _getSortOn(self, item):
        """Used to sort"""
        return item[0]
        
            
   
    
              