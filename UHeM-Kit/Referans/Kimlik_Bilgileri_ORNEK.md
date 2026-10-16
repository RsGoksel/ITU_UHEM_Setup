# Kimlik bilgilerini yerelde tutma şablonu

Bu dosyaya gerçek bilgi yazıp commit etmeyin. Kendi korumalı notunuzda aşağıdaki alanların **nerede saklandığını** kaydedin; parolayı bu tabloya koymak gerekmez.

| Alan | Yerel kayıtta tutulacak |
|---|---|
| Portal | https://portal.uhem.itu.edu.tr/ ve kayıtlı e-posta |
| Proje | Kişisel proje kodu, yürütücü, onaylanan amaç, grant no |
| SSH | Kendi kullanıcı adı, Host alias, özel anahtarın yolu |
| Sunucu kimliği | UHEM'den doğrulanan SSH anahtar parmak izi ve tarih |
| VPN | Profilin korumalı yolu, özel servis/tünel adı |
| Kimlik deposu | Parola yöneticisi veya 0600 izinli auth dosyasının yolu |
| Kota | Kaynak miktarı, dönem sonu ve son teyit zamanı |

Örnek dosya yerleri: ~/.config/uhem/client.ovpn, ~/.config/uhem/auth.txt, ~/.ssh/uhem. Bunlar hazır sağlanmış dosyalar değildir. Kullanıcı adı/şifre, sertifika veya tokenlı indirme adresi bu depoya eklenmez.

auth dosyası gerekiyorsa OpenVPN biçimi kullanıcı adı ve parolanın ayrı satırlarda olmasıdır. Dosyayı parola yöneticisinden veya güvenli editörden oluşturun; komut satırına yazıp kabuk geçmişine düşürmeyin. Sistem servisi kullanılıyorsa [servis rehberindeki](../../UHEM_OpenVPN.md) root erişimli yerleşim geçerlidir.
