from flask import Flask, render_template, url_for, request
import sys
from Python import _Web3
app = Flask(__name__)


_defaultAccount = _Web3.getDefaultAccount()
account = _Web3.getAccounts()

def getMessages(x):
    if x == 1:
        Messages = _Web3.getInbox(_defaultAccount)
    else:
        Messages = _Web3.getOutbox(_defaultAccount)
    return Messages

@app.route('/', methods = ['POST', 'GET'])
def home():
    global _defaultAccount
    Messages = getMessages(1)
    NewMail = 1
    inbox= 2
    outbox = 3
    Page = 2
    msg = ''


    if request.method == 'POST':

        if request.form['InboxButtons'] == 'newMail':

            Page = NewMail
        elif request.form['InboxButtons'] == 'inbox':

            Page = inbox
            Messages = getMessages(1)


        elif request.form['InboxButtons'] == 'outbox':

            Page = outbox
            Messages = getMessages(2)


        elif request.form['InboxButtons'] == 'send':
            to = request.form.get('to')
            title = request.form.get('title')
            message= request.form.get('content')
            sender = _defaultAccount
            Page = NewMail
            msg = _Web3.sendMail(to, sender, title, message)

        for acc in account:
            if request.form['InboxButtons'] == acc:
                _defaultAccount = acc
                if Page == 2:
                    Messages = getMessages(1)

                break
        return render_template('index.html', page=Page, msgs = Messages, mailMessage = msg, defaultAccount = _defaultAccount, accounts = account)
    return render_template('index.html', page=Page, msgs = Messages, accounts = account, mailMessage = msg, defaultAccount = _defaultAccount)


if __name__ == '__main__':
    app.debug = True
    app.run()
