# 03 — GPU İşleri (A100 / DL Eğitimi)

Nanopartikül DL projesi gibi GPU işleri için özel rehber. **Faturalama tuzağını
mutlaka oku** — kotayı en hızlı yiyen yer burasıdır.

## GPU kuyrukları

| Kuyruk | GPU | Süre | Faturalama çarpanı |
|--------|-----|------|--------------------|
| `gpu2dq` | 1× A100 80GB | 2 gün | (kısa/test için önerilen) |
| `a100q` | 1× A100 80GB | 10 gün | **CpuSaat ×2** |
| `a100x4q` | 4× A100 80GB NVLink | 10 gün | **CpuSaat ×4** |
| `mi210q` | AMD MI210 | — | — |

> **`n` kuralı:** a100q ve a100x4q'da çekirdek sayısı `-n` **64 ve katları** olmalı
> (a100q: 64; a100x4q: 64×node). Node'un tüm çekirdekleri sana ayrılır.

## ⚠️ Faturalama tuzağı (KRİTİK)

GPU işlerinde **kullandığın sunucunun TÜM çekirdekleri kullanılmış sayılır** ve
kuyruğa göre çarpılır:

- `a100q` → harcanan çekirdek-saatin **2 katı** CpuSaat olarak düşülür
- `a100x4q` → **4 katı**

**Örnek:** a100x4q'da 64 çekirdekli bir node'da 24 saat iş =
`64 çekirdek × 24 saat × 4 = 6.144 CpuSaat`. Birkaç gün sürerse ~400k'lik havuzu
hızla eritir.

**Sonuç:**
- DL eğitimin **tek A100'e sığıyorsa** (çoğu model sığar) → `gpu2dq` (≤48 sa) veya
  `a100q` kullan.
- `a100x4q`'ya **ancak gerçekten multi-GPU** (DDP, model paralel) gerektiğinde geç,
  ve kodun 4 GPU'yu fiilen kullandığından emin ol.

## Örnek: tek-GPU DL betiği (`gpu.sh` temelli)

```bash
#!/bin/bash
#SBATCH -J nanopdl
#SBATCH -A nakane                 # PROJE adı — kendi projeni yaz
#SBATCH -p a100q                  # test için: gpu2dq
#SBATCH -n 64                     # a100q/a100x4q'da 64 ve katları
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --time=1-00:00:00
#SBATCH -o egitim_%j.log
#SBATCH -e egitim_%j.err

# Ortam
module load ANACONDA/Anaconda3-2024.06-1-python-3.12
module load cuda/cuda-11.7-a100q         # güncel için: mav cuda
source activate nano                     # kendi conda env'in

# Kontrol (log'a GPU'yu bas)
nvidia-smi
python -c "import torch;print('cuda?',torch.cuda.is_available(),torch.cuda.get_device_name(0))"

# Eğitim
python3 train.py --epochs 100 --batch 256 --ckpt /ari/users/$USER/ckpt
```

## Örnek: çok-GPU (`gpu-multiGPU.sh` temelli)

```bash
#!/bin/bash
#SBATCH -J nanopdl-4g
#SBATCH -A nakane
#SBATCH -p a100x4q
#SBATCH -n 64
#SBATCH -N 1
#SBATCH --gres=gpu:4              # 4 GPU
#SBATCH --time=1-00:00:00

module load ANACONDA/Anaconda3-2024.06-1-python-3.12
module load cuda/cuda-11.7-a100q
source activate nano

# Programın 4 GPU'yu FİİLEN kullanacak şekilde yazılmış olmalı
torchrun --nproc_per_node=4 train_ddp.py
```

## YEREL disk (scratch) — sadece a100q/a100x4q

Bu kuyruklardaki sunucularda geçici okuma/yazma için yerel disk vardır:
- `a100q`: **8.8 TB** `/YEREL`
- `a100x4q`: **12 TB** `/YEREL`

Özellikleri:
- Sistem oraya bir şey kopyalamaz; **sen** kopyalarsın, iş bitince geri **sen** alırsın.
- Her sunucuda **ayrı**dır — a120'deki `/YEREL` başka node'dan görünmez.
- Çok-node işlerde her node'a kendi kopyasını koy.
- Büyük veri setiyle çok epoch okuyorsan, `/ari` (paylaşımlı beegfs) yerine veriyi
  iş başında `/YEREL`'e kopyalamak I/O'yu hızlandırır. Örnekler:
  `/ari/progs/slurm_betikleri/YEREL-disk-kullanimi-*.sh`.

## İş verimini izleme

```bash
isler <JOBID>       # node yük + hafıza
# çalışan node'a ssh yapıp:  watch nvidia-smi   (GPU doluluğu)
sacct -j <JOBID> --format=JobID,Elapsed,MaxRSS,State,ExitCode
```

> GPU'yu %100'e yakın dolu tutmak faturalamayı **verimli** kılar; GPU boş beklerken
> geçen her saat de ×2/×4 ile faturalanır. batch size / dataloader worker sayısını
> GPU aç kalmayacak şekilde ayarla.
