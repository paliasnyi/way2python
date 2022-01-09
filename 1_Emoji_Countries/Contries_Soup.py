from bs4 import BeautifulSoup
import requests
import json


# Browsers User-Agent and Accept
HEADERS = {
              'Accept': 'Accept',
               'User-Agent': 'User-Agent'}



url = r'https://apps.timwhitlock.info/emoji/tables/iso3166'



# Download Page
def download_page(url, header):
    req = requests.get(url, headers=header)
    src = req.text
    with open(f'emoji_counties.html', "w", encoding='utf-8') as file:
        file.write(src)


# As a table is html type, we extract it from downloaded file
def get_table_tr():
    with open(f'emoji_counties.html', "r", encoding='utf-8') as file:
        src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        find_text = soup.find_all(class_='table table-bordered table-striped')
        find_tr = soup.find_all(name='tr')
        return find_tr


# Create dict with extracted data
def get_dict_data_from_table(table):
    my_list = []
    for data in range(1, len(table)):
        soup = table[data]
        country = soup.find_all('td')[-1].text.strip()
        abbreviation = soup.find_all('td')[0].text.strip()
        symbol = soup.span.text
        code = soup.a['title']
        my_list.append({'Country': country, 'Abbreviation': abbreviation, 'Symbol': symbol, 'Code': code})
    return my_list


# Save data to json file
def save_json(data):
    with open(f'emoji.json', "w", encoding='utf-8') as file:
        new_data = json.dumps(data, indent=4, ensure_ascii=False)
        file.writelines(new_data)




def main(url, header):
    page = download_page(url, header)
    tr = get_table_tr()
    data = get_dict_data_from_table(tr)
    save_json(data)


if __name__ == '__main__':
    main(url, HEADERS)
