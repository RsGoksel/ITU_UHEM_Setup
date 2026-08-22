# UHeM (Altay) - `ssh UHEM_Nanoparticle` Baglanti Kurulum & Kullanim Rehberi

> Windows host'tan **UHeM Altay login node**'una tek komutla (`ssh UHEM_Nanoparticle`),
> **lokal internet hic bozulmadan** baglanmak icin kurulan sistemin tam belgesi.
> Kurdugu tarih: 2026-08-20. Kalibi `uysm_setup.md` ile aynidir (WSL2 icinde VPN +
> ProxyCommand koprusu) ama VPN teknolojisi farklidir: UHeM = **OpenVPN** (openfortivpn degil).
>
> UYARI - GIZLI DOSYA: Icinde HPC sifresi duz metin gecer. Paylasma, public repoya
> koyma, diski sifreli tut (BitLocker).

---

## 1. Neden boyle bir kurulum? (arka plan)

- UHeM hesaplama sunucularina (Altay) erisim yalnizca **VPN uzerinden** mumkun; login
  node'lar internete acik degil.
- UHeM resmi olarak **OpenVPN** oneriyor (eski Cisco IPSec yerine). Config dosyasi
  (`openvpn-uhem-config.ovpn`) portalin VPN indirme sayfasindan aliniyor.
- Klasik yol: Windows'a **OpenVPN GUI** kur, config'i import et, elle Connect, sonra
  ayrica `ssh` yap. Iki dezavantaji var:
  1. Her seferinde GUI'yi elle acmak/baglanmak gerekiyor (otomatik degil).
  2. GUI tunel Windows'un ag katmanina dokunuyor (block-outside-dns, DNS push vb.).
     UHeM tuneli **split-tunnel** oldugu icin interneti kesmiyor -- ama yine de host'un
     ag durumuna mudahale ediyor ve diger VPN'lerle (uysm/akdeniz/yildiz) yan yana
     yonetimi karisik.
- Cozum: OpenVPN'i **WSL2 icinde** calistir; `UHEM_Nanoparticle` SSH host'u, tuneli
  gerektiginde otomatik acan bir **ProxyCommand koprusu** kullansin. VPN tamamen WSL2'nin
  ag alaninda kalir -> host Windows'un agina hic dokunmaz -> lokal internet hep acik,
  GUI acmaya gerek yok.
- Bu makinede zaten `uysm`/`akdeniz`/`yildiz` icin ayni kalip (WSL2 + ProxyCommand)
  kullaniliyor (bkz. `uysm_setup.md`). UHeM bu aileye 4. uye olarak eklendi; **mevcut
  openfortivpn supervisor sistemine hic dokunulmadi** (ayrinti: bolum 7).

---

## 2. Mimari

```
ssh UHEM_Nanoparticle  /  VS Code Remote-SSH (Windows host)
  |- Host "UHEM_Nanoparticle" (~/.ssh/config)
       |- ProxyCommand: wsl.exe -d Ubuntu-24.04 /usr/local/bin/uhem-nc altay.uhem.itu.edu.tr 22
            |- uhem-nc (WSL2): openvpn calismiyorsa baslatir, 10.128/16 route'unu bekler,
            |                   hedefi VPN IC DNS'i ile cozer, sonra nc ile TCP'yi yollar
                 |- openvpn (WSL2) == UDP 1194 ==> UHeM gateway 160.75.120.252
                      |- tun0 (172.17.x, split-tunnel) : PUSH edilen route'lar
                      |     10.128.0.0/16, 10.0.55.0/24, 160.75.120.120/32, 172.17.0.1/32
                      |- VPN IC DNS (10.128.5.2): altay.uhem.itu.edu.tr -> 10.128.2.40
                           |- nc 10.128.2.40 22 ==> Altay login node sshd (OpenSSH 8.0)
```

Host Windows'un kendi agi/DNS'i bu zincire **hic karismaz** -> internet kesilmez.
VPN sadece WSL2 icinde yasar. Split-tunnel oldugu icin sadece UHeM subnet trafigi
tunelden gider; geri kalan her sey (WSL'in ve host'un interneti) normal cikar.

---

## 3. Sabit degerler

