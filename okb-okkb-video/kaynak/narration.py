import re
html = open('index.html', encoding='utf-8').read()
scenes = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\{id:'([\w-]+)',\s*d:(\d+(?:\.\d+)?)", html)]
T = {
's-hook':  ("Açılış", "Polikliniğe iki genç hasta geliyor. Aileleri ikisi için de aynı şeyi söylüyor: “Çok takıntılı.” Ama biri bir alarmla yaşıyor; diğeri bir kural kitabıyla."),
's-title': ("Başlık", "OKB mi, OKKB mi? Beş dakikada, akılda kalıcı bir ayırıcı tanı rehberi."),
's-worlds':("01 · Temel ayrım", "Aynı sıfat, iki ayrı dünya. OKB’nin çekirdeği obsesyon ve kompulsiyonlardır. OKKB ise düzen, mükemmeliyetçilik ve kontrol üzerine kurulu bir kişilik örüntüsüdür. Üstelik OKKB tanısı için obsesyon ya da kompulsiyon gerekmez."),
's-alarm': ("02 · OKB = yanlış alarm", "OKB’yi yanlış çalan bir alarm gibi düşünün. İstenmeyen bir düşünce araya girer; kaygı ya da “tam olmadı” hissi yükselir. Çocuk alarmı susturmak için bir ritüel yapar ve kısa süre rahatlar. Ama beyin ritüelin işe yaradığını öğrenir; döngü her turda güçlenir. Çocuk çoğu zaman şunu hisseder: “Bunu istemiyorum ama yapmak zorundayım.”"),
's-rules': ("02 · OKKB = kural kitabı", "OKKB ise bir kural kitabıdır. Ayrıntılara boğulma, işi bitirmeyi engelleyen mükemmeliyetçilik, görev devredememe, katılık ve inatçılık… DSM-5-TR’deki sekiz ölçütten en az dördü gerekir. Kritik fark şu: kişi kurallarını yabancı değil, doğru ve haklı bulur. Sıkıntı çoğu zaman başkaları kurala uymadığında başlar."),
's-ece':   ("03 · Vaka: Ece", "Ece dokuz yaşında. “Annem hastalanacak” düşüncesi aklından çıkmıyor; günde onlarca kez el yıkıyor. Her gece annesinden aynı güvenceyi defalarca istiyor ve annesi her seferinde veriyor. Ağlayarak “Durmak istiyorum ama duramıyorum” diyor. Bu bir alarm: OKB."),
's-kerem': ("03 · Vaka: Kerem", "Kerem on altı yaşında. Ödevlerini kusursuz olana kadar baştan yazıyor, teslim tarihlerini kaçırıyor. Grup projesinde kimseye görev vermiyor. Bu katılık iki yıldır okulda, evde ve oyunda aynı. Ona göre sorun kendisinde değil, başkalarında. Bu bir kural kitabı: OKKB örüntüsü."),
's-qintro':("04 · Muayenede 4 soru", "Muayene odasında dört soru sorun. Ayrımı genellikle tek bir ölçüt değil, bu dördünün toplamı yapar."),
's-q1':    ("04 · Soru 1", "Birinci soru: Kime ait? OKB’de düşünce yabancı ve istenmeyendir; çocuk onu itmeye çalışır. OKKB’de ise kurallar benimsenmiştir; kişiliğin bir parçasıdır."),
's-q2':    ("04 · Soru 2", "İkinci soru: Yapmazsan ne olur? OKB’de cevap felaket ya da “tam oturmama” hissidir; ritüel kaygıyı nötralize eder. OKKB’de iş yanlış ya da eksik olur; amaç standardı korumaktır."),
's-q3':    ("04 · Soru 3", "Üçüncü soru: Kim zorlanıyor? OKB’de çoğu zaman çocuğun kendisi. OKKB’de çoğu zaman çevresi: aile, öğretmen, arkadaşlar. Kısacası OKB’de çocuk belirtiyle savaşır; OKKB’de çevre, çocuğun kurallarıyla."),
's-q4':    ("04 · Soru 4", "Dördüncü soru: Ne kadar yaygın, ne zamandır? OKB belirli tetikleyiciler ve ritüellerle seyreder, dalgalanır. OKKB ise yaşamın her alanına yayılmış, kalıcı bir tarzdır; on sekiz yaş altında en az bir yıldır sürmelidir."),
's-p1':    ("05 · Tuzak 1: İçgörü", "Birinci tuzak: içgörü. Pediatrik OKB’de içgörü değişkendir; yaklaşık her on gençten birinde zayıf ya da yoktur ve küçük yaşta daha da azalır. Yani “bence bu gerekli” demesi OKB’yi dışlamaz."),
's-p2':    ("05 · Tuzak 2: Tam oturmama", "İkinci tuzak: “tam oturmama”. Simetri ve düzen OKB’si mükemmeliyetçilik gibi görünebilir. İpucu: ritüelleşme, tekrar ve bölündüğünde yoğun sıkıntı. OKKB’de ise düzen bir verimlilik iddiasıdır; oysa çoğu zaman işi yavaşlatır."),
's-p3':    ("05 · Tuzak 3: Gelişim", "Üçüncü tuzak: gelişim. “Tam böyle olsun” ritüelleri iki ile dört yaş arasında zirve yapar, sonra azalır. Kişilik ise hâlâ gelişmektedir: ergende OKKB tanısını temkinle koyun; çoğu zaman “OKKB özellikleri” demek daha doğrudur."),
's-ddx':   ("05 · Ayırıcı tanı", "Ayırıcı tanı listesini kısa tutmayın: otizm spektrum bozukluğu, tik bozuklukları, yaygın anksiyete, yeme ve istifleme bozuklukları da katılık ve tekrarla gelebilir."),
's-co':    ("06 · Birliktelik ve aile", "İkisi birlikte de görülebilir: OKB’li bireylerin yaklaşık dörtte birinde OKKB de vardır. Kontrollü bir çalışmada OKB’li çocukların ebeveynlerinde OKKB daha sık bulunmuştur. Aile uyumu ise OKB şiddetiyle ilişkilidir ve tedavi yanıtını zayıflatır. Değerlendirmeye aileyi de alın."),
's-tx':    ("07 · Tedavi", "Tedavi de farklıdır. OKB’de alarmı yeniden ayarlarız: maruz bırakma ve tepki önleme içeren BDT, gerektiğinde SSRI ve aile uyumunu azaltmak. OKKB özelliklerinde kitabı esnetiriz: esneklik ve mükemmeliyetçilik odaklı BDT. Ancak kanıt tabanı hâlâ ince."),
's-close': ("Kapanış", "Akılda kalsın: OKB bir alarmdır; çocuk onu susturmak ister. OKKB bir kural kitabıdır; çocuk herkesin onu okumasını ister. Takıldığınızda kendinize sorun: Alarm mı, kural kitabı mı?"),
's-refs':  ("Kaynaklar", "(Anlatım yok: kaynaklar ekranda.)"),
}
def tc(x): return f"{int(x//60)}:{int(x%60):02d}"
out = ["# OKB mi, OKKB mi? Seslendirme metni", "",
       "Video anlatımsız hazırlandı. Kendi sesinizle okumak isterseniz her bölüm, ekrandaki sahnenin süresine sığacak biçimde yazıldı (sakin tempo, saniyede ~2–2,5 kelime).", "",
       "| Zaman | Sahne | Metin | Kelime |", "|---|---|---|---|"]
t = 0
for sid, d in scenes:
    title, txt = T[sid]
    n = len(txt.split()) if not txt.startswith('(') else 0
    out.append(f"| {tc(t)}–{tc(t+d)} | {title} | {txt} | {n} / {d:.0f} sn |")
    t += d
out += ["", f"Toplam süre: {tc(t)}"]
open('../seslendirme_metni.md','w',encoding='utf-8').write('\n'.join(out)+'\n')
for sid, d in scenes:
    txt=T[sid][1]; n=len(txt.split())
    if n/d>2.6: print('FAST', sid, n, d, round(n/d,2))
print('total', t)
