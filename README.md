# İTÜ UHEM erişim ve kullanım kiti

UHEM hesabını bağlamak, mevcut erişimi denetlemek ve Slurm üzerinden iş çalıştırmak için Türkçe rehber ve yardımcı araçlar. **Son doğrulama: 16 Ekim 2026 — Altay, Slurm 20.11.8.** Resmî UHEM ürünü değildir; hesabınıza ait onaylı koşullar geçerlidir.

## Mevcut hesabıyla başlamak isteyenler

Linux veya WSL içinde Python 3.9+, Git ve OpenSSH istemcisi gerekir:

~~~bash
git clone https://github.com/RsGoksel/ITU_UHEM_Setup.git
cd ITU_UHEM_Setup
sh scripts/install-local-tools.sh
python3 scripts/uhem-check.py --local-only
ssh UHEM_Nanoparticle
~~~

SSH kısayolunuz zaten çalışıyorsa yeniden VPN/SSH kurulumu yapmayın. Normal SSH ile sunucu kimliğini ve girişinizi doğruladıktan sonra:

~~~bash
mkdir -p .local
python3 scripts/uhem-check.py --host UHEM_Nanoparticle --output .local/access-check.json
~~~

Kontrol aracı kimlik, proje kotası, kuyruklar, düğümler, kendi işleriniz ve modülleri okur; **iş göndermez, paket kurmaz, VPN/SSH ayarlarını değiştirmez.** Mevcut SSH kısayolunuzun ProxyCommand ayarı VPN'i başlatabilir. PASS_LOCAL_ONLY uzak bağlantının doğrulandığı anlamına gelmez. Ham rapor hesap/proje bilgisi içerir; .local/ Git dışında tutulur ve rapor 0600 izinle oluşturulur. Mevcut raporun üzerine yazılmaz.

Kurulum yalnızca ~/.local/bin/uhem-check dosyasını ekler. Bu dizin PATH içinde değilse tam yolu kullanın. Aynı dosyayla tekrar çalıştırmak güvenlidir; farklı bir mevcut dosya korunur. Güncellemek için önce mevcut aracı yedekleyin veya farklı --prefix seçin.

## Rehber

| İhtiyaç | Belge |
|---|---|
| Hesap açtırma, öğrenci ve akademik destek ayrımı | [Kayıt ve başvuru](UHeM-Kit/Setup_Login/01_Kayit.md) |
| İlk VPN ve SSH bağlantısı | [Erişim](UHeM-Kit/Setup_Login/02_Giris_VPN_SSH.md) |
| Linux/WSL için isteğe bağlı otomatik VPN köprüsü | [OpenVPN ve ProxyCommand](UHEM_OpenVPN.md) |
| Giriş sonrasında kota ve sistem kontrolü | [Kontrol listesi](UHeM-Kit/Setup_Login/03_Giris_Sonrasi_Kontrol.md) |
| İş, GPU, modül, disk ve yedekleme | [Kullanım kiti](UHeM-Kit/README.md) |
| Düzeltilen hatalar ve doğrulamanın sınırları | [Denetim kaydı](AUDIT_2026-10-16.md) |

## Çalıştırılabilir örnekler

[CPU](examples/cpu-check.sbatch) ve [GPU](examples/gpu-check.sbatch) örnekleri kısa tanı işleri içindir. Önce dosyayı okuyun, hesabınıza tanımlı proje kodunu kullanın ve yalnızca doğrulayın:

~~~bash
# UHEM üzerinde, bu dosyaların bulunduğu dizinde:
sbatch --test-only --account=PROJE_KODU examples/cpu-check.sbatch
sbatch --test-only --account=PROJE_KODU examples/gpu-check.sbatch
~~~

--test-only iş göndermez. Gerçek çalıştırma için bu seçeneği kaldırmak kaynak tüketir; talep edilen düğüm ve ücret katsayısını önceden kontrol edin. Login sunucusunda eğitim/simülasyon çalıştırmayın. İnteraktif kaynak almak (salloc) tek başına hesap düğümüne geçirmez; hesaplamayı srun ile başlatın.

## Güncellik ve gizlilik

Öğrenci yüksek lisans desteği resmî ana sitede **50.000 çekirdek-saat** olarak belirtilir; ücretsiz **400.000** desteği belirli koşullardaki **öğretim üyelerine** yöneliktir. Öğrenci projesi ikinci kez açılamaz; danışmanla akademik proje yolu ayrıca değerlendirilir. Eski portal metniyle miktarlar uyuşmadığı için güncel tahsisi UHEM'e teyit ettirin. [Resmî koşullar](https://uhem.itu.edu.tr/kullanim/kullanim-turleri).

Kuyruk envanteri tarihli bir gözlemdir; sinfo ve scontrol show partition ile tekrar bakın. GPU modeli tahsisi veya anlık boş kapasite garantisi değildir. A100 kuyrukları ile aynı düğümleri kullanan gpu2dq ayrı GPU kapasitesi sayılmaz. GH200 erişimi bu depoda doğrulanmış değildir.

VPN profili, parola, özel anahtar, erişim bağlantısındaki token veya kişisel kontrol raporunu depoya eklemeyin. Örneklerde gerçek parola bulunmaz; .gitignore tek başına gizlilik garantisi sağlamaz.

## Geliştirme

~~~bash
python3 -m unittest discover -s tests -v
bash -n scripts/uhem-proxy.sh
sh -n scripts/install-local-tools.sh
~~~

[MIT lisansı](LICENSE).
