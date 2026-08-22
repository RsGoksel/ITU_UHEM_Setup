# 01 — Modül Ortamı (Lmod)

UHeM'de derleyiciler ve programlar **modül** sistemiyle yüklenir. PATH'i kendin
kurcalamak yerine ilgili modülü yüklersin.

## Temel komutlar

```bash
module avail                 # kurulu tüm modüller
mav <arama>                  # module avail'in grep'lenebilir/aranabilir hâli
module load <MODUL>          # modül yükle
ml <MODUL>                   # module load kısayolu (parametresiz: module list)
module list                  # yüklü modüllerin
module unload <MODUL>        # modülü kaldır
module show <MODUL>          # modülün ne yaptığını gör (PATH, değişkenler)
module purge                 # tüm yüklü modülleri temizle
```

> `(D)` işareti = o ailenin **varsayılan** (default) sürümü; sadece aile adını
> yazarsan o gelir.

## DL/Python için önemli modüller (Altay, 2026-08)

Altay'da hazır bir "PyTorch" modülü **yoktur**; DL kullanıcıları genelde
**Anaconda + kendi conda env** yolunu izler ve CUDA'yı modülden alır.

```bash
# Anaconda (Python 3.12 varsayılan)
module load ANACONDA/Anaconda3-2024.06-1-python-3.12

# CUDA (GPU işleri için — gpu.sh örneğindeki isim)
module load cuda/cuda-11.7-a100q
# güncel CUDA'lar için: mav cuda
```

Kendi ortamını kur (bir kez):

```bash
module load ANACONDA/Anaconda3-2024.06-1-python-3.12
conda create -n nano python=3.11 -y
conda activate nano
pip install torch --index-url https://download.pytorch.org/whl/cu118   # CUDA sürümüne uygun wheel
pip install numpy pandas scikit-learn ...     # projenin gereksinimleri
```

> conda env'ler ev dizininde (`/ari/users/$USER`) oluşur ve **proje disk kotasına**
> yazılır. Büyük env'ler kotayı yer; `conda clean -a` ile ara ara temizle.

## Diğer öne çıkan modül aileleri

- **Derleyiciler:** `LLVM` (clang), `AOCC` (AMD), GCC tabanlı MPI modülleri
- **MPI:** `MPI/openmpi-*`, `MPI/mpich-*` (a100q/a100x4q için cuda'lı sürümler var)
- **Matematik:** `AOCL`, `OpenBLAS`, `FFTW`, `BOOST`
- **Uygulamalar:** `GROMACS`, `LAMMPS`, `NAMD`, `ANSYS`/`Fluent`, `MATLAB`, `CASTEP`, `Julia`
- **NVIDIA HPC SDK:** `NVIDIA/nvidia-hpc-sdk-a100q`

Tam liste her zaman `module avail` ile güncel görülür.

## Hazır Slurm iş betikleri

Merkez, yaygın programlar için örnek betikler koymuş:

```bash
ls /ari/progs/slurm_betikleri/
```

İçinde: `gpu.sh`, `gpu-multiGPU.sh`, `gpu-multinode.sh`,
`bir_sunucuda_birden_cok_is.sh`, `YEREL-disk-kullanimi-*.sh`,
`gaussian.sh`, `lammps_*`, `NAMD_*`, `qe-*`, `siesta-*`, `matlab.sh`, `fluent-*` ...

Kendi işin için bunları kopyalayıp uyarla (bkz. `03_GPU_Isleri.md`).
