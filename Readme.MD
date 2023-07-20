# Python ile İnternet Sitelerin Veri Çekmek
## _www.kitapsepeti.com_, _www.kitapyurdu.com_


Proje Python3.7 ve Ubuntu 22.04 gereksinimleriyle gerçekleştirildi.

- _Selenium_
- _BeautifulSoup_

## Proje Ayağa Kaldırmak İçin;

- python3.7 -m venv py37 
- source py37/bin/activate
- pip install -r req.txt
- python kitapSepetiMongo.py yada python kitapYurduMongo.py


> Her iki site içinde çok satanlar kategorisindeki tüm satışta olan kitaplar çekilip, MongoDB'ye kaydedilmiştir.
Projenin siteler tarafından ban yemesi engellemesi için aralarda fazlaca time.sleep kullanılmıştır.
[Özellikle Kitap Yurdu sitesi için 'Genel','Edebiyat','Edebiyat Dışı' ,'Çocuk','İngilizce','Sınav'] kategorilerine ait tüm veriler alınmıştır. Ancak bu site için bazı değerlerin None olma durumu söz konusudur. Koda gerekli koşullar eklenmiştir.]

