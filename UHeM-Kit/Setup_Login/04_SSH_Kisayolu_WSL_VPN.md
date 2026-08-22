# 04 — Tek Komutla Bağlanma (UHEM_Nanoparticle)

OpenVPN GUI'yi elle açıp sonra ayrıca SSH yapmak yerine, tek komutla otomatik
bağlanma. `uysm`/`akdeniz`/`yildiz` ile aynı WSL-köprü mantığı, ama UHeM için
**OpenVPN** (split-tunnel).

## Kullanım

```powershell
ssh UHEM_Nanoparticle
```

Parola sorar (HPC şifresi = `passwd` ile değiştirdiysen yeni şifre). Girince
doğrudan Altay login node'undasın. VS Code Remote-SSH ile de `UHEM_Nanoparticle`
host'unu seçebilirsin.

- İlk bağlantı (soğuk): WSL içinde VPN otomatik kalkar, ~3–10 sn.
- Host'un interneti **etkilenmez** (split-tunnel, sadece UHeM subnet'leri tünelden).
- OpenVPN GUI'yi elle açmana **gerek yok**; hatta açık kalması gerekmez.

## Nasıl çalışıyor

```
ssh UHEM_Nanoparticle (Windows)
  └─ ProxyCommand: wsl.exe -d Ubuntu-24.04 /usr/local/bin/uhem-nc altay.uhem.itu.edu.tr 22
       └─ uhem-nc (WSL2): openvpn calismiyorsa baslatir, 10.128.0.0/16 route'unu bekler
            ├─ openvpn (WSL2) == UDP 1194 ==> UHeM gateway 160.75.120.252
            │    └─ tun0 (172.17.x) : split-tunnel, sadece 10.128/16, 10.0.55/24, 160.75.120.120/32
            └─ hedefi VPN IC DNS'i (10.128.5.2) ile cozer: altay -> 10.128.2.40
                 └─ nc 10.128.2.40 22 ==> Altay sshd
```

Neden iç DNS: public DNS `altay.uhem.itu.edu.tr`'yi `160.75.120.55`'e çözer ama
o IP tünelde route'lu **değil**. VPN'in kendi DNS'i (10.128.5.2) doğru iç IP'yi
(`10.128.2.40`, 10.128/16 içinde → route'lu) verir. Köprü bu yüzden iç DNS kullanır.

## Kurulan dosyalar (WSL2 Ubuntu-24.04, root)

| Dosya | İşlev |
|-------|-------|
| `/usr/local/bin/uhem-nc` | ProxyCommand köprüsü (VPN'i açar, iç DNS çözer, nc'ler) |
| `/etc/openvpn/uhem/uhem.conf` | OpenVPN config (split-tunnel + MTU düzeltmesi) |
| `/etc/openvpn/uhem/creds.txt` | kullanıcı adı + şifre (mod 600) |
| `~/.ssh/config` → `Host UHEM_Nanoparticle` | SSH kısayolu (Windows) |

## Kurulumda çözülen 3 tuzak (başka makinede tekrar için)

1. **MTU kara deliği:** WSL, openvpn'i Hyper-V NAT arkasında çalıştırdığı için
   pushed `tun-mtu 1500` ile SSH KEX (büyük paket) takılıyor/asılıyor. Çözüm:
   config'e `pull-filter ignore "tun-mtu"` + `tun-mtu 1200` + `mssfix 1160`.
2. **İç DNS zorunlu:** public DNS route'suz IP verir (yukarıda). Köprü `dig
   @10.128.5.2` ile çözer.
3. **pgrep pattern:** `pgrep -f "openvpn --config ..."` → pgrep `--config`'i
   opsiyon sanıp hata verir, süreç tespiti bozulur, duplicate tünel açılır.
   Çözüm: `pgrep -f "[o]penvpn.*uhem/uhem.conf"` (--'siz + bracket self-match önler).

## Sorun giderme

```powershell
# WSL tunel durumu
wsl -d Ubuntu-24.04 -u root ip route show | Select-String 10.128
wsl -d Ubuntu-24.04 -u root pgrep -af openvpn
wsl -d Ubuntu-24.04 -u root tail -5 /tmp/uhem-ovpn.log
# tuneli sifirla
wsl -d Ubuntu-24.04 -u root pkill -f "[o]penvpn.*uhem"
```

- `banner exchange timeout` / asılıyor → MTU. `uhem.conf`'ta mssfix'i düşür (1120).
- `Permission denied` → şifre yanlış; `/etc/openvpn/uhem/creds.txt` 2. satırı güncelle.
- Bağlanmıyor, route yok → `tail /tmp/uhem-ovpn.log` (gateway/kimlik hatası).

## Güvenlik notu

`creds.txt` HPC şifresini WSL'de düz metin tutar (mod 600, root). uysm kalıbıyla
aynı ödünleşim. İstemezsen `creds.txt`'i sil ve config'deki `auth-user-pass
/etc/openvpn/uhem/creds.txt` → `auth-user-pass` yap; her bağlanışta sorar.
Diskini şifreli tut (BitLocker).
