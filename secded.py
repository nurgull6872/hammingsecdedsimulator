import tkinter as tk
from tkinter import messagebox
import random

def encodeHamming(dataBits): #girilen verime hamming koda dönüştüren fonksiyonum
    bitsNumber = len(dataBits) 
    pariteBitsNumber = 0 
    
    while (2 ** pariteBitsNumber) < (bitsNumber + pariteBitsNumber + 1):#gerekli olacak parite bits sayımı bulduğum döngü
        pariteBitsNumber += 1
    total = bitsNumber + pariteBitsNumber + 1  
    
    hammingCodeList = ['0'] * total #başta data ve parite konumlarımı 0 olarak tuttuğum listeem
    
    j = 0
    
    for i in range(1, total):
        if not (i & (i - 1)) == 0:  # döngüm binary olarak sayı ve bir önceki sayıyı andler ve sonucuna göre veri bitlerini belirler
            hammingCodeList[i - 1] = dataBits[j]
            j += 1
   
    for i in range(pariteBitsNumber):
        pos = 2 ** i
        parity = 0
        for k in range(1, total):
            if k & pos:  # parite biti kendisini de kapsar
                parity ^= int(hammingCodeList[k - 1])
        hammingCodeList[pos - 1] = str(parity)
   
    # secded için ekstra olarak bulunan biti hesapladım
    bits = hammingCodeList[:-1]  
    numberOfOne = bits.count('1')
    totalParity = numberOfOne % 2
    hammingCodeList[-1] = str(totalParity)

    return ''.join(hammingCodeList)

def decode(codeWord):#hem hatayı tespit edip hem de gerekirse düzeltmesini yapan fonksiyonum
    n = len(codeWord)
    r = 0
    
    while (2 ** r) < n: #parite bit sayısını buldum
        r += 1
    syndrome = 0  #hata yokken sendrom kelimem
   
    for i in range(r):
        pos = 2 ** i
        parity = 0
        for k in range(1, n):
            if k & pos:
                parity ^= int(codeWord[k - 1])
        if parity:
            syndrome += pos
    
    overallParity = sum(int(codeWord[i]) for i in range(n - 1)) % 2
    overallParityReceived = int(codeWord[-1])
    
    if syndrome == 0 and overallParity == overallParityReceived:
        return "Veri doğru hata bulunamadı.", codeWord
    elif syndrome != 0 and overallParity != overallParityReceived:
        corrected = list(codeWord)
        corrected[syndrome - 1] = '0' if corrected[syndrome - 1] == '1' else '1'
        return f"Hata tespit edildi ve düzeltildi! Pozisyonu: {syndrome}", ''.join(corrected)
    else:
        return "Çift hata tespit edildi, düzeltilemez!", codeWord


def controlPowerOfTwo(n):
    return n > 0 and (n & (n - 1)) == 0

def getDataBits(codeword): #sadece kullanıcımın girdiği veriyi aldığım fonksiyonum
    dataInput = []

    for position in range(1, len(codeword)):
        if not controlPowerOfTwo(position):
            dataInput.append(codeword[position - 1])  

    return ''.join(dataInput)

def displayHammingBits(canvas, codeword, title="",highlight_index=None): #bit kutularımı ve üstündeki numaraların stillerini ayarlaadığım fonksiyon
    canvas.delete("all")
    startX = 10
    startY = 10
    canvas.create_text(startX, startY, anchor="nw", text=title, font=("Arial", 8, "bold"), fill="black")

    for index, bit in enumerate(codeword):
        position = index + 1  

        if controlPowerOfTwo(position):
            color = "blue"
        else:
            color = "white"
        
        if highlight_index is not None and index == highlight_index:
            color = "yellow"

        newX = startX + index * 35
        newY = startY + 20

        canvas.create_rectangle(newX, newY, newX + 30, newY + 30, fill=color, outline="white")
        canvas.create_text(newX + 15, newY + 15, text=bit, font=("Arial", 11), fill="gray")