| Anahtar | Deger |
|---|---|
| VPN gecidi (gateway) | `160.75.120.252:1194/udp` (OpenVPN) |
| VPN protokolu | OpenVPN 2.4+, split-tunnel, `auth-user-pass` (istemci sertifikasi YOK) |
| HPC kullanici adi | `<KULLANICI>` (VPN + SSH icin AYNI) |
| HPC sifresi | *(hesap mailinde; `passwd` ile degistir)* |
| Proje adi | `nakane` |
| Grant No | `1022642025` |
| Login node (SSH hedefi) | `altay.uhem.itu.edu.tr` -> **ic IP 10.128.2.40** (VPN DNS'inden) |
| Login node sshd | OpenSSH 8.0 |
| PUSH edilen route'lar | `10.128.0.0/16`, `10.0.55.0/24`, `160.75.120.120/32`, `172.17.0.1/32` |
| VPN IC DNS sunuculari | `10.128.5.2`, `10.128.5.3`, `160.75.121.242`, `160.75.121.243` |
| VPN arama alani | `uhem.itu.edu.tr` |
| VPN yazilim indirme kullanicisi | `yazilimlar` / *(hesap mailinde)* -- sadece .ovpn indirmek icin |
| VPN indirme sayfasi | `https://portal.uhem.itu.edu.tr/vpn-<TOKEN>/` |
| WSL dagitimi | `Ubuntu-24.04` (WSL **2**), default kullanici: **root** |

> Public DNS `altay.uhem.itu.edu.tr`'yi `160.75.120.55`'e cozer -- bu IP tunelde
> **route'lu DEGIL**. Dogru olan, VPN ic DNS'inin verdigi `10.128.2.40` (10.128/16
> icinde, route'lu). Kopru bu yuzden hedefi ic DNS ile cozer (bkz. bolum 6, tuzak 2).

---

## 4. Sifirdan Kurulum (temiz makinede / LLM ile)

### 4.1 - WSL2 + Ubuntu 24.04 (zaten varsa atla)
Windows'ta yonetici PowerShell:
```powershell
wsl --install -d Ubuntu-24.04
```
(Bu makinede WSL default kullanicisi **root**. Farkli ise 4.4/4.5'te `-u root` / `sudo` ayarla.)

### 4.2 - OpenVPN kur (WSL icinde)
```bash
apt-get update && apt-get install -y openvpn dnsutils
```
`openvpn --version` >= 2.6 olmali. `dig` (dnsutils) ic DNS cozumu icin gerekli.
`/dev/net/tun` var olmali.

### 4.3 - Config'i al ve WSL'e yerlestir
Config, portalin VPN indirme sayfasindan (`yazilimlar` kullanicisi ile) veya masaustunden
`openvpn-uhem-config.ovpn` olarak alinir. WSL icine kopyala ve **UHeM'e ozel** hale getir:

```bash
mkdir -p /etc/openvpn/uhem
cp /mnt/c/Users/gokss/OneDrive/Masaustu/openvpn-uhem-config.ovpn /etc/openvpn/uhem/uhem.conf

# auth-user-pass -> creds dosyasina yonlendir
sed -i 's|^auth-user-pass[[:space:]]*$|auth-user-pass /etc/openvpn/uhem/creds.txt|' \
  /etc/openvpn/uhem/uhem.conf

# persist-tun'u kaldir (olu openvpn stale tun/route birakmasin)
sed -i '/^persist-tun/d' /etc/openvpn/uhem/uhem.conf
```

Config'in sonuna asagidaki blogu ekle (izolasyon + MTU duzeltmesi):
```
# --- WSL izolasyonu (2026-08-20) ---
pull-filter ignore "redirect-gateway"   # default route'u kapmasin (host/WSL interneti korunur)
pull-filter ignore "dhcp-option DNS"    # WSL DNS'ine dokunmasin
verb 3

# --- WSL NAT MTU kara deligi duzeltmesi ---
pull-filter ignore "tun-mtu"            # server'in pushladigi 1500'u yoksay
tun-mtu 1200
mssfix 1160
```
```bash
chmod 600 /etc/openvpn/uhem/uhem.conf
```

### 4.4 - Kimlik dosyasi (`/etc/openvpn/uhem/creds.txt`, mod 600)
1. satir kullanici adi, 2. satir sifre:
```bash
umask 177
printf '<KULLANICI>\nSIFRE_BURAYA\n' > /etc/openvpn/uhem/creds.txt
chmod 600 /etc/openvpn/uhem/creds.txt
```
(`SIFRE_BURAYA` -> hesap mailindeki HPC sifresi. Baglandiktan sonra sunucuda `passwd`
ile degistirirsen, bu dosyayi da yeni sifreyle guncelle.)

### 4.5 - Kopru scripti (`/usr/local/bin/uhem-nc`)
ssh ProxyCommand'in cagirdigi script. Gerekirse tuneli acar, ic DNS ile cozer, TCP'yi yollar.
```bash
#!/bin/bash
# ssh ProxyCommand: gerekirse WSL icinde UHeM OpenVPN (split-tunnel) tunelini
# baslatir, hedefi VPN'in IC DNS'i ile cozer, sonra TCP'yi yollar.
# openfortivpn supervisorune (uysm/akdeniz/yildiz) DOKUNMAZ.
HOST="$1"; PORT="$2"
CONF=/etc/openvpn/uhem/uhem.conf
LOG=/tmp/uhem-ovpn.log
VPNDNS=10.128.5.2
ovpn_up(){ pgrep -f "[o]penvpn.*uhem/uhem.conf" >/dev/null 2>&1; }
tun_up(){ ip route show 2>/dev/null | grep -q "10.128.0.0/16.*dev tun"; }

exec 9>/tmp/uhem-ovpn.lock
flock 9
if ! ovpn_up; then
  # openvpn olu ama persist tun/route stale kalmis olabilir -> temizle
  # (yoksa tun_up() yanlis "true" verir, nc olu tun'a gidip blackhole olur)
  for t in tun0 tun1 tun2; do ip link show "$t" >/dev/null 2>&1 && ip link delete "$t" 2>/dev/null; done
  ip route flush 10.128.0.0/16 2>/dev/null
  setsid nohup openvpn --config "$CONF" >"$LOG" 2>&1 </dev/null &
  for i in $(seq 1 60); do ovpn_up && tun_up && break; sleep 0.5; done
fi
flock -u 9

# Public DNS altay icin route'suz 160.75.x verir; VPN ic DNS'i dogru 10.128.x verir.
IP=$(dig +short +time=3 +tries=2 @"$VPNDNS" "$HOST" 2>/dev/null | grep -E '^[0-9]+\.' | tail -1)
[ -z "$IP" ] && IP="$HOST"
exec nc "$IP" "$PORT"
```
```bash
chmod +x /usr/local/bin/uhem-nc
```
> DIKKAT (tuzak 3): `pgrep -f "openvpn --config ..."` KULLANMA -- pgrep `--config`'i
> kendi opsiyonu sanip patlar, surec tespiti bozulur, DUPLICATE tunel acilir. Yukaridaki
> `[o]penvpn.*uhem/uhem.conf` deseni hem `--`'yi hem self-match'i onler.

### 4.6 - Windows SSH config (`C:\Users\<KULLANICI>\.ssh\config`)
```
# UHeM (ITU Ulusal Yuksek Basarimli Hesaplama Merkezi) Altay kumesi - 2026-08-20
# WSL2 icindeki OpenVPN (split-tunnel) uzerinden. Host interneti ETKILENMEZ.
Host UHEM_Nanoparticle
    HostName altay.uhem.itu.edu.tr
    User <KULLANICI>
    Port 22
    ProxyCommand wsl.exe -d Ubuntu-24.04 /usr/local/bin/uhem-nc %h %p
    StrictHostKeyChecking accept-new
    ConnectTimeout 90
    ServerAliveInterval 30
    ServerAliveCountMax 6
```

### 4.7 - (Opsiyonel) VS Code
`%APPDATA%\Code\User\settings.json` icindeki `remote.SSH.remotePlatform` objesine ekle:
```json
"remote.SSH.remotePlatform": { "UHEM_Nanoparticle": "linux" }
```

---

## 5. Gunluk kullanim

```powershell
ssh UHEM_Nanoparticle
```
- Parola sorar -> **HPC sifresi** (creds.txt'teki; degistirdiysen yeni). Girince
  dogrudan Altay login node'undasin.
- VS Code: Remote-SSH: Connect to Host -> `UHEM_Nanoparticle`.
- **OpenVPN GUI acma** -- gerek yok, kopru WSL'de tuneli otomatik kaldirir.
- Ilk baglanti (soguk) ~3-10 sn (VPN kalkiyor). Sonraki baglantilar tunel ayaktaysa hizli.
- **Login node'da agir is calistirma** -> `sbatch`/`salloc` (bkz. UHeM-Kit/Utilize).

Ilk giriste:
```bash
passwd        # sifreyi degistir; sonra creds.txt'i de guncelle
projelerim -l # kota (CpuSaat/disk)
```

---

## 6. Kurulumda cozulen 3 tuzak

### Tuzak 1 - MTU kara deligi (SSH KEX asiliyordu)
**Belirti:** `ssh UHEM_Nanoparticle` -> `Connection timed out during banner exchange` /
`Connection to UNKNOWN port 65535 timed out`. nc baglaniyor ama SSH banner/KEX gelmiyor.
**Kok neden:** WSL, openvpn'i Hyper-V NAT arkasinda calistirir; ekstra kapsulleme yuzunden
efektif yol MTU'su 1500'un altina duser. Server'in pushladigi `tun-mtu 1500` ile buyuk
KEX paketleri (SSH2_MSG_KEX_ECDH_REPLY) parcalanip dusuyor. (Ayni config host GUI'de
1500 ile sorunsuz calisir cunku gercek TAP adapter var, ekstra NAT yok.)
**Cozum:** config'e `pull-filter ignore "tun-mtu"` + `tun-mtu 1200` + `mssfix 1160`.
Hala asiliyorsa mssfix'i 1120'ye dusur.

### Tuzak 2 - Ic DNS zorunlu (public IP route'suz)
**Belirti:** tunel ayakta, ama `nc altay 22` blackhole; ya da yanlis IP'ye gidiyor.
**Kok neden:** public DNS `altay.uhem.itu.edu.tr` -> `160.75.120.55`; bu IP tunelde
route'lu degil (pushed route'lar: 10.128/16, 10.0.55/24, 160.75.120.120/32). Dogru IP
VPN ic DNS'inden gelir: `dig @10.128.5.2 altay.uhem.itu.edu.tr` -> `10.128.2.40`
(10.128/16 icinde -> route'lu). sariyer de ayni sekilde 10.128.2.32.
**Cozum:** kopru hedefi `dig @10.128.5.2` ile cozer, sonra nc'ler.

### Tuzak 3 - pgrep `--config` self-sabotaj
**Belirti:** kopru her cagrida yeni openvpn baslatir -> birden cok tun (tun0, tun1),
cift route, asimetrik yonlendirme, SSH kilitlenir.
**Kok neden:** `pgrep -f "openvpn --config ..."` -> pgrep `--config`'i opsiyon sanip
"unrecognized option" ile patlar; `ovpn_up` hep basarisiz -> her seferinde yeni tunel.
Ayrica desen kendi pgrep surecini de yakalayabilir (self-match).
**Cozum:** `pgrep -f "[o]penvpn.*uhem/uhem.conf"` (`--` yok + `[o]` bracket self-match'i onler).

---

## 7. openfortivpn supervisor'u ile birlikte yasama (KRITIK izolasyon)

Bu makinede `uysm`/`akdeniz`/`yildiz` icin kalici bir **openfortivpn supervisor**
sistemi var (bkz. `uysm_setup.md` bolum 9-12). UHeM kurulumu buna **bilerek hic
dokunmaz**:

- `uhem-nc` yalnizca kendi openvpn'ini yonetir: `pgrep -f "[o]penvpn.*uhem"`,
  `pkill` YOK (supervisor `openfortivpn` surecleriyle ilgilenir, openvpn ile degil).
  Iki taraf birbirinin surecini asla oldurmez.
- UHeM **split-tunnel**; default route'u KAPMAZ (`pull-filter ignore "redirect-gateway"`).
  Yani supervisor'in default-route yonetimi (ppp0 uzerinden uysm/akdeniz) etkilenmez.
  UHeM sadece 10.128/16, 10.0.55/24, 160.75.120.120/32 icin spesifik route ekler.
- WSL DNS'ine dokunmaz (`pull-filter ignore "dhcp-option DNS"`, `update-resolv-conf` YOK).
- Sonuc: uysm/akdeniz/yildiz tunelleri UP iken bile UHeM'e baglanabilirsin; UHeM'in
  spesifik route'lari daha spesifik oldugu icin (10.128.x) dogru sekilde tun0'a gider,
  geri kalan trafik supervisor'in default'una (ppp0) ya da eth0'a gider.

---

## 8. Komutlar / sorun giderme

| Ihtiyac | Komut (Windows PowerShell) |
|---|---|
| WSL tunel ayakta mi? | `wsl -d Ubuntu-24.04 -u root pgrep -af openvpn` |
| 10.128 route var mi? | `wsl -d Ubuntu-24.04 -u root ip route show \| Select-String 10.128` |
| altay ic IP cozumu | `wsl -d Ubuntu-24.04 -u root dig +short '@10.128.5.2' altay.uhem.itu.edu.tr` |
| openvpn logu | `wsl -d Ubuntu-24.04 -u root tail -20 /tmp/uhem-ovpn.log` |
| tuneli sifirla | `wsl -d Ubuntu-24.04 -u root pkill -f '[o]penvpn.*uhem'` |
| ssh testi (parolasiz) | `ssh -o BatchMode=yes UHEM_Nanoparticle exit` -> `Permission denied (...password)` = zincir OK |

Karar agaci:
```
ssh UHEM_Nanoparticle asiliyor / banner timeout
  |
  +-- WSL'de 10.128 route VAR MI?
        |
        +-- YOK -> openvpn kalkmamis. /tmp/uhem-ovpn.log'a bak:
        |          - "AUTH_FAILED" -> creds.txt sifresi yanlis
        |          - "getaddrinfo/Connection refused" -> WSL interneti kesik
        |            (bkz. uysm_setup.md bolum 12: .wslconfig firewall=false)
        |
        +-- VAR ama SSH gelmiyor -> MTU (tuzak 1). uhem.conf'ta mssfix'i 1120'ye dusur,
                                    tuneli sifirla, tekrar dene.
  |
  +-- "Permission denied" aliyorsan -> zincir CALISIYOR, sadece sifre.
        creds.txt 2. satiri guncelle (kopyala-yapistir bosluguna dikkat).
```

WSL diski/ag ile ilgili acayip hatalarda (getpwnam, WSL internet yok) once host tarafina
bak: `uysm_setup.md` bolum 10 (disk dolulugu) ve 12 (.wslconfig firewall).

---

## 9. Bilinen sinirlar

- **Kalicilik yok (per-session cold start).** openvpn, ssh oturumu kapaninca WSL
  tarafindan toparlanir; her yeni baglanti tuneli yeniden acar (~3-10 sn). Kopru,
  sonraki baglantida stale tun/route'u temizleyip yeniden kurar. Warm reconnect ve
  kopma-toparlama istenirse, uysm'deki gibi bir **supervisor** (logon'da baslayan
  kalici dongu + watchdog) gerekir -- ayri bir is.
- **Split-tunnel kapsami sabit.** Sadece pushed subnet'lere (10.128/16 vb.) erisilir.
  Baska bir UHeM ic servisi farkli subnet'teyse route pushlanmiyorsa erisilmez.

---

## 10. Dosya konumlari (mevcut makine)

| Dosya | Yer |
|---|---|
| OpenVPN config (UHeM'e ozel) | WSL: `/etc/openvpn/uhem/uhem.conf` |
| Kimlik (sifre dahil, 600) | WSL: `/etc/openvpn/uhem/creds.txt` |
| Kopru scripti | WSL: `/usr/local/bin/uhem-nc` |
| openvpn logu | WSL: `/tmp/uhem-ovpn.log` |
| Kilit dosyasi | WSL: `/tmp/uhem-ovpn.lock` |
| SSH config (Host `UHEM_Nanoparticle`) | `C:\Users\gokss\.ssh\config` |
| Orijinal .ovpn (Win/Mac) | `C:\Users\gokss\OneDrive\Masaustu\openvpn-uhem-config.ovpn` |
| Orijinal .ovpn (Linux) | `C:\Users\gokss\OneDrive\Masaustu\openvpn-uhem-config-linux.ovpn` |
| Bu rehber | `C:\Users\gokss\UHEM_OpenVPN.md` |
| Genis kullanim kiti | `C:\Users\gokss\OneDrive\Masaustu\UHeM-Kit\` |

---

## 11. Guvenlik notlari

- VPN tuneli UHeM'in resmi OpenVPN config'inin aynisi (ayni gecit/sifreleme/CA/tls-auth).
  Zayiflama yok; sadece istemci Windows GUI yerine WSL openvpn.
- Gizlilik daha iyi: sadece UHeM subnet trafigi tunelden gider (split-tunnel), kisisel
  internet tunelin disinda kalir.
- Odunlesme: HPC sifresi diskte duz metin (`/etc/openvpn/uhem/creds.txt` root-600 + bu md).
  Istemezsen config'deki `auth-user-pass /etc/openvpn/uhem/creds.txt` -> `auth-user-pass`
  yap ve creds.txt'i sil -> her baglanista sorar. Koruyan sey: Windows hesabi + BitLocker.
- Kurumsal IT resmi GUI istiyorsa bilerek WSL openvpn kullaniliyor (tunel ozdes).
- VPN yazilim indirme kullanicisi `yazilimlar` ve HPC hesabi sahsa ozel; ucuncu sahislarla
  paylasilmamasi UHeM sartidir.
```
