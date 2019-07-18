# School_Messaging_Service
This mini project is for sending messages to the pupils of the school using free tier of AWS SNS
The same concept can be used across many industries for sending free sms to alimit of 1,000,000 messages.
As AWS provides 1,000,000 for free tier.
So any industry can use this for sending messages to the staffs.

In this mini project we read the scraped .csv files for reading the phone number of the students of a particular class.
then those numbers are subscribed to the topic ARN of their respective class.
Finally the message is sent to the numbers
We prefer sending one message each time rather than publishing the message to the topic because aws sns does not allow consecutive messages to be sent above the billing of $1 i.e. each message costs $0.00223 for free tier.
So we wait for few seconds before sending another bunch of messages.

we have separate .csv files for each class' students. and another .csv file which contains the topic ARN of each class.
