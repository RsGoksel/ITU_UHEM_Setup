# ITU UHeM Erişim & Kullanım Kiti

İTÜ **Ulusal Yüksek Başarımlı Hesaplama Merkezi (UHeM, eski adıyla UYBHM)** için
sıfırdan erişim, kurulum ve kullanım rehberi. Yeni bir proje kullanıcısının kolayca
başlayabilmesi için hazırlandı — kayıt, VPN, SSH, Slurm iş gönderme, GPU işleri ve
tek komutla otomatik bağlanma (WSL2 + OpenVPN köprüsü) dahil.

> Merkez: **Altay** kümesi (Sarıyer kümesi 2026'da kapatıldı).
> Bu depo **sanitize edilmiştir**: kişisel kimlik bilgileri, şifreler, VPN
> sertifika/anahtar dosyaları (`.ovpn`) ve tokenlı erişim URL'leri **bilerek
> dahil edilmemiştir**. Kendi bilgilerinizi placeholder'ların (`<KULLANICI>`,
> `<TOKEN>`, `SIFRE_BURAYA`) yerine koyun.

## İçerik

### [UHEM_OpenVPN.md](UHEM_OpenVPN.md)
**Tek komutla bağlanma** — `ssh UHEM_Nanoparticle`. Windows'ta WSL2 içinde OpenVPN'i
çalıştırıp ProxyCommand köprüsüyle otomatik bağlanma. Host interneti etkilenmez
(split-tunnel). Sıfırdan kurulum, mimari, ve kurulumda çözülen 3 gerçek tuzak:
MTU kara deliği, iç DNS zorunluluğu, pgrep `--config` self-sabotajı.

### [UHeM-Kit/](UHeM-Kit/)
Geniş erişim + kullanım kiti:

| Klasör | İçerik |
|--------|--------|
| **Setup_Login/** | Kayıt → e-posta onayı → VPN → SSH → giriş sonrası kontroller |
| **Utilize/** | Modüller, Slurm iş gönderme, GPU işleri (A100), komut sözlüğü, disk/veri |
| **Onemli_Notlar/** | 10 kritik uyarı (GPU faturalama tuzağı, login node, yedek, kota) |
| **Referans/** | Kimlik bilgileri şablonu, wiki linkleri, erişim videosu özeti |

## Öne çıkan teknik katkılar

- **WSL2 + OpenVPN + ProxyCommand köprüsü:** UHeM OpenVPN'ini Windows host'un ağına
  hiç dokunmadan, tek `ssh` komutuyla otomatik açan mimari. Aynı makinede birden
  çok kurumsal VPN'i (openfortivpn tabanlı olanlarla birlikte) çakışmadan yan yana
  kullanma.
- **WSL Hyper-V NAT MTU düzeltmesi:** OpenVPN'i WSL'de çalıştırırken SSH KEX'i asan
  MTU kara deliğinin `tun-mtu` + `mssfix` ile çözümü.
- **Split-tunnel iç DNS çözümü:** public DNS'in route'suz IP verdiği durumda hedefi
  VPN iç DNS'i ile çözme.

## Kimler için

İTÜ UHeM'e yeni katılan lisansüstü öğrenciler, araştırmacılar ve proje ekipleri.
WSL/OpenVPN bölümü, benzer split-tunnel kurumsal VPN'leri Windows'ta izole çalıştırmak
isteyen herkes için genellenebilir.

## Sorumluluk reddi

Resmi olmayan, topluluk tarafından hazırlanmış bir rehberdir. Kota, kuyruk, süre
limitleri ve alan adları zamanla değişebilir — güncel bilgi için portal, `projelerim`
komutu ve <http://wiki.uhem.itu.edu.tr> esastır. UHeM'in kullanıcıya özel yazılım ve
kimlik bilgileri (VPN config dahil) üçüncü şahıslarla paylaşılmamalıdır; bu depo o
dosyaları içermez.

## Lisans

[MIT](LICENSE)
