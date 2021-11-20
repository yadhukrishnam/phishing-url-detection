import os
from urllib.parse import urlparse

class Parser:
    def __init__(self, url, status=None) -> None:
        self.url = url
        self.urlobj = urlparse(self.url)
        self.features = {}
        self.status = None
        
        if status != None:
            self.status = status

    def parse(self):
        def check_ip(address):
            return 1 if not address.split('.')[-1].isalpha() else 0

        def check_http_in_path(path):
            return 1 if "http" in path else 0
        
        def check_tld_in_path(path):
            tlds = ["com", "ru", "in", "org", "net", "info", "biz", "online"]
            return 1 if any([(tld in path) for tld in tlds ]) else 0
        
        def is_shortened(domain):
            services = ["bit.ly", "t.co"]
            return 1 if any([(service in domain) for service in services]) else 0
        
        def get_subdomains(domain):
            return domain.split(".")[:-1]

        def tld_in_subdomain(domain):
            tlds = ["com", "ru", "in", "org", "net", "info", "biz", "online"]
            subdomains = get_subdomains(domain)
            for subdomain in subdomains:
                if subdomain in tlds:
                    return 1
            return 0
        
        def path_extension(path):
            return 1 if any(os.path.splitext(path)[-1].lower()) else 0

        counts = {'nb_dots': ".", 'nb_hyphens': "-",  'nb_at': "@",  'nb_qm': "?",   'nb_and': "&", 'nb_or': "|",
                   'nb_eq': "=",  'nb_underscore': "_",  'nb_tilde': "~",  'nb_percent': "%",  'nb_star': "*",  'nb_colon': ":",  'nb_comma': ",",  'nb_semicolumn': ";",  'nb_dollar': "$",
                   'nb_space': " ",  'nb_www': "www",  'nb_com': ".com",  'nb_dslash': "/"}
        for feature in counts:
            self.features[feature] = self.urlobj.geturl().count(counts[feature]) 
        
        self.features["length_url"]  = len(self.urlobj.geturl())
        self.features["length_hostname"]  = len(self.urlobj.hostname)
        self.features["ip"] = check_ip(self.urlobj.hostname)
        self.features["http_in_path"] = check_http_in_path(self.urlobj.path)
        self.features["https_token"] = 1 if "https" in self.urlobj.scheme else 0
        self.features["port"] = 1 if str(self.urlobj.port).isnumeric() else 0
        self.features["tld_in_path"] = check_tld_in_path(self.urlobj.path)
        self.features["shortening_service"] = is_shortened(self.urlobj.netloc)
        self.features["tld_in_subdomain"] = tld_in_subdomain(self.urlobj.netloc)
        #self.features["abnormal_subdomain"] = 0
        self.features["nb_subdomains"] = len(get_subdomains(self.urlobj.netloc))
        #self.features["char_repeat"] = 0
        self.features["path_extension"] = path_extension(self.urlobj.path)
        
        self.features["url"] = self.url
        
        if self.status != None:
            self.features["status"] = self.status
        
        return self.features