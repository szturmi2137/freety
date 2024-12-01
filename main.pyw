from tkinter import *
import os
import vlc
from pytube import *
from tkinter import Menu
from random import randint
from datetime import timedelta
from ttkwidgets.frames import ScrolledFrame

# -boczne okineko z wyborem muzyki / przycisk z aktualnie lecącą piosenką jest aktywny a nie powinien
# -progressbar / odpada bo jedno nachodzi na drugie
# -glosnosc int / glosnosc zmienia się po ruszeniu myszką a nie po odkliknięciu

sciezka = 'muzyka'
nazwyutowru = []
utwory = []
kolejka = []

def zmianaUtworu(k):
    global i
    media = vlc.Media(nazwyutowru[k])
    media_player.set_media(media)
    stop()
    stop()
    okno.after(50, pobierzDlugosc)
    uaktualnijDlugosc()
    aktualna.config(text=utwory[k])
    i = k
    try:
        nieaktywnuUtwor()
    except:
        print("czeaj")

def pobierzDlugosc():
    labelCzasStaly.config(text=godzinowka(int(media_player.get_length()/1000)))

def uaktualnijDlugosc():
    global pomijacz
    labelCzasAktualny.config(text=godzinowka(int(media_player.get_time()/1000)))
    okno.after(500, uaktualnijDlugosc)

moznaPominac = True

def uaktualnijPomijacz():
    global pomijacz
    if moznaPominac == True:
        pomijacz.set(media_player.get_position())
    okno.after(500, uaktualnijPomijacz) 

def skipper(zmiennaponic=None):
    global pomijacz, moznaPominac
    skip = pomijacz.get()
    uaktualnijPomijacz()
    media_player.set_position(skip)
    moznaPominac = True

def stopPomijacz(zmiennaponic=None):
    global moznaPominac
    moznaPominac = False


def godzinowka(s):
    czas = str(timedelta(seconds=s))
    if czas[0] == '0':
        czas = czas[:0] + czas[2:]
    return czas

def stop():
    global odtwarzanie, i, playStop
    if odtwarzanie == True :
        # print("puszczono")
        media_player.play()
        odtwarzanie = False
        return 0
    if odtwarzanie == False:
        # print("zatrzymano")
        media_player.set_pause(1)
        odtwarzanie = True
        return 0
    
def next():
    global i, okno, vKoleyka, autoodtwarzanie, petla, przypadkowe, kolejek
    if i < len(utwory) - 1:
        if vKoleyka == False:
            i += 1
            zmianaUtworu(i)
            media_player.play()
            # print(i)
        else:
            try:
                zmianaUtworu(kolejka[0])
                kolejka.pop(0)
                print(kolejka)
            except:
                pstryczkowanie(autoodtwarzanie, petla, przypadkowe, kolejek, 1)
                next()
                print("prawdopodobnie skonczyla sie lista")

    
def prev():
    global i, okno, vKoleyka, autoodtwarzanie, petla, przypadkowe, kolejek
    if i > 0:
        if vKoleyka == False:
            i -= 1
            zmianaUtworu(i)
            media_player.play()
            # print(i)


def vol(zmiennaponic=None):
    global skalaDziweku, glosnoscText
    vol = int(skalaDziweku.get())
    glosnoscText.config(text=vol)
    # print(vol)
    media_player.audio_set_volume(vol)
    
def download():
    global src, link
    print("pobieranie")
    dwd = Toplevel()
    dwd.title("Pobierz nie krępuj się :)")

    link = Entry(dwd)
    link.grid(column=0, row=0, columnspan=3)
    

    pob = Button(dwd, text="pobierz",command=faktycznepobieranie)
    pob.grid(column=0, row=1)

    dwd.mainloop()

def faktycznepobieranie():
    global src, link, sciezka
    src = YouTube(str(link.get()))
    video = src.streams.filter(only_audio=True).first()
    destination = 'muzyka'
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(src.title + " pobrano")
    restart()

def restart():
    okno.destroy()
    media_player.set_pause(1)
    main()

#ALR
# background=okno.cget('bg')
def pstryczkowanie(on, off1, off2, off3, ptri):
    global vAutoplay, vLoop, vRandom, vKoleyka
    # print("przełączono tryb")
    on.config(state=DISABLED, background="grey75")
    off1.config(state=NORMAL, background=okno.cget('bg'))
    off2.config(state=NORMAL, background=okno.cget('bg'))
    off3.config(state=NORMAL, background=okno.cget('bg'))
    if ptri == 1:
        vAutoplay = True
        vLoop = False
        vRandom = False
        vKoleyka = False
        autoplay()
    if ptri == 2:
        vLoop = True
        vAutoplay = False
        vRandom = False
        vKoleyka = False
        loop()
    if ptri == 3:
        vRandom = True
        vAutoplay = False
        vLoop = False
        vKoleyka = False
        random()
    if ptri == 4:
        vKoleyka = True
        vRandom = False
        vAutoplay = False
        vLoop = False
        koleyka()

