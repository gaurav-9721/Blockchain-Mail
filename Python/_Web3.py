from web3 import Web3
from Python.contract import _abi, contractAddress, ganacheURL
from datetime import datetime

web3 = Web3(Web3.HTTPProvider(ganacheURL))

if not web3.isConnected():
    raise Exception("Please start Ganache Blockchain or use a different Node Provider.")
else:
    print("Connected to "+ str(ganacheURL))

contract = web3.eth.contract(address=contractAddress, abi=_abi)
web3.eth.default_account = web3.eth.accounts[1]

def getDefaultAccount():
    return web3.eth.default_account


def updateCurrentUser(addressIndex):
    web3.eth.default_account = web3.eth.accounts[addressIndex]


def totalReceivedMails(address):
    return contract.functions.getTotalReceivedMails(address).call()

def totalSentMails(address):
    return contract.functions.getTotalSentMails(address).call()

def sendMail(receiver,sender, title, content):
    now = datetime.now()
    timeStamp = now.strftime("%H:%M    %d-%m-%Y")
    web3.eth.default_account = sender

    try:
        contract.functions.sendMail(receiver, sender, title, content, timeStamp).transact()
        print("Main sent successfully")
        return "Mail Sent"
    except:
        return "Error while sending mail"

def getMail(address, serialNumber, mailType):
    mail = []
    if mailType == 1:
        mail = contract.functions.getRecievedMail(address, serialNumber).call()
    else:
        mail = contract.functions.getSentMail(address, serialNumber).call()

    return mail

def deleteMail(address, serialNumber, mailType):
    web3.eth.default_account = address
    contract.functions.deleteMail(address, serialNumber, mailType).transact()


def getInbox(address):
    N = totalReceivedMails(address)
    INBOX = []

    i = N
    print(N)
    while i > 0:
        mail = getMail(address, i, 1)

        if len(mail[0]) > 1:
            INBOX.append(mail)

        i -= 1

    return INBOX


def getOutbox(address):
    N = totalSentMails(address)
    Outbox = []

    i = N
    while i > 0:
        mail = getMail(address, i, 0)

        if len(mail[0]) > 1:

            Outbox.append(mail)

        i -= 1

    return Outbox

def getAccounts():
    Accounts = {}
    i = 1
    for acc in web3.eth.accounts:
        bal = web3.fromWei(web3.eth.get_balance(acc), 'ether')
        bal = float(bal)
        Accounts[acc] = ['Account ' + str(i), bal]
        i += 1

    return Accounts
