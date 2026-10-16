# Linux / WSL için OpenVPN ve SSH köprüsü

Bu kurulum **isteğe bağlıdır**. Mevcut VPN ve SSH çalışıyorsa yeniden kurmayın. Yardımcı proxy yalnızca kendi adı açıkça belirtilen systemd servisini başlatır; başka VPN süreçlerini, tünellerini veya rotalarını temizlemez.

16 Ekim 2026'da yeni proxy mevcut çalışan Linux VPN servisi üzerinden gerçek SSH girişiyle doğrulandı. Sıfırdan VPN profili kurulumu ve Windows/WSL ağ matrisi bu ortamda sınanmadı.

## Mimari

~~~text
SSH kısayolu → uhem-proxy.sh
  → adı belirtilen UHEM servisi (gerekirse başlat)
  → UHEM iç DNS'inden Altay IPv4 adresi
  → hedef rotanın seçilen UHEM tünelinden geçtiğini doğrula
  → nc ile yalnızca Altay:22 bağlantısı
~~~

Proxy TLS profilini değiştirmez; DNS cevabını SSH kimlik doğrulamasının yerine koymaz. Dış DNS'e geri dönüş yapmaz. Örnek iç DNS 10.128.5.2 ve hedef ağ 10.128.0.0/16 bu bağlantıda doğrulanmıştır; başka profil/sistem için UHEM'e teyit edin. Betik farklı hedefe veya porta genel ağ geçidi değildir.

## 1. Ön koşullar

Linux: systemd, OpenVPN, OpenSSH, iproute2, dig ve nc. Ubuntu/Debian örneği, **yalnız eksik paketler için**:

~~~bash
sudo apt-get update
sudo apt-get install openvpn openssh-client iproute2 dnsutils netcat-openbsd
systemctl --version
test -c /dev/net/tun
~~~

Windows'ta WSL2 kullanılıyorsa systemd desteğini ve ağ modunu önce doğrulayın. [Microsoft systemd yönergesi](https://learn.microsoft.com/en-us/windows/wsl/systemd). WSL'nin NAT veya mirrored ağ modları farklı etkilere sahiptir; “Windows internetini hiçbir koşulda etkilemez” garantisi verilemez. Windows'tan Linux proxy çağıracaksanız dağıtım adı, kullanıcı ve tam betik yolunu kendi kurulumunuza göre düzenleyin; Linux SSH kısayolunun çalışması Windows OpenSSH için otomatik kurulum değildir.

## 2. Kişisel profil ve özel tünel

Önce mevcut servis/rotaların kaydını alın:

~~~bash
systemctl list-units '*openvpn*' '*uhem*'
ip -brief link
ip -4 route show default
ip -4 route show
~~~

Yeni kurulumda örnek dizin /etc/openvpn/uhem, servis uhem-vpn.service, tünel tun-uhem'dir. **Bu adlar/dosyalar zaten varsa üzerlerine yazmayın.** Kendi profilinizi UHEM'in verdiği özgün dosyadan, korumalı bir editörle hazırlayın.

- Dizin root'a ait 0700; profil ve gerekiyorsa auth.txt 0600 olmalı.
- Profilde tek bir dev tun-uhem tanımı kullanın; mevcut dev ayarını ona göre düzenleyin. Tünel adı başka servisle çakışmamalı.
- UHEM profili parolalıysa auth-user-pass /etc/openvpn/uhem/auth.txt ve auth-nocache kullanın. Auth dosyasını kabuk geçmişine parola yazarak oluşturmayın.
- Profilin CA, sertifika, anahtar ve remote-cert-tls / sunucu kimliği ayarlarını koruyun.
- Profildeki script, plugin, redirect-gateway ve route ayarlarını okuyun. Mevcut çalışan kullanıcıya ait profil için toplu yeniden yazma yapmayın.

**Split tunnel:** UHEM yönergesine uygunluğu teyit edilmişse route-nopull ve route 10.128.0.0 255.255.0.0 ile yalnız UHEM ağı yönlendirilebilir. route-nopull sunucunun ilettiği başka rotaları da dışlar; VPN uç noktası/profiliniz daha fazlasını gerektiriyorsa bu örneği körlemesine uygulamayın. Proxy özel DNS'e doğrudan sorar; sistemin genel DNS'ini değiştirmeye ihtiyaç duymaz. Başlangıçtan sonra varsayılan rotayı ve diğer VPN erişimlerini yeniden karşılaştırın.

Profildeki dosya yolları servis bağlamında okunabilir olmalı; örnek servis ProtectHome=true kullandığından /root veya /home içindeki sertifikalara başvurmayın. Anahtarları/sertifikaları korumalı /etc/openvpn/uhem dizininde tutun.

