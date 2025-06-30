import string
import secrets
import math
import tkinter as tk
from tkinter import ttk, messagebox
from zxcvbn import zxcvbn

class SifreOlusturucu:
    def __init__(self, master):
        self.master = master
        self.master.title("Şifre Oluşturucu")
        self.master.geometry("520x450")
        self.son_sifre = ""


        ttk.Label(master, text="Şifre Uzunluğu:").pack(pady=5)
        self.entry_uzunluk = ttk.Entry(master)
        self.entry_uzunluk.pack()


        self.var_buyuk = tk.BooleanVar(value=True)
        self.var_kucuk = tk.BooleanVar(value=True)
        self.var_rakam = tk.BooleanVar(value=True)
        self.var_ozel = tk.BooleanVar(value=True)

        ttk.Checkbutton(master, text="Büyük Harf", variable=self.var_buyuk).pack(anchor="w")
        ttk.Checkbutton(master, text="Küçük Harf", variable=self.var_kucuk).pack(anchor="w")
        ttk.Checkbutton(master, text="Rakam", variable=self.var_rakam).pack(anchor="w")
        ttk.Checkbutton(master, text="Özel Karakter", variable=self.var_ozel).pack(anchor="w")

        ttk.Button(master, text="Şifre Oluştur", command=self.sifre_olustur).pack(pady=10)


        self.etk_sifre = ttk.Label(master, text="")
        self.etk_guc = ttk.Label(master, text="")
        self.etk_skor = ttk.Label(master, text="")
        self.etk_zaman = ttk.Label(master, text="")
        self.etk_uyari = ttk.Label(master, text="")
        self.etk_oneri = ttk.Label(master, text="")

        self.etk_sifre.pack()
        self.etk_guc.pack()
        self.etk_skor.pack()
        self.etk_zaman.pack()
        self.etk_uyari.pack()
        self.etk_oneri.pack()


        self.btn_kopya = ttk.Button(master, text="Kopyala", command=self.sifre_kopyala)
        self.btn_kopya.pack(pady=5)
        self.btn_kopya["state"] = "disabled"

    def sifre_uret(self, uzunluk, buyuk, kucuk, rakam, ozel):
        karakter_seti = ''
        zorunlu = []

        if buyuk:
            karakter_seti += string.ascii_uppercase
            zorunlu.append(secrets.choice(string.ascii_uppercase))
        if kucuk:
            karakter_seti += string.ascii_lowercase
            zorunlu.append(secrets.choice(string.ascii_lowercase))
        if rakam:
            karakter_seti += string.digits
            zorunlu.append(secrets.choice(string.digits))
        if ozel:
            karakter_seti += string.punctuation
            zorunlu.append(secrets.choice(string.punctuation))

        if not karakter_seti or uzunluk < len(zorunlu):
            return None, None

        kalan = [secrets.choice(karakter_seti) for _ in range(uzunluk - len(zorunlu))]
        sifre = zorunlu + kalan
        secrets.SystemRandom().shuffle(sifre)
        return ''.join(sifre), len(karakter_seti)

    def entropi_hesapla(self, charset, uzunluk):
        if charset == 0 or uzunluk == 0:
            return 0
        return math.log2(charset ** uzunluk)

    def sifre_olustur(self):
        try:
            uzunluk = int(self.entry_uzunluk.get())
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı girin.")
            return

        b = self.var_buyuk.get()
        k = self.var_kucuk.get()
        r = self.var_rakam.get()
        o = self.var_ozel.get()

        sifre, charset = self.sifre_uret(uzunluk, b, k, r, o)
        if not sifre:
            messagebox.showerror("Hata", "Seçim hatalı veya uzunluk yetersiz.")
            return

        self.son_sifre = sifre
        entropi = self.entropi_hesapla(charset, uzunluk)
        analiz = zxcvbn(sifre)

        self.etk_sifre["text"] = f" Şifre: {sifre}"
        self.etk_guc["text"] = f" Entropi: {entropi:.2f} bit"
        self.etk_skor["text"] = f" zxcvbn Skor: {analiz['score']}/4"
        self.etk_zaman["text"] = f"Tahmini kırılma süresi: {analiz['crack_times_display']['offline_fast_hashing_1e10_per_second']}"
        self.etk_uyari["text"] = f" {analiz['feedback']['warning'] or 'Uyarı yok'}"
        self.etk_oneri["text"] = f" {' '.join(analiz['feedback']['suggestions']) or 'Ek öneri yok'}"

        self.btn_kopya["state"] = "normal"

    def sifre_kopyala(self):
        if self.son_sifre:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.son_sifre)
            self.master.update()
            messagebox.showinfo("Kopyalandı", "Şifre panoya kopyalandı!")


if __name__ == "__main__":
    pencere = tk.Tk()
    app = SifreOlusturucu(pencere)
    pencere.mainloop()
