import hh
import sj
from dotenv import load_dotenv
from utils import print_table


if __name__ == "__main__":
    load_dotenv()
    print_table(sj.get_stats(), 'SuperJob Moscow')
    print_table(hh.get_stats(), 'HeadHunter Moscow')
