# 02 — Slurm ile İş Gönderme

UHeM'de iş çalıştırmanın **tek yolu kuyruk sistemidir (Slurm)**. Login node'da
doğrudan program çalıştırmak yasaktır (bkz. Önemli Notlar).

## İki yol

| Yol | Ne zaman |
|-----|----------|
| **`sbatch betik.sh`** | Toplu/uzun işler — script yaz, kuyruğa at, sonucu dosyaya al |
| **`salloc` / `srun`** | İnteraktif çalışma — makine iste, üstünde elle komut çalıştır |

## A) sbatch — betikle iş gönderme

En basit CPU betiği (`is.sh`):

```bash
#!/bin/bash
#SBATCH -J denemem              # işin adı
#SBATCH -A nakane               # PROJE adı (account) — kendi projeni yaz!
#SBATCH -p defq                 # kuyruk
#SBATCH -N 1                    # sunucu (node) sayısı
#SBATCH -n 8                    # çekirdek (işlemci) sayısı
#SBATCH --time=01:00:00         # süre limiti (SS:DD:SS veya G-SS:DD:SS)
#SBATCH -o cikti_%j.log         # stdout (%j = job id)
#SBATCH -e hata_%j.log          # stderr

module load ANACONDA/Anaconda3-2024.06-1-python-3.12
python3 programim.py
```

Gönder / izle / iptal:

```bash
sbatch is.sh          # işi teslim et → "Submitted batch job <JOBID>"
isler                 # işlerini gör (veya: squeue -u $USER)
isler <JOBID>         # o işin node yük/hafıza durumu
scancel -v <JOBID>    # işi iptal et
```

### Sık kullanılan #SBATCH satırları

| Satır | Anlamı |
|-------|--------|
| `-J ad` | iş adı |
| `-A nakane` | **proje adı** (yanlışsa iş reddedilir) |
| `-p defq` | kuyruk |
| `-N 1` | node sayısı |
| `-n 8` | toplam çekirdek |
| `--ntasks-per-node=` | node başına görev |
| `--cpus-per-task=` | görev başına çekirdek (thread) |
| `--gres=gpu:1` | GPU iste (GPU kuyruklarında) |
| `--time=1-00:00:00` | 1 gün |
| `--mem=32G` | bellek (opsiyonel) |
| `-o / -e` | çıktı/hata dosyaları |
| `--mail-type=END --mail-user=...` | bitince mail |

## B) salloc / srun — interaktif

```bash
salloc -A nakane -p gpu2dq -N 1 -n 16 --gres=gpu:1 --time=02:00:00
# node ayrılınca o node'a düşersin (ya da: srun --pty bash)
# artık ağır komutları BURADA çalıştırabilirsin
module load cuda/cuda-11.7-a100q
python3 train.py
exit          # bitince ayrılan kaynağı bırak
```

> İnteraktif oturumu açık unutma — ayrılan kaynak (ve GPU faturalaması) sen `exit`
> yapana kadar devam eder.

## Kuyruk seçimi (Altay)

| Kuyruk | Kaynak | Süre | Not |
|--------|--------|------|-----|
| `defq` | CPU | 10 gün | varsayılan |
| `cpu2dq` | CPU | 2 gün | kısa CPU |
| `bigjobq` | CPU çok-node | 3 gün | büyük paralel |
| `longq` | CPU | 21 gün | çok uzun |
| `gpu2dq` | 1×A100 | 2 gün | **kısa GPU / test** |
| `a100q` | 1×A100 | 10 gün | uzun tek-GPU |
| `a100x4q` | 4×A100 NVLink | 10 gün | çok-GPU |
| `mi210q` | AMD MI210 | — | AMD GPU |

GPU işleri için detay + faturalama → `03_GPU_Isleri.md`.

## Faydalı kontroller

```bash
spart               # kuyruk doluluğu + boş çekirdek
projelerim -l       # kota (CpuSaat, disk)
kullanim-istatigi   # son 1 ay iş istatistiğin
sacct -j <JOBID>    # bitmiş işin özeti (süre, durum, exit code)
```