def process(): # hata ve uyarı mesajlarımı verdiğim ve işleyişi ayarladığım kısım
    global originalData, current_codeWord, corrected_codeWord, error_positions
    userInputData = entry.get()
    if len(userInputData) not in [8, 16, 32] or not all(c in '01' for c in userInputData):
        messagebox.showerror("VERİ GİRİŞİ HATASI", "Lütfen 8, 16 veya 32 bitlik ikili veri girin.")
        return
    originalData = userInputData
    current_codeWord = encodeHamming(userInputData)
    corrected_codeWord = current_codeWord
    error_positions.clear()
    displayHammingBits(canvas_encoded, current_codeWord, "Oluşturulmuş Hamming Kodu")
    canvas_errored.delete("all")
    canvas_corrected.delete("all")
    label_user_data.config(text="", fg="orange")

def addError(): # kendine seçilmemiş konum seçip 1se 0, 0 sa 1 yapan fonksiyonum
    global current_codeWord, error_positions
    if not current_codeWord:
        return
    
    # hata eklenmemiş yeni bir pozisyon için döngüm
    while True:
        pos = random.randint(0, len(current_codeWord) - 1)
        if pos not in error_positions or len(error_positions) >= len(current_codeWord):
            break
    
    error_positions.append(pos)
    
    code_list = list(current_codeWord)
    code_list[pos] = '1' if code_list[pos] == '0' else '0'
    current_codeWord = ''.join(code_list)
    
    displayHammingBits(canvas_errored, current_codeWord, "Hata Eklenmiş Kod")


def correct():# hata düzelt butonuna basılınca yapılacaklar geri bildirimleri ayarladığım fonksiyon
    global current_codeWord, corrected_codeWord
    if not current_codeWord:
        return

    if len(error_positions) > 1:
        displayHammingBits(canvas_corrected, current_codeWord, "1'den Fazla Hata")
        label_user_data.config(
            text=" Birden fazla hata bulundu.Düzeltilemez!", fg="red"
        )
        return
    msg, corrected = decode(current_codeWord)
    corrected_codeWord = corrected
    
    _, fixed_position = find_error_position(current_codeWord, corrected)

    displayHammingBits(canvas_corrected, corrected_codeWord, "Düzeltilmiş Kod", highlight_index=fixed_position)
    
    label_user_data.config(
        text=f" {msg}\nOrijinal Veri: {getDataBits(corrected)}", fg="green"
    )

def find_error_position(original, corrected):# karşılaştırarak farklı hatalı biti bulan fonksiyonum
    for i in range(len(original)):
        if original[i] != corrected[i]:
            return "Hatalı bit bulundu.", i
    return "Hata bulunamadı.", None

root = tk.Tk()
root.title("Nurgul's Hamming SEC-DED Simülatörü")
root.geometry("950x650")
root.configure(bg="#eaeeff")  

tk.Label(root, text="Veri girin (8/16/32 bit):", font=("Arial", 15), bg="#eaeeff").pack()
entry = tk.Entry(root, font=("Courier", 15), width=40)
entry.pack(pady=5)

tk.Button(root, text="Hamming Kod Oluştur", command=process, bg="#52db72", fg="white", width=20).pack(pady=10)
canvas_encoded = tk.Canvas(root, width=850, height=70, bg="white")
canvas_encoded.pack(pady=5)

tk.Button(root, text="Hata Ekle", command=addError, bg="#ff0019", fg="white", width=20).pack(pady=10)
canvas_errored = tk.Canvas(root, width=850, height=70, bg="white")
canvas_errored.pack(pady=5)

tk.Button(root, text="Hata Düzelt", command=correct, bg="#6fb5ff", fg="white", width=20).pack(pady=10)
canvas_corrected = tk.Canvas(root, width=850, height=70, bg="white")
canvas_corrected.pack(pady=5)

label_user_data = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#eaeeff", fg="darkgreen")
label_user_data.pack(pady=10)

originalData = ""
current_codeWord = ""
corrected_codeWord = ""
error_positions = []

root.mainloop()