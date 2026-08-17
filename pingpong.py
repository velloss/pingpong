# Game Pong - Navigasi Menu Menggunakan Panah Keyboard & Enter
import turtle
import time

# 1. SETUP LAYAR UTAMA
win = turtle.Screen()
win.title("Game Pong - Keyboard Navigation Menu")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Status Game: "MENU", "DIFFICULTY_MENU", "PLAYING"
status_game = "MENU"
mode = "1"           # "1" = 2 Players, "2" = Bot
bot_speed = 0.22     # Kecepatan bawaan bot

# Indeks Pilihan Menu (0 = Pilihan pertama, 1 = Pilihan kedua, dst)
pilihan_aktif = 0

# Skor Utama
skor_a = 0
skor_b = 0

# Variabel Jeda Waktu (Countdown)
waktu_mulai_bola = 0
bola_sedang_jeda = False

# Dictionary untuk melacak tombol ditahan (Smooth Movement Gameplay)
keys = {"w": False, "s": False, "Up": False, "Down": False}

# Fungsi status tombol keyboard untuk gerakan papan
def press_w(): keys["w"] = True
def release_w(): keys["w"] = False
def press_s(): keys["s"] = True
def release_s(): keys["s"] = False
def press_up(): keys["Up"] = True
def release_up(): keys["Up"] = False
def press_down(): keys["Down"] = True
def release_down(): keys["Down"] = False

# 2. MEMBUAT OBJEK GRAFIS GAME
papan_a = turtle.Turtle()
papan_a.speed(0)
papan_a.shape("square")
papan_a.color("white")
papan_a.shapesize(stretch_wid=5, stretch_len=1)
papan_a.penup()
papan_a.goto(-350, 0)
papan_a.hideturtle()

papan_b = turtle.Turtle()
papan_b.speed(0)
papan_b.shape("square")
papan_b.color("white")
papan_b.shapesize(stretch_wid=5, stretch_len=1)
papan_b.penup()
papan_b.goto(350, 0)
papan_b.hideturtle()

bola = turtle.Turtle()
bola.speed(0)
bola.shape("circle")
bola.color("white")
bola.penup()
bola.goto(0, 0)
bola.dx = 0.35
bola.dy = 0.35
bola.hideturtle()

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

# Teks khusus untuk hitung mundur di tengah layar
pen_countdown = turtle.Turtle()
pen_countdown.speed(0)
pen_countdown.color("yellow")
pen_countdown.penup()
pen_countdown.hideturtle()

# 3. FUNGSI LAYOUT & RE-DRAWING GUI

def gambar_menu_utama():
    pen.clear()
    pen.goto(0, 120)
    pen.write("GAME PONG", align="center", font=("Courier", 36, "bold"))
    
    # Cetak opsi dengan indikator panah (>) jika sedang aktif terpilih
    panah_0 = "> " if pilihan_aktif == 0 else "  "
    panah_1 = "> " if pilihan_aktif == 1 else "  "
    
    pen.goto(0, 10)
    pen.write(f"{panah_0}Main Berdua (2 Players)", align="center", font=("Courier", 18, "normal"))
    pen.goto(0, -30)
    pen.write(f"{panah_1}Lawan Komputer (Bot)", align="center", font=("Courier", 18, "normal"))
    
    pen.goto(0, -150)
    pen.color("gray")
    pen.write("Navigasi: Panah Atas/Bawah | Pilih: ENTER", align="center", font=("Courier", 12, "italic"))
    pen.color("white")

def gambar_menu_kesulitan():
    pen.clear()
    pen.goto(0, 120)
    pen.write("PILIH KESULITAN BOT", align="center", font=("Courier", 28, "bold"))
    
    panah_0 = "> " if pilihan_aktif == 0 else "  "
    panah_1 = "> " if pilihan_aktif == 18 else "  " # Indikator panah dinamis
    panah_1 = "> " if pilihan_aktif == 1 else "  "
    panah_2 = "> " if pilihan_aktif == 2 else "  "
    
    pen.goto(0, 20)
    pen.write(f"{panah_0}Mudah (Easy)", align="center", font=("Courier", 18, "normal"))
    pen.goto(0, -20)
    pen.write(f"{panah_1}Normal (Medium)", align="center", font=("Courier", 18, "normal"))
    pen.goto(0, -60)
    pen.write(f"{panah_2}Sulit (Hard)", align="center", font=("Courier", 18, "normal"))
    
    pen.goto(0, -150)
    pen.color("gray")
    pen.write("Navigasi: Panah Atas/Bawah | Pilih: ENTER", align="center", font=("Courier", 12, "italic"))
    pen.color("white")

# 4. LOGIKA NAVIGASI TOMBOL INTERAKTIF DI MENU

def menu_ke_atas():
    global pilihan_aktif
    if status_game == "MENU" or status_game == "DIFFICULTY_MENU":
        # Kurangi indeks menu, jika mentok di atas kembali ke bawah (looping)
        pilihan_aktif -= 1
        batas_maks = 1 if status_game == "MENU" else 2
        if pilihan_aktif < 0:
            pilihan_aktif = batas_maks
        
        # Gambar ulang menu untuk memperbarui posisi tanda panah
        if status_game == "MENU": gambar_menu_utama()
        else: gambar_menu_kesulitan()
    else:
        # Jika sedang bermain, tombol panah berfungsi sebagai kontrol gerakan papan
        press_up()

def menu_ke_bawah():
    global pilihan_aktif
    if status_game == "MENU" or status_game == "DIFFICULTY_MENU":
        # Tambah indeks menu, jika mentok di bawah kembali ke atas (looping)
        pilihan_aktif += 1
        batas_maks = 1 if status_game == "MENU" else 2
        if pilihan_aktif > batas_maks:
            pilihan_aktif = 0
            
        if status_game == "MENU": gambar_menu_utama()
        else: gambar_menu_kesulitan()
    else:
        press_down()

