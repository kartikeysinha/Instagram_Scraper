from selenium import webdriver
import time
import sys
import pandas as pd
from pandas import ExcelWriter
import os.path

driver = webdriver.Chrome()

#get the website URL as a command line argument
driver.get(sys.argv[1])
time.sleep(3)

#if user not logined
try:
    close_button = driver.find_element_by_class_name('xqRnw')
    close_button.click()
except:
    pass

#scroll through the comments of a post and click 'load more' as specified by command line argument
try:
    load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
    print("Found {}".format(str(load_more_comment)))
    i = 0
    while load_more_comment.is_displayed() and i < int(sys.argv[2]):
        load_more_comment.click()
        time.sleep(1.5)
        load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
        print("Found {}".format(str(load_more_comment)))
        i += 1
except Exception as e:
    print(e)
    pass

#Store all the username and comments in a list
user_names = []
user_comments = []
comment = driver.find_elements_by_class_name('gElp9 ')
for c in comment:
    container = c.find_element_by_class_name('C4VMK')
    name = container.find_element_by_class_name('_6lAjh').text
    content = container.find_element_by_tag_name('span').text
    content = content.replace('\n', ' ').strip().rstrip()
    user_names.append(name)
    user_comments.append(content)


#Export the list to a .csv file using excel_exporter
user_names.pop(0)
user_comments.pop(0)
fname = 'comments.xlsx'
temp = {}
temp_names = []
temp_comments = []
if os.path.isfile(fname):
    saved = pd.read_excel(fname)
    temp_names.extend(saved['name'])
    temp_comments.extend(saved['comment'])
temp_names.extend(user_comments)
temp_comments.extend(user_comments)
temp.update({'name': temp_names, 'comment': temp_comments})
df = pd.DataFrame(temp)
writer = ExcelWriter(fname)
df.to_excel(writer, 'Kartikey Sinha', index=False)
writer.save()

driver.close()
