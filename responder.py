import secrets
import threading
import time
import re
import random
import json

from fbchat import log, Client, Message

with open('contacts.json', 'r', encoding='utf-8') as file:
	contacts = json.load(file)

log.info("Loaded contacts:")
for contact in contacts["contacts"]:
		log.info("* " + contact)

log.info("")

with open('replies.json', 'r', encoding='utf-8') as file:
	replies = json.load(file)

log.info("Loaded replies:")
for reply in replies["replies"]:
		log.info("* " + reply)

log.info("")
log.info("")
log.info("")

class Bot(Client):
	#Listen for the event
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		#Mark the newest received messagfe as delivered and as read
		self.markAsDelivered(thread_id, message_object.uid)

		#Fetch sender name to check for whitelist
		sender_name =  client.fetchUserInfo(author_id)[author_id].name

		log.info("Received message from" + sender_name + ", text: " + message_object.text)

		def sendReply():
			#Handle replying
			log.info("Sending message to " + sender_name + ", text:" + reply)

			#Send the message
			self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

		#Check whether the sender is on whitelist
		for contact in contacts["contacts"]:
			if contact in sender_name:
				#Select random reply...
				reply = secrets.choice(replies['replies'])

				#Handle interactive replies
				if "{}" in reply:
					reply = reply.format(sender_name.split()[0])

				#Generate a random delay to make it more humanlike?
				delayTime = float(random.randrange(5,25,1))

				#Mark it as read...
				self.markAsRead(thread_id)

				#Make a thread so it doesn't clog up the main thread
				threading.Timer(delayTime, sendReply).start()


#Log in and listen
client = Bot("login@mail.com", "password")
client.listen()