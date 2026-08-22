# 02 — VPN Kurulumu ve SSH ile Giriş

HPC hesap mailin geldiyse (kullanıcı adı + şifre) buradan devam et.
UHeM'e erişim **iki katmanlıdır**: önce VPN ile ağa gir, sonra SSH ile sunucuya bağlan.

> **Kimlik:** VPN ve SSH **aynı** kullanıcı adı/şifreyi kullanır (örn. `<KULLANICI>`).
> `yazilimlar` kullanıcısı sadece VPN dosyasını indirmek içindir, bağlantıda kullanılmaz.

---

## A) OpenVPN kurulumu (Windows)

Merkez, eski Cisco yerine **OpenVPN** öneriyor (daha hızlı, sorunsuz).

1. **OpenVPN istemcisini indir:** https://openvpn.net/community-downloads/ → Windows 64-bit MSI.
   Kurulumda yönetici izni + sanal ağ adaptörü onayı ister → hepsine **evet**.
2. **Config dosyasını al:** `openvpn-uhem-config.ovpn`
   (bu kitte `Referans/` veya masaüstünde mevcut; ya da VPN indirme sayfasından
   `yazilimlar` / şifresi ile).
3. Görev çubuğu sağ altında **OpenVPN ikonu** çıkar (pencere açmaz, bu normaldir).
   İkona **sağ tık → Import file** → `openvpn-uhem-config.ovpn`'i seç.
4. **Bağlan:** ikona sağ tık → **Connect** → **HPC kullanıcı adı + şifre**.
   İkon **yeşile** dönerse tünel kalkmış demektir.

> **Linux için:** `openvpn-uhem-config-linux.ovpn` kullanılır (içinde
> `up/down /etc/openvpn/update-resolv-conf` satırları farklı). Paket
> yöneticisinden `openvpn` kurup `sudo openvpn --config openvpn-uhem-config-linux.ovpn`.

### VPN bağlantısını DOĞRULA (önemli)

İkonun yeşil olması **tek başına yeterli kanıt değildir** — VPN bazen "bağlandım"
der ama ağ yönlendirmesini kuramaz. Kesin test:

- Tarayıcıda **http://sari.uhem.itu.edu.tr** (ya da `sariyer.uhem.itu.edu.tr`)
  aç. Pembe zeminli UHeM sayfası + güncellenen saat gelirse tünel gerçekten çalışıyor.
- Bu adresler dışarıdan (VPN'siz) DNS'te **hiç çözülmez**; açılıyorsa iş tamamdır.

---

## B) SSH ile sunucuya bağlan

Windows 10/11'de OpenSSH **hazır kuruludur**, PuTTY şart değil (video PuTTY anlatır
ama gerek yok). PowerShell veya CMD'de:

```bash
ssh <KULLANICI>@altay.uhem.itu.edu.tr
```

- **İlk bağlantıda** host key sorar → `yes`.
- Şifre sorulunca HPC şifreni gir (ekranda görünmez, normaldir).

### Sunucular

| Adres | Ne |
|-------|-----|
| `altay.uhem.itu.edu.tr` | **Altay** login node (güncel, aktif küme) |
| `sariyer.uhem.itu.edu.tr` | Sarıyer login node — **KAPANDI**, artık kullanılmaz |

> Not: Sarıyer verileri Altay'da `/SARIYER` altında salt-okunur duruyor (bkz. Önemli Notlar).

---

## Şifre reddi mi alıyorsun? ("Permission denied")

Yeni açılan hesaplarda sık görülür. Sırayla:

1. **VPN çalışıyor ama SSH reddediyor** → hesabın küme tarafında henüz
   **aktifleşmemiş** olabilir (LDAP/home dizini yayılması birkaç saat sürebilir).
   Bu geçicidir; birkaç saat sonra kendiliğinden düzelir.
2. **Üst üste deneme yapma** — 5-10 başarısız denemede fail2ban IP/hesabı geçici
   kilitleyebilir. Aralıklı, birer kez dene.
3. **Kopyala-yapıştır tuzağı:** Şifreyi önce **formatsız bir editöre** (Not Defteri)
   yapıştır, sonunda görünmez boşluk olmadığından emin ol, oradan kopyala — ya da
   **elle** gir. Kaynak mailin HTML biçimi bazen sona boşluk ekliyor.
4. Bir gün içinde düzelmezse **destek@uhem.itu.edu.tr**'ye yaz:
   "VPN çalışıyor, sariyer/altay SSH parola doğrulaması reddediliyor, hesabın
   aktifleştirilmesi gerekiyor olabilir." (Aynı projede birden çok kişi aynı
   durumdaysa bunu belirt — sistem tarafı sorunu olduğunu kanıtlar.)

---

## İlk giriş sonrası hemen

```bash
passwd        # şifreni değiştir (özellikle mail/sohbetle paylaşıldıysa)
```

Sonra → `03_Giris_Sonrasi_Kontrol.md`.
