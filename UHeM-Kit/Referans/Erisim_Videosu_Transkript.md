# UHeM Erişim Videosu — Düzenli Özet

Masaüstündeki **uhem-erisim.mp4 / uhem-erisim.mp3** dosyasının içeriğinin
temizlenmiş, yapılandırılmış hâli. Orijinal videoda VPN kurulumu ve SSH bağlantısı
adım adım anlatılıyor. (Video dosyaları büyük — mp4 ~248 MB, mp3 ~24 MB.)

> Bu özet, videoyu izlemeden hızlı başvuru içindir. Ekran görüntüleri için videoyu aç:
> http://wiki.uhem.itu.edu.tr/w/uhem-erisim.mp4

---

## 1. Önce hesap mailini kontrol et

- Hesabın açıldığına dair, **kullanıcı adı ve şifreni içeren** e-posta gelmiş olmalı.
- Bu mailde: VPN bilgileri + sistemlere bağlanıp iş verme bilgileri + wiki linki var.
- Böyle bir mail almadıysan bağlanman **mümkün değil** — önce hesap onayını bekle.

## 2. VPN yazılımını indir

- Mailde geçen **VPN indirme adresine** git (`.../vpn-...`).
- Sayfa kullanıcı adı/şifre sorar → bunlar **senin hesabın değil**, mailde
  *"indirme kullanıcısı"* olarak verilen `yazilimlar` kullanıcısı ve şifresidir.
- İki VPN sunucusu var:
  - **Cisco IPSec** — eski.
  - **OpenVPN** — yeni, önerilen. Daha güvenli, hızlı, sorunsuz. Özellikle Windows
    kullanıcıları için tavsiye edilir (Windows'ta VPN sorunu daha az).

## 3. OpenVPN kurulumu (Windows)

- Sayfadaki linklerden:
  - **Ayar dosyası** (`openvpn-uhem-config.ovpn`) — tek başına config.
  - **Windows istemcisi + gömülü ayar** — ikinci link; hem client programı hem
    ayar dosyası birlikte gelir. Windows için **en kolay yol** (tek kurulum).
  - Alternatif: openvpn.net'ten daha yeni client (3. link), macOS için en alttaki link.
- **Önemli:** OpenVPN sürümü **2.4 ve üstü** olmalı (config yeni parametreler içerir).
- Kurulumda Windows tekrar tekrar izin sorar (VPN ağ ayarlarını değiştirdiği için) →
  hepsine izin ver. "Bilinmeyen yayıncı" uyarısı çıkabilir → yine de çalıştır.

## 4. OpenVPN'i çalıştırma (ikon tuzağı)

- Kurulum sonrası masaüstü ikonuna tıklayınca **hiçbir şey olmuyormuş gibi** görünür.
- Program aslında **sağ alt köşede küçük bir ikon** olarak çalışır (ekrana pencere açmaz).
- Masaüstü ikonu ile sistem tepsisindeki ikon arasında bağ yoktur — programı orada ara.

## 5. Config'i tanıtma (gerekirse)

- Client'ı **bizim sayfamızdan** kurduysan config zaten gömülü gelir.
- Client'ı **openvpn.net'ten** kurduysan: tepsi ikonu → sağ tık → **Import file** →
  `.ovpn` dosyasını göster (uzantı `.ovpn` olmalı).

## 6. Bağlanma

- Tepsi ikonu → **Connect**.
- Açılan pencere **kullanıcı adı ve şifre** sorar → bunlar mailde **kırmızı zemin
  üzerine beyaz** yazılı "Kullanıcı adı / Şifre / Proje adı" satırındaki bilgilerdir
  (indirme kullanıcısı DEĞİL).
- Bağlanınca pencere kaybolur, ikon **yeşile** döner, atanan IP görünür.

## 7. Bağlantıyı doğrula (kritik)

- VPN "bağlandım" deyip aslında ağ yönlendirmesini kuramamış olabilir.
- Tarayıcıya **sari.uhem.itu.edu.tr** yaz → pembe zeminli UHeM sayfası + güncellenen
  saat gelirse bağlantı **gerçekten** çalışıyor demektir.

## 8. SSH client (PuTTY) — modern Windows'ta opsiyonel

> Video PuTTY anlatır, ama Windows 10/11'de OpenSSH hazır kuruludur; PowerShell/CMD'de
> doğrudan `ssh kullanici@altay.uhem.itu.edu.tr` yeterlidir. Aşağısı video akışıdır.

- Windows'ta hazır SSH client yoksa **PuTTY** indir.
- Dikkat: Google'da ilk çıkan `putty.org` **gerçek site değildir** (reklam). Gerçek
  indirme: **greenend.org.uk** üzerinden (`putty.exe` veya installer).
- `putty.exe` kurulum gerektirmez, doğrudan çalışır.

## 9. SSH ile bağlanma

- PuTTY'de "Host Name" alanına sunucu adresi (örn. `sariyer.uhem.itu.edu.tr` /
  güncelde `altay.uhem.itu.edu.tr`). İstersen "Saved Sessions" ile kaydet.
- **İlk bağlantıda** sunucunun SSH key'i gösterilir → güvenip güvenmediğin sorulur →
  güvenilen ağdan bağlanıp **kabul et**. Sonraki seferlerde key değişmedikçe sormaz
  (key değişirse uyarı verir = güvenlik).
- Kullanıcı adı + şifre ile giriş.

## 10. Giriş sonrası ilk komutlar (videodan)

- `bos_makineler` — tanımlı kuyruklar, boş işlemci sayıları, min/max makine, süre →
  işi hangi kuyruğa vereceğine karar vermek için. (Güncelde `spart` de aynı işlevde.)
- `pwd` — ev dizinin (`/ari/users/<kullanici>` benzeri).
- `projelerim` — tanımlı projelerin, o projelerdeki diğer kullanıcılar, iş/CPU limitleri,
  ayrılan ve kullanılan CpuSaat + disk.

## 11. En kritik uyarı: login node'da çalıştırma!

- Bağlandığın makine (sarıyer/altay) **login node**'dur — sadece **iş vermek** içindir.
- Burada doğrudan program çalıştırırsan ve çok CPU/RAM tüketirse **otomatik öldürülür**
  ("çok fazla hafıza/işlemci kullandığınız için program öldürülmüştür" mesajı).
- Doğru yol: **Slurm'e iş vermek** (`sbatch`) ya da **Slurm'den makine talep edip**
  (`salloc`/`srun`) o makinede çalışmak.

---

*Kullanım detayları için → `../Utilize/` klasörü.*
