# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:01:32 2022

@author: Umut Şahin
"""
import tkinter as tk
import random
import os
from gtts.tts import gTTS
import pandas as pd
import numpy as np


icerik=sorted(os.listdir())
#klasör içerisinden sadece sonu .txt ile bitenleri çektik.
icerik = [s for s in icerik if s.endswith('.txt')]
words=[]
merged_df = pd.DataFrame()
ceviri=[]
k=-1
dosya_icerik=[]
tr_words=[]
eng_words=[]
flag=0
secilen_txt_ismi =''
dosya_yolu=''


def iceri_aktar():
    #globaldeki değişkenleri çağırdık
    global words
    global txt_indexi
    global dosya_icerik
    global secilen_txt_ismi
    global dosya_yolu
    #listboxta hangi içeriği seçtiysek onu açıp oku ve dosya_icerik değişkenine at
    with open((os.getcwd()+"\\"+icerik_sozluk[lb.curselection()[0]]),encoding="utf8") as dosya:
        dosya_icerik=dosya.readlines()
    

    if len(dosya_icerik)>0:
        etiket3["text"]=str(icerik_sozluk[lb.curselection()[0]])+" basariyla aktarildi."
    else:
        etiket3["text"]="Bir sorunla karşılaşıldı."

    secilen_txt_ismi = str(icerik_sozluk[lb.curselection()[0]]).split('.')[0]

    dosya_yolu = f'{secilen_txt_ismi}_merged.csv'

    # Eğer dosya mevcutsa oku, yoksa oluşturup sonra oku
    if os.path.exists(dosya_yolu):
        merged_df = pd.read_csv(dosya_yolu)
    else:
        # Veri çerçevesi oluşturun (örneğin bir boş DataFrame)
        merged_df = pd.DataFrame(columns=['turkce', 'ingilizce','puan','olasilik'])  # Sütun isimlerini buraya göre değiştirin
        
        # Dosyayı oluşturun ve başlıkları yazın
        merged_df.to_csv(dosya_yolu, index=False)
        
        # Dosyayı tekrar okuyun
        merged_df = pd.read_csv(dosya_yolu)
    
    
    
    

def yukle():
    #global değişkenleri getir
    global ceviri
    global k
    global dosya_icerik
    global kelimeler
    global dosya_yolu
    global merged_df
    tr_words=[]
    eng_words=[]
    kelimeler = pd.DataFrame()
    merged_df = pd.read_csv(dosya_yolu)
    
    #Bu kısmın olma nedeni. TXT güncellenirse ekstra olan kelimeler de merge_df'e ve ordan da .csv'e dahil edilebilsin diye.
    for i in dosya_icerik:
        eng_word,tr_word=i.split("-")
        if "\n" in tr_word:
            tr_word=tr_word.replace("\n","")
        eng_words.append(eng_word)
        tr_words.append(tr_word)
        #ayırdığımız kelimelerin ceviri değişkenine atılması
        ceviri.append([eng_word,tr_word])
        

    kelimeler['turkce']=tr_words
    kelimeler['ingilizce']=eng_words

    #Eğer farklılık varsa diye txt ile .csv arasında merge işlemi yapılıyor
    merged_df = pd.merge(merged_df, kelimeler, on='turkce', how='right')
    merged_df = merged_df.drop(columns=['ingilizce_x'])
    merged_df = merged_df.rename(columns={'ingilizce_y': 'ingilizce'})

    merged_df['puan'] = merged_df['puan'].fillna(value=80)
    total_percentage = merged_df['puan'].sum()
    merged_df['olasilik'] = merged_df['puan'] / total_percentage * 100

     # yeni eklenen kelime varsa puan null olacak. buna 0 puan veriyoruz.
    merged_df[['turkce','ingilizce','puan','olasilik']].to_csv(f'{dosya_yolu}')


    

def next_word(ceviri=ceviri):
    etiket_tr2["text"]=""
    etiket_eng2["text"]=""
    global side
    global k
    
    #side 1 olursa türkçe soracak,side 0 olursa ingilizce soracak.
    side=random.randint(0,1)
   


    # Ağırlıklı rastgele seçim için numpy.random.choice kullanalım
    selected_row = np.random.choice(merged_df.index, p=merged_df['olasilik']/100)

    k = selected_row
    
        
        
    #ingilizce mi türkçe mi soracak bunun sorgusunun yapıldığı yer.
    if side==1:
        etiket_tr2["text"]=ceviri[selected_row][1]
    elif side==0:
        etiket_eng2["text"]=ceviri[selected_row][0]

        
    #sıradaki kelimeye geçildiğinde translate için oluşturulan mp3 dosyası silinsin.
    if os.path.exists("text.mp3"):
        os.remove("text.mp3")


def dogru(ceviri=ceviri):
    global merged_df
   
    kosul = merged_df['ingilizce'] == ceviri[k][0]

    if merged_df.loc[kosul, 'puan'].iloc[0] > 5:
        merged_df.loc[kosul, 'puan'] -= 5

        total_percentage = merged_df['puan'].sum()
        merged_df['olasilik'] = merged_df['puan'] / total_percentage * 100
        merged_df[['turkce','ingilizce','puan','olasilik']].to_csv(f'{secilen_txt_ismi}_merged.csv')
        print('Puan islendi')
    else:
        pass

def yanlis(ceviri=ceviri):
    global merged_df
   
    kosul = merged_df['ingilizce'] == ceviri[k][0]

    if merged_df.loc[kosul, 'puan'].iloc[0] <= 78:
        merged_df.loc[kosul, 'puan'] += 2
        total_percentage = merged_df['puan'].sum()
        merged_df['olasilik'] = merged_df['puan'] / total_percentage * 100

        merged_df[['turkce','ingilizce','puan','olasilik']].to_csv(f'{secilen_txt_ismi}_merged.csv')
        print('Puan islendi')
    else:
        pass
    
    
    
        
    
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


next_word_buton=tk.Button(form,text="next word",command=next_word)
form.bind("<Return>",lambda event:next_word(ceviri))
next_word_buton.pack(pady=20)

dogru_buton=tk.Button(form,text="dogru",command=dogru)
form.bind("<Return>",lambda event:dogru(ceviri))
dogru_buton.pack(pady=20)

yanlis_buton=tk.Button(form,text="yanlis",command=yanlis)
form.bind("<Return>",lambda event:yanlis(ceviri))
yanlis_buton.pack(pady=20)



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