import pyperclip

# def fast_response(myprompt):
#     beep(300, 250)
#     chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                                    messages=[
#                                                        {"role": "user", "content": myprompt}
#                                                    ],
#                                                    temperature=1
#                                                    )
#     return chat_completion.choices[0].message.content

#with open('openai.key','r') as key_file:
#    openai.api_key=key_file.read().strip()
#
#conn = sqlite3.connect('log.db')
#sqlcc = conn.cursor()

JDdoc = pyperclip.paste()
#JD = f"<Job description START>{JDdoc}<Job description END>"
# print(JD)

with open('JD.txt', 'w') as txt_file:
    txt_file.write(JDdoc)
print('-=Job decription saved=-')