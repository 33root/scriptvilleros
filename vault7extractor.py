from bs4 import BeautifulSoup
import requests
from IPython import embed


base_url = "https://wikileaks.org/vault7/document/"

req = requests.get(base_url)
if req.status_code != 200:
    print "fail forever fail BSOD bye xoxo"
else:
    soup = BeautifulSoup(req.content, "html.parser")
    divs_docs = soup.find_all("div", {"class": "document-col"})
    docs_urls = []
    docs_reports = []
    report = {}

    for div in divs_docs:
        docs_urls.append(div.find_all("a"))

    for doc in docs_urls:
        if doc != []:
            doc_leaked = requests.get(
                base_url + str(doc[0].attrs['href'].replace("../document/", "")))

        # print base_url + str(doc[0].attrs['href'].replace("../document/",
        # ""))

            if doc_leaked.status_code == 200:
                doc_soup = BeautifulSoup(doc_leaked.content, "html.parser")
                sidebar = doc_soup.find("div", {"class": "sidebar-section"})
                if not sidebar:
                    continue
                name = str(sidebar.find("a")["href"]).split("/")[4]

                report[name] = {}
                report[name]["docs_urls"] = []

                for doc_url in sidebar.find_all("a"):
                    report[name]["docs_urls"].append(str(doc_url["href"]).replace(
                        "../../document/", ""))

                report[name]["docs_urls"] = list(
                    set(map(str, report[name]["docs_urls"])))
                
                for doc_pdf in report[name]["docs_urls"]:
                    leak_file = requests.get(base_url + doc_pdf)
                    if leak_file.status_code == 200:
                        f = open(name, "w+")
                        f.write(leak_file.content)
                        f.close()
                    else:
                        print "no funco: " + base_url + doc_pdf
