# İlk VPN ve SSH bağlantısı

UHEM'in hesabınıza gönderdiği güncel yönergeler ve VPN profili esastır. Portal, VPN ve SSH kimliklerinin aynı olduğunu varsaymayın; size verilen bilgileri ayrı doğrulayın.

## VPN

1. İşletim sisteminize uygun OpenVPN istemcisini güvenilir kaynaktan kurun.
2. UHEM'in verdiği kişisel profili içe aktarın. Profil sertifika/özel anahtar içerebilir; paylaşmayın, Git'e koymayın.
3. Gerekiyorsa hesabınıza ait VPN kimliğini girin. Profildeki TLS sertifika ve sunucu doğrulamasını kapatmayın.
4. Bağlantı sonrasında Altay'a erişimi sınayın. İstemcinin yeşil görünmesi tek başına SSH hesabınızın çalıştığını kanıtlamaz.

Linux ve systemd destekli WSL için [isteğe bağlı köprü rehberi](../../UHEM_OpenVPN.md) vardır. Zaten çalışan VPN'iniz varsa doğrudan SSH ile devam edin.

## SSH ve sunucu kimliği

~~~bash
ssh KULLANICI_ADI@altay.uhem.itu.edu.tr
~~~

İlk bağlantıda görünen sunucu anahtarı parmak izini UHEM'in güvenilir kanalından teyit edin. Körlemesine yes vermeyin; ssh-keyscan yalnızca anahtarı toplar, kimliği doğrulamaz. Teyit edilmiş anahtar kaydedildikten sonra otomatik araçlar StrictHostKeyChecking=yes kullanır ve bilinmeyen anahtarı kabul etmez.

Parola yerine size tanımlanmış SSH anahtarı varsa özel dosyayı koruyun:

~~~bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/uhem
ssh -i ~/.ssh/uhem KULLANICI_ADI@altay.uhem.itu.edu.tr
~~~

Mevcut anahtarın üzerine yeni anahtar üretmeyin. Başarılı girişten sonra:

~~~bash
hostname
whoami
~~~

Bu çıktı kimliği doğrulanmış oturumu gösterir. Permission denied başarısız kimlik doğrulamasıdır; başarılı giriş sayılmaz.

## Sorunu ayırın

| Belirti | Önce bakılacak |
|---|---|
| DNS hatası | VPN iç DNS'i, profilin verdiği adresler |
| Connection timed out | VPN rotası, hesaplanan hedef IP ve SSH erişimi |
| Permission denied | Kullanıcı adı, parola/anahtar, hesap etkinliği |
| Host key changed | İşlemi durdurup UHEM'e yeni parmak izini teyit ettirin |
| Portal açılıyor ama SSH açılmıyor | Portal hesabıyla hesaplama hesabı ayrı etkinleşebilir |
| KEX/aktarım takılıyor | Profil, yol MTU'su ve ağ; [tanı adımları](../../UHEM_OpenVPN.md) |

Yanlış parolayı döngüyle denemeyin; kilitlenme eşikleri/süresi bu rehberde doğrulanmadı. Destek isterken saat, hata türü ve istemci sürümünü paylaşın; parola, tam profil, anahtar veya tokenlı URL paylaşmayın.
