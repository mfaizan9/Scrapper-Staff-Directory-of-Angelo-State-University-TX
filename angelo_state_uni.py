import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
import string

Total_Data = []
profile_links = []
def get_data(url):
    r = requests.get(url).text
    s = BeautifulSoup(r , 'lxml')
    container = s.find('div', class_='container-fluid')
    # NAME
    try:
        fullname = container.find('h1').text.replace('"' , '').strip().split(' ')
        first_name = fullname[-2]
        last_name = fullname[-1]
    except:
        first_name = ''
        last_name = ''
    
    # JOB TITLE
    try:
        try:
            title = container.find('span', class_='profile-job-title').text.strip()
        except:
            title = container.find('span', class_='profile-primary-department').text.strip()
    except:
        title = ''
    # CONTACT
    contact_div = container.find('div', class_='profile-contact-info')
    ## EMAIL
    try:
        email = contact_div.find('dd').find('a').text.strip()
    except:
        email = ''
    
    data = {
        'First Name': first_name,
        'Last Name': last_name,
        'Job Title': title,
        'Email': email
    }
    Total_Data.append(data)
    return





def get(x):
    link = f'https://www.angelo.edu/directory/faculty_staff/?lname={x}'
    r = requests.get(link).text
    soup = BeautifulSoup(r , 'lxml')
    # main_div = soup.find('div' , {'id':'lw_widget_596deff8'})
    try:
        ul = soup.find('ul' , class_='lw_widget_results lw_widget_results_profiles')
        lis = ul.find_all('li')
        for li in lis:
            p_link = li.find('a')['href']
            path = ('https://www.angelo.edu'+p_link)
            profile_links.append(path)

    except:
        pass
    return

alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

print('Scrapping Begins !!!!!')
for i in alphabet_list:
    get(i)
# print(len(profile_links))


for i in profile_links:
    try:
        get_data(i)
    except:
        pass


print(len(Total_Data))

print('Scrapping DONE !!!!!!')


df = pd.DataFrame(Total_Data)
df.to_csv('angelo_state_uni.csv', index=False)

print('Data Stored to CSV')







