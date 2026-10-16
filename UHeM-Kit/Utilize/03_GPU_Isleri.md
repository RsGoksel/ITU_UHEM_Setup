# GPU seçimi ve kaynak maliyeti

**Altay canlı envanteri — 16 Ekim 2026.** Anlık boşluk garantisi değildir; sinfo -N ve scontrol show partition ile yeniden kontrol edin.

| Kuyruk | Düğüm | GPU | Slurm RAM/düğüm | Azami süre |
|---|---:|---|---:|---|
| a100q | 30 | 1 × A100, 80 GB | 500.000 MB | 10 gün |
| a100x4q | 10 | 4 × A100, her biri 80 GB | 1.000.000 MB | 10 gün |
| gpu2dq | Aynı 30 a100q düğümü | 1 × A100, 80 GB | 250.000 MB | 48 saat; varsayılan 24 saat |
| mi210q | 2 | AMD MI210 ailesi | Canlı çıktıyı okuyun | 10 gün |

MI210 model belleği 64 GB'dır; bu denetimde Slurm GRES alanı GPU sayısını bildirmediği için kart sayısı doğrulanmış kabul edilmedi. MI210, NVIDIA CUDA değildir; yazılımın ROCm desteği ayrıca sınanmalıdır. [AMD MI210](https://www.amd.com/en/products/accelerators/instinct/mi200/mi210.html).

A100 düğümlerinde fiziksel sistem belleği sırasıyla 512/1024 GB; Slurm'un işe ayırdığı RAM daha düşüktür. GPU belleğiyle sistem RAM'ini karıştırmayın. Dört kartın 320 GB belleği, her yazılım için tek birleşik GPU belleği anlamına gelmez.

**UHEM GH200:** Resmî donanım sayfasında ayrı bir GH200 altyapısı vardır; Arm işlemci ve hesap erişimi Altay A100 kuyruğuyla aynı varsayılmamalıdır. Bu hesapla erişimi doğrulanmadı. Eski Sarıyer/V100 örneklerini güncel kapasite olarak kullanmayın. [UHEM donanım](https://uhem.itu.edu.tr/altyapimiz/donanim).

## Kota hesabı

projelerim -l tarafından bildirilen katsayılar:

| Kuyruk | Bir düğüm-saatin karşılığı |
|---|---:|
| a100q | 64 CPU × 1 saat × 2 = 128 çekirdek-saat |
| a100x4q | 64 CPU × 1 saat × 4 = 256 çekirdek-saat |

Düğümün tüm CPU'ları kullanılmış gibi ücretlenir. Kısa işin gerçek tüketimini kendi muhasebe kaydı ve UHEM bildirimiyle kontrol edin; burada yuvarlama/asgari ücretlendirme garantisi verilmez. gpu2dq ve MI210 için özel katsayı bu denetimde teyit edilmedi; a100q ile aynı olduğunu varsaymayın.

Bu nedenle “100 GPU-saat istiyorum” tek başına kaynak gerekçesi değildir: kuyruk, düğüm sayısı, GPU/düğüm, süre ve toplam kota karşılığını yazın. Aynı düğümde dört GPU'yu etkin kullanamayan uygulama için dört kartlı kuyruğu seçmek verimsiz olabilir.

## İlk GPU kontrolü

[GPU tanı betiğini](../../examples/gpu-check.sbatch) okuyun; --test-only ile sınayın. Gerçek çalıştırma ayrıca kaynak tüketir. Betik NVIDIA donanımını sorgular; UHEM_PYTHON tanımlıysa mevcut PyTorch ortamında küçük bir çarpım denetler. MI210'da bu NVIDIA betiğini kullanmayın. Bu revizyon GPU uygulamasını hesap düğümünde çalıştırılmış olarak raporlamaz.
