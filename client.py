from socket import *
import os
import math
import time

serverName = '127.0.0.1'  # Sunucu IP adresi buraya yazılacak
serverPort = 50000
clientPort = 60001
loginUsername=""
while True:
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.bind(('', clientPort))
        clientSocket.connect((serverName, serverPort))

        islem=input("1-Giriş Yap 2-Kayıt Ol \n=> ")
        if(islem=="1"):
            username=input("Kullanıcı adı : ")
            password=input("Şifre : ")
            clientSocket.send("Giris".encode())
            clientSocket.send(f"{username}|{password}".encode())
            if clientSocket.recv(2048).decode() == "1":
                print("< < Giriş yapıldı > >")
                loginUserame=username
            else:
                print("< < Giriş Başarısız > >")
                clientSocket.close()
                exit()
        elif(islem=="2"):
            username=input("Kullanıcı adı: ")
            password=input("Şifre: ")
            clientSocket.send("Kayıt".encode())
            clientSocket.send(f"{username}|{password}".encode())
            if clientSocket.recv(2048).decode() == "1":
                print("-- Kayıt yapıldı --")
                loginUsername=username
            else:
                print("-- Kayıt Başarısız --")
                clientSocket.close()
                exit()
        
        islem=input("1-İndir 2-Yükle \n=> ")

        if islem in ["1","2"]:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.bind(('', clientPort))
            clientSocket.connect((serverName, serverPort))

        if islem=="1":
            clientSocket.send("indir".encode())
            time.sleep(0.2)
            clientSocket.send(loginUsername.encode())
            dosyalar=clientSocket.recv(2048).decode().split(";")
            i=0
            for dosya in dosyalar:
                print(f"{i} - {dosya}")
                i+=1
            dosyaIndex=input("Seçtiğiniz dosyanın başındaki sayıyı gir \n=> ")
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            print(download_path)
            dosya=dosyalar[int(dosyaIndex)]
            clientSocket.send(dosya.encode())

            packetCount,fileName= clientSocket.recv(2048).decode().split(";")
            i=int(packetCount)
            file=open(download_path+"/"+fileName,"wb")
            pakets=bytearray()
            while i>=0:
                paket=clientSocket.recv(2048)
                pakets=paket+pakets
                #print(i)
                i-=1
            file.write(pakets)
            print(len(pakets))
            file.close()
            print("Dosya Alındı")
        elif islem=="2":
            dosyaYol=input("Kaydedilecek dosya yolunu gir ( \\ ları / a çevir ) \n=>")
            dosyaYol=dosyaYol.replace("\\","/")
            file_name = os.path.basename(dosyaYol)
            size = os.path.getsize(dosyaYol)
            paketSayisi=math.ceil(size/2048)

            clientSocket.send("kaydet".encode())
            time.sleep(1)
            print(loginUsername)
            print(paketSayisi)
            print(file_name)
            clientSocket.send(f"{loginUsername};{str(paketSayisi)};{file_name}".encode())
            i=paketSayisi
            file = open(dosyaYol,"rb")
            dosyaBytes=file.read()
            file.close()
            print(len(dosyaBytes))
            while i>=0:
                paket=dosyaBytes[i*2048:i*2048+2048]
                clientSocket.send(paket)

                i-=1
            print("Dosya Gönderildi..")

    finally:
        clientSocket.close()

    break