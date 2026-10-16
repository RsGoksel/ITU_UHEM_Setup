# Slurm ile iş gönderme

Önce projelerim -l ve scontrol show partition çıktısından proje kodunuzu ve kuyruk erişimini doğrulayın. Aşağıdaki PROJE_KODU yer tutucusunu kendi onaylı hesabınızla değiştirin.

## Ön kontrol ve batch işi

Bu depodaki examples dizinini UHEM'e aktardıktan sonra:

~~~bash
sbatch --test-only --account=PROJE_KODU examples/cpu-check.sbatch
sbatch --test-only --account=PROJE_KODU examples/gpu-check.sbatch
~~~

--test-only isteği sınar ve tahminî başlama bilgisi verebilir; **iş göndermez ve uygulamayı çalıştırmaz**. Daha sonra gerçek kısa CPU tanısı istenirse:

~~~bash
sbatch --account=PROJE_KODU examples/cpu-check.sbatch
squeue -u "$USER"
~~~

Çıktı cpu-check-IS_NUMARASI.log dosyasına gider. Örnek CPU betiği bir tam CPU düğümü ister; 128 görev rezervasyonu Python kodunu kendiliğinden 128 kopya çalıştırmaz. Kaynak eşlemesini gerçek programınıza göre düzenleyin; MPI süreçlerini srun ile başlatın.

## İnteraktif kullanım: salloc ardından srun

~~~bash
salloc --account=PROJE_KODU --partition=a100q --nodes=1 --ntasks=64 --gres=gpu:1 --time=00:10:00
# Allocation granted mesajından sonra hâlâ login kabuğunda olabilirsiniz:
srun --ntasks=1 --pty bash -i
hostname
echo "$SLURM_JOB_ID"
nvidia-smi
# Hesap düğümündeki işiniz bittiğinde:
exit
# salloc kabuğunu da kapatıp tahsisi bırakın:
exit
~~~

salloc kaynak ayırır; srun uygulamayı hesap düğümünde başlatır. Bekleyen tahsiste hiçbir eğitim komutu çalıştırmayın. İnteraktif kabuk boş beklerken de tahsis kaynak tüketebilir. Tek komut alternatifi salloc [kaynak seçenekleri] srun --ntasks=1 --pty bash -i biçimindedir.

## Görev ve çekirdek farklıdır

- --nodes: düğüm sayısı.
- --ntasks: süreç/görev sayısı; paralelliği uygulamanın başlatılma biçimi belirler.
- --cpus-per-task: her görevin kullanacağı CPU sayısı.
- --gres=gpu:1: uygun kuyrukta bir GPU talebi.

Uygulamaya göre tek süreç/çok iş parçacığı veya çok süreç tasarımı seçin. Bir CPU talebini azaltmanın tam düğüm ücretlendirmesini azaltacağı varsayılmamalıdır. Örnekler 16 Ekim'deki canlı Slurm yapılandırmasında ön kontrolden geçirilmiştir; gelecekteki kabul için yeniden sınayın.

## Durum, iptal ve hata

~~~bash
squeue -u "$USER"
sacct -j IS_NUMARASI --format=JobID,State,ExitCode,Elapsed,AllocCPUS,NodeList
scancel IS_NUMARASI
~~~

scancel yalnızca belirttiğiniz işi iptal etmelidir. TimeLimit, out-of-memory, ortam hatası ve iptali ayırın; başarısız işler de kaynak tüketmiş olabilir. Yeniden başlatılabilir checkpoint ve deney kaydı hazırlayın. [Slurm salloc](https://slurm.schedmd.com/salloc.html), [sbatch](https://slurm.schedmd.com/sbatch.html).
