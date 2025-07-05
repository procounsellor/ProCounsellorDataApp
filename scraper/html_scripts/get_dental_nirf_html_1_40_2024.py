from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path

# Always resolve from script location
data_file = Path(__file__).parent.parent / "html_data"/"get_dental_nirf_ranking_1_40_2024.html"
driver = webdriver.Chrome()
driver.get("https://www.nirfindia.org/Rankings/2024/DentalRanking.html")

soup = BeautifulSoup(driver.page_source, 'html.parser')

with open(data_file, 'w') as f:
    f.write(soup.prettify())
print(data_file)
driver.quit()