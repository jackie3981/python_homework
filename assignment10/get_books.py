#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time

def extract_page_results(driver):
    """Extract book results from the current page"""
    results = []
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    list_result = body.find_element(By.CSS_SELECTOR, 'section.results-list.row')

    item_list = list_result.find_elements(By.CSS_SELECTOR, 'li.row.cp-search-result-item')
    print(f"Found {len(item_list)} results on this page")

    for item in item_list:
        # Title
        title_element = item.find_element(By.CSS_SELECTOR, 'h2.cp-title span.title-content')
        title_text = title_element.text.strip()

        # Authors (can be multiple)
        author_elements = item.find_elements(By.CSS_SELECTOR, 'span.cp-author-link')
        author_names = [a.text.strip() for a in author_elements]
        authors_str = "; ".join(author_names)

        # Format and year
        format_year_element = item.find_element(By.CSS_SELECTOR, 'span.display-info-primary')
        format_year_text = format_year_element.text.strip()

        # Create dict for this book
        book_dict = {
            "Title": title_text,
            "Author": authors_str,
            "Format-Year": format_year_text
        }

        results.append(book_dict)

    return results

def scrape_all_pages(driver, url):
    """Scrape all pages starting from the given URL"""
    driver.get(url)
    all_results = []

    while True:
        # Extract results from current page
        page_results = extract_page_results(driver)
        all_results.extend(page_results)

        # Finding "Next" button
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        next_buttons = body.find_elements(By.CSS_SELECTOR, 'li.cp-pagination-item.pagination__next-chevron a')

        if next_buttons:
            next_buttons[0].click()
            time.sleep(2)  
        else:
            break 

    return all_results


driver = webdriver.Chrome()
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

results = scrape_all_pages(driver, url)

driver.quit()

# Create DataFrame
df = pd.DataFrame(results)
print(df)

# Save results
with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

df.to_csv("get_books.csv", index=False, encoding="utf-8")
# %%
