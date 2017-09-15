from requests import Session, Request
from bs4 import BeautifulSoup
import time
import csv
'''
By Angelis Pseftis

'''
BASE_URL = 'https://nvd.nist.gov{}'
INDEX_URL = 'https://nvd.nist.gov/vuln/search/results?adv_search=false&form_type=basic&results_type=overview&search_type=all&query=DOS'


request_headers = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.8',
	'Connection': 'keep-alive',
	'Host': 'nvd.nist.gov',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}
session = Session()

csv_file = open('results.csv', "wt")
writer = csv.writer(csv_file, delimiter=',')    

url = INDEX_URL

# Loop over all the pages
while True:
	req = Request('GET', url, data={}, headers=request_headers)
	prepared_request = req.prepare()
	resp = session.send(prepared_request)

	html_soup = BeautifulSoup(resp.text, 'html.parser')
	results_table = html_soup.find('table', attrs={'data-testid': 'vuln-results-table'})
	table_body = results_table.tbody
	table_rows = table_body.find_all('tr')
	for row in table_rows:
		vuln_id = row.find('th').text.strip()
		summary = row.find_all('td')[0].text.strip()
		cvss_severity = row.find_all('td')[1].text.strip()

		# Write to CSV
		writer.writerow([vuln_id, summary, cvss_severity])
		
	next_page = html_soup.find('a', attrs={'aria-label':'Next Page'})
	if not next_page:
		break
	next_page_url = next_page['href']
	url = BASE_URL.format(next_page_url)
	time.sleep(5)

csv_file.close()
