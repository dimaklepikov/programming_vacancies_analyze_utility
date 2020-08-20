import os
import hh
import sj
from dotenv import load_dotenv
from utils import print_table, programming_languages


if __name__ == "__main__":
    load_dotenv()
    KEY = os.getenv('SJ_SECRET_KEY')
    table_content_sj = []
    table_content_hh = []
    for language in programming_languages:
        table_content_sj.append(sj.get_stats(language, KEY))
        table_content_hh.append(hh.get_stats(language))
    print_table(table_content_sj, 'Superjob Moscow')
    print_table(table_content_hh, 'HeadHunter Moscow')
