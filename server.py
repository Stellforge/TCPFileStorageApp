from socket import *
import os
import math

serverPort = 50000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(200)

def create_directory(directory_path):
    try:
        os.mkdir(directory_path)
        print(f"Klasör oluşturuldu: {directory_path}")
    except FileExistsError:
        print(f"Klasör zaten mevcut: {directory_path}")
    except FileNotFoundError:
        i=directory_path.rfind("/")

        create_directory(directory_path[0:i])
        create_directory(directory_path)
    except OSError as e:
        print(f"Klasör oluşturma hatası: {e}")
        exit()

open("./sifreler.txt","a").close()


while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected to {addr}")
    try:
        islem=connectionSocket.recv(2048).decode()
        if islem=="Giris":
            username,password=connectionSocket.recv(2048).decode().split("|")
            sifreDosya=open("./sifreler.txt","r")
            sifreler=sifreDosya.readlines()
            sifreDosya.close()
            kullanıcı=None
            for sifre in sifreler[1:]:
                u,p=sifre.split(";")
                p=p.replace("\n","")
                if u==username and p==password:
                    kullanıcı=sifre
            if(kullanıcı!=None):
                connectionSocket.send("1".encode())
            else:
                connectionSocket.send("0".encode())
        if islem=="Kayıt":
            username,password=connectionSocket.recv(2048).decode().split("|")
            sifreDosya=open("./sifreler.txt","r")
            sifreler=sifreDosya.readlines()
            sifreDosya.close()
            kullanıcı=None
            for sifre in sifreler[1:]:
                u,p=sifre.split(";")
                if u==username :
                    kullanıcı=sifre
            if(kullanıcı!=None):
                connectionSocket.send("0".encode())
            else:
                sifreDosya=open("./sifreler.txt","a")
                sifreDosya.write(f"\n{username};{password}")
                sifreDosya.close()
                create_directory("./Files/"+username)
                connectionSocket.send("1".encode())
        if islem=="indir":
            username=connectionSocket.recv(2048).decode()
            file_list = os.listdir("./Files/"+username+"/")
            connectionSocket.send(str.join(";",file_list).encode())
            secilen=connectionSocket.recv(2048).decode()
            dosyaYol=f"./Files/{username}/{secilen}"

            file_name = os.path.basename(dosyaYol)
            size = os.path.getsize(dosyaYol)
            paketSayisi=math.ceil(size/2048)
            file_name= ""+file_name
            connectionSocket.send(f"{paketSayisi};{file_name}".encode())

            i=paketSayisi
            file = open(dosyaYol,"rb")
            dosyaBytes=file.read()
            file.close()
            print(len(dosyaBytes))

            while i>=0:
                paket=dosyaBytes[i*2048:i*2048+2048]
                connectionSocket.send(paket)
                i-=1
        if islem=="kaydet":
            username,paketSayisi,fileName=connectionSocket.recv(2048).decode().split(";")

            file=open("./Files/"+username+"/"+fileName,"wb")
            i=int(paketSayisi)
            pakets=bytearray()
            while i>=0:
                paket=connectionSocket.recv(2048)
                pakets=paket+pakets
                
                i-=1
            print(len(pakets))
            file.write(pakets)
            file.close()
    finally:
        connectionSocket.close()