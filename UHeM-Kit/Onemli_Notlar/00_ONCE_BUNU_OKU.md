# ⚠️ ÖNCE BUNU OKU — Kritik Notlar

UHeM kullanmadan önce bilinmesi gereken, çoğu "sonradan öğrenilen" ve pahalıya
mal olabilen noktalar. Tek sayfada.

---

## 1. Login node'da ağır iş ÇALIŞTIRMA

`altay` login node'u sadece **iş göndermek** içindir. Orada doğrudan eğitim/derleme/
büyük kopyalama başlatırsan, çok CPU/RAM tüketince **otomatik öldürülür**.

✅ Doğru: `sbatch betik.sh` ile kuyruğa ver, ya da `salloc`/`srun` ile node alıp orada çalış.

---

## 2. GPU faturalama tuzağı (kotayı en hızlı yiyen şey)

GPU işinde **sunucunun TÜM çekirdekleri** kullanılmış sayılır ve çarpılır:

- `a100q` → harcanan çekirdek-saatin **×2**'si CpuSaat düşülür
- `a100x4q` → **×4**

4×A100'lü node'da birkaç günlük iş ~400k'lik havuzu hızla eritir.
**Tek GPU yetiyorsa `gpu2dq`/`a100q` kullan; `a100x4q`'ya sadece gerçek multi-GPU'da geç.**
GPU boş beklerken geçen saat de faturalanır → GPU'yu dolu tut (batch/worker ayarı).

---

## 3. Yedekleme YOK

UHeM diskleri yedeklenmez. Kritik veri/kod/sonucu **UHeM dışında da** yedekle
(scp/rsync ile kendi makinene). Disk arızası = veri gider.

---

## 4. Kota PROJEYE ait, kişisel değil

Tüm proje kullanıcıları aynı CpuSaat + disk havuzunu paylaşır (nakane: ~396k CpuSaat,
1.124 GB disk, 8 kullanıcı). Sen çok harcarsan ekibe kalan azalır. `projelerim -l` ile takip et.

---

## 5. Sarıyer verisi 31.08.2026'da silinecek

Sarıyer kümesi kapandı. Eski verilerin Altay'da `/SARIYER` altında **salt-okunur**.
İçinde işine yarar veri varsa **31 Ağustos 2026'a kadar** `/ari`'ye kopyala:
`ls /SARIYER/users/$USER` ile kontrol et. (Yeni kullanıcıysan muhtemelen boş.)

---

## 6. Şifre yönetimi

- HPC kullanıcı adı/şifresi **hem VPN hem SSH** için aynıdır.
- İlk girişte `passwd` ile değiştir (mail/mesajla paylaşıldıysa mutlaka).
- Kopyala-yapıştırda **sona görünmez boşluk** takılabilir → Not Defteri'ne yapıştırıp
  temizle veya elle gir. ("Permission denied" alıyorsan ilk şüphelenilecek şey.)

---

## 7. VPN "yeşil" ≠ bağlı

OpenVPN ikonu yeşil olsa da yönlendirme kurulmamış olabilir. Kesin test:
tarayıcıda **http://sari.uhem.itu.edu.tr** açılıyorsa tünel gerçekten çalışıyor.

---

## 8. Yeni hesap "Permission denied" verirse panik yok

VPN çalışıp SSH reddediyorsa hesap küme tarafında **henüz aktifleşmemiş** olabilir
(birkaç saat). Üst üste deneme yapma (fail2ban kilitler), aralıklı dene; sürerse
`destek@uhem.itu.edu.tr`.

---

## 9. Maildeki `portal.uybhm...` linki ölü

Eski alan adının DNS'i yok. `uybhm` → `uhem` yaz: `portal.uhem.itu.edu.tr`.

---

## 10. Atıf (yayın/bildiri zorunluluğu)

UHeM kaynağı kullanan her yayında atıf gerekir + sonucu portala eklemelisin:

> Computing resources used in this work were provided by the National Center for
> High Performance Computing of Turkey (UHeM) under grant number **1022642025**.

Türkçe:

> Bu çalışmada kullanılan hesaplama kaynakları Ulusal Yüksek Başarımlı Hesaplama
> Merkezi'nin (UHeM), **1022642025** numaralı desteğiyle sağlanmıştır.
