# Youtube Müzik İndirici
from tkinter import *
from yt_dlp import YoutubeDL as ytdl
from threading import Thread as thr
from time import sleep
import plyer.platforms.win.notification
from plyer import notification as bildirim
from os import path, getcwd
from sys import exit as exitt
import logging

win = Tk()
win.config(bg= "#7AC5CD")
win.geometry("800x535")
win.title("Müzikİndirici")
win.maxsize(900, 600)
win.minsize(680, 420)

Label(text= "YouTube Müzik İndirici").pack()

# Link girilen alan
giris = Entry(width= 50)
giris.place(anchor= CENTER, relx= 0.5, rely= 0.5)

linkyazi = Label(text= "Link:")
linkyazi.place(anchor= CENTER, relx= 0.25, rely= 0.5)

# Pencere üstünde bilgilendirme yazıları göstermeye yarayan class
class Yazan:
    def __yaziYaz(self, metin, sure= 0, yer= "orta"):
        global yazi1, yazi2, yazi3
        if yer == "üst":
            try: yazi1.destroy()
            except: pass
            yazi1 = Label(text= metin)
            yazi1.place(anchor= CENTER, relx= 0.5, rely= 0.2)
            if sure: 
                sleep(sure)
                if not kapatildi: yazi1.destroy()
        elif yer == "orta":
            try: yazi2.destroy()
            except: pass
            yazi2 = Label(text= metin)
            yazi2.place(anchor= CENTER, relx= 0.5, rely= 0.3)
            if sure:
                sleep(sure)
                if not kapatildi: yazi2.destroy()
        elif yer == "alt":
            try: yazi3.destroy()
            except: pass
            yazi3 = Label(text= metin)
            yazi3.place(anchor= CENTER, relx= 0.5, rely= 0.4)
            if sure:
                sleep(sure)
                if not kapatildi: yazi3.destroy()
    
    def hata(self):
        def f(): self.__yaziYaz("Hata oluştu, linki kontrol edin..", 4, "alt")
        thr(target= f).start()

    def mesaj(self, mesaj):
        def f(): self.__yaziYaz(mesaj, 4, "orta")
        thr(target= f).start()

    def txtmesaj(self, mesaj):
        def f(): self.__yaziYaz(mesaj, 4, "üst")
        thr(target= f).start()
yaz = Yazan()



def indir(url:str):
    options = {
        "format": "bestaudio",
    }
    with ytdl(options) as ydl:
        ydl.download([url])


# İlk butonun işlevi
def Indir():
    kilitle()
    isimDegis("Ses İndiriliyor", "Ses İndiriliyor")
    link = giris.get()
    giris.delete(0, END)
    try:
        indir(link)
        yaz.mesaj("Ses İndirildi")
        if bildirimler == 1:
            bildirim.notify("Ses İndirildi 🎶", f"{getcwd()} dizinine indirildi.")
    except:
        yaz.hata()
    finally:
        isimDegis("İndir", txtyazi())
        kilitac()
def buton1():
    t = thr(target= Indir)
    t.daemon = True
    t.start()




# İkinci butonun görevi için class
class Linklertxt:

    def Indirtxt(self, linkmz):
        global success, fail
        try:
            print("İndiliyor..")
            indir(linkmz)
            print("İndirildi.")
            success += 1
            return False
        except:
            fail += 1
            print("İndirilemedi.")
            return True


    def islem(self):
        global success, fail
        isimDegis("txt dosyasındaki linkler İndiriliyor..", "Konsoldan takip edebilirsiniz..")
        success, fail = 0, 0
        try:
            with open("linkler.txt", "r") as fff:
                yaz.txtmesaj("txt Dosyasındaki Videolar İndiriliyor")
                sleep(0.5)
                uzunluk = len(fff.readlines())
                fff.seek(0)
                basarisizlar = []
                for i, satir in enumerate(fff.readlines(), 1):
                    sıra = f"{i}/{uzunluk}"; print(sıra)
                    if self.Indirtxt(satir): basarisizlar.append(sıra)
                print(f"İşlem {success} başarıyla, {fail} başarısızlıkla tamamlandı.")
                if basarisizlar: print("Başarısız olanlar:", basarisizlar)
                yaz.mesaj(f"İşlem {success} başarıyla, {fail} başarısızlıkla tamamlandı.")
                isimDegis("İndir", txtyazi())
                kilitac()
                if bildirimler == 1:
                    bildirim.notify("İşlem Tamamlandı 🎶", f"Başarılı İndirme: {success} - Başarısız İndirme: {fail}")
                print("\n")
        except:
            yaz.txtmesaj("linkler.txt dosyası bulunamadı.")




    def txtrun(self):
        if path.exists("linkler.txt"):
            kilitle()
            isimDegis("İndiriliyor", "İndiriliyor")
            t = thr(target= self.islem)
            t.daemon = True
            t.start()
        else:
            with open("linkler.txt", "w") as fff:
                yaz.txtmesaj("linkler.txt Dosyası Oluşturuldu")
            txtbutonu['text'] = "linkler.txt dosyasındaki linkleri İndir"




def kilitle():                       # butonları kilitler
    indirbutonu['state'] = "disabled"
    txtbutonu['state'] = "disabled"
def kilitac():                       # butonların kilidini açar
    indirbutonu['state'] = "active"
    txtbutonu['state'] = "active"
def isimDegis(indirbuton, txtbuton): # butonların üzerindeki yazıları değiştirir
    indirbutonu['text'] = indirbuton
    txtbutonu['text'] = txtbuton


# Bildirim ayarlarını yapan buton(ların)un fonksiyonları
bildirimler = 0
def bildirimAktif():
    global bildirimler, bildirAktif, bildirPasif
    bildirimler = 1
    bildirAktif.destroy()
    bildirPasif = Button(text= "Bildirimleri kapat", width= 14, command= bildirimPasif)
    bildirPasif.place(anchor= CENTER, relx= 0.9, rely= 0.85)
def bildirimPasif():
    global bildirimler, bildirAktif, bildirPasif
    bildirimler = 0
    bildirPasif.destroy()
    bildirAktif = Button(text= "Bildirimleri aç", width= 14, command= bildirimAktif)
    bildirAktif.place(anchor= CENTER, relx= 0.9, rely= 0.85)

bildirAktif = Button(text= "Bildirimleri aç", width= 14, command= bildirimAktif)
bildirAktif.place(anchor= CENTER, relx= 0.9, rely= 0.85)


# İndir butonu
indirbutonu = Button(text= "İndir", width= 35, height= 2, command= buton1)
indirbutonu.place(anchor= CENTER, relx= 0.5, rely= 0.65)

# txt indirici butonu
def txtyazi():
    if path.exists("linkler.txt"): return "linkler.txt dosyasındaki linkleri İndir"
    else: return "linkler.txt dosyası oluştur"
txtbutonu = Button(text= txtyazi(), width= 35, height= 2, command= Linklertxt().txtrun)
txtbutonu.place(anchor= CENTER, relx= 0.5, rely= 0.75)


kapatildi = 0
def kapat():
    global kapatildi
    kapatildi = 1
    win.destroy(); exitt()
win.protocol("WM_DELETE_WINDOW", kapat)
Kapat = Button(text= "Kapat", width= 14, command= kapat)
Kapat.place(anchor= CENTER, relx= 0.9, rely= 0.92)

win.mainloop()
