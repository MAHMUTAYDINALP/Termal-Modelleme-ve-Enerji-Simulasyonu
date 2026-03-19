import customtkinter as ctk 
import tkintermapview
import requests
# +++ YENİ: Resim dosyalarını okumak için Pillow kütüphanesini ekledik +++
from PIL import Image, ImageTk
import os # Dosya yollarını kontrol etmek için

# Arayüz için genel ayarlar
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TermalSimulasyonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Termal Simülasyon ve Enerji Analizi - Alpha V1.2")
        self.geometry("1050x700") # Yüksekliği biraz arttırdım görsel sığsın diye

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.secilen_enlem = None
        self.secilen_boylam = None

        # ==================== SOL PANEL ====================
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.label_baslik = ctk.CTkLabel(self.left_frame, text="1. Aşama: Konum ve Parametreler", font=("Arial", 16, "bold"))
        self.label_baslik.pack(pady=5)

        # Harita 
        self.map_widget = tkintermapview.TkinterMapView(self.left_frame, corner_radius=10, height=250)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=y&hl=tr&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.pack(pady=5, padx=10, fill="both", expand=True)

        self.map_widget.set_position(39.92077, 32.85411)
        self.map_widget.set_zoom(5)
        self.map_widget.add_right_click_menu_command(label="Evin Konumunu Seç", command=self.konum_secildi, pass_coords=True)

        self.lbl_koordinat = ctk.CTkLabel(self.left_frame, text="Haritaya sağ tıklayarak konumu seçin", text_color="yellow")
        self.lbl_koordinat.pack(pady=5)

        # PARAMETRELER BÖLÜMÜ
        self.param_frame = ctk.CTkFrame(self.left_frame)
        self.param_frame.pack(pady=5, padx=10, fill="x")

        self.lbl_m2 = ctk.CTkLabel(self.param_frame, text="Evin Büyüklüğü (m²):")
        self.lbl_m2.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_m2 = ctk.CTkEntry(self.param_frame, placeholder_text="Örn: 100")
        self.entry_m2.grid(row=0, column=1, padx=10, pady=5)

        self.lbl_yalitim = ctk.CTkLabel(self.param_frame, text="Yalıtım Durumu:")
        self.lbl_yalitim.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_yalitim = ctk.CTkComboBox(self.param_frame, values=["Yalıtımsız", "Yalıtımlı"])
        self.combo_yalitim.grid(row=1, column=1, padx=10, pady=5)

        self.lbl_ev_tipi = ctk.CTkLabel(self.param_frame, text="Ev Tipi:")
        self.lbl_ev_tipi.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # +++ Değerleri dosya isimleriyle uyumlu hale getirdim +++
        self.combo_ev_tipi = ctk.CTkComboBox(self.param_frame, values=["Müstakil", "Daire"])
        self.combo_ev_tipi.grid(row=2, column=1, padx=10, pady=5)

        self.lbl_cephe = ctk.CTkLabel(self.param_frame, text="Hakim Cephe:")
        self.lbl_cephe.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combo_cephe = ctk.CTkComboBox(self.param_frame, values=["Güney", "Kuzey", "Doğu", "Batı"])
        self.combo_cephe.grid(row=3, column=1, padx=10, pady=5)

        self.btn_hesapla = ctk.CTkButton(self.left_frame, text="SİMÜLASYONU BAŞLAT", font=("Arial", 14, "bold"), fg_color="darkred", hover_color="red", command=self.simulasyonu_baslat)
        self.btn_hesapla.pack(pady=10)


        # ==================== SAĞ PANEL (GÖRSEL VE SONUÇ) ====================
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        self.label_sag = ctk.CTkLabel(self.right_frame, text="2. Aşama: Görselleştirme ve Sonuç", font=("Arial", 16, "bold"))
        self.label_sag.pack(pady=10)
        
        # +++ YENİ: Görselin geleceği yer. Başlangıçta boş bir kutu olacak. +++
        # text="" diyerek içini boşalttık, image=None başlangıçta resim yok.
        self.lbl_gorsel_kutusu = ctk.CTkLabel(self.right_frame, text="", height=250, fg_color="gray20", corner_radius=10)
        self.lbl_gorsel_kutusu.pack(pady=10, padx=20, fill="x")

        self.lbl_bilgi = ctk.CTkLabel(self.right_frame, text="Henüz hesaplama yapılmadı.\nVerileri girip butona basın.", justify="left", font=("Arial", 14))
        self.lbl_bilgi.pack(pady=20, padx=20)


    # ==================== FONKSİYONLAR ====================
    def konum_secildi(self, coords):
        self.map_widget.delete_all_marker()
        self.map_widget.set_marker(coords[0], coords[1], text="Hedef Ev")
        self.secilen_enlem = round(coords[0], 4)
        self.secilen_boylam = round(coords[1], 4)
        self.lbl_koordinat.configure(text=f"Seçildi: Enlem {self.secilen_enlem}, Boylam {self.secilen_boylam}", text_color="lightgreen")


    def simulasyonu_baslat(self):
        # GÜVENLİK KONTROLLERİ
        if self.secilen_enlem is None or self.secilen_boylam is None:
            self.lbl_bilgi.configure(text="HATA: Lütfen önce haritadan evin konumunu seçin!", text_color="red")
            return
        m2_degeri = self.entry_m2.get()
        if m2_degeri == "":
            self.lbl_bilgi.configure(text="HATA: Lütfen evin büyüklüğünü (m²) girin!", text_color="red")
            return
            
        # Parametreleri alıyoruz
        yalitim_secimi = self.combo_yalitim.get() # "Yalıtımlı" veya "Yalıtımsız"
        ev_tipi_secimi = self.combo_ev_tipi.get() # "Müstakil" veya "Daire"
        cephe = self.combo_cephe.get()

        # Bekleme mesajı
        self.lbl_bilgi.configure(text="Hesaplamalar yapılıyor ve görsel hazırlanıyor...\nLütfen bekleyin.", text_color="yellow")
        self.update() 

        # +++ YENİ: GÖRSEL SEÇİM MANTIĞI (4 VARYASYON) +++
        try:
            # 1. Dosya adının parçalarını belirle (Türkçe karakterleri düzelterek)
            tip_kodu = "mustakil" if ev_tipi_secimi == "Müstakil" else "daire"
            yalitim_kodu = "yalitimli" if yalitim_secimi == "Yalıtımlı" else "yalitimsiz"
            
            # 2. Dosya yolunu oluştur: assets/mustakil_yalitimsiz.png gibi
            dosya_yolu = f"assets/{tip_kodu}_{yalitim_kodu}.png"
            
            # 3. Dosyanın gerçekten orada olup olmadığını kontrol et (Hata almamak için)
            if os.path.exists(dosya_yolu):
                # Resmi yükle ve boyutlandır (CustomTkinter Image nesnesi olarak)
                # size=(350, 250) görselin ekrandaki boyutu
                gorsel_nesnesi = ctk.CTkImage(light_image=Image.open(dosya_yolu), 
                                              dark_image=Image.open(dosya_yolu), 
                                              size=(700, 400))
                
                # Sağ paneldeki boş kutuya bu resmi koy
                self.lbl_gorsel_kutusu.configure(image=gorsel_nesnesi)
            else:
                self.lbl_bilgi.configure(text=f"HATA: Görsel dosyası bulunamadı!\nAranan yol: {dosya_yolu}", text_color="red")
                return # Görsel yoksa devam etme

        except Exception as e_img:
             self.lbl_bilgi.configure(text=f"Görsel Yükleme Hatası: {str(e_img)}", text_color="red")
             return
        # +++++++++++++++++++++++++++++++++++++++++++++++++++


        # API'DEN VERİ ÇEKME (Burası aynı)
        try:
            api_url = f"https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat={self.secilen_enlem}&lon={self.secilen_boylam}&peakpower=1&loss=14&outputformat=json"
            cevap = requests.get(api_url)
            veri = cevap.json()
            yillik_gunes_potansiyeli = veri['outputs']['totals']['fixed']['E_y']
            
            sonuc_metni = (
                f"--- SİMÜLASYON SONUCU ---\n"
                f"Seçilen Konfigürasyon: {ev_tipi_secimi}, {yalitim_secimi}, {cephe} Cephe\n\n"
                f"Büyüklük: {m2_degeri} m²\n\n\n"
                f"Bölgesel Güneş Potansiyeli (Yıllık): {yillik_gunes_potansiyeli} kWh\n\n\n"
                f"Tahmini Yıllık Tasarruf: (Hesaplanıyor...)\n\n\n"
                f"Amortisman Süresi: (Hesaplanıyor...)"
            )
            self.lbl_bilgi.configure(text=sonuc_metni, text_color="white")

        except Exception as e_api:
            self.lbl_bilgi.configure(text=f"API/İnternet Hatası: {str(e_api)}", text_color="red")

if __name__ == "__main__":
    app = TermalSimulasyonApp()
    app.mainloop()