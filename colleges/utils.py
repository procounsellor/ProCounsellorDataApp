# colleges/utils.py
import os
import sys
import django
import json
from openai import OpenAI
from django.conf import settings
import re


# Setup Django and system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "procounsel.settings")
django.setup()
from colleges.models import EnggCollegeInfo

# Setup OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def fetch_college_info_from_gpt(college_name: str) -> dict:
    prompt = f'''
    You are an expert in Indian higher education data.

    Your task is to return structured, accurate and up-to-date informIITation about the college named "{college_name}". Fetch the latest data from official and authoritative sources only — including NIRF 2024, official college websites, Shiksha, Careers360, or recent verified news articles.

    ### Important Instructions:
    - Respond strictly in **valid JSON** format.
    - **Do not hallucinate or guess data**. Always rely on verified sources.
    - Ensure `"nirf_rank"` is strictly from **NIRF 2024 Engineering category only**. Do not use ranks from previous years.
    - For the following fields, if current (2024) data is not available, you MUST use the **most recent verified historical data (2023 or earlier)**. **Do NOT leave them blank or return "NA" under any circumstances**:
    - `"description"`
    - `"accreditation"`
    - `"infrastructure"`
    - `"hostel_facility"`
    - `"courses_offered"`
    - `"fee_per_year"`
    - `"total_fee"`
    - For placement fields (`avg_placement`, `highest_placement`, `top_recruiters`), use only the **latest available data from the 2023–24 placement season**.
    - Fees should be sourced from official college websites or reliable education platforms (e.g., Shiksha, Careers360, Collegedunia).
    - The "description" field must be a clean, fact-based paragraph in plain English between 200 and 250 words. Avoid any special formatting or citation markers..
    - For `"courses_offered"`, return **all undergraduate (UG) engineering courses offered** by the college. If seat data is not available, use `"NA"` for `"seats"`, but do not skip the course name.
    - Do not skip any fields unless absolutely no data exists across any verified source, including historical ones.
    - Maintain consistent format and naming across all outputs.

    ### Fields to return (strictly in JSON format):

    {{
    "nirf_rank": "NIRF Engineering rank of the college for the year 2024. If the college is not listed in the 2024 rankings, return 'NA'.",
    "avg_placement": "Average placement package in LPA",
    "highest_placement": "Highest placement package in LPA",
    "top_recruiters": ["List of top recruiting companies"],
    "fee_per_year": "Fees per year for B.Tech (in INR)",
    "total_fee": "Total fees for the full B.Tech program (in INR)",
    "courses_offered": [
        {{
        "name": "Name of UG course",
        "seats": "Number of seats"
        }}
    ],
    "location": {{
        "city": "City name",
        "state": "State name"
    }},
    "infrastructure": "Brief summary of campus and facilities (1-2 sentences)",
    "hostel_facility": "Availability of hostels (Yes/No + brief details)",
    "scholarships": "Types of scholarships offered",
    "accreditation": {{
        "naac": "NAAC Grade (e.g., A+)",
        "nba": "Yes/No"
    }},
    "college_type": "Government / Private / Deemed / Autonomous",
    "established_year": "Year in which the college was established",
    "description": "Brief overview of the college in 200-250 words"
    }}
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Could not parse GPT response", "raw": content}


# Run as standalone script
if __name__ == "__main__":
    college_name = input("Enter college name: ").strip()
    data = fetch_college_info_from_gpt(college_name)

    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Save to DB
    from colleges.models import EnggCollegeInfo
    college_obj, created = EnggCollegeInfo.objects.update_or_create(
        name=college_name,
        defaults={'data': data}
    )

    if created:
        print(f"✅ Created new entry for '{college_name}' in the database.")
    else:
        print(f"✅ Updated existing entry for '{college_name}' in the database.")

