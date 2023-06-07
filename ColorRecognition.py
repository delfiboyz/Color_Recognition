import cv2
import numpy as np
import pandas as pd

# Mengimpor file csv yang berisi daftar nama warna dan nilainya dalam format RGB
index=["color", "color_name", "hex", "R", "G", "B"]
colors = pd.read_csv('colors.csv', names=index, header=None)

# Inisialisasi variabel global sebagai penanda ketika klik kursor mouse aktif
clicked = False
r = g = b = xpos = ypos = 0

# Fungsi untuk menghitung jarak Euclidean terdekat antara warna yang dikenali dan warna yang terdeteksi oleh kamera
def get_color_name(R,G,B):
    minimum = 10000
    for i in range(len(colors)):
        d = abs(R-int(colors.loc[i,"R"])) + abs(G-int(colors.loc[i,"G"]))+ abs(B-int(colors.loc[i,"B"]))
        if d <= minimum:
            minimum = d
            cname = colors.loc[i,"color_name"]
    return cname

# Fungsi untuk mengambil nilai RGB pada titik koordinat X,Y
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = frame[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# Konfigurasi kamera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

# Membuat jendela dengan nama 'image'
cv2.namedWindow('image')

# Menampilkan tampilan kamera dan memproses data
while(1):
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Menambahkan kotak warna atas untuk menampilkan nama warna
    cv2.rectangle(frame, (20,20), (750,60), (b,g,r), -1)
   
    # Menampilkan nama warna yang terdeteksi
    text = get_color_name(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
    cv2.putText(frame, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2,cv2.LINE_AA)

    # Jika ada warna yang diklik, tambahkan frame di sekitar warna tersebut
    if clicked:
        cv2.rectangle(frame, (xpos-20, ypos-20), (xpos+20, ypos+20), (255,255,255), 2)
        cv2.putText(frame, get_color_name(r,g,b), (xpos+25, ypos-25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2,cv2.LINE_AA)
        clicked = False
   
    # Mengatur fungsi pemanggilan balik mouse
    cv2.setMouseCallback('image',draw_function)

    # Menampilkan gambar pada window
    cv2.imshow("image",frame)

    if cv2.waitKey(20) & 0xFF ==27:
        break

camera.release()
cv2.destroyAllWindows()
