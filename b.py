import openai
import subprocess
from docx import Document

def save_as_docx(text, output_file):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file)

def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def generate_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=1,
    )
    #print("+RRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    #print(response)  # Print the full response object for troubleshooting
    #print("-RRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    return response.choices[0].text.strip()

with open('openai.key','r') as key_file:
    openai.api_key=key_file.read().strip()
#JDdoc=pyperclip.paste()
with open('JD.txt', 'r') as file:
    JDdoc = file.read()
JD = f"<<<JD START>>>{JDdoc}<<<JD END>>>"
#print(JD)

with open('CV.txt', 'r') as file:
    CVdoc = file.read()
CV = f"<<<CV START>>>{CVdoc}<<<CV END>>>"
#print(CV)

beep(500,250)
prompt = "Write the cover letter based on CV and the JD. Please avoid senstenses longer than 230 symbols."+JD+CV
#print(prompt)
print('-Sending request to ChatGPT-')
resultCV = generate_completion(prompt)
#print(result)
beep(500,250)
with open("Cover_letter.txt", "w") as file:
    file.write(resultCV)

save_as_docx(resultCV,"Cover_letter.docx")

print('=File saved=')

