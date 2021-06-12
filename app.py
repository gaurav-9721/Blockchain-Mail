from flask import Flask, render_template, url_for, request
import sys
from Python import _Web3
app = Flask(__name__)


_defaultAccount = _Web3.getDefaultAccount()


@app.route('/', methods = ['POST', 'GET'])
def home():
    global _defaultAccount

    NewMail = 1
    inbox= 2
    outbox = 3
    Messages = _Web3.getInbox(_defaultAccount)
    account = _Web3.getAccounts()
    Page = 2
    msg = ''


    if request.method == 'POST':

        if request.form['InboxButtons'] == 'newMail':

            Page = NewMail
        elif request.form['InboxButtons'] == 'inbox':

            Page = inbox
            Messages = _Web3.getInbox(_defaultAccount)

        elif request.form['InboxButtons'] == 'outbox':

            Page = outbox
            Messages = _Web3.getOutbox(_defaultAccount)


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
                    Messages = _Web3.getInbox(_defaultAccount)

                print('switch account' + account[acc][0], file=sys.stderr )
                break
        return render_template('index.html', page=Page, msgs = Messages, mailMessage = msg, defaultAccount = _defaultAccount, accounts = account)
    return render_template('index.html', page=Page, msgs = Messages, accounts = account, mailMessage = msg, defaultAccount = _defaultAccount)


if __name__ == '__main__':
    app.debug = True
    app.run()
