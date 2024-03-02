from pyvis.network import Network
from bs4 import BeautifulSoup
import json
import random
import tldextract
import bs4, requests
import requests

net = Network()

def extract_domain(url):
    extracted = tldextract.extract(url)
    subdomain = f"{extracted.subdomain}." if extracted.subdomain else ''  # Include subdomain if it exists
    return f"{subdomain}{extracted.domain}.{extracted.suffix}"



def get_all_links(url):
    # Send a GET request to the URL
    print("\n")
    print("Fetching links from:", url)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        all_links = [link.get('href') for link in links if link.get('href') and not link.get('href').startswith('#')]
        ban = open("ban.txt", "r+").readlines()
        ban = [x.strip() for x in ban]
        filtered_links = [link for link in all_links if not any(b in link for b in ban)]
        filtered_links = [extract_domain(link) for link in filtered_links]
        filtered_links = list(set(filtered_links))
        return filtered_links
    except:
        return []


counter = 1
host = 1
visited_links = set()

# Example usage:
print("\n\n-----------------------------------------------")

print("This is PageMap")
print("If you want to delete nodes with words like google, twitter, netlify etc. Please write them in ban.txt file.")
url = input("Insert full URL of your website (e.g., https://example.com): ")
visited_links.add(url)
url_name = url.split("//")[1]
net.add_node(url_name, label=url_name)

all_links_original = get_all_links(url)
print(all_links_original)

# Link all nodes to original
for link in all_links_original:
    net.add_node(link, label=link)
    net.add_edge(url_name, link)
    counter += 1

for link in all_links_original:
    url = "https://" + link
    visited_links.add(url)
    url_name = url.split("//")[1]
    net.add_node(url_name, label=url_name)

    all_links = get_all_links(url)

    # Link all nodes to original
    for link in all_links:
        net.add_node(link, label=link)
        net.add_edge(url_name, link)
        counter += 1

# Visualize the network
net.write_html('net.html')

print("-----------------Your network has been created-----------------")
print("Click on net.html file to view your creation.")
input("Press any key to exit.")
