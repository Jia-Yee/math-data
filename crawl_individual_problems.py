import json
import os
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from playwright.sync_api import sync_playwright

def extract_problem_links(html_file):
    """
    Extract links to individual problem pages from the main Wikipedia page
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    
    # Focus on the main content area
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        print("Could not find main content area")
        return links
    
    # Find all links in list items, which is where the problems are typically listed
    list_items = content_div.find_all('li')
    print(f"Examining {len(list_items)} list items")
    
    # Look for mathematical problem links
    for i, li in enumerate(list_items[:100]):  # Check first 100 items
        links_in_li = li.find_all('a', href=True)
        for link in links_in_li:
            href = link['href']
            title = link.get('title', '')
            text = link.get_text().strip()
            
            # Check if it's a valid Wikipedia link to a mathematical problem
            if (any(keyword in href.lower() or keyword in title.lower() or keyword in text.lower() 
                    for keyword in ['conjecture', 'hypothesis', 'problem', 'theorem', 'prize']) and
                'wikipedia.org/wiki/' in href and
                not any(ex_keyword in href for ex_keyword in ['#cite', 'edit', 'redlink'])):
                
                # Convert to absolute URL if needed
                if href.startswith('/wiki/'):
                    full_url = urljoin('https://en.wikipedia.org', href)
                elif href.startswith('https://en.wikipedia.org/wiki/'):
                    full_url = href
                else:
                    continue  # Skip non-Wikipedia links
                    
                # Check if we already added this link
                if not any(existing_link['url'] == full_url for existing_link in links):
                    links.append({
                        'url': full_url,
                        'title': title,
                        'text': text
                    })
                    print(f"Added link {len(links)}: {full_url} - {text}")
    
    return links

def download_page(url, file_path, delay=2):
    """
    Download a single page using Playwright and save it to file
    """
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Set user agent to mimic a real browser
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })
            
            # Navigate to the page
            page.goto(url, timeout=30000)
            
            # Get page content
            content = page.content()
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Close browser
            browser.close()
        
        time.sleep(delay)  # Be respectful to the server
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        time.sleep(5)
        return False

def crawl_individual_problems():
    """
    Crawl individual problem pages
    """
    # Create directory for problem pages
    problems_dir = 'data/problems'
    os.makedirs(problems_dir, exist_ok=True)
    
    # Extract problem links from the main page
    main_page = 'data/List of unsolved problems in mathematics - Wikipedia.html'
    links = extract_problem_links(main_page)
    
    print(f"Found {len(links)} potential problem links")
    
    # Remove duplicates (just in case)
    unique_links = []
    seen_urls = set()
    for link in links:
        if link['url'] not in seen_urls:
            unique_links.append(link)
            seen_urls.add(link['url'])
    
    print(f"Found {len(unique_links)} unique problem links")
    
    # Download each problem page
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for link in tqdm(unique_links, desc="Downloading problem pages"):
        # Create a filename from the URL
        parsed_url = urlparse(link['url'])
        path = parsed_url.path
        filename = path.replace('/wiki/', '').replace('/', '_') + '.html'
        file_path = os.path.join(problems_dir, filename)
        
        # Check if file already exists
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            skipped_count += 1
            continue
        
        # Download the page
        if download_page(link['url'], file_path, delay=3):
            success_count += 1
        else:
            error_count += 1
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded: {success_count} pages")
    print(f"Skipped (already existed): {skipped_count} pages")
    print(f"Errors: {error_count} pages")

if __name__ == "__main__":
    crawl_individual_problems()