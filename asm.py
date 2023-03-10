__License__ = "GNU General Public License V.3"
__Name__ = "otomatik Magment Otomasyonu"
__Author__ = "Naci Caner"
__Code__ = "python3.8"


import requests as req 
from bs4 import BeautifulSoup as btu
import telebot 
import time


urlcvedetailse = "https://www.cvedetails.com/"
urlmitre = "https://cve.mitre.org/"
headers = {
    "User-Agnet": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
}
versıon = "aix 4.3"
kontrol = versıon
istek = req.get(urlmitre + f"cgi-bin/cvekey.cgi?keyword={versıon.replace(' ', '+')}", headers=headers)
html = istek.text
soupmitre = btu(html, "html.parser")
tablomitre = soupmitre.find_all("div", id="TableWithRules")


for tbody in tablomitre:
   tr_itemclass = tbody.find_all("tr")

#### Cve Tanımlarını Çekip Text'e Çevirdim Listeye Ekledim ###
liste = []
sayac = 0
sc = []
endliste = []
sayac_li =0
num = 0
token = "BOT-TOKEN"
bot = telebot.TeleBot(token)

for cevirme in tr_itemclass:
    try:
        td_top = cevirme.find_all("td", {"valign": "top"})

        td_top_valign = td_top[1]  # [td,td] Şeklinde Geldiği için ve liste olduğu için Listenin 1'c, elemanını aldım
        for cevir in td_top_valign:
           liste.append(cevir.text.strip())  # Texte çevirdim Sağ ve Sol'daki Boşluklalrı Sildim
    except:
        pass


for cveli in tr_itemclass:
   try:
       td_nowrap = cveli.find("td", {"nowrap":"nowrap"}).find("a").get("href")
       td_nowrap_link = "https://cve.mitre.org"+td_nowrap
       endliste.append(f"{liste[sayac]} {td_nowrap_link}")
       sayac += 1
   except:
       pass



@bot.message_handler(commands=["start"])
def BotChat(message):
     global num
     while len(endliste) > num:
         time.sleep(1)
         bot.send_message(message.chat.id, endliste[num])
         num+=1 
         
def main():
    bot.polling()

    
if __name__=="__main__":
    main()
