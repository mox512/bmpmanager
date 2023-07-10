import requests

with open('JD.txt', 'r') as file:
    jd_text = file.read()

with open('CV.txt', 'r') as file:
    resume_text = file.read()

url = "https://resumeworded.com/upload-resume-to-server-rt.php"  # Replace with the actual URL
data = {
    'job_description_full_text': jd_text,
    'resume_full_text': resume_text
}

response = requests.post(url, data=data)
print(response)
