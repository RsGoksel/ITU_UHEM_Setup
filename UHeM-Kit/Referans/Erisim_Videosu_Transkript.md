# Eski erişim videosu hakkında

Bu dosya önceki sürümde bir video özetini güncel kurulum reçetesi gibi sunuyordu. İstemci sürümleri, Windows/WSL ağ davranışı, sertifika ve küme bilgileri değiştiği için **birebir transkript veya güncel resmî talimat olarak kullanılmamalıdır**.

Korunan genel akış: kullanıcı hesabı onayı → kişisel VPN profili → VPN bağlantısı → doğrulanmış SSH sunucu kimliği → başarılı kullanıcı oturumu → Slurm üzerinden hesaplama.

Aşağıdaki genellemeler güncel rehberden kaldırıldı:

- Bilinmeyen yayıncıya ait yazılımı uyarıları önemsemeden çalıştırmak.
- Güvenlik duvarını veya TLS doğrulamasını genel çözüm olarak kapatmak.
- SSH'da ilk görülen anahtarı doğrulamadan kabul etmek.
- VPN istemcisindeki renk göstergesini başarılı hesap girişi saymak.
- Eski Sarıyer/V100 komut ve limitlerini Altay'a uygulamak.

Yeni kurulum için [VPN ve SSH](../Setup_Login/02_Giris_VPN_SSH.md), isteğe bağlı otomasyon için [OpenVPN rehberini](../../UHEM_OpenVPN.md) kullanın. Video bu revizyonda tekrar izlenerek doğrulanmadı; bu dosya o sınırlamayı açıkça kaydeder.
