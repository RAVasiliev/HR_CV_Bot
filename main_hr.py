

import os
import random
import telebot
import openai 

bot = telebot.TeleBot('6201574067:AAEk1A6RnTPBZbvYtcPtUnD_iboxlHNef94')

openai.api_key = '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'

user_answers = {}

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
    user_id = message.from_user.id
    user_answers[user_id] = []
    bot.reply_to(message, "Hi! I am an HR bot that will help you make your CV flawless! \
    The commands available now are: /about, /experience, /skills. Send me one of these tags and the corresponding CV block in one message and together we will make it better :)")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    cv_title = ''
    if '/title' in message.text:
        cv_title = message.text.replace('/title', "").strip()
        user_id = message.from_user.id
        if user_id in user_answers:
            user_answers[user_id].append(cv_title)
        else:
            user_answers[user_id] = [cv_title]
        print(str(user_id) + ': ' + cv_title)
    elif '/about' in message.text:
        user_id = message.from_user.id
        title = ''
        if user_id in user_answers:
            title = user_answers[user_id][-1]
        if title.strip() == "":
            prompt_for_blank = 'Imagine you are a professional, highly skilled HR, and you help me to create an "About me" that summarises all your experience in a short, attractive, proofed, valuable, and sellable bio with the highlighted results in numbers with symbol limitation in 500 characters. The main goal is to attract the top HRs from IT companies.'
            prompt_for_non_blank = 'Imagine you are a professional, highly skilled HR, and you help me to fix an "About me" that summarises all your experience in a short, attractive, proofed, valuable, and sellable bio with the highlighted results in numbers with symbol limitation in 500 characters. The main goal is to attract the top HRs from IT companies.'
        else:
            prompt_for_blank = 'Imagine you are a professional, highly skilled HR, and you help me to create an "About me" for ' + title + ' position that summarises all your experience in a short, attractive, proofed, valuable, and sellable bio with the highlighted results in numbers with symbol limitation in 500 characters. The main goal is to attract the top HRs from IT companies.'
            prompt_for_non_blank = 'Imagine you are a professional, highly skilled HR, and you help me to fix an "About me" for ' + title + ' position that summarises all your experience in a short, attractive, proofed, valuable, and sellable bio with the highlighted results in numbers with symbol limitation in 500 characters. The main goal is to attract the top HRs from IT companies.'
        try:
            about_message = message.text.replace('/about', "").strip()
            if about_message == "":
                print(str(user_id) + ': about me (empty) prompt \n' + prompt_for_blank)
                bot.reply_to(message, generate_response(prompt_for_blank))
            else:
                final_prompt = prompt_for_non_blank + '\n\n' + about_message
                print(str(user_id) + ': about me prompt \n' + final_prompt)
                bot.reply_to(message, generate_response(final_prompt))
        except: 
            bot.reply_to(message, 'Smth wrong')
    elif '/experience' in message.text:
        user_id = message.from_user.id
        title = ''
        if user_id in user_answers:
            title = user_answers[user_id][-1]
        if title.strip() == "":
            prompt = 'Imagine you are a professional highly skilled HR and you help me to rewrite my work experience in a resume based on the STAR method (without dividing by STAR) with achieved results in numbers, each line not longer than 300 symbols. Use direct action like "I did". The main goal is to attract the top HRs from IT companies.'
        else:
            prompt = 'Imagine you are a professional highly skilled HR and you help me to rewrite my work experience for the ' + title + ' in a resume based on the STAR method (without dividing by STAR) with achieved results in numbers, each line not longer than 300 symbols. Use direct action like "I did". The main goal is to attract the top HRs from IT companies.'
        prompt_w_message = prompt + '\n\n' + message.text.replace('/experience', "").strip()
        try:
            print(str(user_id) + ': experience prompt \n' + prompt_w_message)
            bot.reply_to(message, generate_response(prompt_w_message))
        except: 
            bot.reply_to(message, 'Smth wrong')
    elif '/skills' in message.text:
        user_id = message.from_user.id
        title = ''
        if user_id in user_answers:
            title = user_answers[user_id][-1]
        if title.strip() == "":
            prompt_for_blank = 'Imagine you are a professional, highly skilled HR, and you help me to create the list of skills  (20 skills) base on the below resume and make my CV appear in the LinkedIn HR search on the top position. Provide the list of LinkedIn skills in the same format on each new line without other text.'
            prompt_for_non_blank = 'Imagine you are a professional, highly skilled HR, and you help me to fix the below list of skills  (20 skills) and make my CV appear in the LinkedIn HR search on the top position. Provide the list of LinkedIn skills in the same format on each new line without other text.'
        else:
            prompt_for_blank = 'Imagine you are a professional, highly skilled HR, and you help me to create the list of skills  (20 skills) for the ' + title + ' position base on the below resume and make my CV appear in the LinkedIn HR search on the top position. Provide the list of LinkedIn skills in the same format on each new line without other text.'
            prompt_for_non_blank = 'Imagine you are a professional, highly skilled HR, and you help me to fix the below list of skills  (20 skills) for the ' + title + ' position and make my CV appear in the LinkedIn HR search on the top position. Provide the list of LinkedIn skills in the same format on each new line without other text.'
        try:
            skills_message = message.text.replace('/skills', "").strip()
            if skills_message == "":
                print(str(user_id) + ': skills (empty) prompt \n' + prompt_for_blank)
                bot.reply_to(message, generate_response(prompt_for_blank))
            else:
                final_prompt = prompt_for_non_blank + '\n\n' + skills_message
                print(str(user_id) + ': skills prompt \n' + final_prompt)
                bot.reply_to(message, generate_response(final_prompt))
        except: 
            bot.reply_to(message, 'Smth wrong')

    else:
        bot.reply_to(message, 'Please, send me message like that: [/about; /experience; /skills] + [Your pattern]. For example, "/about Middle DA, worked in 2 corporations"' + message.text)

def handle_answer(update, context, answer):
    user_id = update.effective_chat.id

    if user_id in user_answers:
        user_answers[user_id].append(answer)
    else:
        user_answers[user_id] = [answer]
    print(user_id, answer)

# Define a function to retrieve the answers for a specific user
def get_answers(user_id):
    if user_id in user_answers:
        return user_answers[user_id]
    else:
        return []

# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
