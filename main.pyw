from tkinter import *
import os
import vlc
from pytube import *
from tkinter import Menu

sciezka = 'muzyka'
i = 0

nazwyutowru = []
utwory = []

x = 1
x + x = y
print(y)

for file_path in os.listdir(sciezka):
    if os.path.isfile(os.path.join(sciezka, file_path)):
        nazwyutowru.append("muzyka/" + file_path)
print(nazwyutowru, len(nazwyutowru))

for file_path in os.listdir(sciezka):
    if os.path.isfile(os.path.join(sciezka, file_path)):
        utwory.append(file_path)
print(utwory, len(utwory))


odtwarzanie = True
player = vlc.Instance() 
media_list = player.media_list_new() 
media_player = player.media_list_player_new() 


for x in nazwyutowru:
    media = player.media_new(x)
    media_list.add_media(media)
    media_player.set_media_list(media_list)


def stop():
    global odtwarzanie, i
    print(utwory[i])
    print(i)
    if odtwarzanie == True :
        print("puszczono")
        media_player.play()
        odtwarzanie = False
        return 0
    if odtwarzanie == False:
        print("zatrzymano")
        media_player.set_pause(1)
        odtwarzanie = True
        return 0
    
def next():
    global i
    if i < len(utwory) - 1:
        media_player.next()
        i += 1
        aktualna.config(text=utwory[i])
        print(i)
    
def prev():
    global i 
    if i > 0:
        media_player.previous()
        i -= 1
        aktualna.config(text=utwory[i])
        print(i)

def vol(zmiennaponic=None):
    vol = int(suwak.get())
    print(vol)
    # pyautogui.press('volumedown', 100)
    # pyautogui.press('volumeup', int(vol/2))
    media_player.get_media_player().audio_set_volume(vol)

    
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
    global src, link
    src = YouTube(str(link.get()))
    video = src.streams.filter(only_audio=True).first()
    destination = 'muzyka'
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(src.title + " pobrano")
        

okno = Tk()
okno.title('Muaplay V1.4beta01')
okno.geometry('300x200')
okno.resizable(0, 0)
okno['padx'] = 10

aktualna = Label(okno,text=utwory[i], height=3, wraplength=250)
aktualna.grid(column=0, row=0, columnspan=3)

poprzedni = Button(okno, text="Poprzedni", padx=10, pady=5, command=prev)
poprzedni.grid(column=0, row=1)

stopy = Button(okno, text="Zatrzymaj/Puść", padx=14, pady=5, command=stop)
stopy.grid(column=1, row=1)

suwak = Scale(okno, from_=100, to=0)
suwak.grid(column=0, row=2, sticky=E)
suwak.bind("<ButtonRelease-1>", vol)
suwak.set(50)
vol()

nastepny = Button(okno, text="Następny", padx=10, pady=5, command=next)
nastepny.grid(column=2, row=1)


#MENU

menuglowne = Menu(okno)
menupobierania = Menu(menuglowne, tearoff=0)
menupobierania.add_command(label="YouTube", command=download)
menuglowne.add_cascade(label="Pobierz", menu=menupobierania)

menuustawien = Menu(menuglowne, tearoff=0)
menuustawien.add_command(label="tryb nocny", command=0)
menuustawien.add_separator()
menuustawien.add_command(label="ustawienia", command=0)
menuglowne.add_cascade(label="Ustawienia", menu=menuustawien)

okno.config(menu=menuglowne)

okno.mainloop()

# TO DO:
# -playlisty
# -szufla i lub
# -bez restartu na poczatku
# -tryb nocny