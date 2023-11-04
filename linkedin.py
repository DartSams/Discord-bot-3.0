from bs4 import BeautifulSoup
import requests


###TIP
#when scraping and getting html classes do in incognito browser html is different when signed in on browser


def extract(job_name,location_type="hybrid",location="United States"):
    job_name = job_name.replace(" ","%20") #needed because in parsing spaces are treated as %20
    if location_type == "remote":
        num = 2 #linkedin query for remote jobs
    elif location_type == "onsite":
        num = 1 #linkedin query for on site jobs
    elif location_type == "hybrid":
        num = 3 #linkedin query for hybrid jobs
    url=rf'https://www.linkedin.com/jobs/search/?keywords={job_name}&location={location}&f_TPR=&f_WT={num}&refresh=true&position=1&pageNum=0'
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    return soup


def transform(soup):
    jobs = [] #list to hold all job objects
    # lst = soup.find_all("ul",class_="jobs-search__results-list")
    # print(len(lst))
    link_objects = soup.find_all("a",class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
    links = [i.get("href") for i in link_objects]
    title_objects = soup.find_all("h3",class_="base-search-card__title")
    title = [i.text.strip() for i in title_objects]
    # print(title)
    company_objects = soup.find_all("h4",class_="base-search-card__subtitle")
    company = [i.text.strip() for i in company_objects]
    location_objects = soup.find_all("span",class_="job-search-card__location")
    location = [i.text.strip() for i in location_objects]
    time_objects = soup.find_all("time",class_="job-search-card__listdate")
    posted_ago = [i.text.strip() for i in time_objects]
    # print(len(posted_ago))
    # print(len(link_objects))


    for index,i in enumerate(link_objects):
        data = {
            "link":links[index],
            # "title":title[index],
            # "company":company[index],
            # "location":location[index],
            # "post date":posted_ago[index]
        }

        if len(title_objects) == len(link_objects):
            data["title"] = title[index]
        if len(company_objects) == len(link_objects):
            data["company"] = company[index]
        if len(location_objects) == len(link_objects):
            data["location"] = location[index]
        if len(time_objects) == len(link_objects):
            data["post date"] = posted_ago[index]

        #if statements are needed because some postings dont all have the same data Ex. not all postings have a due date



        # print(data)
        jobs.append(data)
    return jobs

# transform(extract())
