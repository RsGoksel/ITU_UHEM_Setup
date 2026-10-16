# Giriş sonrası kontrol

Önce yerelde:

~~~bash
python3 scripts/uhem-check.py --local-only
python3 scripts/uhem-check.py --host UHEM_Nanoparticle --output .local/access-check.json
~~~

İlk komut yalnızca yerel OpenSSH bulunurluğunu denetler. İkinci komut mevcut SSH bağlantısından okur; kendi kuyruğunuza iş eklemez. SSH kısayolunuz VPN başlatıyorsa o davranış devam eder. Herhangi bir zorunlu kontrol başarısızsa PARTIAL döner; sıfır olmayan çıkış kodunu atlamayın.

UHEM oturumunda elle kontrol:

~~~bash
hostname
whoami
/ari/progs/uhem-bin/projelerim -l
sinfo -o "%P %a %l %D %t %G"
scontrol -o show partition
squeue -u "$USER"
bash -lc 'module -t avail'
~~~

**Kota:** Toplam ve kullanılan çekirdek-saat, başlangıç/bitiş ve disk limitini projelerim -l çıktısından okuyun. Toplam eksi kullanım kalan kredidir; GPU-saat ile aynı birim değildir. CPU kullanım bilgisi son 6 saati/çalışan işleri, disk bilgisi yaklaşık son 2 saati içermeyebilir.

**Kuyruk:** PartitionName, MaxTime, DefaultTime, AllowAccounts, Nodes, GRES ve düğüm durumunu birlikte inceleyin. UP olan bir kuyrukta tüm düğümler dolu, DOWN veya DRAIN olabilir.

**Yazılım:** Modüller giriş kabuğuna bağlı olabilir; SSH ile tek komut çalıştırıldığında module bulunamıyorsa bash -lc kullanın. Bu durum tek başına ortamların silindiği anlamına gelmez.

**Kontrolün sınırı:** Başarılı erişim, GPU üzerinde gerçek hesap çalıştığını kanıtlamaz. Bu depo revizyonunda tanı betikleri yalnızca Slurm --test-only ile sınandı; hesap düğümünde yeni eğitim/simülasyon başlatılmadı.

Ham JSON proje üyelerini ve hesap bilgilerini içerebilir. Yerelde koruyun; kamuya açık denetim kaydına yalnızca anonimleştirilmiş sonucu koyun.
