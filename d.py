import openai
import pyperclip
import subprocess
import datetime
import json
from docx import Document
import sqlite3
import hashlib


def save_as_docx(text, output_file):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file)


def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def docx_to_txt(docx_path):
    document = Document(docx_path)
    text = ''
    for paragraph in document.paragraphs:
        text += paragraph.text + '\n'

    return text


def docx_replace(old_file, new_file, replacements):
    doc = Document(old_file)
    for paragraph in doc.paragraphs:
        if replacements:
            for key in replacements.keys():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, replacements[key])
    doc.save(new_file)

totalrate=0
def prep_rep(JD):
    global run_id
    replacements = {}
    reps = ["__rep1", "__rep2", "__rep3"]
    global totalrate
    for rep in reps:

        # repsa = []
        # with open(rep + '.txt', 'r') as ffile:
        #     for line in ffile:
        #         repsa[line] = 0
        reprate = 0
        repsa = set()
        with open(rep + '.txt', 'r') as f:
            for id, line in enumerate(f, start=1):
                # name = line.strip()  # Remove newline characters
                repsa.add((id, line, 0))

        # print('Repsa vvvvvv')
        # for item in repsa:
        #     print(item)
        # print('Repsa ^^^^^^')
        repsa_str = json.dumps(list(repsa))

        prompt = f"""
Imagine you are an AI-based hiring manager. Your task is to evaluate the relevance of various bullet points of a candidate's bullet points {repsa_str} against a provided job description {JD}. The bullet points is in the form of string representations of list, having fileds (id, name, score).
Score each bullet point on a scale from 1 to 10 based on how closely it matches with the job description. 
Return this data in the form of a JSON object where each key corresponds to the id in double quotes, and the value is the score you assigned.
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

        totalpoint = ''
        tuple_dict = {item[0]: item for item in repsa}
        ic = 0
        for key, value in sorted(data_dict.items(), key=lambda x: int(x[1]), reverse=True):
            pn = tuple_dict[int(key)][1]
            id_var = int(hashlib.md5(pn.encode()).hexdigest()[:15], 16)

            sqlcc.execute("SELECT id FROM bup WHERE id = ?", (id_var,))
            existing_id = sqlcc.fetchone()
            if existing_id is None:
                values = (id_var, pn, rep, run_id)
                sqlcc.execute("INSERT INTO bup (id, nm, em, run_id) VALUES (?, ?, ?, ?)", values)
                bup_id = sqlcc.lastrowid
                is_new="Y"
            else:
                bup_id = int(existing_id[0])
                is_new='N'

            ic += 1
            if ic <= 6:
                totalpoint = totalpoint + '- ' + pn
                #print('-A-', value, '<', id_var, '>', key, is_new,' ', pn, end='')
                decision = 1
                reprate+=value
            else:
                #print('-D-', value, '<', id_var, '>', key, is_new, ' ', pn, end='')
                decision = 0

            values = (value, decision, run_id, bup_id)
            sqlcc.execute("INSERT INTO sco (sc, de, run_id, bup_id) VALUES (?, ?, ?, ?)", values)


        print('^---',reprate,'----=|', rep, '                   |=-----------------^')
        replacements[rep] = totalpoint
        totalrate+=reprate
    print('^--',totalrate,'----=| Total                     |=-----------------^')
    return replacements


def fast_response(myprompt):
    beep(300, 250)
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

JDdoc = pyperclip.paste()
JD = f"<Job description START>{JDdoc}<Job description END>"
# print(JD)

with open('JD.txt', 'w') as txt_file:
    txt_file.write(JDdoc)

with open('CV.txt', 'r') as file:
    CVdoc = file.read()
CV = f"<Resume START>{CVdoc}<Resume END>"
# print(CV)

values = (JDdoc, CVdoc)
sqlcc.execute("INSERT INTO run (dt, jd, cv) VALUES (datetime('now'), ?, ?)", values)
run_id = sqlcc.lastrowid

replacements = prep_rep(JD)
# print('----V-----')
# print(replacements)
# print('----^-----')

current_time = datetime.datetime.now()
mfilename = "CV_"+str(totalrate)+"_"+current_time.strftime("_%H_%M%S")
old_file = "__cv.docx"
docx_replace(old_file, mfilename + ".docx", replacements)

docx_file_path = mfilename + ".docx"
txt_content = docx_to_txt(docx_file_path)
with open('CV.txt', 'w') as txt_file:
    txt_file.write(txt_content)
# with open(filename+".txt", "w") as file:
#    file.write(result)
# save_as_docx(result, filename + ".docx")

# pyperclip.copy(result)

conn.commit()
conn.close()

beep(400, 150)
beep(500, 150)
beep(300, 350)
print('<-----------=| All done: ' + mfilename + '.docx |=----------->')