def tekan_enter():
    global status_game, mode, bot_speed, pilihan_aktif
    if status_game == "MENU":
        if pilihan_aktif == 0:
            mode = "1" # Mode 2 Players
            mulai_game()
        elif pilihan_aktif == 1:
            mode = "2" # Mode Bot
            status_game = "DIFFICULTY_MENU"
            pilihan_aktif = 0 # Reset indeks untuk menu berikutnya
            gambar_menu_kesulitan()
            
    elif status_game == "DIFFICULTY_MENU":
        if pilihan_aktif == 0:
            bot_speed = 0.18  # Easy
        elif pilihan_aktif == 1:
            bot_speed = 0.30  # Medium
        elif pilihan_aktif == 2:
            bot_speed = 0.45  # Hard
        mulai_game()

# REGISTER INPUT UTAMA KEYBOARD
win.listen()
win.onkeypress(press_w, "w")
win.onkeyrelease(release_w, "w")
win.onkeypress(press_s, "s")
win.onkeyrelease(release_s, "s")

# Tombol Panah digabung fungsionalitasnya antara navigasi menu dan gameplay
win.onkeypress(menu_ke_atas, "Up")
win.onkeyrelease(release_up, "Up")
win.onkeypress(menu_ke_bawah, "Down")
win.onkeyrelease(release_down, "Down")

# Tombol konfirmasi pilihan
win.onkeypress(tekan_enter, "Return") # "Return" adalah sebutan tombol Enter di Turtle

# 5. LOGIKA GAMEPLAY

def mulai_game():
    global status_game, skor_a, skor_b
    status_game = "PLAYING"
    pen.clear()
    
    papan_a.showturtle()
    papan_b.showturtle()
    bola.showturtle()
    
    skor_a = 0
    skor_b = 0
    papan_a.goto(-350, 0)
    papan_b.goto(350, 0)
    
    update_skor()
    trigger_jeda_bola()

def update_skor():
    pen.clear()
    pen.goto(0, 250)
    nama_b = "Komputer" if mode == "2" else "Pemain B"
    pen.write(f"Pemain A: {skor_a}   {nama_b}: {skor_b}", align="center", font=("Courier", 24, "bold"))

def trigger_jeda_bola():
    global waktu_mulai_bola, bola_sedang_jeda
    bola.goto(0, 0)
    bola_sedang_jeda = True
    waktu_mulai_bola = time.time()

# Tampilkan UI menu utama pertama kali
gambar_menu_utama()

# 6. LOOP UTAMA GAME
while True:
    win.update()

    if status_game == "PLAYING":
        
        # LOGIKA HITUNG MUNDUR (COUNTDOWN) 3 DETIK
        if bola_sedang_jeda:
            selisih_waktu = time.time() - waktu_mulai_bola
            detik_tersisa = 3 - int(selisih_waktu)
            
            if detik_tersisa > 0:
                pen_countdown.clear()
                pen_countdown.goto(0, -30)
                pen_countdown.write(f"{detik_tersisa}", align="center", font=("Courier", 48, "bold"))
                continue 
            else:
                pen_countdown.clear()
                bola_sedang_jeda = False 

        # GERAKAN HALUS (SMOOTH MOVEMENT) PAPAN
        if keys["w"] and papan_a.ycor() < 250:
            papan_a.sety(papan_a.ycor() + 0.5)
        if keys["s"] and papan_a.ycor() > -240:
            papan_a.sety(papan_a.ycor() - 0.5)
            
        if mode == "1": 
            if keys["Up"] and papan_b.ycor() < 250:
                papan_b.sety(papan_b.ycor() + 0.5)
            if keys["Down"] and papan_b.ycor() > -240:
                papan_b.sety(papan_b.ycor() - 0.5)

        # GERAKAN BOT OTOMATIS
        if mode == "2" and bola.dx > 0:
            if papan_b.ycor() < bola.ycor() and papan_b.ycor() < 250:
                papan_b.sety(papan_b.ycor() + bot_speed)
            elif papan_b.ycor() > bola.ycor() and papan_b.ycor() > -240:
                papan_b.sety(papan_b.ycor() - bot_speed)

        # Gerakkan Bola
        bola.setx(bola.xcor() + bola.dx)
        bola.sety(bola.ycor() + bola.dy)

        # Batas Atas dan Bawah (Pantulan Bola)
        if bola.ycor() > 290:
            bola.sety(290)
            bola.dy *= -1
        if bola.ycor() < -290:
            bola.sety(-290)
            bola.dy *= -1

        # Gol Kanan (Skor Pemain A)
        if bola.xcor() > 390:
            bola.dx *= -1
            skor_a += 1
            update_skor()
            trigger_jeda_bola()

        # Gol Kiri (Skor Pemain B / Bot)
        if bola.xcor() < -390:
            bola.dx *= -1
            skor_b += 1
            update_skor()
            trigger_jeda_bola()

        # Deteksi Tabrakan Bola dengan Papan Kanan
        if (340 < bola.xcor() < 350) and (papan_b.ycor() - 50 < bola.ycor() < papan_b.ycor() + 50):
            bola.setx(340)
            bola.dx *= -1

        # Deteksi Tabrakan Bola dengan Papan Kiri
        if (-350 < bola.xcor() < -340) and (papan_a.ycor() - 50 < bola.ycor() < papan_a.ycor() + 50):
            bola.setx(-340)
            bola.dx *= -1
