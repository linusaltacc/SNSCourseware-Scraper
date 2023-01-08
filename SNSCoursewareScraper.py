import requests
from bs4 import BeautifulSoup
import re
import os

main_page = requests.get('http://www.snscourseware.org/')
soup = BeautifulSoup(main_page.text, 'html.parser')
clg = {'name':[],'links':[]}
for a in soup.find_all('a'):
    try:
        if a.get('href').startswith("http://www.snscourseware.org/"):
            clg['name'].append(a.get('href').split('http://www.snscourseware.org/')[1])
            clg['links'].append(a.get('href'))
    except:
        pass
for n in range(len(clg['name'])):
    print(f'{n}: ',clg['name'][n])
inp_clg_name = int(input())
clg_link = clg['links'][inp_clg_name]+'/'
index = requests.get(clg_link)
soup = BeautifulSoup(index.text, 'html.parser')
depts_name = soup.findAll(class_='green')
depts = []
for i in depts_name:
    depts.append(i.text)
for dept in range(len(depts)):
    print(f"{dept}: {depts[dept]}")
inp_dept = int(input())
dept_page = requests.get(f"{clg_link}/department.php?dept={depts[inp_dept]}")
soup = BeautifulSoup(dept_page.text, 'html.parser')
container = soup.find(class_='container')
p_element = container.find_all('p')[1]
a_elements = p_element.find_all('a')
sem_link = {"name":[],"link":[]}
for a in a_elements:
    sem_link['name'].append(a.text)
    sem_link['link'].append(a['href'])
for sem in sem_link['name']:
    print(f'{sem}')
inp_sem = int(input())
sem_page = requests.get(f"{clg_link}/department.php?sems={inp_sem}&dept={depts[inp_dept]}")
soup = BeautifulSoup(sem_page.text, 'html.parser')
stories_section = soup.find('div', {'class': 'stories-section'})
subject_links = {'name':[],'cw':[]}
for a in stories_section.find_all('a'):
    h4 = a.find('h4').text
    href = a['href']
    subject_links['name'].append(h4)
    match = re.search(r'cw=([^&]+)', href)
    if match:
        cw = match.group(1)
    subject_links['cw'].append(cw)
for sub_name in range(len(subject_links['name'])):
    print(f'{sub_name}:', subject_links['name'][sub_name])
inp_sub = int(input())
lecture_notes = requests.get(f"{clg_link}/notes.php?cw={subject_links['cw'][inp_sub]}")
soup = BeautifulSoup(lecture_notes.text, 'html.parser')
pdf_links = soup.find_all('a', href=lambda x: x and x.startswith('files/') and x.endswith('.pdf'))
notes_link = {'name':[],'link':[]}
if not os.path.exists('SNSCourseware/'+subject_links['name'][inp_sub]):
  os.makedirs('SNSCourseware/'+subject_links['name'][inp_sub]) # Create the folder if it doesn't exist
fnames = []
for fname in soup.findAll("div", {"id": "filetitile"}):
    fnames.append(fname.text.rstrip())
i = 0
for link in pdf_links: # Iterate through the list of PDF links
    response = requests.get(clg_link+ link['href'])
    filename = fnames[i]+'.pdf'
    i+=1
    if filename.find('/'):
        fname = ''
        fname = fname.join(filename.split('/'))
        filename=fname
    with open('SNSCourseware/'+subject_links['name'][inp_sub]+'/'+str(filename), 'wb') as f:
        print('SNSCourseware/'+subject_links['name'][inp_sub]+'/'+str(filename))
        f.write(response.content)
        print('Downloaded ',fnames[i-1]+'.pdf')
        f.close()