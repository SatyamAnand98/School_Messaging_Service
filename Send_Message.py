import boto3
import csv
import time

arn_dict = {}						# Stores The ARN against class name
list_of_contacts = []				# Stores the subscribed numbers in the arn
loop_count = 0						# Stores the number of looping


'''
Taking the necessary inputs
'''
stan = str(input("Enter the class: "))
Msg = str(input("Enter the message: "))
# "Dear Students,\nAs per the yearly schedule ordered by D.C, on each Monday of Shravan, School will be closed.\nRegards,\nB.V.P."


'''
opens the directory for reading the arn	of respective classes
'''
arn_directory = "/home/stoneduser/Desktop/school_students/arn.csv"
with open(arn_directory, "r") as file:
    reader = csv.reader(file, delimiter=',')
    header = next(reader)
    for row in reader:
        arn_dict[row[0]] = row[1]


'''
Creating a list of the phone numbers from the .csv files to whomever want to send the message.
'''
Directory = str("/home/stoneduser/Desktop/school_students/"+std+".csv")
with open(Directory, "r") as file:
    reader = csv.reader(file, delimiter=',')
    header = next(reader)
    for row in reader:
        list_of_contacts.append(row[1])
    print(some_list_of_contacts)


'''
Creating the client for the aws account with secret key and access key
'''
client = boto3.client(
    "sns",
    aws_access_key_id="ACCESS_KEY_OF_YOUR_AWS_ACCOUNT",
    aws_secret_access_key="SECRET_KEY_OF_YOUR_AWS_ACCOUNT",
    region_name="us-east-1"
)


'''
From the list of arn finds the arn for the input class
'''
Topic_Arn = arn_dict[std]


'''
Gets the list of subscribed phone numbers
'''
response = client.list_subscriptions_by_topic(
    TopicArn=Topic_Arn
)


'''
Sets the message attributes
'''
client.set_sms_attributes(
           attributes={"DefaultSMSType": "Transactional"}
)


'''
creates a list of subscribed numbers
'''
for subscription in response['Subscriptions']:
    list_of_contacts.append(subscription['Endpoint'])
    print(subscription['Endpoint'])


'''
For each contact in the contact list
'''
for number in some_list_of_contacts:
    '''
    Creats Subscription of each phone number to the ARN topic
    '''
    client.subscribe(
        TopicArn=Topic_Arn,
        Protocol='sms',
        Endpoint=numbers        #  <------ Phone Number which has to receive the message
    )


    '''
    checking for loop count because aws sns does not allow consecutive messages to be sent
    above the billing of $1 i.e. each message costs $0.00223. So the loop waits for few minutes
    before sending another bunch of messages
    '''
    if(loop_count%4==0 and loop_count!=0):
        time.sleep(120)                     # waits for 2 minutes
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
