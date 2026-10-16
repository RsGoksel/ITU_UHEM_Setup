# Başlamadan önce

1. **Hesaplama Slurm üzerinden yapılır.** Login düğümünde eğitim/simülasyon başlatmayın; salloc sonrası srun ile hesap düğümüne geçin.
2. **Kota çekirdek-saat olarak izlenir.** Düğümün tüm işlemcileri kullanılmış gibi faturalandırılır; uygulamanın az çekirdek kullanması mutlaka tasarruf sağlamaz.
3. **A100 katsayıları farklıdır.** 16 Ekim 2026 canlı bildirimi: a100q 2×, a100x4q 4×. 64 çekirdekli bir düğüm için bir saat sırasıyla 128 ve 256 kota birimi. gpu2dq/MI210 katsayısı bu incelemede doğrulanmadı.
4. **Bir düğümün GPU sayısına bakın.** a100x4q dört A100 içerir; kodunuz tek GPU kullanıyorsa kalanları otomatik kullanmaz.
5. **Kuyruklar örtüşebilir.** gpu2dq, a100q ile aynı düğüm havuzunu paylaşır; ayrı 30 GPU daha varmış gibi toplamayın.
6. **Zaman ve kaynak ayrı sınırlardır.** Proje son tarihi, kredi, disk ve kuyruk çalışma süresi farklı kontrollerdir. Aylık otomatik kredi yenilemesi varsaymayın.
7. **Öğrenci ve öğretim üyesi desteği farklıdır.** Öğrenciye ücretsiz 400.000 verilmez; [başvuru koşullarına](../Setup_Login/01_Kayit.md) bakın.
8. **Düğümler paylaşılan hizmettir.** Başka projeyi ancak o projeye uygun tahsis ve yürütücü onayıyla çalıştırın; mevcut projenin kaynaklarını otomatik devretmeyin.
9. **Yedek kullanıcı sorumluluğundadır.** Genel dosya sistemi boşluğu sizin disk kotanız değildir; scratch kalıcı arşiv değildir.
10. **Bağlantı dosyaları kişiseldir.** VPN/SSH ayarlarını düzeltirken başka VPN'leri, varsayılan rotayı veya doğrulanmış sunucu anahtarlarını topluca silmeyin.

Kaynaklar: [kullanım türleri](https://uhem.itu.edu.tr/kullanim/kullanim-turleri), projelerim -l ve [denetim kaydı](../../AUDIT_2026-10-16.md).
