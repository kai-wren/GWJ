import telebot
import parser
from biorxiv import BiorxivRetriever
 

#main variables
TOKEN = "1435376107:AAGa7qgq_KRviieCrP1ivipTppce1DeXnmY"
bot = telebot.TeleBot(TOKEN)
br = BiorxivRetriever()


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Welcome to GWJ_Bot.')


@bot.message_handler(commands=['search'])
def search_handler(message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Please, enter what you want to search.')
    bot.register_next_step_handler(msg, search_response)


def search_response(message):
    chat_id = message.chat.id
    text = message.text
    res_string = "Relevant articles:\n"

    search_res = search(text)

    if len(search_res) == 0:
        bot.send_message(chat_id, "No relevant articles were found.")
    else:
        res_string += format_output(search_res)
        bot.send_message(chat_id, res_string)


def search(search_term):
    try:
        res = br.query(search_term, metadata=False, full_text=False)
    except:
        res = []
    return res[:10]


def format_output(article_list):
    res_string = ""
    for i in range(len(article_list)):
        res_string += str(i+1) + ". "
        res_string += article_list[i]["title"] + ", "
        res_string += article_list[i]["biorxiv_url"]
        res_string += "\n"
    return res_string
        


if __name__ == "__main__":
    bot.polling()


