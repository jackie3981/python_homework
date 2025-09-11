#%% Task 1: Review robots.txt to Ensure Policy Compliance
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

robots_url = "https://durhamcountylibrary.org/robots.txt"
driver.get(robots_url)
print(driver.page_source)
driver.quit()

# %% Task 2: Understanding HTML and the DOM for the Durham Library Site
driver = webdriver.Chrome()
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

# Initialize lists to store all authors and titles
titles = []
authors = []
formats = []
years = []

body = driver.find_element(By.CSS_SELECTOR,'body')
if body:
    list_result = body.find_element(By.CSS_SELECTOR,'section.results-list.row')

    item_list = list_result.find_elements(By.CSS_SELECTOR,'li')
    for item in item_list:
        # Title
        title = item.find_element(By.CSS_SELECTOR,'h2.cp-title span.title-content')
        print(f"title: {title.text}")
        titles.append(title.text)
        
        # Authors (handle multiple)
        author_elements = item.find_elements(By.CSS_SELECTOR,'span.cp-author-link')
        author_names = [a.text for a in author_elements]  # list of author names
        author_str = ', '.join(author_names)              # join as single string if needed
        print(f"author: {author_str}")
        authors.append(author_str)

        # format and year
        format_year = item.find_element(By.CSS_SELECTOR,'span.display-info-primary')
        format_year_text = format_year.text.strip()
        parts = format_year_text.split(',')
        book_format = parts[0].strip()
        year = parts[1].strip() if len(parts) > 1 else ""
        print(f"format and year: {format_year.text}")
        formats.append(format_year.text)
        print('---')

driver.quit()

# %%
