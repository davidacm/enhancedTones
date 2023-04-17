# Gelişmiş tonlar NVDA Eklentisi #
Bu eklenti, işlemi daha verimli hale getirmek için NVDA'daki bip seslerini yönetme yöntemini yeniden tanımlar.  

Ayrıca, bu eklenti kullanıcının bip sesini özelleştirmesine izin vermek için çeşitli dalga üreticileri uygular. Daha fazla üreticiyi çok kolay bir şekilde uygulamanıza olanak tanır.  

Kendi dalga üretecinizi oluşturmak ve bu eklentiye entegre etmekle ilgileniyorsanız, geliştirici bölümüne bakın.  

## Özellikler:

* Tamamlanana veya yeni bir tonla kesilene kadar tonu parçalar halinde çalarak bipleme sürecini iyileştirir.
* Birbirinden çok farklı sesler çıkaran çeşitli dalga üreticileri uygular. Farklı üreticileri denerken eğlenin, belki bir tanesini seversiniz!
* Eğer bir ton aynı frekanstaki başka bir ton tarafından kesilirse, dalga kesilmez, sadece süresi uzar. Böylece tonlar hızlı bir şekilde çalındığında rahatsız edici kesintiler önlenir. farklı faktörler nedeniyle bu durumdan kaçınmak her zaman mümkün değildir.
* Bir ton farklı frekanstaki başka bir ton tarafından kesilirse, yeni frekansa atlamak için bir frekans taraması yapılacaktır. Bu aynı zamanda tonlar arasındaki kesintileri önlemenizi sağlar.

Son iki özellik, sesli fare izleme gibi özellikleri kullanırken daha hoş bir ses elde edilmesini sağlar.  

