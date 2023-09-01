import openai
import subprocess
from docx import Document
import datetime
import sqlite3

# Check if there's at least one argument passed
def save_as_docx(text, output_file):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file)

def createfilename(text):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return text.translate(tr).replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_").replace(":", "_")

def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def fast_response(myprompt):
    beep(300, 250)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[
                                                       {"role": "user", "content": myprompt}
                                                   ],
                                                   temperature=0.9
                                                   )
    return chat_completion.choices[0].message.content
    #print("+RRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    #print(response)  # Print the full response object for troubleshooting
    #print("-RRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    return response.choices[0].text.strip()


conn = sqlite3.connect('log.db')
sqlcc = conn.cursor()
with open('run_id.txt', 'r') as file:
    run_id = int(file.read())
company_name="_"
#print(f"-= Received Run_id: {run_id} =-")

sqlcc.execute("SELECT * FROM run WHERE id = ?", (run_id,))
rows = sqlcc.fetchall()
company_name=rows[0][4]
if rows and len(rows[0]) > 4:
    company_name = rows[0][4]
else:
    print("! No suitable run record found.")
print(' -= Company Name:', company_name,' =-')

with open('openai.key','r') as key_file:
    openai.api_key=key_file.read().strip()

### Should be replaced to DB querry in future
with open('JD.txt', 'r') as file:
    JDdoc = file.read()
JD = f"<<<JD START>>>{JDdoc}<<<JD END>>>"
### Should be replaced to DB querry in future
with open('CV.txt', 'r') as file:
    CVdoc = file.read()
CV = f"<<<CV START>>>{CVdoc}<<<CV END>>>"

beep(500,250)
prompt = "Write the cover letter based on CV and the JD. Please avoid senstenses longer than 230 symbols."+JD+CV
#print(prompt)
resultCL = fast_response(prompt)
#print(result)
beep(500,250)
current_time = datetime.datetime.now()
filename=createfilename('CL_'+company_name+"_"+current_time.strftime("_%H_%M%S"))
with open(filename+".txt", "w") as file:
    file.write(resultCL)

save_as_docx(resultCL,filename+".docx")

sqlcc.execute("UPDATE run SET cl = ? WHERE id = ?", (resultCL, run_id))
conn.commit()
conn.close()

print('-= Cover Letter saved =-')

