#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
top_10_url = "https://owasp.org/www-project-top-ten/"
driver.get(top_10_url)

body = driver.find_element(By.CSS_SELECTOR,'body')
if body:
    list_result = body.find_element(By.CSS_SELECTOR,'h2[id="top-10-web-application-security-risks"]')
    item_list = list_result.find_elements(By.XPATH,'following-sibling::ul[1]/li')

    top_10_data = []
    for item in item_list:
        risk = item.text.strip()
        link = item.find_element(By.TAG_NAME,'a').get_attribute('href')
        top_10_data.append({"Risk": risk, "Link": link})

driver.quit()

df = pd.DataFrame(top_10_data)
df.to_csv("owasp_top_10.csv", index=False, encoding="utf-8")
print(df)

# %%
## challenges.txt

challenge_text = """I faced a challenge in this task when it came to finding the correct tags and navigating through them. 
The HTML structure can sometimes be complicated if it doesn’t behave as expected. 
However, I still find it interesting to learn how to do web scraping.
"""
with open("challenges.txt", "w", encoding="utf-8") as f:
    f.write(challenge_text)
    
# %%