vAutoplay = False
def autoplay():
    if vAutoplay == True:
        if media_player.get_state() == 6:
            next()
        okno.after(500, autoplay)

vLoop = False
def loop():
    if vLoop == True:
        if media_player.get_state() == 6:
            media_player.set_media(media_player.get_media())
            media_player.play()
        okno.after(500, loop)

vRandom = False
def random():
    global i
    if vRandom == True:
        if media_player.get_state() == 6:
            i = randint(0, len(utwory) - 1)
            zmianaUtworu(i) 
        okno.after(500, random)

vKoleyka = False
def koleyka():
        if vKoleyka == True:
            if media_player.get_state() == 6:
                try:
                    zmianaUtworu(kolejka[0])
                    kolejka.pop(0)
                    print(kolejka)
                except:
                    print("kaj te listy")
            okno.after(750, koleyka)


#LISTA
przyciskiLista = []
listaBool = False
def otworzListe():
    global listaBool, listaOkno
    if listaBool == False:
        listaOkno = Toplevel()
        listaOkno.resizable(0, 0)
        listaOkno.title("LPM - puszcza")
        listaOkno.geometry("226x200")

        lframe = ScrolledFrame(listaOkno, compound=RIGHT, canvasheight=200)
        lframe.pack(fill='both', expand=True)

        def dodajDoKolejki(poz):
            kolejka.append(poz)
            print(kolejka)

        for z in range(len(nazwyutowru)):
            plista = Button(lframe.interior, disabledforeground="black", anchor=W, justify=LEFT, width=25, text=utwory[z], command=lambda istala=z: zmianaUtworu(istala))
            zmiono = lambda istala2=z: print(istala2)

            plista.bind('<Button-3>', zmiono)
            plista.grid(column=0, row=z)
            przyciskiLista.append(plista)

            pkolejka = Button(lframe.interior, command=lambda istala2=z: dodajDoKolejki(istala2), width=20)
            pkolejka.grid(column=1, row=z)
        
        nieaktywnuUtwor()

        listaBool = True
        return 0
    if listaBool == True:
        listaOkno.destroy()
        przyciskiLista.clear()
        listaBool = False
        return 0
    
def nieaktywnuUtwor():
    global i
    for n in range(len(przyciskiLista)):
        przyciskiLista[n].config(state=NORMAL, background=okno.cget('bg'))
    przyciskiLista[i].config(state=DISABLED, background="grey75")    

zmiennaTytulu = True
def tytulZmienny():
    global okno, zmiennaTytulu, i
    if zmiennaTytulu == True:
        okno.title(str(utwory[i]))
        zmiennaTytulu = False
        okno.after(2000, tytulZmienny)
    elif zmiennaTytulu == False:
        okno.title(str(godzinowka(int(media_player.get_time()/1000))) + " / " + str(godzinowka(int(media_player.get_length()/1000))))
        zmiennaTytulu = True
        okno.after(2000, tytulZmienny)

    
