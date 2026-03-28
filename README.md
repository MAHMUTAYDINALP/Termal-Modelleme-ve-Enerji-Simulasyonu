# ☀️ Güneş Enerjili Isınma Fizibilite Simülasyonu (Thermal Core Engine)

Bu proje, bir konuta veya binaya **güneş enerjisi destekli ısınma sistemi** kurmanın finansal ve fiziksel olarak "mantıklı olup olmadığını" hesaplayan bir karar destek (simülasyon) çekirdeğidir. Müşteri ön gösterimi (PoC) amacıyla geliştirilmiştir.
---

🧾NOT: Yeter veri sahada toplandıgı zaman veri işlenip parametrelerin etki miktarı hesaplanıp simüle edecek sistem oluşturulacaktır. 



## 🎯 Projenin Amacı

Güneş enerjisi yatırımları yüksek maliyetlidir ve her bina için uygun olmayabilir. Bu yazılım, kulaktan dolma bilgiler yerine matematiksel ve termodinamik verileri kullanarak yatırımcıya net bir cevap üretir: **"Bu eve bu sistemi kurmak verimli mi?"** Proje şu an çekirdek algoritma (core engine) seviyesindedir ve dışarıdan aldığı değişkenlerle sistemin kendini amorti etme/evi ısıtabilme kapasitesini simüle eder.

## ⚙️ Hesaplama Parametreleri (Girdiler)

Simülasyon motoru, doğru bir hesaplama yapabilmek için aşağıdaki temel fiziksel ve coğrafi parametreleri kullanır:

* **Güneş Enerjisi Potansiyeli:** Binanın bulunduğu konumun aldığı ortalama güneş enerjisi (radyasyon) miktarı(APİ ile gerçek veri çekiliyor).
* **Evin Büyüklüğü:** Isıtılacak toplam alan (metrekare).
* **Cephe ve Yönelim:** Güneş panellerinin/evin baktığı yön (Güney cephesi avantajı vb.).
* **Bina Tipi:** Müstakil, apartman dairesi veya endüstriyel yapı.
* **Yalıtım Durumu:** Binanın ısı kaybı katsayısı (Mantolama var/yok, pencere tipleri).

*
* <img width="1919" height="1079" alt="Ana ekran" src="https://github.com/user-attachments/assets/349a445d-efa6-49e7-8ece-14664c4856d0" />
<img width="1919" height="1079" alt="yatılımlı ve müstakil" src="https://github.com/user-attachments/assets/ab99c373-5941-4e1b-96b3-77523c1619e7" />
<img width="1919" height="1079" alt="yalıtımsız ve müstakil" src="https://github.com/user-attachments/assets/b0c62ee0-dd53-400d-b7d9-35da804522e3" />
<img width="1919" height="1074" alt="yalıtımsız ve daire" src="https://github.com/user-attachments/assets/fb2e16ff-0aad-4151-9e17-67b9b6861e21" />
<img width="1919" height="1079" alt="yalıtımlı ve daire" src="https://github.com/user-attachments/assets/c54ec485-cf57-4ec5-8a04-6e6c72fb9d09" />






## 💻 Sistem Nasıl Çalışır?

1. Kullanıcıdan (veya bir veritabanından) yukarıdaki parametreler sisteme beslenir.
2. Çekirdek algoritma, evin ısı kaybı ile güneşten elde edilebilecek potansiyel ısı kazancını karşılaştırır.
3. Sonuç olarak bir fizibilite raporu üretir (Örn: "Sistem evin %60 ısınma ihtiyacını karşılar, kurulum mantıklıdır" veya "Yalıtım yetersiz olduğu için yatırım verimsizdir").

## 🚀 Nasıl Test Edilir?

Çekirdek algoritmayı ve test senaryolarını bilgisayarınızda çalıştırmak için:

1. Projeyi klonlayın:
   ```bash
   git clone [https://github.com/MAHMUTAYDINALP/Termal-Modelleme-ve-Enerji-Simulasyonu.git](https://github.com/MAHMUTAYDINALP/Termal-Modelleme-ve-Enerji-Simulasyonu.git)
