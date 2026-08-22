# UHeM Erişim & Kullanım Kiti

İTÜ Ulusal Yüksek Başarımlı Hesaplama Merkezi (UHeM, eski adıyla UYBHM) için
sıfırdan erişim + kullanım rehberi. Yeni bir proje kullanıcısının kolayca
başlayabilmesi ve mevcut kullanıcıların hızlı başvurabilmesi için hazırlandı.

> Proje: **nakane** · Grant No: **1022642025** · Küme: **Altay**
> (Sarıyer kümesi 2026'da kapatıldı, artık sadece Altay aktif.)

## Klasör yapısı

| Klasör | İçerik |
|--------|--------|
| **Setup_Login/** | Sıfırdan erişim: kayıt → e-posta onayı → hesap → VPN → SSH → giriş sonrası ilk kontroller |
| **Utilize/** | Kümeyi kullanma: modüller, Slurm iş gönderme, GPU işleri, komut sözlüğü, disk/veri |
| **Onemli_Notlar/** | Kritik uyarılar tek sayfada (faturalama tuzağı, login node, yedek, kota) |
| **Referans/** | Kimlik bilgileri şablonu, wiki linkleri, erişim videosu transkripti |

## Nereden başlamalı

1. **İlk kez mi kuruyorsun?** → `Setup_Login/01_Kayit.md` sırayla.
2. **Hesabın var, kullanmaya mı başlıyorsun?** → `Onemli_Notlar/00_ONCE_BUNU_OKU.md`, sonra `Utilize/02_Slurm_Is_Gonderme.md`.
3. **Bir komut mu unuttun?** → `Utilize/04_Komut_Sozlugu.md`.

## Okuma sırası (yeni kullanıcı)

```
Setup_Login/01_Kayit.md
Setup_Login/02_Giris_VPN_SSH.md
Setup_Login/03_Giris_Sonrasi_Kontrol.md
Onemli_Notlar/00_ONCE_BUNU_OKU.md
Utilize/01_Moduller.md
Utilize/02_Slurm_Is_Gonderme.md
Utilize/03_GPU_Isleri.md
Utilize/04_Komut_Sozlugu.md
Utilize/05_Disk_ve_Veri.md
```

---
*Hazırlanma: 2026-08-20. Bilgiler o tarihteki Altay kümesi durumuna göredir;
kota/kuyruk/süre limitleri zamanla değişebilir — güncel durum için
`projelerim` ve `spart` komutlarına ve wiki.uhem.itu.edu.tr'ye bakın.*
