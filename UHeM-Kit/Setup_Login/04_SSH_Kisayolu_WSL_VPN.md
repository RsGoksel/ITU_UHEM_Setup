# SSH kısayolu — Linux ve WSL

Tek kurulum tarifi [OpenVPN ve ProxyCommand rehberindedir](../../UHEM_OpenVPN.md). Bu sayfa aynı kodu tekrar etmez; iki farklı sürümün zamanla ayrışmasını önler.

- Linux'ta systemd ve TUN desteğini doğrulayın.
- WSL'de Linux içinden systemctl kullanılabiliyor olmalıdır; ağ modu/NAT/mirrored networking davranışı değişebilir.
- Çalışan SSH/VPN yapılandırması varsa koruyun; yeni profil kurmak zorunlu değildir.
- Depodaki [SSH örneğini](../../examples/ssh_config) kişisel kullanıcı ve tam betik yoluyla uyarlayın.
- Proxy yalnızca belirtilen UHEM servisini başlatır; genel openvpn süreçlerini öldürmez, tun0/tun1/tun2 veya başka VPN rotalarını silmez.

SSH kısayolu, açık sunucu anahtarı doğrulaması ve mevcut yetkilendirme gerektirir. UHEM kimlik bilgileri olmadan otomatik erişim sağlamaz.