## 3. Servis

[Servis örneğini](examples/uhem-vpn.service) okuyun. Önce hedefte servis olmadığını kontrol edin; örneği yeni bir servis dosyası olarak yönetici yetkisiyle yerleştirin. OpenVPN binary yolunu işletim sisteminizde command -v openvpn ile teyit edin.

~~~bash
sudo systemd-analyze verify /etc/systemd/system/uhem-vpn.service
sudo systemctl daemon-reload
sudo systemctl start uhem-vpn.service
systemctl is-active uhem-vpn.service
ip -4 route get 10.128.5.2
~~~

Servisin active olması tek başına hazır tünel anlamına gelmez; proxy DNS ve rota kontrolü de yapar. Otomatik açılış isteniyorsa enable kararı ayrıca verilir; bu kit mevcut servisleri otomatik değiştirmez.

Kök olmayan kullanıcı, servisi başlatma yetkisi yoksa önce yetkili yöneticiyle servisi başlatmalıdır. Kullanıcıya sınırsız parolasız systemctl/sudo yetkisi vermeyin. Tanı için journalctl -u uhem-vpn.service çıktısı kişisel bilgi içerebilir; kamuya açık paylaşmayın.

## 4. SSH kısayolu

~~~bash
chmod 755 scripts/uhem-proxy.sh
~~~

[SSH örneğinde](examples/ssh_config) kullanıcıyı ve betiğin tam yolunu düzenleyin; ~/.ssh/config dosyanızın diğer Host bloklarını koruyun. Kullanılan ayarlar:

~~~sshconfig
Host UHEM_Nanoparticle
    HostName altay.uhem.itu.edu.tr
    User KULLANICI_ADI
    ProxyCommand /TAM/YOL/ITU_UHEM_Setup/scripts/uhem-proxy.sh %h %p
    StrictHostKeyChecking yes
    ConnectTimeout 30
    ServerAliveInterval 30
    ServerAliveCountMax 3
~~~

UHEM'den teyit edilmiş sunucu anahtarını önce bilinen sunuculara kaydedin. Parola/anahtar yöntemi hesabınızda hangisiyse onu kullanın; mevcut IdentityFile/UserKnownHostsFile yolunu gereksiz yere değiştirmeyin.

Başka **mevcut ve doğrulanmış** servis/tünel adı için yalnız ilgili ProxyCommand satırını uyarlayın:

~~~sshconfig
ProxyCommand env UHEM_VPN_SERVICE=BENIM_UHEM_SERVISIM.service UHEM_TUN_DEVICE=BENIM_TUNELIM /TAM/YOL/scripts/uhem-proxy.sh %h %p
~~~

İç DNS farklıysa UHEM_VPN_DNS kullanılabilir; betik güvenlik sınırı olarak yalnız 10.128.0.0/16 IPv4 adreslerini kabul eder. Bu ağ dışındaki resmî bir yeni profil için betik ayrıca gözden geçirilmelidir.

~~~bash
ssh UHEM_Nanoparticle
~~~

Sunucuya girişten sonra hostname ve whoami ile doğrulayın. BatchMode kullanan uhem-check, etkileşimli parola istemez; önce anahtar/ssh-agent ile normal bağlantı hazır olmalıdır.

## 5. Sorun giderme

| Belirti | Tanı |
|---|---|
| Servis başlamıyor | Profil yolları, izinler, /dev/net/tun ve özel servis günlüğü |
| İç DNS yanıtı yok | VPN hazır mı, 10.128.5.2 rotası doğru mu? |
| Rota yanlış tünelden | Mevcut VPN ağ çakışması; proxy bağlantıyı reddeder |
| SSH anahtar değişikliği | UHEM'e teyit; known_hosts topluca silinmez |
| KEX/aktarımı takılıyor | ssh -vv ile aşamayı ayırın; yol MTU'sunu ölçün |
| İşlemsiz oturum düşüyor | SSH keepalive ve ağ; proxy nc için kısa idle timeout koymaz |

tun-mtu/mssfix değerini her kullanıcı için 1200 gibi sabitlemek doğru değildir; paketleme ve yol koşullarına göre ölçün. Önce güncel UHEM profilini kullanın. [OpenVPN kılavuzu](https://openvpn.net/community-docs/community-articles/openvpn-2-6-manual.html).

Eski rehberdeki pgrep açıklaması da düzeltildi: tırnak içinde verilen “openvpn --config ...” tek bir desen argümanıdır; içindeki --config kendiliğinden seçenek olarak yorumlanmaz. Asıl olası sorunlar yanlış kabuk ayrıştırması, genel süreç eşlemesi ve self-match'tir. Yeni çözüm süreç adıyla tahmin yerine özel servis durumunu kullanır.
