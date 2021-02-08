import requests
import os
import smtplib


def mail_it(msg):
    from0 = 'jaimin.mailbot@gmail.com'
    pw = 'Ffuzz4949@'
    to0 = 'bug.jaimin@gmail.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(from0, pw)
        smtp.sendmail(from0, to0, msg.encode('utf-8'))

url = input('Enter Site URL: ')

rq = requests.get(url)
data = str(rq.content)

splitedData = list(data.split(".s3"))

buckets = []
for i in range(len(splitedData)-1):
    temp = ''
    for j in range(len(splitedData[i])-1, -1, -1):

        if splitedData[i][j] != '/':
            temp = splitedData[i][j] + temp

        if splitedData[i][j] == '/':
            break
    if temp not in buckets:
        buckets.append(temp)

print(f'\n->> Total {len(buckets)} Buckets Found:')

for i in range(len(buckets)):
    if i != len(buckets)-1:
        print('-> ' + buckets[i] + ',')
    else:
        print('-> ' + buckets[i])

val_nonVul = {}
for i in range(len(buckets)):
    l = os.system(f'cmd /c "aws s3 ls s3://{buckets[i]} --no-sign-request"')

    if str(l) == '0':
        val_nonVul[buckets[i]] = 'Vulnerable'
    else:
        val_nonVul[buckets[i]] = 'Not Vulnerable'

body = ''
for i in range(len(val_nonVul)):
    body = body + buckets[i] + ' - ' + val_nonVul[buckets[i]] + '\n'

body = 'Site Name:\n' + url + '\n\n' + body
subject = 's3-information'
mail_it(f'Subject:{subject}\n\n{body}')
