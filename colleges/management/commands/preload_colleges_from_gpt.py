# colleges/management/commands/preload_colleges_from_gpt.py

from django.core.management.base import BaseCommand
from colleges.models import CollegeInfo
from colleges.utils import fetch_college_info_from_gpt
import pandas as pd
import time

class Command(BaseCommand):
    help = 'Preload college info using GPT'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('colleges.csv')  # Assume it has a 'name' column

        for index, row in df.iterrows():
            name = row['name']
            if CollegeInfo.objects.filter(name__iexact=name).exists():
                continue

            print(f"Fetching {name}...")
            data = fetch_college_info_from_gpt(name)
            CollegeInfo.objects.create(name=name, data=data)
            time.sleep(3)  # avoid hitting OpenAI rate limits
