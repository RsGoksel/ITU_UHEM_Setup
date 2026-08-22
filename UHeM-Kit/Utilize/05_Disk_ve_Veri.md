# 05 — Disk, Veri ve Kota Yönetimi

## Dosya sistemleri (Altay)

| Yol | Ne | Özellik |
|-----|-----|---------|
| `/ari` | Ana paylaşımlı disk (beegfs) | Tüm node'lardan görünür. Ev dizinin burada: `/ari/users/$USER` |
| `/ari/progs` | Modüller, hazır betikler | Salt-okunur (sistem) |
| `/SARIYER` | Eski Sarıyer/Okyanus verisi | **Salt-okunur**, 31.08.2026'a kadar |
| `/YEREL` | Yerel scratch disk | **Sadece** a100q (8.8TB) ve a100x4q (12TB) node'larında, node'a özel |

## Kota

- Kota **projeye** bağlıdır, kullanıcıya değil. Tüm proje kullanıcıları aynı
  CpuSaat + disk havuzunu paylaşır.
- Ev dizini kişisel kotası "unlimited" görünebilir; **bağlayıcı olan proje disk
  kotasıdır** (örn. nakane: 1.124 GB).
- Kontrol:

```bash
projelerim -l                            # CpuSaat + disk % (2 saat gecikmeli)
beegfs-ctl --getquota --uid $USER        # anlık kişisel beegfs kullanımı
du -sh ~/*                               # neyin ne kadar yer kapladığı
```

## Dosyanın hangi projeye sayıldığını değiştirme

Yeni oluşan tüm dosyalar **öntanımlı projene** (örn. nakane) sayılır. Farklı bir
projeye geçirmek için:

```bash
degistir <PROJE> <DIZIN>
```

## Sarıyer verisi taşıma (2026 geçişi — 31.08.2026 son tarih)

Sarıyer kümesi kapandı; verilerin Altay'da `/SARIYER` altında salt-okunur.

```bash
ls -la /SARIYER/users/$USER              # veri var mı?
# varsa /ari altına kopyala:
cp -a /SARIYER/users/$USER/onemli_klasor /ari/users/$USER/
# veya seçili büyük veriyi rsync ile:
rsync -ah --info=progress2 /SARIYER/users/$USER/veri/ /ari/users/$USER/veri/
```

> Büyük kopyalama login node'u yorabilir → gerekiyorsa `salloc` ile bir node alıp
> orada kopyala.

## ⚠️ Yedekleme YOK

UHeM disk sistemleri **yedeklenmez**. Kritik verini (kod, sonuç, işlenmiş veri
seti) mutlaka **UHeM dışında** da yedekle:

```bash
# örnek: sonuçları kendi makinene çek (kendi bilgisayarından çalıştır, VPN açıkken)
scp -r <KULLANICI>@altay.uhem.itu.edu.tr:/ari/users/<KULLANICI>/sonuclar ./yedek/
# veya rsync
rsync -ah <KULLANICI>@altay.uhem.itu.edu.tr:/ari/users/<KULLANICI>/sonuclar/ ./yedek/sonuclar/
```

## Disk kotası dolarsa

- `du -sh ~/*` ile en büyük klasörleri bul.
- conda env'leri şişer → `conda clean -a`, kullanılmayan env'leri `conda env remove -n <ad>`.
- Ara çıktıları/checkpoint'leri temizle veya dışarı taşı.
- Geçici/scratch veriyi iş sırasında `/YEREL`'e yaz, `/ari`'yi doldurma.
