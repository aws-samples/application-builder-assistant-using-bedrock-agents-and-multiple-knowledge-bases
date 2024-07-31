import xml.etree.ElementTree as ET

import json
import boto3
import requests
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

# fixes a bug with asyncio and jupyter
import nest_asyncio
nest_asyncio.apply()

kb_files_loc = "./kb_appbuilder/aws_best_practices_2/"


def extract_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap: {response.status_code}")
        return []

    sitemap_content = response.content
    root = ET.fromstring(sitemap_content)

    # Extract the URLs from the sitemap
    urls = [
        elem.text
        for elem in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    ]

    return urls


def load_html_text(sitemap_urls_html):
    loader = WebBaseLoader(sitemap_urls_html)
    #loader.requests_kwargs = {'verify':False}
    
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    documents = text_splitter.split_documents(data)

    doc_cntr = 0
    for document in documents:
        web_url = document.to_json()['kwargs']['metadata']['source']
        print(f"web_url ::: {web_url}")
        file_name_save = web_url.split("/")[-2] + "_" + str(doc_cntr) + "_" + web_url.split("/")[-1]
        file_name_save = file_name_save.replace(".html" , ".txt") # "KB does not support .json"
        #print(f"file_name to save ::: {file_name_save}")
        with open(kb_files_loc + file_name_save , "w") as writer:
            writer.write(json.dumps(document.to_json()['kwargs']))
        
        doc_cntr +=1

        print(f"Finished writing file ::::: {file_name_save}")



def get_texts_from_well_arch_framework():
    # Site maps for the AWS Well-Architected Framework
    sitemap_url_list = [
        "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/framework/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/sitemap.xml",
        "https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sitemap.xml",
    ]

    # Get all links from the sitemaps
    full_sitemap_list = []
    for sitemap in sitemap_url_list:
        full_sitemap_list.extend(extract_urls_from_sitemap(sitemap))

    print(f"full_sitemap_list >>>> {full_sitemap_list} \n\n")
    load_html_text(full_sitemap_list)



def get_aws_best_practices() -> None:
    """
    Purpose:
        Extracts AWS best practices from database
    Args:
        N/A
    Returns:
        N/A
    """

    # get the raw html text
    get_texts_from_well_arch_framework()
    