#MAIN
def main():
    global okno, glosnoscText, labelCzasStaly, kolejek, listaPrzebojow, vol, labelCzasAktualny, pomijacz, aktualna, skalaDziweku, autoodtwarzanie, petla, przypadkowe, i, nazwyutowru, utwory, odtwarzanie, media_player, media, nastepny, poprzedni, playStop, menuglowne, autoodtwarzanie

    i = 0

    nazwyutowru = []
    utwory = []

    for sciezkaPliku in os.listdir(sciezka):
        if os.path.isfile(os.path.join(sciezka, sciezkaPliku)):
            nazwyutowru.append("muzyka/" + sciezkaPliku)
    # print(nazwyutowru, len(nazwyutowru))

    for sciezkaPliku in os.listdir(sciezka):
        if os.path.isfile(os.path.join(sciezka, sciezkaPliku)):
            utwory.append(sciezkaPliku)
    # print(utwory, len(utwory))


    odtwarzanie = True
    media_player = vlc.MediaPlayer()
    media = vlc.Media(nazwyutowru[i])
    media_player.set_media(media)

    #GUI

    okno = Tk()
    okno.title('FreeTy V0.8')
    okno.geometry('340x150')
    okno.resizable(0, 0)

    aktualna = Label(okno,text=utwory[i], height=3, wraplength=250)
    aktualna.place(x=170, y=24, anchor=CENTER, width=340)


    labelCzasAktualny = Label(okno, text="21:37")
    labelCzasAktualny.place(x=5, y=50, width=45)

    pomijacz = Scale(okno, from_=0, to=1, orient=HORIZONTAL, showvalue=False, resolution=0.01)
    pomijacz.place(x=55, y=50, width=230)
    pomijacz.bind("<Button-1>", stopPomijacz)
    pomijacz.bind("<ButtonRelease-1>", skipper)
    uaktualnijPomijacz()

    labelCzasStaly = Label(okno, text="21:37")
    labelCzasStaly.place(x=290, y=50, width=45)
    zmianaUtworu(i)


    poprzedni = Button(okno, text="Poprzedni", padx=10, pady=5, command=prev)
    poprzedni.place(x=5, y=75, width=90)

    playStop = Button(okno, text="Zatrzymaj/Puść", padx=14, pady=5, command=stop)
    playStop.place(x=100, y=75, width=140)

    nastepny = Button(okno, text="Następny", padx=10, pady=5, command=next)
    nastepny.place(x=245, y=75, width=90)

    glosnoscText = Label(okno, text="2137", width=3, height=1)
    glosnoscText.place(x=110, y=115)

    skalaDziweku = Scale(okno, from_=0, to=100, orient=HORIZONTAL, showvalue=False)
    skalaDziweku.place(x=5, y=115, width=110, height=40)
    skalaDziweku.bind("<Motion>", vol)
    skalaDziweku.set(60)

    autoodtwarzanie = Button(okno, text="A", padx=2, pady=2, disabledforeground="black")
    autoodtwarzanie.place(x=155, y=115, width=30)

    petla = Button(okno, text="L", padx=3, pady=2, disabledforeground="black")
    petla.place(x=190, y=115, width=30)
    
    przypadkowe = Button(okno, text="S", padx=2, pady=2, disabledforeground="black")
    przypadkowe.place(x=225, y=115, width=30)

    kolejek = Button(okno, text="K", padx=2, pady=2, disabledforeground="black")
    kolejek.place(x=260, y=115, width=30)

    autoodtwarzanie.config(command=lambda: pstryczkowanie(autoodtwarzanie, petla, przypadkowe, kolejek, 1))
    petla.config(command=lambda: pstryczkowanie(petla, autoodtwarzanie, przypadkowe, kolejek, 2))
    przypadkowe.config(command=lambda: pstryczkowanie(przypadkowe, autoodtwarzanie, petla, kolejek, 3))
    kolejek.config(command=lambda: pstryczkowanie(kolejek, autoodtwarzanie, petla, przypadkowe, 4))
    pstryczkowanie(autoodtwarzanie, petla, przypadkowe, kolejek, 1)

    listaPrzebojow = Button(okno, text=">", command=otworzListe)
    listaPrzebojow.place(x=305, y=115, width=30, height=28)

    #MENU

    menuglowne = Menu(okno)
    menupobierania = Menu(menuglowne, tearoff=0)
    menupobierania.add_command(label="YouTube", command=download)
    menuglowne.add_cascade(label="Pobierz", menu=menupobierania)

    menuustawien = Menu(menuglowne, tearoff=0)
    menuustawien.add_command(label="tryb nocny", command=0)
    menuustawien.add_separator()
    menuustawien.add_command(label="ustawienia", command=0)
    # menuglowne.add_cascade(label="Ustawienia", menu=menuustawien)

    okno.config(menu=menuglowne)
    vol()
    tytulZmienny()
    okno.mainloop()

 
main()

# TO DO:
# -root.tittle(zmienne)
# -okno z przenoszeniem plików
# -kolejka

# -wyświetla się w okno.title() nazwa utworu albo czas czy coś
# -minimalizacja do paska zadań
# -kolejkowanie
# -autopaczki
# -boczne okineko z wyborem muzyki
# -playlisty
# -automatyczny tryb nocny
# -tryb nocny
# -gui ładne (custom tkinter?)
# -kolorowe gui (.cget['bg'])
# -baza danych (nazwa utworu, id, playlista)






# DONE
# -ile uplynelo i ile trwa utwór
# -pasek stanu
# -poprzedni następny
# -pobieranie
# -głośność
# -odtwarzanie pobranych bez restartu
# -shuffler i loop
# -autoplay