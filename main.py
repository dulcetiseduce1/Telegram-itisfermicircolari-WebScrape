# per far funzionare le emoji sul rasp
import emoji
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

# emoji
newspaper = emoji.emojize(':newspaper:')
label = emoji.emojize(':label:')
clipboard = emoji.emojize(':clipboard:')
linkemoji = emoji.emojize(':link:')

# tokenbot
TOKEN = "replacewithtoken"
chatid = "@replacewithchatid"


# comando start
def start(update, context):
    # dichiaro descrizione come global per la exception
    global descrizione, linkpdfstampa, linkpdf
    source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
    soup = BeautifulSoup(source, 'html.parser')
    verificatitolo = soup.find('div', class_='blog-content').a.text
    titolo = soup.find('div', class_='blog-content').a.text
    # loop
    while True:
        context.bot.send_message(chat_id='@canaletest', text='check')
        # verifica del titolo che si ripete in loop
        if titolo == verificatitolo:
            # debug
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' check')
            # aggiornamento di verificatitolo
            source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
            soup = BeautifulSoup(source, 'html.parser')
            verificatitolo = soup.find('div', class_='blog-content').a.text
        # stampa della nuova circolare
        else:
            # debug
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S') + ' nuova circolare')
            # prelevamento informazioni
            source = requests.get('https://www.itisfermi.edu.it/comunicazioni/').text
            soup = BeautifulSoup(source, 'html.parser')
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
            finally:
                # verifica di Loading
                if descrizione.find("Loading"):
                    source = requests.get(linkcircolare).text
                    soup = BeautifulSoup(source, 'html.parser')
                    linkpdf = soup.find('a', class_='ead-document-btn')
                    # handle exception
                    # TypeError: href...
                    # se nella descrizione non c'è nessun file stampa il linkcricolare
                    try:
                        linkpdfstampa = linkpdf['href']
                    except TypeError:
                        context.bot.send_message(chat_id=chatid,
                                                 disable_web_page_preview=True,
                                                 parse_mode=ParseMode.HTML,
                                                 text=newspaper + " " + verificatitolo[:-1]
                                                      + "\n" + label + " " + descrizione + "\n"
                                                      + '<a href="' + linkcircolare + '">' + linkemoji
                                                      + ' Link della circolare</a>')
                        # se nella descrizione c'è loading stampa il linkpdf
                    else:
                        # i=1 equivale al primo pdf e 2 ai pdf successivi
                        i = 1
                        for linkloop in soup.find_all("a", attrs={"class": "ead-document-btn", "target": "_blank"}):
                            links = (linkloop.get('href'))

                            if i == 1:
                                context.bot.send_message(chat_id=chatid,
                                                         disable_web_page_preview=False,
                                                         parse_mode=ParseMode.HTML,
                                                         text=newspaper + " " + verificatitolo[:-1] + "\n"
                                                              + '<a href="' + links + '">' + clipboard
                                                              + ' Allegato</a>' + "\n"
                                                              + '<a href="' + linkcircolare
                                                              + '">' + linkemoji + ' Link della circolare</a>')
                                i = 2
                            else:
                                context.bot.send_message(chat_id=chatid,
                                                         disable_web_page_preview=False,
                                                         parse_mode=ParseMode.HTML,
                                                         text='<a href="' + links + '">' + clipboard
                                                              + ' Allegato</a>')
                # update titolo
                titolo = verificatitolo
        # attesa di 5 minuti
        time.sleep(300)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
