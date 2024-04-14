import json
import csv
from datetime import datetime

def processJsonOutput():
    date_today = datetime.now().strftime('%Y%m%d')
    input_json_file = f'{date_today}.json'
    output_csv_file = f'{date_today}.csv'

    with open(input_json_file, 'r') as file:
        data = [json.loads(line) for line in file]

    base_headers = ['company name', 'company tagline', 'company link', 'product hunt link', 'company email 1', 'company email 2', 'company email 3', 'company social 1', 'company social 2', 'company social 3']
    team_member_headers = ['team member {} name', 'team member {} link 1', 'team member {} link 2', 'team member {} link 3', 'team member {} link 4']

    def create_headers(data):
        max_team_members = max(len(company['team']) for company in data)
        headers = base_headers.copy()
        for i in range(1, max_team_members + 1):
            headers.extend([header.format(i) for header in team_member_headers])
        return headers

    def process_company(company):
        row = [company.get('companyName', ''), company.get('companyTagline', ''), company.get('companyLink', ''), company.get('productHuntLink', ''), company.get('companyEmail1', ''), company.get('companyEmail2', ''), company.get('companyEmail3', ''), company.get('companySocial1', ''), company.get('companySocial2', ''), company.get('companySocial3', '')]
        for member in company['team']:
            row.extend([member.get('name', '')] + [member.get(f'link{i}', '') for i in range(1, 5)])
        return row

    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        headers = create_headers(data)
        writer.writerow(headers)
        
        for company in data:
            row = process_company(company)
            writer.writerow(row)

    print(f"CSV file '{output_csv_file}' created successfully.")

# processJsonOutput()