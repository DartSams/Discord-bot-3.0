from dotenv import load_dotenv
import os


load_dotenv()

#psn api https://pypi.org/project/PSNAWP/
psn_data = {"npsso":os.getenv('npsso_api_key')}