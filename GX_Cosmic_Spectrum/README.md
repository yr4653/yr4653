# Cosmic Spectrum Opera GX Modu

Cosmic Spectrum, tarayıcıyı parlak mor bulutsularla saran, tamamen özelleştirilmiş bir Opera GX temasıdır. Mod, prosedürel olarak oluşturulmuş görsel öğeler ve "Cosmic Spectrum" kimliğine uygun, özenle seçilmiş bir renk paletiyle birlikte gelir.

## Özellikler

- **Dinamik kozmik duvar kağıtları** – statik 4K görüntü ve yıldızlar arası girdaplardan esinlenen, döngüsel animasyonlu bir GIF.
- **Elle ayarlanmış renk paleti** – vurgu, kenar çubuğu, GX Köşesi ve vurgu renkleri, zengin menekşeler ve pastel vurgularla uyum içindedir.
- **Kare logo** – Opera GX mod listeleri ve GX Köşesi kartı için hazır.
- **Sürükleyici ses profili** – prosedürel olarak oluşturulmuş arka plan müziği ve o uhrevi mor havayı taşıyan eşleştirilmiş ses efektleri. - **Genişletilebilir yapılandırma** – `config/theme_tokens.json` dosyasını düzenleyip mod paketini yeniden dışa aktararak renkleri hızlıca ayarlayın.

## Başlarken

1. Python 3.11+ sürümünün mevcut olduğundan emin olun.
2. Bağımlılıkları bir kez yükleyin: `pip install pillow numpy`.
3. Sanat varlıklarını yeniden oluşturun (oluşturulan dosyalar takip edilmediği için yeni bir ödemede gereklidir):
```bash
python scripts/generate_assets.py
```
4. Modu bir `.zip` arşivine paketleyin:
```bash
python scripts/package_mod.py
```
Paketleme betiği önce görseli ve sesi yeniden oluşturur, ardından `dist/GX_Cosmic_Spectrum.zip` dosyasını oluşturur. **GX Control → Mods → Developer → Load unpacked** yoluyla Opera GX'e içe aktarın.

## Özelleştirme ipuçları

- Bileşen renk tonlarını ince ayarlamak için `manifest.json` ve `config/theme_tokens.json` dosyalarındaki renkleri güncelleyin.
- Oluşturucuyu çalıştırdıktan sonra kendi görsellerinizi eklemek için `GX_Cosmic_Spectrum/assets/` dosyasında oluşturulan varlıkları değiştirin veya düzenleyin.
- Opera GX, animasyonlu duvar kağıtlarını `.gif`, `.webm` veya `.mp4` olarak kabul eder. Dahil edilen GIF, projeyi bağımlılıktan uzak tutar, ancak daha yüksek kaliteli bir video klip ekleyebilir ve bildirim yolunu güncelleyebilirsiniz.
- `GX_Cosmic_Spectrum/assets/audio/` dosyasındaki dosyaları değiştirerek sesi ayarlayın. Yeni prosedürel pad'ler için `scripts/generate_assets.py` dosyasıyla bunları yeniden oluşturun veya kendi `.wav`/`.ogg` parçalarınızı ekleyerek bildirim ses seviyelerini istediğiniz gibi güncelleyin.

## Atıf

Tüm görseller `scripts/generate_assets.py` dosyası tarafından prosedürel olarak oluşturulmuştur. Kişisel markanızla uyumlu hale getirmek için komut dosyası üzerinde değişiklik yapmaktan çekinmeyin.