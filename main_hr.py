#  Copyright (c) ChernV (@otter18), 2021.

import os
import random
import telebot
import openai 

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

openai.api_key = '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'

def generate_response(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response['choices'][0]['text']


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hi! I am an HR bot that will help you make your CV flawless! \
    The commands available now are: /about, /experience, /skills. Send me one of these tags and the corresponding CV block in one message and together we will make it better :)")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if '/about' in message.text:
        prompt = 'Imagine you are a professional, highly skilled HR, and you help me to fix an "About me" that summarises all your experience in a short, attractive, proofed, valuable, and sellable bio with the highlighted results in numbers with symbol limitation in 500 characters. The main goal is to attract the top HRs from IT companies. Here is the pattern that you should upgrade: '
        prompt_w_message = prompt + message.text
        try:
            bot.reply_to(message, generate_response(prompt_w_message))
        except: 
            bot.reply_to(message, 'Smth wrong')
    elif '/experience' in message.text:
        prompt = 'Imagine you are a professional highly skilled HR and you help me to rewrite my work experience in a resume based on the STAR method (without dividing by STAR) with achieved results in numbers, each line not longer than 300 symbols. Use direct action like "I did". The main goal is to attract the top HRs from IT companies. Here is the pattern that you should upgrade: '
        prompt_w_message = prompt + message.text
        try:
            bot.reply_to(message, generate_response(prompt_w_message))
        except: 
            bot.reply_to(message, 'Smth wrong')
    elif '/skills' in message.text:
        prompt = 'Imagine you are a professional, highly skilled HR, and you help me to fix the below list of skills  (20 skills) and make my CV appear in the LinkedIn HR search on the top position. Provide the list of LinkedIn skills in the same format on each new line without other text. Here is the pattern that you should upgrade: '
        prompt_w_message = prompt + message.text
        try:
            bot.reply_to(message, generate_response(prompt_w_message))
        except: 
            bot.reply_to(message, 'Smth wrong')

    else:
        bot.reply_to(message, 'Please, send me message like that: [/about; /experience; /skills] + [Your pattern]. For example, "/about Middle DA, worked in 2 corporations"' + message.text)



# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
