import boto3
import csv
import time

ACCESS_KEY = "ACCESS_KEY"
SECRET_ACCESS_KEY = "SECRET_ACCESS_KEY"

list_of_contacts = []               # Stores the subscribed numbers in the arn

def Create_ARN_Dictionary():        #opens the directory for reading the arn    of respective classes
    arn_directory = "/home/stoneduser/Desktop/school_students/arn.csv"
    with open(arn_directory, "r") as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for row in reader:
            arn_dict[row[0]] = row[1]
        return(arn_dict)

def Read_PhoneNumbers(std):    #Creating a list of the phone numbers from the .csv files to whomever want to send the message.
    Directory = str("/home/stoneduser/Desktop/school_students/"+std+".csv")
    with open(Directory, "r") as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        list_of_contacts = []
        for row in reader:
            list_of_contacts.append(row[1])
        return(list_of_contacts)

def Create_client():        #Creating the client for the aws account with secret key and access key
    client = boto3.client(
        "sns",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name="us-east-1"
    )
    return client


def Create_topic(topic_name):
    client = Create_client()
    response = client.create_topic(Name=topic_name)


def Topic_arn_scanner(arn_dict,std):           #From the list of arn finds the arn for the input class
    Topic_Arn = arn_dict[std]
    return Topic_Arn


def Topic_Subscriber(client, Topic_Arn):
    '''
    Gets the list of subscribed phone numbers
    '''
    response = client.list_subscriptions_by_topic(
        TopicArn=Topic_Arn
    )
    return response


def Attributes(client):
    '''
    Sets the message attributes
    '''
    client.set_sms_attributes(
               attributes={"DefaultSMSType": "Transactional"}
    )

def Topic_Subscriber_List(response, list_of_contacts):
    '''
    creates a list of subscribed numbers
    '''
    for subscription in response['Subscriptions']:
        list_of_contacts.append(subscription['Endpoint'])
    return list_of_contacts


def Subscribe_topic(list_of_contacts, Topic_Arn, client):
    '''
    For each contact in the contact list
    '''
    for number in list_of_contacts:
        '''
        Creats Subscription of each phone number to the ARN topic
        '''
        client.subscribe(
            TopicArn=Topic_Arn,
            Protocol='sms',
            Endpoint=number        #  <---- Phone Number which has to receive the message
        )

def Send_msg(list_of_contacts,loop_count,client,Msg):
    for number in list_of_contacts:
        '''
        checking for loop count because aws sns does not allow consecutive messages to be sent
        above the billing of $1 i.e. each message costs $0.00223. So the loop waits for few minutes
        before sending another bunch of messages
        '''
        if(loop_count%2==0 and loop_count!=0):
            time.sleep(70)                     # waits for 2 minutes
            client.publish(
                PhoneNumber=number,
                Message=Msg
            )
        else:
            client.publish(
                PhoneNumber=number,
                Message=Msg
            )
        loop_count += 1

def Subscribe_contact_list(arn_dict, list_of_contacts, std):
    arn_dict = Create_ARN_Dictionary()
    client = Create_client()
    if(std=="All" or std=="all"):
        for i in arn_dict:
            std = i
            list_of_contacts = []
            list_of_contacts = Read_PhoneNumbers(std)
            Attributes(client)
            Topic_Arn = Topic_arn_scanner(arn_dict,std)
            Subscribe_topic(list_of_contacts, Topic_Arn, client)
    else:
        list_of_contacts = Read_PhoneNumbers(std)
        Attributes(client)
        Topic_Arn = Topic_arn_scanner(arn_dict,std)
        Subscribe_topic(list_of_contacts, Topic_Arn, client)


def Subscribe_new_contact(arn_dict,new_number,std):
    arn_dict = Create_ARN_Dictionary()
    client = Create_client()
    Attributes(client)
    Topic_Arn = Topic_arn_scanner(arn_dict,std)
    Subscribe_topic(new_number, Topic_Arn, client)


def Send_message_to_topic(arn_dict, list_of_contacts, std, loop_count, Msg):
    arn_dict = Create_ARN_Dictionary()
    client = Create_client()
    if(std=="All"):
        for i in arn_dict:
            Topic_Arn = arn_dict[i]
            response = Topic_Subscriber(client, Topic_Arn)
            list_of_contacts = Topic_Subscriber_List(response, list_of_contacts)
            Attributes(client)
            Send_msg(list_of_contacts, loop_count, client, Msg)
    else:
        Topic_Arn = Topic_arn_scanner(arn_dict,std)
        response = Topic_Subscriber(client, Topic_Arn)
        list_of_contacts = Topic_Subscriber_List(response, list_of_contacts)
        Attributes(client)
        Send_msg(list_of_contacts, loop_count, client, Msg)


if __name__ == "__main__":
    arn_dict = {}                       # Stores The ARN against class name
    loop_count = 0
    new_number = []                     # Stores the number of looping

    print("You want a new number to be subscribed or want to send a message?")
    print("1. Create Class\n2. Subscribe\n3. Register a new number\n4. Message")
    option = int(input())

    if(option==2):
        std = str(input("Enter the class: "))
        Subscribe_contact_list(arn_dict,list_of_contacts,std)
    elif(option==4):
        std = str(input("Enter the class: "))
        Msg = str(input("Enter the message: "))
        Send_message_to_topic(arn_dict,list_of_contacts,std, loop_count, Msg)
    elif(option==3):
        std = str(input("Enter the class: "))
        new_number.append(input("Enter the new number:\n"))
        Subscribe_new_contact(arn_dict,new_number,std)
    elif(option==1):
        accept_response = "yes"
        while(accept_response=="Yes" or accept_response=="yes" or accept_response=='y'):
            topic_name = input("Enter class name:   ")
            Create_topic(topic_name)
            accept_response = input("Do you want to add another class?  ")
    else:
        print("Oops!! Sorry... wrong choice!!")




'''
Dear Students,
As per the yearly schedule ordered by D.C., on each Monday of Shravan,School will be closed,
Regard,
B.V.P.
'''
