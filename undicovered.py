import requests
import queue
import threading
import sys
import time
import os
from requests.adapters import HTTPAdapter

class DirectoryScanner:
    def __init__(self, host):
        self.host = host
        self.extensions = []  # User-defined extensions
        self.http_method = 'GET'  # Default HTTP method
        self.threads = 25  # Default number of threads
        self.wordlist_size = 0  # Initialize wordlist size
        self.directory_wordlist_file = ''
        self.output_file = ''
        self.desired_status_codes = [200]  # Default desired status code
        self.session = None

    def set_extensions(self, extensions):
        self.extensions = extensions

    def set_http_method(self, http_method):
        self.http_method = http_method

    def set_threads(self, threads):
        self.threads = threads

    def set_directory_wordlist_file(self, directory_wordlist_file):
        self.directory_wordlist_file = directory_wordlist_file
        self.wordlist_size = self.get_wordlist_size(directory_wordlist_file)

    def set_desired_status_codes(self, desired_status_codes):
        self.desired_status_codes = desired_status_codes

    def get_wordlist_size(self, directory_wordlist_file):
        try:
            with open(directory_wordlist_file, 'r') as f:
                return sum(1 for _ in f)
        except FileNotFoundError:
            return 0

    def start_scan(self):
        if not self.directory_wordlist_file:
            print("Error: Directory wordlist file not provided.")
            return

        try:
            requests.get(self.host)
        except Exception as e:
            print(e)
            return

        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(pool_connections=100, pool_maxsize=100))  # Adjust connection pool size

        q = queue.Queue()
        found_directories = []
        count = 0

        def dirbuster(thread_no, q):
            nonlocal count
            while True:
                url = q.get()
                try:
                    response = self.session.request(self.http_method, url, allow_redirects=True, timeout=5)
                    count += 1
                    if response.status_code in self.desired_status_codes:
                        directory_url = str(response.url)
                        print("[+] Directory found: {} (Status code: {})".format(directory_url, response.status_code))
                        found_directories.append((directory_url, response.status_code))
                except:
                    pass
                q.task_done()

        with open(self.directory_wordlist_file, 'r') as f:
            for line in f:
                for ext in self.extensions:
                    url = f"{self.host}/{line.strip()}{ext}"
                    q.put(url)

        start = time.time()

        for i in range(self.threads):
            t = threading.Thread(target=dirbuster, args=(i, q))
            t.daemon = True
            t.start()

        q.join()

        self.output_file = self.create_output_file()
        with open(self.output_file, 'w') as f:
            for directory, status_code in found_directories:
                f.write("{} (Status code: {})\n".format(directory, status_code))

        print("Time taken: {}".format(time.time() - start))
        print("Found directories saved to: {}".format(self.output_file))

    def create_output_file(self):
        directory = os.path.join(os.path.dirname(__file__), 'reports', self.host)
        os.makedirs(directory, exist_ok=True)
        timestamp = time.strftime("%d-%m-%y_%H-%M-%S")
        return os.path.join(directory, f"{timestamp}.txt")

    def display_info(self):
        print("Undiscover")
        print(f"Extensions: {', '.join(self.extensions)} | HTTP method: {self.http_method} | Threads: {self.threads} | Wordlist size: {self.wordlist_size}")
        #print(f"Output File: {self.output_file}")
        print(f"Target: {self.host}")

if __name__ == "__main__":
    host = sys.argv[1]
    scanner = DirectoryScanner(host)

    # Ask user for the file extensions to search for
    extensions_str = input("Enter file extensions separated by commas (e.g., php,aspx,jsp,html,js,json,xml,sql,conf): ")
    extensions = ['.' + ext.strip() for ext in extensions_str.split(',')]
    scanner.set_extensions(extensions)

    # Set other parameters
    scanner.set_http_method('GET')

    # Ask user for the number of threads
    threads_input = input("Enter the number of threads (default is 25): ")
    if threads_input:
        scanner.set_threads(int(threads_input))
    else:
        scanner.set_threads(25)

    # Ask user for the directory wordlist file
    directory_wordlist_file = input("Enter the path to the directory wordlist file: ")
    scanner.set_directory_wordlist_file(directory_wordlist_file)

    # Ask user for desired status codes
    status_codes_str = input("Enter desired status codes separated by commas (e.g., 200,302,404): ")
    desired_status_codes = [int(code.strip()) for code in status_codes_str.split(',')]
    scanner.set_desired_status_codes(desired_status_codes)

    # Start scanning
    scanner.display_info()
    scanner.start_scan()
