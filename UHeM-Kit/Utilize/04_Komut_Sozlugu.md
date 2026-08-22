# 04 — Komut Sözlüğü

UHeM'in kendi kısayol komutları (`/ari/progs/uhem-bin/`) + standart Slurm/modül
komutları. Kümede `komutlar` yazınca bu özetin bir kısmına ulaşılır.

## UHeM'e özel komutlar

| Komut | Ne yapar |
|-------|----------|
| `komutlar` | Sık kullanılan komutların özetini gösterir |
| `spart` | Kuyrukların doluluğu, boş/toplam çekirdek, kullanıcının iş sayısı |
| `isler` | Kullanıcının işlerini gösterir |
| `isler <JOBID>` | O işin çalıştığı makinelerin yük/hafıza durumu |
| `projelerim` | Projelerin özeti (durum, kullanıcılar, anlık iş limitleri) |
| `projelerim -l` | **Detaylı**: kullanılan/toplam CpuSaat, disk GB, başlangıç-bitiş |
| `sunucular` | Bir işe ayrılmış sunucuların adları |
| `kullanim-istatigi` | Son 1 aylık iş istatistiğin |
| `degistir <PROJE> <DIZIN>` | Dizini/dosyayı verilen projenin kotasına geçirir |
| `bos_makineler` | Boş makine/kuyruk özeti (video'daki komut; `spart` benzeri) |

## Slurm komutları

| Komut | Ne yapar |
|-------|----------|
| `sbatch betik.sh` | İş betiğini kuyruğa teslim eder |
| `salloc ...` | İnteraktif çalışma için sunucu ayırır |
| `srun --pty bash` | Ayrılan node'da interaktif kabuk |
| `scancel -v <JOBID>` | İşi iptal eder |
| `squeue -u $USER` | Kuyruktaki/çalışan işlerin (isler'e benzer) |
| `sacct -j <JOBID>` | Bitmiş işin özeti (süre, durum, exit code) |
| `sinfo` | Kuyruk/node durumu (ham) |
| `scontrol show job <JOBID>` | İşin tüm detayları |

## Modül komutları

| Komut | Ne yapar |
|-------|----------|
| `module avail` | Kurulu modüller |
| `mav <arama>` | Aranabilir/grep'lenebilir module avail |
| `module load <M>` / `ml <M>` | Modül yükle |
| `module list` / `ml` | Yüklü modüller |
| `module unload <M>` | Modülü kaldır |
| `module show <M>` | Modülün içeriği |
| `module purge` | Tümünü temizle |

## Dizin / disk

| Komut | Ne yapar |
|-------|----------|
| `pwd` | Bulunduğun dizin (`/ari/users/$USER`) |
| `quota -s` | (varsa) disk kotası |
| `beegfs-ctl --getquota --uid $USER` | beegfs (/ari) kullanıcı kotası |
| `du -sh <dizin>` | Dizin boyutu |
| `ls /SARIYER/users/$USER` | Eski Sarıyer verisi (salt-okunur) |

## Editör

| Komut | Ne yapar |
|-------|----------|
| `nano <dosya>` | Basit metin editörü |
| `vim <dosya>` | (kuruluysa) gelişmiş editör |

## Hazır betikler

```bash
ls /ari/progs/slurm_betikleri/     # örnek Slurm iş betikleri
```

## Küçük hatırlatmalar

- Uzun süren aktarım/derleme bile login node'da ağır ise öldürülür → `salloc` içinde yap.
- `$USER` = kullanıcı adın, `$HOME` = `/ari/users/$USER`.
- Ayrıntılı wiki: **http://wiki.uhem.itu.edu.tr**
