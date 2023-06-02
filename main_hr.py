import telebot 
import PyPDF2
import urllib.request
import openai 

TG_TOKEN = '6093361965:AAEYt6M4JSZcpLrGjC0tqaTExLYQqbXQNIQ'
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



def pdf_to_text(pdf_path):
    # Открываем PDF файл в режиме чтения бинарного файла
    with open(pdf_path, 'rb') as file:
        # Создаем объект PDFReader
        pdf_reader = PyPDF2.PdfReader(file)

        # Переменная для хранения текста из PDF
        text = ""

        # Проходимся по всем страницам PDF
        for page_num in range(len(pdf_reader.pages)):
            # Получаем объект страницы
            page = pdf_reader.pages[page_num]

            # Извлекаем текст из страницы
            page_text = page.extract_text()

            # Добавляем текст из текущей страницы в общий текст
            text += page_text

    # Возвращаем извлеченный текст
    return text

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = '/Users/ravasiliev/Documents/HR Bot/data/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    file_text = pdf_to_text(src)
    response_to_user = generate_response('привет, что происходит в тексте далее? текст: ' + file_text[:1000])

    
    bot.reply_to(message, response_to_user)


bot.infinity_polling()
