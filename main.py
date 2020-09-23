# stampa di debug con orario
import datetime
# tempo usato nel loop
import time
# utilizzati per ricevere codice
import requests
from bs4 import BeautifulSoup
# cose di telegram
from telegram import update
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# tokenbot
TOKEN = "replacewithtoken"


# comando start
def start(update, context):
    # dichiaro descrizione come global per la exception
    global descrizione
    source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
    soup = BeautifulSoup(source, 'lxml')
    verificatitolo = soup.find('div', class_='blog-content').a.text
    titolo = soup.find('div', class_='blog-content').a.text

    # loop

    while True:
        # verifica del  titolo
        if titolo == verificatitolo:
            # debug
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' check')
            # aggiornamento di verificatitolo
            source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
            soup = BeautifulSoup(source, 'lxml')
            verificatitolo = soup.find('div', class_='blog-content').a.text

        else:
            # stampda della nuova circolare
            # debug
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' nuova circolare')
            # prelevamento informazioni
            source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
            soup = BeautifulSoup(source, 'lxml')
            # linkdocumento
            link = soup.find('a', title=True)
            linkcircolare = (link['href'])
            # handle exception
            #    descrizione = soup.find('div', class_='blog-content').p.text
            #    AttributeError: 'NoneType' object has no attribute 'text'
            try:
                descrizione = soup.find('div', class_='blog-content').p.text
            except AttributeError:
                descrizione = "Nessuna Descrizione"
            else:
                # verifica di Loading
                if descrizione.find("Loading"):
                    source = requests.get(linkcircolare).text
                    soup = BeautifulSoup(source, 'html.parser')
                    linkpdf = soup.find('a', class_='ead-document-btn')
                    linkpdfstampa = linkpdf['href']
                    context.bot.send_message(chat_id="@itisfermicircolari",
                                             disable_web_page_preview=False,
                                             parse_mode=ParseMode.HTML,
                                             text="📰 " + verificatitolo[:-1] + "\n"
                                                  + '<a href="' + linkpdfstampa + '">🔗 Allegato</a>')
                else:
                    # stampa informazioni
                    context.bot.send_message(chat_id='@itisfermicircolari',
                                             disable_web_page_preview=True,
                                             text="📰 " + verificatitolo[:-1] +
                                                  "\n" + "🏷 " + descrizione +
                                                  "\n🔗 Link della circolare \n" + linkcircolare)
                # update titolo
                titolo = verificatitolo
        # attesa di 60 secondi prima di ripetere
        time.sleep(60)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
