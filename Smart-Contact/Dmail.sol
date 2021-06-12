
pragma solidity >=0.7.0 <0.9.0;

contract DMail {


    struct Mail{

        int serialNumber;
        string title;
        string content;
        string time;
        address _sender;
        address reciever;
    }

    struct Inbox{
        int numberOfRecievedMails;
        int numberOfSentMails;

        mapping(int => Mail) receivedMails;
        mapping(int => Mail) sentMails;
    }

    mapping(address => Inbox) users;
    mapping(address => bool) registerd;



    function checkUser(address _address) public{

        if(!registerd[_address]){
            registerd[_address] = true;

            //users[_address] = inbox;

        }


    }

    function getTotalReceivedMails(address _address) view public returns(int){
        return users[_address].numberOfRecievedMails;
    }

    function getTotalSentMails(address _address) view public returns(int){
        return users[_address].numberOfSentMails;
    }

    //function to send Mail
    function sendMail(address recieverAddress, address senderAddress, string memory Title, string memory Content, string memory Time)  public{

        checkUser(recieverAddress);
        checkUser(senderAddress);

        users[senderAddress].numberOfSentMails++;
        users[recieverAddress].numberOfRecievedMails++;


        Mail memory mail;

        mail.title  = Title;
        mail.reciever = recieverAddress;
        mail._sender = senderAddress;
        mail.time = Time;
        mail.content = Content;
        mail.serialNumber = getTotalReceivedMails(recieverAddress);

        Inbox storage inboxR = users[recieverAddress];
        Inbox storage inboxS = users[senderAddress];
        inboxR.receivedMails[getTotalReceivedMails(recieverAddress)] = mail;
        inboxS.sentMails[getTotalSentMails(senderAddress)] = mail;



    }

    function deleteMail(address _address, int serialNumber, int  _type) public{
        if(_type == 1){
            users[_address].receivedMails[serialNumber].content = '';
            users[_address].receivedMails[serialNumber].title = '';
            users[_address].receivedMails[serialNumber].time = '';

        }
        else{
            users[_address].sentMails[serialNumber].content = '';
            users[_address].sentMails[serialNumber].title = '';
            users[_address].sentMails[serialNumber].time = '';

        }

    }

    function getRecievedMail(address _address, int serialNumber) public view returns(string memory ,string memory, string memory, address){
        string memory content =   users[_address].receivedMails[serialNumber].content;
        string memory Title = users[_address].receivedMails[serialNumber].title;
        string memory time = users[_address].receivedMails[serialNumber].time;
        address _add = users[_address].receivedMails[serialNumber]._sender;
        return (time, Title, content, _add);
    }

    function getSentMail(address _address, int serialNumber) public view returns(string memory ,string memory, string memory,address){
        string memory content =   users[_address].sentMails[serialNumber].content;
        string memory Title = users[_address].sentMails[serialNumber].title;
        string memory time = users[_address].sentMails[serialNumber].time;
        address _add = users[_address].sentMails[serialNumber].reciever;
        return (time, Title, content, _add);
    }
}