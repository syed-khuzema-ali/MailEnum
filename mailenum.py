#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import re
import urllib2
import argparse
import threading
import time
import json
import os
from urlparse import urlparse, urljoin
from Queue import Queue
from datetime import datetime

# ANSI color codes for hackers green
GREEN = '\033[92m'
RESET = '\033[0m'
BRIGHT_GREEN = '\033[1;92m'


class MailEnum:
    def __init__(self):
        self.banner = BRIGHT_GREEN + """
.·:''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.
: :                    _  _                                 : :
: :  _ __ ___    __ _ (_)| |  ___  _ __   _   _  _ __ ___   : :
: : | '_ ` _ \  / _` || || | / _ \| '_ \ | | | || '_ ` _ \  : :
: : | | | | | || (_| || || ||  __/| | | || |_| || | | | | | : :
: : |_| |_| |_| \__,_||_||_| \___||_| |_| \__,_||_| |_| |_| : :
'·:.........................................................:·'
""" + RESET
        
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.discovered_emails = set()
        self.visited_urls = set()
        self.lock = threading.Lock()
        self.queue = Queue()
        self.delay = 0
        self.quick_mode = False

    def print_colored(self, text):
        """Print text in bright hackers green"""
        print(BRIGHT_GREEN + text + RESET)

    def crawl_page(self, url, base_url):
	    try:
	        if self.delay > 0:
	            time.sleep(self.delay)
	            
	        headers = {'User-Agent': 'Mozilla/5.0 (MailEnum v1.0)'}
	        req = urllib2.Request(url, headers=headers)
	        response = urllib2.urlopen(req, timeout=10)
	        content = response.read()
	        
	        # Extract emails
	        emails = re.findall(self.email_pattern, content)
	        
	        with self.lock:
	            for email in emails:
	                if email not in self.discovered_emails:
	                    self.discovered_emails.add(email)
	                    self.print_colored("[+] Found email: {}".format(email))
	        
	        # Extract links for further crawling (if not in quick mode or quick mode is enabled)
	        if not self.quick_mode or (self.quick_mode and len(self.visited_urls) < 20):
	            links = re.findall(r'href=["\'](.*?)["\']', content)
	            for link in links:
	                full_url = urljoin(url, link)
	                parsed = urlparse(full_url)
	                
	                # Skip non-HTTP/HTTPS URLs and common non-web links
	                if not full_url.startswith(('http://', 'https://')):
	                    continue
	                
	                # Skip specific non-web protocols
	                if full_url.startswith(('mailto:', 'tel:', 'javascript:', 'ftp:', 'file:')):
	                    continue
	                
	                # Skip URLs with fragments (#) that point to same page
	                if '#' in full_url:
	                    full_url = full_url.split('#')[0]
	                
	                # Skip empty URLs
	                if not full_url or full_url == '#':
	                    continue
	                
	                # Only crawl links from the same domain
	                if parsed.netloc == urlparse(base_url).netloc:
	                    if full_url not in self.visited_urls:
	                        self.visited_urls.add(full_url)
	                        self.queue.put(full_url)
	                        
	    except Exception as e:
	        with self.lock:
	            if '404' in str(e) or 'Not Found' in str(e):
	                # Silently skip 404 errors to reduce noise
	                pass
	            else:
	                print("[-] Error crawling {}: {}".format(url, str(e)))

    def worker(self, base_url):
        """Worker thread function"""
        while True:
            try:
                url = self.queue.get(timeout=5)
                self.crawl_page(url, base_url)
                self.queue.task_done()
            except:
                break

    def start_crawling(self, url, threads):
        """Start the crawling process with multiple threads"""
        self.print_colored("\n[+] Starting email enumeration on: {}".format(url))
        self.print_colored("[+] Using {} threads".format(threads))
        self.print_colored("[+] Quick mode: {}".format('Enabled' if self.quick_mode else 'Disabled'))
        if self.delay > 0:
            self.print_colored("[+] Delay between requests: {} seconds".format(self.delay))
        self.print_colored("=" * 40)
        
        # Start with the base URL
        self.queue.put(url)
        self.visited_urls.add(url)
        
        # Start worker threads
        for _ in range(threads):
            t = threading.Thread(target=self.worker, args=(url,))
            t.daemon = True
            t.start()
        
        # Wait for queue to be processed
        self.queue.join()
        
        return self.discovered_emails

    def save_results(self, emails, output_file):
        """Save results to file"""
        if output_file:
            if output_file.endswith('.json'):
                with open(output_file, 'w') as f:
                    json.dump(list(emails), f, indent=4)
                self.print_colored("\n[+] Results saved to {} (JSON format)".format(output_file))
            else:
                with open(output_file, 'w') as f:
                    for email in emails:
                        f.write(email + '\n')
                self.print_colored("\n[+] Results saved to {} (TXT format)".format(output_file))

    def print_summary(self, emails, start_time):
        """Print summary of the enumeration"""
        elapsed_time = time.time() - start_time
        self.print_colored("\n" + "="*60)
        self.print_colored("ENUMERATION SUMMARY")
        self.print_colored("="*60)
        self.print_colored("Total emails found: {}".format(len(emails)))
        self.print_colored("Total URLs crawled: {}".format(len(self.visited_urls)))
        self.print_colored("Time elapsed: {:.2f} seconds".format(elapsed_time))
        
        if emails:
            self.print_colored("\nDiscovered emails:")
            for email in sorted(emails):
                print(BRIGHT_GREEN + "  • {}".format(email) + RESET)

def main():
    tool = MailEnum()
    
    # Print banner
    print(tool.banner)
    
    parser = argparse.ArgumentParser(
        description='MailEnum - Email Enumeration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  %(prog)s -u https://example.com
  %(prog)s -u https://example.com -t 20 -o results.txt
  %(prog)s -u https://example.com -q -o emails.json
  %(prog)s -u https://example.com -d 0.5 -t 5
        '''
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target website URL (required)')
    parser.add_argument('-o', '--output', help='Output file (JSON or TXT)')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay between requests in seconds')
    parser.add_argument('-q', '--quick', action='store_true', help='Quick crawl (limit pages)')
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Set tool parameters
    tool.delay = args.delay
    tool.quick_mode = args.quick
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'http://' + args.url
    
    # Start enumeration
    start_time = time.time()
    emails = tool.start_crawling(args.url, args.threads)
    
    # Save results if output file specified
    tool.save_results(emails, args.output)
    
    # Print summary
    tool.print_summary(emails, start_time)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(BRIGHT_GREEN + "\n\n[!] Interrupted by user. Exiting..." + RESET)
        sys.exit(0)
    except Exception as e:
        print(BRIGHT_GREEN + "\n[!] Error: {}".format(str(e)) + RESET)
        sys.exit(1)