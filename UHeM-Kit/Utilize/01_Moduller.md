# Modüller ve Python ortamları

UHEM oturumunda hafif keşif:

~~~bash
bash -lc 'module -t avail'
~~~

Giriş kabuğunda module tanımlıysa doğrudan module avail, module list ve module show MODUL_ADI kullanabilirsiniz. Modül adını listeden alın; bu rehber sabit bir CUDA/GROMACS sürümünün gelecekte bulunacağını garanti etmez.

## Var olan ortamı koruyun

Bir uygulamanın mevcut Python yolu biliniyorsa yeniden ortam kurmadan sürümleri okuyun:

~~~bash
/ORTAMIN/TAM/YOLU/bin/python -c 'import sys; print(sys.executable); print(sys.version)'
~~~

Başkalarının veya tamamlanmış deneylerin ortamını güncellemeyin. Yeni bağımlılıklar için kullanıcı alanında ayrı ortam ve sabit sürüm/lock dosyası kullanın. Python venv mevcutsa etkinleştirmek yerine tam yolu kullanmak yanlış Python seçimini azaltır. Conda kullanılıyorsa kurulu Conda'nın başlatma yordamını izleyin; source activate ORTAM her kabukta çalışmaz.

## PyTorch ve CUDA

PyTorch'un hazır CUDA paketleri çoğunlukla CUDA çalışma zamanı bağımlılıklarıyla gelir. Sistemde yüklü toolkit ile paket etiketinin birebir eşit olması genel şart değildir; NVIDIA sürücüsü ve paket uyumluluğunu kontrol edin. Özel CUDA uzantısı derliyorsanız toolkit/derleyici uyumluluğu ayrıca gerekir. [PyTorch kurulum seçicisi](https://pytorch.org/get-started/locally/) ve [CUDA uyumluluk belgesi](https://docs.nvidia.com/deploy/cuda-compatibility/) esas alınmalıdır.

GPU görüldüğünü login düğümünden çıkarımlamayın. Hesap düğümünde, ayrılmış Slurm işi içinde:

~~~bash
nvidia-smi
/ORTAMIN/TAM/YOLU/bin/python -c 'import torch; print(torch.__version__, torch.version.cuda); print(torch.cuda.is_available())'
~~~

Depodaki GPU tanı betiğine UHEM_PYTHON olarak mevcut ortamın tam yolu verilebilir; hiçbir paket kurmaz. Bu revizyonda büyük bir Python/GPU ortamı yeniden kurulmadı.
