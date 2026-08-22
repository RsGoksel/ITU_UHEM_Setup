# 03 — Giriş Sonrası İlk Kontroller

Altay'a ilk kez bağlandığında, iş vermeye başlamadan önce şu kontrolleri yap.

## 1. Şifreyi değiştir

```bash
passwd
```

## 2. Kim/nerede olduğunu gör

```bash
whoami          # kullanıcı adın (örn. <KULLANICI>)
hostname        # altay (login node'dasın)
pwd             # /ari/users/<kullanici> (ev dizinin, /ari beegfs üzerinde)
id              # grup/proje üyeliklerin
```

## 3. Projeni ve kotanı gör

```bash
projelerim      # projelerinin özeti (durum, kullanıcılar, anlık iş limitleri)
projelerim -l   # DETAYLI: kullanılan CpuSaat / toplam, disk GB, başlangıç-bitiş tarihi
```

Örnek çıktı (nakane projesi, 2026-08-20):

```
nakane  ACIK(active)  MaxSubmit=36  MaxCpuRunning=19424  MaxJobRunning=12
Kullanilan-CpuSaat: 132,909/395,904 (%33)   Disk: 573/1,124 GB (%50)
Baslangic: 2025-04-07   Bitis: 2026-10-07
```

> Bu kota **projeye ortak** (tüm proje kullanıcıları aynı havuzu paylaşır),
> kişisel değil. `%` doldukça ekip olarak dikkat.

## 4. Kuyrukları ve boş makineleri gör

```bash
spart           # kuyruklar, boş/toplam çekirdek, senin iş sayın
```

Altay kuyrukları (2026-08):

| Kuyruk | Kaynak | Süre limiti |
|--------|--------|-------------|
| `defq` (varsayılan) | CPU | 10 gün |
| `cpu2dq` | CPU | 2 gün |
| `bigjobq` | CPU (çok node) | 3 gün |
| `longq` | CPU | 21 gün |
| `gpu2dq` | 1× A100 80GB | 2 gün |
| `a100q` | 1× A100 80GB | 10 gün |
| `a100x4q` | 4× A100 80GB NVLink | 10 gün |
| `mi210q` | AMD MI210 | — |

## 5. Sarıyer'den taşınacak verin var mı? (2026 geçişi)

```bash
ls /SARIYER/users/$USER      # eski Sarıyer/Okyanus verilerin (salt-okunur)
```

Doluysa **31.08.2026'a kadar** `/ari` altına kopyala (bkz. Önemli Notlar).
Yeni kullanıcıysan büyük ihtimalle boştur.

## 6. İşlerini görme

```bash
isler           # senin işlerin (kuyrukta/çalışan)
isler <JOBID>   # o işin çalıştığı makinelerin yük/hafıza durumu
sunucular       # bir işine ayrılmış sunucuların adları
kullanim-istatigi   # son 1 aylık iş istatistiğin
```

## Kontrol listesi

- [ ] `passwd` ile şifre değişti
- [ ] `projelerim -l` çalışıyor, kota görünüyor
- [ ] `spart` çalışıyor
- [ ] `/SARIYER/users/$USER` kontrol edildi (veri varsa kopyalandı)
- [ ] Önemli Notlar okundu → `../Onemli_Notlar/00_ONCE_BUNU_OKU.md`
- [ ] Modüller ve iş gönderme öğrenildi → `../Utilize/`
