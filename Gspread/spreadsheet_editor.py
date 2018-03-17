import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import os

os.chdir(os.path.dirname(__file__))
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
printer = pprint.PrettyPrinter()

sheet = client.open('vocab').sheet1
# printer.pprint(records)
# printer.pprint(sheet.row_values(1))
# printer.pprint(sheet.col_values(1))
row = ["Temperate", "A trait of someone who can moderate his/her behaviors"]
sheet.delete_row(1)
