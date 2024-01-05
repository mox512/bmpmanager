import openai
import subprocess
import datetime
import json
from docx import Document
import sqlite3
import hashlib
import sys

def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def docx_to_txt(docx_path):
    document = Document(docx_path)
    text = ''
    for paragraph in document.paragraphs:
        text += paragraph.text + '\n'

    return text


def fast_response(myprompt):
    beep(300, 250)     #"gpt-3.5-turbo"
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[
                                                       {"role": "user", "content": myprompt}
                                                   ],
                                                   temperature=1
                                                   )
    return chat_completion.choices[0].message.content

#____________________________________________________________________________________________________________
with open('openai.key','r') as key_file:
    openai.api_key=key_file.read().strip()

conn = sqlite3.connect('log.db')
sqlcc = conn.cursor()

with open('JD.txt', 'r') as file:
    JDdoc = file.read()

JD = f"<Job description START>{JDdoc}<Job description END>"
# print(JD)

old_file = "__cv.docx"
CVdoc = docx_to_txt(old_file)
with open('CV.txt', 'w') as file:
    file.write(CVdoc)

CV = f"<Resume START>{CVdoc}<Resume END>"
# print(CV)

prompt = f"""
Here is Job descirption {JD} Can you please look into it and return to me only JSON object with keys "company_name" "position_name"  containging company name, position name repsectively.
"""
resp_txt = fast_response(prompt)
try:
    data_dict = json.loads(resp_txt)
except json.JSONDecodeError as e:
    print("Failed to decode JSON: ", str(e))
    print("JSON:", resp_txt)
    beep(700, 450)
    beep(700, 450)
    beep(700, 450)
    exit(1)

for key, value in data_dict.items():
    if key == "company_name": company_name=value;
    if key == "position_name": position_name = value;

print(company_name,' | ',position_name)
print('________________________________________________________')

sqlcc.execute("SELECT * FROM run WHERE com LIKE ?", ('%' + company_name + '%',))
rows = sqlcc.fetchall()
requires_confirm_toproceed=0
for row in rows:
    if row[5] == position_name:
        beep(500, 350)
        beep(500, 350)
        utc_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        pst_time = utc_time - datetime.timedelta(hours=8)
        print("\033[91m", pst_time, row[4], row[5], "\033[0m")
        requires_confirm_toproceed = 1
    else:
        print('',row[1],row[4],row[5])

if requires_confirm_toproceed:
    input("Press Enter to continue, or Ctrl+C to abort!")

values = (JDdoc, CVdoc, company_name, position_name)
sqlcc.execute("INSERT INTO run (dt, jd, cv, com, pos) VALUES (datetime('now'), ?, ?, ?, ?)", values)
run_id = sqlcc.lastrowid
with open('run_id.txt', 'w') as txt_file:
    txt_file.write(str(run_id))

conn.commit()
conn.close()

beep(400, 150)
beep(500, 150)
beep(300, 350)
print('-= Data saved =-')