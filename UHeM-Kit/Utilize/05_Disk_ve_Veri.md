# Disk, aktarım ve yedek

Önce proje kotası:

~~~bash
/ari/progs/uhem-bin/projelerim -l
du -sh KENDI_CALISMA_DIZINIM
df -h .
~~~

projelerim proje limiti/kullanımını; du belirttiğiniz dosyaları; df tüm dosya sistemini gösterir. Bu üç değer aynı şeyi ölçmez. Kota bildirimi yaklaşık 2 saat geriden gelebilir.

## Güvenli aktarım

Yerelde, dosya yollarını kendi dizinlerinizle değiştirin:

~~~bash
rsync -av --partial --info=progress2 ./yerel-calisma/ UHEM_Nanoparticle:~/calisma/
rsync -av --partial --info=progress2 UHEM_Nanoparticle:~/calisma/ ./yedek/
~~~

İlk aktarımda --delete kullanmayın; kaynak/hedef sonundaki eğik çizginin içeriği nasıl etkilediğini kontrol edin. Büyük arşivler için önce boyut ve boş alan hesaplayın. Kaynak veriyle sonuçları ayrı tutun; ham veri üzerine yazmayın.

Kritik dosya için iki uçta sha256sum DOSYA çalıştırıp eşleştirin. Aktarım tamamlandı mesajı tek başına uygulamanın doğru veriyi kullandığını kanıtlamaz. Kısmi dosyaları tamamlanmış sonuç sanmayın.

## Scratch ve kalıcı kayıt

Düğümün yerel diski ile paylaşılan dosya sistemi farklıdır. Scratch yolunu kümenin güncel yönergesinden öğrenin; eski Sarıyer/RunSpace temizleme sürelerini Altay BeeGFS'e aynen taşımayın. Düğüm kapanışı veya temizlik işinde veri kaybını önlemek için sonuçları tahsis bitmeden proje dizinine, sonra dış yedeğe taşıyın.

UHEM'in yedekleme garantisi varsayılmamalıdır; öğrenci politikası yedeği kullanıcıya bırakır. [Öğrenci politikası](https://portal.uhem.itu.edu.tr/studentterms.php). Proje sonu saklama ve silme takvimini güncel hesap koşulundan teyit edin.

## Deney kaydı

Her koşu için Git commit'i, veri sürümü/hash'i, ortam sürümleri, Slurm iş numarası, kuyruk, düğüm/GPU, kaynak talebi, başlangıç/bitiş, rastgele tohum, hata ve çıktı hash'lerini kaydedin. Başarısız denemeler de kayda girmelidir. Tek klasöre kontrolsüz tüm ortamı, cache'i ve büyük ara dosyaları yedeklemek yerine yeniden üretim için gerekli girdileri belirleyin.
