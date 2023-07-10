import openai
import subprocess

def beep(frequency=1000, duration=500):
    cmd = f'play -n synth {duration / 1000} sin {frequency} vol 0.5'
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

with open('openai.key','r') as key_file:
    openai.api_key=key_file.read().strip()

def fast_response(myprompt):
    beep(300, 250)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": myprompt}])

    # print("--vv Fast prompt    vv--")
    # print(prompt)
    # print("--^^ Fast prompt ^^--")
    # print("--vv Fast response vv--")
    # print("->>",response.choices[0].text.strip(),"<<-")
    # print("--^^ Fast response ^^--")
    return chat_completion.choices[0].message.content


#JDdoc = pyperclip.paste()
with open('JD.txt', 'r') as file:
    JDdoc = file.read()
JD = f"<Job description START>{JDdoc}<Job description END>"
# print(JD)

with open('TE.txt','r') as file:
    TEdoc = file.read()
#with open('TE.txt', 'w') as file:
#    pass

with open('CV.txt', 'r') as file:
    CVdoc = file.read()
CV = f"<Resume START>{CVdoc}<Resume END>"
# print(CV)

prompt = f"""
    Imagine you are an AI-based hiring manager.
    Helping me to improve matching to the a provided job description {JD}
    Please identify expertise areas in job description that are not covered in my resume: {CV}
    Address these gaps with new 5 action-oriented detail focused bullet point in past tense. 
    Length of the bullet points should be no more than 200 character long.
    Plain text,no formatting.
"""
print('_________________________')
print('TE:', TEdoc)
print('JD:', JDdoc)

resp_txt = fast_response(prompt)
print('vvv---- Start ----vvv')
print(resp_txt)
print('^^^----  End  ----^^^')

#pyperclip.copy(resp_txt)

beep(300, 350)
beep(300, 350)
beep(300, 350)
