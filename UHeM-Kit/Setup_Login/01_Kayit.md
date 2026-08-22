# 01 — Kayıt ve E-posta Onayı

UHeM'e bireysel başvuru genelde **yürütücü (öğretim üyesi)** tarafından yapılır;
öğrenciler/araştırmacılar mevcut bir projeye **kullanıcı olarak eklenir**.
Bu doküman "bir projeye eklendim, hesabımı nasıl aktifleştiririm" akışını anlatır.

## Genel akış (özet)

```
1. Yürütücü seni projeye kullanıcı olarak ekler
2. Sana "e-posta onayı" maili gelir        → sen onaylarsın
3. Portal şifresi maili gelir              → portala girebilirsin
4. UHeM hesabını ELLE kontrol edip onaylar → bekleme burada
5. HPC hesabı açılır: VPN + SSH kullanıcı adı/şifresi ayrı mail gelir
6. VPN kur + SSH ile bağlan                → 02 ve 03'e geç
```

## Adım adım

### 1. E-posta onay maili

Konu: *"Your e-mail address has been submitted to the ... Portal"*.
İçinde bir **onay linki** ve **onay kodu** (40 haneli hash) bulunur.

> ⚠️ **Alan adı tuzağı:** Maildeki link `portal.uybhm.itu.edu.tr` yazar.
> Bu eski alan adının **DNS kaydı YOK** — tarayıcıda `DNS_PROBE...` hatası verir.
> **Çözüm:** Host adını `uybhm` → `uhem` yap, gerisi aynı kalır:
>
> ```
> https://portal.uhem.itu.edu.tr/userConfirm.php?proId=<PROJE>&hashStr=<KOD>
> ```

Linke tıkla **veya** `https://portal.uhem.itu.edu.tr/userConfirm.php?proId=<PROJE>`
formundaki "Onay Kodu" kutusuna kodu yapıştır.

> ⚠️ **Onay kodu TEK KULLANIMLIKTIR.** Onay başarılı olduktan sonra kod tükenir.
> Tekrar denersen *"Onay kodunuzu yanlış girdiniz"* der — bu bir **hata değildir**,
> kodun zaten kullanıldığı anlamına gelir. Portala girebiliyorsan onay tamamdır.

### 2. Portal şifresi

Onaydan sonra *"Portal Şifreniz: ..."* maili gelir. Bu şifre **sadece portal**
içindir; VPN/hesaplama sistemlerinde ÇALIŞMAZ.

- Giriş: https://portal.uhem.itu.edu.tr/ → sol üstteki kutuya **İTÜ e-posta adresin** + portal şifresi.
- Portal hesabı hangi adrese eklendiyse o adresle girilir (genelde `@itu.edu.tr`, gmail değil).
- İlk girişten sonra **🔑 Portal Şifrenizi Değiştirin**.

### 3. Portaldaki "boş başvuru" normaldir

Girişte sol menüde *"Onay Bekleyen Projeler > [Proje Başlığı Belirtilmemiş]"*
görünür ve senden proje başlığı/özet ister. **Bu bir arıza değildir** — projesi
olmayan her hesaba gösterilen standart "yeni başvuru sihirbazı"dır ve senin
eklendiğin projeyle ilgisi yoktur.

- **Doldurma, gönderme, SİLME.** (Sil'e basarsan kendi taslağını silersin, zararsız ama gereksiz.)
- Tek yapman gereken: **1. İletişim ve Özlük Bilgileri**ni doldurmak (kişisel bilgin).
- Not: Öğrenciysen bu boş başvuruyu *bilerek* doldurup göndererek "öğrencilere
  ücretsiz 400.000 çekirdek-saat" programından ayrıca yararlanabilirsin — bu ayrı
  bir fırsat, zorunlu değil.

### 4. HPC hesabının açılması

UHeM, kaydını elle kontrol edip onaylar (birkaç saat–birkaç iş günü). Sonra
**"proje kullanıcısı hesabı onayı"** maili gelir. İçinde:

- **Kullanıcı adı** (örn. `<KULLANICI>`) — VPN ve SSH için AYNI
- **Şifre** — VPN ve SSH için AYNI
- **Proje Adı** (örn. `nakane`) ve **Grant No**
- VPN yazılımı indirme kullanıcısı: `yazilimlar` / (şifre mailde) — *sadece dosya indirmek için*

> Bu mail geldiğinde `02_Giris_VPN_SSH.md`'ye geç.

## İletişim (kayıt sorunları)

| Konu | Adres |
|------|-------|
| Hesap/proje/onay işlemleri | **hesap@uhem.itu.edu.tr** |
| Teknik sorunlar (SSH, iş, modül) | **destek@uhem.itu.edu.tr** |
| Genel | iletisim@uhem.itu.edu.tr |
| Telefon | **+90 212 285 70 64** |

> İpucu: Onay/aktivasyon gecikirse **telefon**, mailden belirgin şekilde hızlıdır.
> Ayrıca yürütücünün tek satırlık hatırlatma maili, senin üç mailinden etkilidir.
