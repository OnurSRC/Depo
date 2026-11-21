# OKB mi, OKKB mi? Çocuk ve ergen psikiyatristleri için ayırıcı tanı videosu

**Dosya:** `okb_mi_okkb_mi.mp4`: 1920×1080, 30 fps, 5:15, Türkçe ekran metni, sentezlenmiş fon müziği (anlatım yok).

## Akılda kalıcı çekirdek

- **OKB bir alarmdır.** Çocuk onu susturmak ister. Ego-distoniktir, ama çocuklarda içgörü değişkendir.
- **OKKB bir kural kitabıdır.** Çocuk herkesin onu okumasını ister. Ego-sintoniktir.
- **Muayenede 4 soru:**
  1. Kime ait?
  2. Yapmazsan ne olur?
  3. Kim zorlanıyor?
  4. Ne kadar yaygın, ne zamandır?

## Akış

1. Açılış ve başlık
2. Temel ayrım: DSM-5-TR bölümleri ve sıklık
3. İki metafor: alarm döngüsü ve kural kitabının 8 ölçütü
4. İki kurgusal vaka: Ece (9) ve Kerem (16)
5. Muayenede 4 soru
6. Çocuk psikiyatrisine özgü 3 tuzak ve ayırıcı tanı:
   - içgörü
   - "tam oturmama"
   - gelişimsel ritüeller
7. Birliktelik ve aile
8. Tedavi
9. Kapanış ve kaynaklar

## Kanıt notları

Ekrandaki sayısal iddiaların hepsi PubMed'de tek tek doğrulandı. Hiçbir kaynakta geri çekme ya da endişe bildirimi yok. İki noktada metin bilinçli olarak yumuşatıldı:

- **POTS (2004):** Kombinasyon tedavisi belirtileri en çok azalttı. Remisyonda ise tek başına BDT ile farkı anlamlı değildi (%53,6 ve %39,3; p=0,42).
- **"OKKB eşlik edince OKB daha erken başlar" iddiası videoya alınmadı.** Coles 2008 erken başlangıç buldu. Pozza 2021 meta-analizi ise çalışma düzeyinde tersini gösterdi.

Diğer ayrıntılar:

- **İçgörü:** Selles 2018, n=852. Zayıf ya da hiç olmayan içgörü yaklaşık %11.
- **OKB + OKKB birlikteliği:** yaklaşık %25 (Pozza 2021, 34 çalışmanın meta-analizi).
- **Ebeveyn bulgusu:** Calvo 2009. Küçük örneklemli ve kör olmayan bir çalışma, ekranda da böyle belirtildi.

Tam kaynak listesi PMID'leriyle videonun son sahnesinde yer alıyor.

## Kendi sesinizle seslendirme

`seslendirme_metni.md` her sahnenin süresine göre yazılmış, zaman kodlu bir metindir. Kayıt alıp videoya eklemek için:

```bash
ffmpeg -i okb_mi_okkb_mi.mp4 -i ses.wav -filter_complex "[0:a]volume=0.35[m];[m][1:a]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k okb_mi_okkb_mi_sesli.mp4
```

## Yeniden üretme

Kaynak dosyalar `kaynak/` klasöründe. Videonun tamamı HTML ve GSAP zaman çizelgesi olarak yazıldı. Playwright her kareyi deterministik olarak çekiyor.

```bash
cd kaynak && npm install
mkdir -p segs prev
node preview.js                       # her sahnenin son karesini prev/ klasörüne çeker
for w in 0 1 2; do node render.js $w 3 30 & done; wait   # segs/seg_*.mp4
python3 music.py                      # music_raw.wav (numpy gerekir)
```

Eğitim amaçlıdır; klinik değerlendirmenin yerini tutmaz. Vakalar kurgusaldır.
