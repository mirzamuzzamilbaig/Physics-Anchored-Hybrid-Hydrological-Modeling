import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os

os.makedirs('papers', exist_ok=True)

def search_arxiv():
    print("=== Searching arXiv ===")
    query = 'all:"hydrology" OR all:"hydrological" AND all:"water management" AND (all:"basin" OR all:"river basin")'
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Python-Hydrology-Search/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        results = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', ns).text
            paper_id = entry.find('atom:id', ns).text
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
            pdf_url = ""
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('title') == 'pdf':
                    pdf_url = link.attrib.get('href')
                elif link.attrib.get('type') == 'application/pdf':
                    pdf_url = link.attrib.get('href')
            if not pdf_url and '/abs/' in paper_id:
                pdf_url = paper_id.replace('/abs/', '/pdf/') + '.pdf'
                
            results.append({
                'source': 'arXiv',
                'title': title,
                'published': published,
                'authors': authors,
                'id': paper_id,
                'pdf_url': pdf_url,
                'summary': summary
            })
        return results
    except Exception as e:
        print(f"arXiv search error: {e}")
        return []

def search_europe_pmc():
    print("=== Searching Europe PMC ===")
    query = '("hydrological" OR "hydrology") AND "water management" AND ("river basin" OR "large basin") OPEN_ACCESS:Y'
    url = f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(query)}&format=json&pageSize=10&sort=P_PD_DATE%20desc'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Python-Hydrology-Search/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        results = []
        result_list = data.get('resultList', {}).get('result', [])
        for item in result_list:
            title = item.get('title', '')
            pub_date = item.get('firstPublicationDate', item.get('pubYear', ''))
            doi = item.get('doi', '')
            pmcid = item.get('pmcid', '')
            authors = item.get('authorString', '')
            summary = item.get('abstractText', '')
            pdf_url = ""
            if pmcid:
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
            
            # Check fullTextUrl list if present
            ft_urls = item.get('fullTextUrlList', {}).get('fullTextUrl', [])
            for ft in ft_urls:
                if ft.get('documentStyle') == 'pdf':
                    pdf_url = ft.get('url')
                    break

            results.append({
                'source': 'Europe PMC',
                'title': title,
                'published': pub_date,
                'authors': authors,
                'doi': doi,
                'pmcid': pmcid,
                'pdf_url': pdf_url,
                'summary': summary
            })
        return results
    except Exception as e:
        print(f"Europe PMC search error: {e}")
        return []

def search_openalex():
    print("=== Searching OpenAlex ===")
    query = "hydrological water management large basin river basin"
    url = f'https://api.openalex.org/works?search={urllib.parse.quote(query)}&filter=is_oa:true,type:article&sort=publication_year:desc,cited_by_count:desc&per-page=10'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:user@example.com'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        results = []
        for item in data.get('results', []):
            title = item.get('display_name', '')
            pub_year = item.get('publication_year', '')
            pub_date = item.get('publication_date', str(pub_year))
            doi = item.get('doi', '')
            oa_location = item.get('best_oa_location') or item.get('primary_location') or {}
            pdf_url = oa_location.get('pdf_url') or oa_location.get('landing_page_url') or ""
            authorships = item.get('authorships', [])
            authors = [a.get('author', {}).get('display_name') for a in authorships if a.get('author')]
            
            results.append({
                'source': 'OpenAlex',
                'title': title,
                'published': pub_date,
                'authors': authors,
                'doi': doi,
                'pdf_url': pdf_url,
                'citations': item.get('cited_by_count', 0),
                'openalex_id': item.get('id')
            })
        return results
    except Exception as e:
        print(f"OpenAlex search error: {e}")
        return []

if __name__ == '__main__':
    arxiv_results = search_arxiv()
    pmc_results = search_europe_pmc()
    openalex_results = search_openalex()
    
    all_results = {
        'arxiv': arxiv_results,
        'europe_pmc': pmc_results,
        'openalex': openalex_results
    }
    
    with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print("Search complete. Results saved to search_results.json")
