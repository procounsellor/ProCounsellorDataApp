from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Always resolve from script location
data_file = Path(__file__).parent.parent / "html_data" / "get_college_nirf_ranking_1_100_2024.html"
save_to = Path(__file__).parent.parent / "data" / "nirf_college_1_100_2024.csv"

# Read the saved HTML file
with open(data_file, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

# Extract rows from the table
rows = soup.select("tbody tr")

data = []

for row in rows:
    # Only get top-level <td> (not nested ones)
    tds = row.find_all("td", recursive=False)
    if len(tds) < 6:
        continue

    # College name is the first direct text in tds[1]
    college_name = tds[1].find(text=True, recursive=False).strip()

    city = tds[2].get_text(strip=True)
    state = tds[3].get_text(strip=True)

    score_td = row.find("td", class_="dt-type-numeric sorting_1")
    rank_td = row.find_all("td", class_="dt-type-numeric")
    if not rank_td:
        # print(f"[WARN] Skipping row with no numeric td: {row}")
        continue
    rank_td = rank_td[-1]
    score = score_td.get_text(strip=True) if score_td else ""
    rank = rank_td.get_text(strip=True) if rank_td else ""

    data.append({
        "College Name": college_name,
        "City": city,
        "State": state,
        "Score": score,
        "Rank": rank
    })

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv(save_to, index=False)
# print("Data saved to nirf_engineering_2024.csv")
print(df.tail)
