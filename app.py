import json
import tweepy
from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
from TwitterAPI import TwitterAPI, TwitterPager

load_dotenv()

consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

auth = tweepy.OAuth1UserHandler( consumer_key, consumer_secret, access_token, access_token_secret )
api = tweepy.API(auth)

twapi = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret, api_version='2') 

app = Flask(__name__)
CORS(app)


@app.route('/senders')
def get_unique_senders():

    direct_messages = api.get_direct_messages()
    id = str(api.verify_credentials().id)
    senders = []
    unique = [id]

    for messages in direct_messages:
        sender = messages.message_create['target']['recipient_id']
        if sender not in unique:
            name = api.get_user(user_id=sender).name
            senders.append({'id': sender, 'name': name})
            unique.append(sender)

        sender = messages.message_create['sender_id']
        if sender not in unique:
            name = api.get_user(user_id=sender).name
            senders.append({'id': sender, 'name': name})
            unique.append(sender)

    response = {'status': 200, 'senders': senders,
                'unique': unique}

    return jsonify(response)


@app.route('/outreach')
def messages_list_by_recipient_id():
    # comment out line 67 and 74 when working with messages_sample.json file
    f = open('messages_sample.json')
    direct_messages = json.load(f)
    f.close()
    id = "851739529711157249"
    # direct_messages = api.get_direct_messages()
    # id = str(api.verify_credentials().id)
    

    
    # for messages in direct_messages:
    #     # messages = messages._json
    #     recepient_id = messages['message_create']["target"]['recipient_id']

    #     if recepient_id == id:
    #         recepient_id = messages['message_create']['sender_id']

    #     for message in direct_messages:
    #         # message = message._json
    #         if recepient_id == message['message_create']["target"]['recipient_id'] or recepient_id == message['message_create']['sender_id']:
    #             message['message_create']['timestamp'] = message['created_timestamp']
    #             response = message['message_create']
                
    #             if recepient_id not in messageStack.keys():
    #                 messageStack[recepient_id] = list()
                    
    #             messageStack[recepient_id].append(response)

    # for recepient_id, target in messageStack.items():

    #     if target[-1]["sender_id"] == id:
    #         data = { 'response': False }
    #         data["handle"] = api.get_user(user_id=recepient_id).name
    #         data['id'] = recepient_id

    #         timestamp = int(target[-1]['timestamp'])/1000
    #         data["date"] = datetime.fromtimestamp(
    #             timestamp).strftime('%d-%m-%y')

    #         for messages in target:

    #             if messages['sender_id'] == recepient_id:
    #                 data['response'] = True
    #                 break
        
    #         outreach.append(data)
    outreach = get_outreach(id,create_conversation_tree(id,direct_messages,False))
    

    response = {'status':200, 'outreach':outreach}
    return jsonify(response)


@app.route('/tweet/<id>')
def get_tweet_commenters(id):

    pager = TwitterPager(twapi, 'tweets/search/recent',
                        {
                            'query': f'conversation_id:{id}',
                            'tweet.fields': 'author_id,conversation_id,created_at,in_reply_to_user_id'
                        })

    users = []
        
    for reply in pager.get_iterator(wait=5):
        user_name = api.get_user(user_id=reply['author_id'])
        users.append({'id':reply['author_id'],'user_name':user_name.name})

    print(users)
    return jsonify(users)


@app.route('/followup')
def followup_list_by_recipient_id():
    # comment out line 67 and 74 when working with messages_sample.json file
    # f = open('messages_sample.json')
    # direct_messages = json.load(f)
    # f.close()
    # id = "851739529711157249" 
    direct_messages = api.get_direct_messages()
    id = str(api.verify_credentials().id)
    followups = []
    # if using default message file use this function and comment line 139
    # message_stack = create_conversation_tree(id,direct_messages, api_fetch=False)
    message_stack = create_conversation_tree(id,direct_messages)
    followups = get_followups(id,message_stack)
    stats = get_stats(id,message_stack)
    response  = {'status':200,'followups':followups,'stats':stats}
    return jsonify(response)



def get_stats(id,messageStack):
    '''This function is resposible to return the following stats 
    {
        response_rate,\n
        total_messages_sent,\n
        total_initial_messages_sent,\n
        total_followups
    }
    
    '''
    
    mes_sent_in_total = 0
    total_initial_messages = 0
    total_followups = 0
    response_rate = None
    
    for recepient,conversation in messageStack.items():
        for message in conversation:
            if message['sender_id'] == id:
                mes_sent_in_total+=1

    total_followups = len(get_followups(id,messageStack))    
    outreach = get_outreach(id,messageStack)
    total_initial_messages = len(outreach)
    response_rate  = calculate_response_rate(outreach)

    statistics  = {'sent_message_count':mes_sent_in_total,'total_initial_messages':total_initial_messages,'total_followups':total_followups,'response_rate':response_rate}
    return statistics
            
def create_conversation_tree(id,direct_messages,api_fetch=True):
    ''' This function is responsible to return a conversation tree/message stack'''
    messageStack = {}
    for messages in direct_messages:
        # if fetching data from api 
        if api_fetch:
            messages = messages._json

        recepient_id = messages['message_create']["target"]['recipient_id']

        if recepient_id == id:
            recepient_id = messages['message_create']['sender_id']

        for message in direct_messages:
            if api_fetch:
                message = message._json
            if recepient_id == message['message_create']["target"]['recipient_id'] or recepient_id == message['message_create']['sender_id']:
                message['message_create']['timestamp'] = message['created_timestamp']
                response = message['message_create']
               
                if recepient_id not in messageStack.keys():
                    messageStack[recepient_id] = list()
                    if response not in messageStack[recepient_id]:
                        messageStack[recepient_id].append(response)
                else:
                    if response not in messageStack[recepient_id]:
                        messageStack[recepient_id].append(response)
    return messageStack

def get_followups(id,messageStack):
    '''This function is responsible for extracting the followups from the message stack and return it'''
    followups = []
    for conversation in messageStack.values():
        if len(conversation) >= 2:
            if conversation[-1]["sender_id"] == id and conversation[-2]["sender_id"] == id :
                data = {'followup':True,'followup_content':"_"}
                if data['followup_content'] == '_':
                    reverse = conversation[::-1]
                    data['followup_content'] = reverse[1]["message_data"]["text"]
                followups.append(data)  

    return followups
 
def get_outreach(id,messageStack):
    '''This function is responsible for extracting outreaches from the messagestack and return it'''
    outreach = []
    for recepient_id, target in messageStack.items():

        if target[-1]["sender_id"] == id:
            data = { 'response': False }
            data["handle"] = api.get_user(user_id=recepient_id).name
            data['id'] = recepient_id

            timestamp = int(target[-1]['timestamp'])/1000
            data["date"] = datetime.fromtimestamp(
                timestamp).strftime('%d-%m-%y')

            for messages in target:

                if messages['sender_id'] == recepient_id:
                    data['response'] = True
                    break
        
            outreach.append(data)
    return outreach

def calculate_response_rate(outreach):
    '''The function is responsible for calculating response rate and rate% in outreaches and return them'''
    positive_response = 0
    total_response = len(outreach)
    
    for data in outreach:
        print(data)
        if data['response']:
            positive_response+=1
    
    rate = positive_response / total_response
    return {'rate':rate,'rate%':f'{rate * 100} %'}


