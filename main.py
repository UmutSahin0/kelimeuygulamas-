# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:01:32 2022

@author: PC
"""
import tkinter as tk
import random
import os
from gtts.tts import gTTS

#dizin değiştirme
#os.chdir("C:\\Users\\PC\\Desktop\\Masaüstü\\kelimeler")
#kelimeler klasörünün içindekileri sıralayıp içerik değişkeninin içine attık
icerik=sorted(os.listdir())
#klasör içerisinden sadece sonu .txt ile bitenleri çektik.
icerik = [s for s in icerik if s.endswith('.txt')]
words=[]

ceviri=[]
k=-1
dosya_icerik=[]
tr_words=[]
eng_words=[]
flag=0
def iceri_aktar():
    #globaldeki değişkenleri çağırdık
    global words
    global txt_indexi
    global dosya_icerik
    #listboxta hangi içeriği seçtiysek onu açıp oku ve dosya_icerik değişkenine at
    with open((os.getcwd()+"\\"+icerik_sozluk[lb.curselection()[0]]),encoding="utf8") as dosya:
        dosya_icerik=dosya.readlines()
        
    if len(dosya_icerik)>0:
        etiket3["text"]=str(icerik_sozluk[lb.curselection()[0]])+" basariyla aktarildi."
    else:
        etiket3["text"]="Bir sorunla karşılaşıldı."
    
    
    
    

def yukle():
    #global değişkenleri getir
    global ceviri
    global k
    global dosya_icerik
    
    #dosya içeriğinin satır satır split edilip ingilizce ve türkçe olarak ayrı listelere alınması
    for i in dosya_icerik:
        eng_words,tr_words=i.split("-")
        if "\n" in tr_words:
            tr_words=tr_words.replace("\n","")
        
        #ayırdığımız kelimelerin ceviri değişkenine atılması
        ceviri.append([eng_words,tr_words])
        
    #çeviri listesini karıştırıyoruz. Düzenli olarak aynı sıra ile sormaması için
    random.shuffle(ceviri)
    etiket4["text"]="basariyla yuklendi çalışabilirsin"
    

def next_word(ceviri=ceviri):
    etiket_tr2["text"]=""
    etiket_eng2["text"]=""
    global side
    global k
    
    #side 1 olursa türkçe soracak,side 0 olursa ingilizce soracak.
    side=random.randint(0,1)
   
    k=k+1
    
    if k==len(ceviri):
        k=0
        random.shuffle(ceviri)
        
        
    #ingilizce mi türkçe mi soracak bunun sorgusunun yapıldığı yer.
    if side==1:
        etiket_tr2["text"]=ceviri[k][1]
    elif side==0:
        etiket_eng2["text"]=ceviri[k][0]

        
    #sıradaki kelimeye geçildiğinde translate için oluşturulan mp3 dosyası silinsin.
    if os.path.exists("text.mp3"):
        os.remove("text.mp3")
    
    
        
    
def show_answer():
    global k
    global ceviri
    
    if side==1:
        etiket_eng2["text"]=ceviri[k][0]
    elif side==0:
        etiket_tr2["text"]=ceviri[k][1]
    #k yı next_word ile değil show_answer ile arttırıyorum. anca show_answer yaptıkça k yı arttırıp
    #çevirideki kelimelerde bi sonraki sıraya geçebiliyoruz. Böylelikle çevirisini görmediğimiz kelime kalmıyor.
   
    
        
def translate():
    text = str(ceviri[k][0])
    language = 'en'
    speech = gTTS(text = text, lang = language, slow = False)
    speech.save("text.mp3")
    os.system("text.mp3")

    
        
    
form=tk.Tk()
#başlık ekleme
form.title("İngilizce - Türkçe Kelime Uygulaması")
#boyutlandırma
form.geometry("500x500+500+350")


next_word_button=tk.Button(form,text="next",command=next_word)
form.bind("<Return>",lambda event:next_word(ceviri))
next_word_button.pack(pady=20)


show_answer_button=tk.Button(form,text="show",command=show_answer)
form.bind("<,>",lambda event:show_answer())
show_answer_button.pack()

etiket_eng=tk.Label(text="English:")
etiket_eng.pack()
etiket_eng2=tk.Label(text="",font=(15))
etiket_eng2.pack()

etiket_tr=tk.Label(text="Turkish:")
etiket_tr.pack()
etiket_tr2=tk.Label(text="",font=(15))
etiket_tr2.pack()

#listbox ve ona ait labe,buton oluşturma
lb = tk.Listbox()
icerik_sozluk={}
for x,y in enumerate(icerik):
    lb.insert(x,y)
    icerik_sozluk[x]=y
lb.pack()


#butonunu oluşturma
iceri_aktar_buton=tk.Button(form,text="iceri aktar",command=iceri_aktar)
form.bind("<d>",lambda event:iceri_aktar())
iceri_aktar_buton.pack()
    #etiketini oluşturma
etiket3=tk.Label(form)
etiket3.pack()



#yukleme butonu
aktarilanlari_yukle_buton=tk.Button(form,text="aktarılanları yükle",command=yukle)
form.bind("<f>",lambda event:yukle())
aktarilanlari_yukle_buton.pack()
etiket4=tk.Label(form)
etiket4.pack()

#translate butonu
translate_button=tk.Button(form,text="translate",command=translate)
form.bind("<t>",lambda event:translate())
translate_button.pack()


#formu ekrana bastırma
form.mainloop()


