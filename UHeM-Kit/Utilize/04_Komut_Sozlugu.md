# Komut sözlüğü

| Amaç | Komut |
|---|---|
| Giriş | ssh UHEM_Nanoparticle |
| Kimlik | hostname ; whoami |
| Proje, kredi, disk, tarih | /ari/progs/uhem-bin/projelerim -l |
| Kuyruk özeti | sinfo -o "%P %a %l %D %t %G" |
| Kuyruk ayrıntısı | scontrol show partition a100q |
| Düğüm/GPU eşlemesi | sinfo -N -h -o "%N %P %t %c %m %G" |
| Kendi işlerim | squeue -u "$USER" |
| Ön kontrol, iş göndermeden | sbatch --test-only --account=PROJE_KODU DOSYA.sbatch |
| İş gönder | sbatch --account=PROJE_KODU DOSYA.sbatch |
| Hesap düğümünde kabuk | Kaynak ayrıldıktan sonra srun --ntasks=1 --pty bash -i |
| Tek işi iptal | scancel IS_NUMARASI |
| İş sonucu | sacct -j IS_NUMARASI --format=JobID,State,ExitCode,Elapsed,AllocCPUS |
| Modüller | bash -lc 'module -t avail' |
| Kendi dizin boyutum | du -sh KENDI_DIZINIM |
| Genel dosya sistemi | df -h . |
| Dosya doğrulama | sha256sum DOSYA |
| Kullanıcı ortamı | /ORTAM/bin/python -c 'import sys; print(sys.executable)' |

quotas/projelerim yolları kurulumla değişebilir; bu yol 16 Ekim 2026'da Altay'da doğrulandı. quota -s bazı dosya sistemlerinde yanıt vermeyebilir ve bu denetimde kullanılmadı. Genel df boşluğu kişisel proje kotası değildir.

sacct çıktısında işin üst kaydı, batch/extern adımları ve job array üst kayıtlarını toplayıp tüketimi iki kez saymayın. kullanim-istatistigi gibi yardımcı özetler başarısız/kısa işleri atlayabiliyorsa resmî kota yerine kullanılamaz.