## İndirme:
[En son sürüm bu bağlantıdan indirilebilir](https://davidacm.github.io/getlatest/gh/davidacm/enhancedTones)

## Bu eklentinin ana fikri:

Bu eklenti, belirli ses kartlarıyla ilgili bazı sorunları çözmek için oluşturuldu, daha iyi ses kartı sürücülerine sahip olduğumuz için bu sorunlar artık daha az yaygın. Ancak bazı kişiler, tonları çalarken yüksek gecikmeler veya ilk tonların hiç çalmaması gibi bu sorunların hala mevcut olduğunu bildirdi. Şimdi, bu eklentinin daha fazla özelliği var, bu nedenle yerel ton oluşturma ile ilgili sorunlarınız olmasa bile bu yararlı olabilir. Bunu kendiniz deneyin ve sizin için işe yarayıp yaramadığını görün.

### Orijinal bip işleminin açıklaması:

Bağlam içinde olmak. NVDA bir bip sesi verdiğinde aşağıdakileri yapar:

1. Üretilen Bip sesini içe aktarma.
2. oynatıcıyı durdurur.
3. dalga formu tonunu üretir.
4. oluşturulan tonu oynatıcıya gönderir.

Bu, bazı ses kartlarında tonları çalarken yüksek gecikmeler veya ilk tonların hiç çalınmaması gibi sorunlu olabilir. Sorun oynatıcının durdurulmasıyla ortaya çıkıyor gibi görünüyor, özellikle de bu hızlı bir şekilde tekrarlandığında.
Geçmişte bilgisayarlarımdan birinde bu sorunu yaşadım. Bu yüzden, bu eklentiyi oluşturmamın nedeni buydu. Eklentim oynatıcıyı durdurmuyor ve bu sorunu çözdü.

### Ek bip sesi işleminin açıklaması:

1. İlk olarak, bir arka plan iş parçacığı oluşturulur, bu iş parçacığı bip seslerini ve oynatıcı çıkışı ile iletişimi idare eder.
2. İş parçacığı, bir olay kilidi kullanılarak verilerin bir bip sesi çıkarması için bekletilir.
3. Bip işlevi çağrıldığında, bilgi iş parçacığına gönderilir ve iş parçacığı kilidi serbest bırakılır.
4. İş parçacığı, ton için dalga biçiminin oluşturulmasını başlatan işlevi çağırır ve olay sinyalini yeniden kilitler.
5. Üreticiden dalga formunu parçalar halinde ister ve her bir parçayı çıkış oynatıcısına gönderir. Üretic, gönderme sırasında dalga biçimini paralel olarak oluşturabilir veya tüm dalga biçimini başlangıçta oluşturabilir.
6. Dalga formunu oynatıcıya gönderirken kilit serbest bırakılırsa, bu yeni bir bip sesi için bir istek alındığı anlamına gelir, o zaman veri göndermeyi durdurur ve gerekli yeni bip sesini işlemeye başlamak için 3 numaralı adıma atlar.
7. Dalga formunun tamamı kesintisiz olarak oynatıcıya gönderildiyse, başka bir bip sinyali beklemek için 2 numaralı adıma atlar. Kilidin 4. adımda bloke edildiğini unutmayın, bu nedenle 2. adım tekrar beklemeye alınacaktır.

Bu sayede çıkış oynatıcısı hiçbir zaman durdurulmaz ve süreç daha verimli olur.

## Bu eklenti hakkında notlar:

Bu eklentiyi denerseniz orijinal ton oluşturma yönteminde sorun yaşamasanız bile özellikle hızlı tekrarlanan tonlarda tonların daha akıcı olduğunu görebilirsiniz.  

Ayrıca, bu eklenti birkaç ton üreteci uygular, sinüs üreteci varsayılan olarak etkindir. Ancak bunu NVDA'nın ton üreteci ile değiştirebilirsiniz.
Benim özel ton üreteçlerim tamamen Python ile yazılmıştır. Bu yüzden, NVDA ton üretecinden daha az etkilidirler, ancak fark fark edilebilir değildir.  

Kullanıcıların bip sesini özelleştirmesine izin vermek için başka ton üreteçleri oluşturmaya karar verdim ve ben de dahil olmak üzere bazı insanlar bunu beğendi. İşitme kaybı olan bir kullanıcı, sinüs ton üreteci ile daha rahat hissettiğini bildirdi.  

Not: Ton oluşturma, sesleri ses kartınıza verme işleviyle aynı değildir. Bu nedenle, NVDA'nın yerel ton üretecini kullansanız bile, iyileştirmeleri görmeye devam edeceksiniz.  

## İndirme:
	[En son sürüm bu bağlantıdan indirilebilir.](https://davidacm.github.io/getlatest/gh/davidacm/EnhancedTones)

## Gereksinimler:

  NVDA 2018.3 veya sonrasına ihtiyacınız var.

## Kurulum:

  Sadece bir NVDA eklentisi olarak kurun.

## kullanım:

  Eklenti işlevi, yüklediğinizde etkinleştirilecektir.  
  Etkinleştirmek veya devre dışı bırakmak için NVDA ayarlarına gidin ve "Geliştirilmiş tonlar "ı seçin. Bu kategoride aşağıdaki parametreleri ayarlayabilirsiniz:

* Eklentiyi etkinleştir. Devre dışı bırakılırsa, NVDA'nın orijinal işlevi kullanılacaktır.
Ton üretici: Ton üretecini buradan değiştirebilirsiniz. Birini seçin ve ayarları kaydetmek için enter tuşuna basın, ardından seçilen oluşturucuyu deneyin.

## geliştiriciler için:

Yeni ton oluşturma dalga biçimleri uygulamak istiyorsanız, kodda bulunan ton oluşturuculara benzer bir sınıf oluşturun ve bunu registerGenerator işlevini kullanarak kaydedin.  

Her oluşturucu sınıfı için bir kimlik, ad, startGenerate ve nextChunk yöntemleri sağlamalısınız.  

en önemli yöntemleri uygulayan AbstractGenerator sınıfını uygulayabilirsiniz. Bu sınıfı doğru bir şekilde genişletmenin minimum adımları, sampleGenerator işlevini uygulamaktır ve geçerli bir oluşturucu oluşturmak için bir kimlik ve ad sağlamanız gerekir. Sıfırdan bir jeneratör oluşturmaktan daha kolaydır.  

## katkılar, raporlar ve bağışlar:

Projemi beğendiyseniz veya bu yazılım günlük hayatınızda işinize yararsa ve bir şekilde katkıda bulunmak isterseniz aşağıdaki yöntemlerle bağışta bulunabilirsiniz:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [kripto para birimleri ve diğer yöntemler.](https://davidacm.github.io/donations/)

Hataları düzeltmek, sorunları bildirmek veya yeni özellikler istiyorsanız benimle <dhf360@gmail.com> adresinden iletişime geçebilirsiniz.  

  Veya bu projenin github deposunda:  
  [GitHub'da geliştirilmiş tonlar](https://github.com/davidacm/enhancedtones)  

    Bu eklentinin en son sürümünü bu depodan edinebilirsiniz.
