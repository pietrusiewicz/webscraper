import asyncio
import httpx
from bs4 import BeautifulSoup

"""async def fetch_html(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
"""
async def parse_cryptocom():
    url = "https://crypto.com/price"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html= response.text
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.findAll('tr', "css-1cxc880")
    namesprices = {_.find("div", "css-87yt5a").get_text(): _.find("div", "css-b1ilzc").get_text().strip(',')[1:].replace(",","") for _ in tabela}
    return namesprices

async def parse_gemini():
    url = "https://www.gemini.com/prices"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html= response.text
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.findAll('div', "sc-240d42a2-2 icmeJc")
    namesprices = {_.find("div", "sc-240d42a2-10 kCIdbM").get_text()[:-3]: 
    _.find("h2", "sc-240d42a2-11 cwAovh").get_text()[1:].replace(",","") for _ in tabela}
    items = list(namesprices.items())[:50]
    namesprices = dict(items)
    return namesprices
    
async def main():
    #url = "https://www.python.org"
    #html = await fetch_html(url)


    tasks = [
        parse_cryptocom(),
        parse_gemini(),
        #parse_headers(html),
        #parse_links(html),
        #parse_footer(html)
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

