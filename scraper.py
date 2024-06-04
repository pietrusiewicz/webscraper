import asyncio
import httpx
from bs4 import BeautifulSoup

async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

async def parse_address(html):
    soup = BeautifulSoup(html, 'html.parser')
    addresses = soup.find_all('address')
    return addresses

async def parse_headers(html):
    soup = BeautifulSoup(html, 'html.parser')
    headers = [soup.find_all(f'h{i}') for i in range(1, 7)]
    return headers

async def parse_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    return links
    
async def parse_footer(html):
    soup = BeautifulSoup(html, 'html.parser')
    footer = soup.find('footer')
    return footer   
    
async def main(url):
    #url = "https://www.python.org"
    html = await fetch_html(url)


    tasks = [
        fetch_html(url),
        parse_address(html),
        parse_headers(html),
        parse_links(html),
        parse_footer(html)
    ]
    results = await asyncio.gather(*tasks)
    #return results
    #fetched_html, addresses, headers, links = await asyncio.gather(*tasks)
    return results
    """
    print("DANE ADRESOWE:")
    for address in addresses:
        print(address)

    print("NAGŁÓWKI:")
    for header in headers:
        print(header)

    print("ODNOSNIKI:")
    for link in links:
        print(link)
    """
    
if __name__ == "__main__":
    asyncio.run(main())

