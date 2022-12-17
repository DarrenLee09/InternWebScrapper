import requests
from bs4 import BeautifulSoup
import pyodbc

# URL to scrape from
URL = "https://realpython.github.io/fake-jobs/" 
# stores the HTML data retrieved from the URL
page = requests.get(URL)

# # prints the HTML data (HTML file contents)
# print(page.text)

#page.content is the HTML file contents stored in "page", and "html.parser" is the parser used to parse the HTML file
soup = BeautifulSoup(page.content, "html.parser")

# finds and stores the HTML contents of element with id "ResultsContainer" (HOW TO SCRAPE VIA IDS)
results = soup.find(id="ResultsContainer") 

# # prettify formats the HTML contents conveniently
# print(results.prettify())

# finds and stores the HTML contents of all elements in div tags with class "card-content" (how each job is stored on the page) - returns iterable (HOW TO SCRAPE VIA CLASSES)
job_elements = results.find_all("div", class_="card-content") 


for job_element in job_elements:
    title_element = job_element.find("h2", class_="title") # finds the first instance of an h2 tag with class "title" - returns HTML contents
    company_element = job_element.find("h3", class_="company") # finds the first instance of an h3 tag with class "company" - returns HTML contents
    location_element = job_element.find("p", class_="location") # finds the first instance of a p tag with class "location" - returns HTML contents
    print(title_element.text.strip()) # .text prints the text of the HTML contents, .strip() removes whitespace
    print(company_element.text.strip()) # .text prints the text of the HTML contents, .strip() removes whitespace
    print(location_element.text.strip()) # .text prints the text of the HTML contents, .strip() removes whitespace
    print()

# finds all instances of h2 tags with string "Python" (h2 tags on the page are job titles), string attribute is case sensitive - returns iterable
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

# print(python_jobs)

# print(len(python_jobs))

# how to access parent elements (in this case because the job details are not contained in the h2 tag, but in the parent elements of the h2 tag)
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

for job_element in python_job_elements:
    links = job_element.find_all("a") # finds all instances of anchor tags in the job element
    for link in links:
        link_url = link["href"] # accesses the href attribute of the link (HOW TO ACCESS ATTRIBUTES OF TAGS)
        print(f"Apply here: {link_url}\n")


#SQL Stuff Templates
# Replace with your own database connection string
connection_string = "DRIVER={SQL Server};SERVER=<server-name>;DATABASE=<database-name>;UID=<username>;PWD=<password>"

# Connect to the database using the connection string
conn = pyodbc.connect(connection_string)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Use the cursor to execute a SQL query to create a table
cursor.execute("CREATE TABLE jobs (title VARCHAR(255), company VARCHAR(255), location VARCHAR(255))")

# Use the cursor to execute a SQL query to insert data into the table
cursor.execute("INSERT INTO jobs (title, company, location) VALUES (?, ?, ?)", (title, company, location))

# Use the cursor to execute a SQL query to commit the data to the database
cursor.commit()