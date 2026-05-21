# Ozon category collection

## Current status

Ozon Seller API has the best official category source:

- `POST https://api-seller.ozon.ru/v1/description-category/tree`
- requires `Client-Id` and `Api-Key`
- returns category tree with `description_category_id` and `type_id`

We cannot use it now because there is no Ozon Seller account/API key.

Public Ozon sitemap and catalog endpoints checked from the local environment returned `403`, so the current practical path is extracting the visible catalog tree from a logged-in browser session.

## Normalized output

Current normalized file: `data/ozon_categories_full.json`.

Current build status:

- raw payloads in this document: `27`
- normalized categories: `2450`
- roots: `31`
- unresolved payloads: `0`

The full Electronics DevTools JSON with `count: 196` is included below as `Raw payload: Electronics 196 links`.

## Browser extraction format

The first successful DevTools extraction from `https://www.ozon.ru/` returned:

- `count`: 196 category links
- `page_url`: `https://www.ozon.ru/`
- `root`: `Unknown`
- content: top Ozon categories plus the expanded `Электроника` catalog section

The `root: Unknown` value is expected for the current script because the catalog overlay was opened from the main page and the script did not infer the selected sidebar category. The next extractor should set `root` from the selected catalog item or allow manual root override.

## Captured Electronics Groups

Captured root section: `Электроника`.

Visible groups from the extraction:

- `Телефоны и смарт-часы`
- `Ноутбуки, планшеты и электронные книги`
- `Оптические приборы`
- `Наушники и аудиотехника`
- `Комплектующие для ПК`
- `Компьютеры и периферия`
- `Фото и видеокамеры`
- `Игровые приставки и ноутбуки`
- `Офисная техника`
- `Квадрокоптеры и аксессуары`
- `Навигаторы`
- `Умный дом`
- `Телевизоры и видеотехника`
- `Охранные системы и видеонаблюдение`
- `Аксессуары для электроники`

Examples of captured leaf URLs:

- `Смартфоны` -> `https://www.ozon.ru/category/smartfony-15502/`
- `Наушники` -> `https://www.ozon.ru/category/naushniki-15547/`
- `Видеокарты и графические ускорители` -> `https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/`
- `Настольные/умные устройства освещения` are under `Умный дом / Освещение` -> `https://www.ozon.ru/category/umnoe-osveshchenie-39963/`
- `Телевизоры` -> `https://www.ozon.ru/category/televizory-15528/`
- `Кабели и переходники` -> `https://www.ozon.ru/category/kabeli-i-perehodniki-15913/`

## Better DevTools Extractor Requirements

Next script should:

- infer selected root category from the active sidebar item;
- preserve visual section headers as parent groups;
- output rows as `root / group / category`;
- keep `url`;
- deduplicate repeated labels by URL and full path, not only by label;
- produce a payload that can be appended to `data/ozon_categories_full.json`.

## Collection Plan

For each Ozon sidebar category:

1. Open the category in the catalog overlay.
2. Expand all visible collapsed groups.
3. Scroll the category panel to the bottom.
4. Run the improved DevTools extractor.
5. Send/save the JSON payload.
6. Merge payloads into a normalized category tree.

Необработанные результаты:

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 93,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Женская одежда",
      "url": "https://www.ozon.ru/category/zhenskaya-odezhda-7501/"
    },
    {
      "root": "Unknown",
      "name": "Блузы и рубашки",
      "url": "https://www.ozon.ru/category/bluzy-i-rubashki-zhenskie-7511/"
    },
    {
      "root": "Unknown",
      "name": "Брюки, бриджи и капри",
      "url": "https://www.ozon.ru/category/bryuki-zhenskie-7512/"
    },
    {
      "root": "Unknown",
      "name": "Верхняя одежда",
      "url": "https://www.ozon.ru/category/verhnyaya-odezhda-zhenskaya-7528/"
    },
    {
      "root": "Unknown",
      "name": "Джемперы, свитеры и кардиганы",
      "url": "https://www.ozon.ru/category/svitery-dzhempery-i-kardigany-zhenskie-7537/"
    },
    {
      "root": "Unknown",
      "name": "Джинсы и джеггинсы",
      "url": "https://www.ozon.ru/category/dzhinsy-zhenskie-7503/"
    },
    {
      "root": "Unknown",
      "name": "Домашняя одежда",
      "url": "https://www.ozon.ru/category/domashnyaya-odezhda-zhenskaya-7541/"
    },
    {
      "root": "Unknown",
      "name": "Комбинезоны",
      "url": "https://www.ozon.ru/category/kombinezony-zhenskie-7513/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы и комплекты",
      "url": "https://www.ozon.ru/category/kostyumy-i-komplekty-odezhdy-zhenskie-7536/"
    },
    {
      "root": "Unknown",
      "name": "Купальники и пляжная одежда",
      "url": "https://www.ozon.ru/category/plyazhnaya-odezhda-zhenskaya-31690/"
    },
    {
      "root": "Unknown",
      "name": "Лонгсливы",
      "url": "https://www.ozon.ru/category/longslivy-zhenskie-36407/"
    },
    {
      "root": "Unknown",
      "name": "Нижнее белье",
      "url": "https://www.ozon.ru/category/nizhnee-bele-zhenskoe-7538/"
    },
    {
      "root": "Unknown",
      "name": "Носки, колготки и чулки",
      "url": "https://www.ozon.ru/category/chulki-noski-kolgotki-zhenskie-31688/"
    },
    {
      "root": "Unknown",
      "name": "Пиджаки, жакеты и жилеты",
      "url": "https://www.ozon.ru/category/zhakety-i-zhilety-zhenskie-7535/"
    },
    {
      "root": "Unknown",
      "name": "Платья и сарафаны",
      "url": "https://www.ozon.ru/category/platya-zhenskie-7502/"
    },
    {
      "root": "Unknown",
      "name": "Термобелье",
      "url": "https://www.ozon.ru/category/termobele-zhenskoe-30246/"
    },
    {
      "root": "Unknown",
      "name": "Толстовки, свитшоты и худи",
      "url": "https://www.ozon.ru/category/tolstovki-i-olimpiyki-zhenskie-7788/"
    },
    {
      "root": "Unknown",
      "name": "Туники",
      "url": "https://www.ozon.ru/category/tuniki-zhenskie-7507/"
    },
    {
      "root": "Unknown",
      "name": "Футболки и топы",
      "url": "https://www.ozon.ru/category/futbolki-i-topy-zhenskie-7505/"
    },
    {
      "root": "Unknown",
      "name": "Шорты",
      "url": "https://www.ozon.ru/category/shorty-zhenskie-7514/"
    },
    {
      "root": "Unknown",
      "name": "Юбки",
      "url": "https://www.ozon.ru/category/yubki-zhenskie-7504/"
    },
    {
      "root": "Unknown",
      "name": "Одежда больших размеров",
      "url": "https://www.ozon.ru/category/zhenskaya-odezhda-bolshih-razmerov-36728/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для беременных",
      "url": "https://www.ozon.ru/category/odezhda-dlya-beremennyh-30108/"
    },
    {
      "root": "Unknown",
      "name": "Свадебные платья",
      "url": "https://www.ozon.ru/category/svadebnye-platya-7798/"
    },
    {
      "root": "Unknown",
      "name": "Мужская одежда",
      "url": "https://www.ozon.ru/category/muzhskaya-odezhda-7542/"
    },
    {
      "root": "Unknown",
      "name": "Брюки",
      "url": "https://www.ozon.ru/category/bryuki-muzhskie-7552/"
    },
    {
      "root": "Unknown",
      "name": "Верхняя одежда",
      "url": "https://www.ozon.ru/category/verhnyaya-odezhda-muzhskaya-7543/"
    },
    {
      "root": "Unknown",
      "name": "Джемперы, свитеры и кардиганы",
      "url": "https://www.ozon.ru/category/svitery-dzhempery-i-kardigany-muzhskie-7554/"
    },
    {
      "root": "Unknown",
      "name": "Джинсы",
      "url": "https://www.ozon.ru/category/dzhinsy-muzhskie-7556/"
    },
    {
      "root": "Unknown",
      "name": "Домашняя одежда",
      "url": "https://www.ozon.ru/category/domashnyaya-odezhda-muzhskaya-7577/"
    },
    {
      "root": "Unknown",
      "name": "Комбинезоны",
      "url": "https://www.ozon.ru/category/kombinezony-muzhskie-30249/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы и комплекты",
      "url": "https://www.ozon.ru/category/komplekty-odezhdy-muzhskie-31080/"
    },
    {
      "root": "Unknown",
      "name": "Лонгсливы",
      "url": "https://www.ozon.ru/category/longslivy-muzhskie-36306/"
    },
    {
      "root": "Unknown",
      "name": "Нижнее белье",
      "url": "https://www.ozon.ru/category/nizhnee-bele-muzhskoe-7578/"
    },
    {
      "root": "Unknown",
      "name": "Носки и гетры",
      "url": "https://www.ozon.ru/category/noski-muzhskie-36563/"
    },
    {
      "root": "Unknown",
      "name": "Пиджаки, жилеты и жакеты",
      "url": "https://www.ozon.ru/category/kostyumy-muzhskie-7550/"
    },
    {
      "root": "Unknown",
      "name": "Пляжная одежда",
      "url": "https://www.ozon.ru/category/plyazhnaya-odezhda-muzhskaya-i-plavki-36665/"
    },
    {
      "root": "Unknown",
      "name": "Рубашки",
      "url": "https://www.ozon.ru/category/rubashki-muzhskie-7553/"
    },
    {
      "root": "Unknown",
      "name": "Термобелье",
      "url": "https://www.ozon.ru/category/termobele-muzhskoe-7570/"
    },
    {
      "root": "Unknown",
      "name": "Толстовки, свитшоты и худи",
      "url": "https://www.ozon.ru/category/tolstovki-i-olimpiyki-muzhskie-7555/"
    },
    {
      "root": "Unknown",
      "name": "Футболки и майки",
      "url": "https://www.ozon.ru/category/futbolki-i-polo-muzhskie-7558/"
    },
    {
      "root": "Unknown",
      "name": "Шорты",
      "url": "https://www.ozon.ru/category/shorty-muzhskie-7557/"
    },
    {
      "root": "Unknown",
      "name": "Одежда больших размеров",
      "url": "https://www.ozon.ru/category/muzhskaya-odezhda-bolshih-razmerov-36705/"
    },
    {
      "root": "Unknown",
      "name": "Детская одежда",
      "url": "https://www.ozon.ru/category/detskaya-odezhda-7580/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для девочек",
      "url": "https://www.ozon.ru/category/odezhda-dlya-devochek-7581/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для мальчиков",
      "url": "https://www.ozon.ru/category/odezhda-dlya-malchikov-7605/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для новорожденных",
      "url": "https://www.ozon.ru/category/odezhda-dlya-novorozhdennyh-7627/"
    },
    {
      "root": "Unknown",
      "name": "Школа",
      "url": "https://www.ozon.ru/category/shkolnaya-forma-7803/"
    },
    {
      "root": "Unknown",
      "name": "Униформа и рабочая одежда",
      "url": "https://www.ozon.ru/category/spetsodezhda-i-sredstva-individualnoy-zashchity-10189/"
    },
    {
      "root": "Unknown",
      "name": "Академическая одежда",
      "url": "https://www.ozon.ru/category/akademicheskaya-odezhda-36179/"
    },
    {
      "root": "Unknown",
      "name": "Медицинская одежда",
      "url": "https://www.ozon.ru/category/meditsinskaya-odezhda-7787/"
    },
    {
      "root": "Unknown",
      "name": "Поварам и официантам",
      "url": "https://www.ozon.ru/category/odezhda-dlya-povarov-31611/"
    },
    {
      "root": "Unknown",
      "name": "Рабочая спецодежда",
      "url": "https://www.ozon.ru/category/spetsodezhda-dlya-remonta-i-stroitelstva-10190/"
    },
    {
      "root": "Unknown",
      "name": "Сигнальная одежда",
      "url": "https://www.ozon.ru/category/signalnaya-odezhda-33119/"
    },
    {
      "root": "Unknown",
      "name": "Форменная одежда",
      "url": "https://www.ozon.ru/category/formennaya-odezhda-34989/"
    },
    {
      "root": "Unknown",
      "name": "Церковное облачение",
      "url": "https://www.ozon.ru/category/tserkovnoe-oblachenie-36811/"
    },
    {
      "root": "Unknown",
      "name": "Уход за одеждой",
      "url": "https://www.ozon.ru/category/sredstva-dlya-uhoda-za-odezhdoy-7757/"
    },
    {
      "root": "Unknown",
      "name": "Бретели, резинки и штрипки",
      "url": "https://www.ozon.ru/category/breteli-30505/"
    },
    {
      "root": "Unknown",
      "name": "Красители",
      "url": "https://www.ozon.ru/category/krasiteli-dlya-odezhdy-32949/"
    },
    {
      "root": "Unknown",
      "name": "Машинки для удаления катышков",
      "url": "https://www.ozon.ru/category/mashinki-dlya-udaleniya-katyshkov-14624/"
    },
    {
      "root": "Unknown",
      "name": "Ролики и щётки",
      "url": "https://www.ozon.ru/category/roliki-shchetki-dlya-snyatiya-vorsinok-7762/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода за одеждой",
      "url": "https://www.ozon.ru/category/antistatiki-i-propitki-7813/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 79,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Женская обувь",
      "url": "https://www.ozon.ru/category/zhenskaya-obuv-7640/"
    },
    {
      "root": "Unknown",
      "name": "Аквашузы",
      "url": "https://www.ozon.ru/category/akvaobuv-zhenskie-36499/"
    },
    {
      "root": "Unknown",
      "name": "Босоножки и сандалии",
      "url": "https://www.ozon.ru/category/bosonozhki-zhenskie-7645/"
    },
    {
      "root": "Unknown",
      "name": "Ботинки и полуботинки",
      "url": "https://www.ozon.ru/category/botinki-zhenskie-7651/"
    },
    {
      "root": "Unknown",
      "name": "Домашняя обувь",
      "url": "https://www.ozon.ru/category/tapochki-zhenskie-7655/"
    },
    {
      "root": "Unknown",
      "name": "Кроссовки и кеды",
      "url": "https://www.ozon.ru/category/krossovki-i-kedy-zhenskie-36484/"
    },
    {
      "root": "Unknown",
      "name": "Мокасины и топсайдеры",
      "url": "https://www.ozon.ru/category/mokasiny-i-topsaydery-zhenskie-7648/"
    },
    {
      "root": "Unknown",
      "name": "Резиновая обувь",
      "url": "https://www.ozon.ru/category/rezinovaya-obuv-zhenskaya-36497/"
    },
    {
      "root": "Unknown",
      "name": "Сабо и мюли",
      "url": "https://www.ozon.ru/category/sabo-i-myuli-zhenskie-7646/"
    },
    {
      "root": "Unknown",
      "name": "Сапоги и полусапоги",
      "url": "https://www.ozon.ru/category/sapogi-i-polusapogi-zhenskie-7652/"
    },
    {
      "root": "Unknown",
      "name": "Туфли и балетки",
      "url": "https://www.ozon.ru/category/tufli-zhenskie-7644/"
    },
    {
      "root": "Unknown",
      "name": "Угги, валенки и дутики",
      "url": "https://www.ozon.ru/category/uggi-i-valenki-zhenskie-7653/"
    },
    {
      "root": "Unknown",
      "name": "Шлепанцы и сланцы",
      "url": "https://www.ozon.ru/category/shlepantsy-zhenskie-7657/"
    },
    {
      "root": "Unknown",
      "name": "Эспадрильи",
      "url": "https://www.ozon.ru/category/espadrili-zhenskie-7649/"
    },
    {
      "root": "Unknown",
      "name": "Медицинская обувь",
      "url": "https://www.ozon.ru/category/obuv-meditsinskaya-zhenskaya-36942/"
    },
    {
      "root": "Unknown",
      "name": "Рабочая обувь",
      "url": "https://www.ozon.ru/category/obuv-rabochaya-zhenskaya-36941/"
    },
    {
      "root": "Unknown",
      "name": "Мужская обувь",
      "url": "https://www.ozon.ru/category/muzhskaya-obuv-7658/"
    },
    {
      "root": "Unknown",
      "name": "Аквашузы",
      "url": "https://www.ozon.ru/category/akvaobuv-muzhskaya-36693/"
    },
    {
      "root": "Unknown",
      "name": "Ботинки и полуботинки",
      "url": "https://www.ozon.ru/category/botinki-muzhskie-7665/"
    },
    {
      "root": "Unknown",
      "name": "Домашняя обувь",
      "url": "https://www.ozon.ru/category/tapochki-muzhskie-7671/"
    },
    {
      "root": "Unknown",
      "name": "Кеды, кроссовки и слипоны",
      "url": "https://www.ozon.ru/category/kedy-i-slipony-muzhskie-7660/"
    },
    {
      "root": "Unknown",
      "name": "Мокасины и топсайдеры",
      "url": "https://www.ozon.ru/category/mokasiny-i-topsaydery-muzhskie-7662/"
    },
    {
      "root": "Unknown",
      "name": "Резиновая обувь",
      "url": "https://www.ozon.ru/category/rezinovaya-obuv-muzhskaya-36692/"
    },
    {
      "root": "Unknown",
      "name": "Сандалии",
      "url": "https://www.ozon.ru/category/sandalii-muzhskie-7663/"
    },
    {
      "root": "Unknown",
      "name": "Сапоги и полусапоги",
      "url": "https://www.ozon.ru/category/sapogi-i-polusapogi-muzhskie-7667/"
    },
    {
      "root": "Unknown",
      "name": "Туфли",
      "url": "https://www.ozon.ru/category/tufli-muzhskie-7664/"
    },
    {
      "root": "Unknown",
      "name": "Угги, валенки и дутики",
      "url": "https://www.ozon.ru/category/uggi-i-valenki-muzhskie-7670/"
    },
    {
      "root": "Unknown",
      "name": "Шлепанцы и сланцы",
      "url": "https://www.ozon.ru/category/shlepantsy-muzhskie-7666/"
    },
    {
      "root": "Unknown",
      "name": "Эспадрильи",
      "url": "https://www.ozon.ru/category/espadrili-muzhskie-7661/"
    },
    {
      "root": "Unknown",
      "name": "Медицинская обувь",
      "url": "https://www.ozon.ru/category/obuv-meditsinskaya-35278/"
    },
    {
      "root": "Unknown",
      "name": "Рабочая обувь",
      "url": "https://www.ozon.ru/category/obuv-rabochaya-30835/"
    },
    {
      "root": "Unknown",
      "name": "Детская обувь",
      "url": "https://www.ozon.ru/category/detskaya-obuv-7639/"
    },
    {
      "root": "Unknown",
      "name": "Обувь для девочек",
      "url": "https://www.ozon.ru/category/obuv-dlya-devochek-7672/"
    },
    {
      "root": "Unknown",
      "name": "Обувь для мальчиков",
      "url": "https://www.ozon.ru/category/obuv-dlya-malchikov-7685/"
    },
    {
      "root": "Unknown",
      "name": "Школа",
      "url": "https://www.ozon.ru/category/shkolnaya-obuv-37051/"
    },
    {
      "root": "Unknown",
      "name": "Уход и аксессуары",
      "url": "https://www.ozon.ru/category/sredstva-dlya-uhoda-za-obuvyu-7763/"
    },
    {
      "root": "Unknown",
      "name": "Губки и щетки",
      "url": "https://www.ozon.ru/category/shchetki-dlya-obuvi-7771/"
    },
    {
      "root": "Unknown",
      "name": "Измерители стопы",
      "url": "https://www.ozon.ru/category/izmeriteli-stopy-7768/"
    },
    {
      "root": "Unknown",
      "name": "Колодки",
      "url": "https://www.ozon.ru/category/kolodki-7777/"
    },
    {
      "root": "Unknown",
      "name": "Косметика и чистящие средства",
      "url": "https://www.ozon.ru/category/kosmetika-i-chistyashchie-sredstva-dlya-obuvi-14629/"
    },
    {
      "root": "Unknown",
      "name": "Ледоступы и противоскользящие наклейки",
      "url": "https://www.ozon.ru/category/ledostupy-dlya-obuvi-35910/"
    },
    {
      "root": "Unknown",
      "name": "Ложки и рожки",
      "url": "https://www.ozon.ru/category/lozhki-i-rozhki-dlya-obuvi-7779/"
    },
    {
      "root": "Unknown",
      "name": "Растяжители",
      "url": "https://www.ozon.ru/category/rastyazhiteli-dlya-obuvi-31892/"
    },
    {
      "root": "Unknown",
      "name": "Стельки",
      "url": "https://www.ozon.ru/category/stelki-dlya-obuvi-7774/"
    },
    {
      "root": "Unknown",
      "name": "Сушилки для обуви",
      "url": "https://www.ozon.ru/category/sushki-dlya-obuvi-14631/"
    },
    {
      "root": "Unknown",
      "name": "Украшения",
      "url": "https://www.ozon.ru/category/ukrasheniya-dlya-obuvi-7783/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы и защита для обуви",
      "url": "https://www.ozon.ru/category/bahily-mnogorazovye-31824/"
    },
    {
      "root": "Unknown",
      "name": "Шнурки",
      "url": "https://www.ozon.ru/category/shnurki-7773/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 178,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Посуда и кухонные принадлежности",
      "url": "https://www.ozon.ru/category/posuda-i-kuhonnye-prinadlezhnosti-14501/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для приготовления",
      "url": "https://www.ozon.ru/category/posuda-dlya-prigotovleniya-19005/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные принадлежности",
      "url": "https://www.ozon.ru/category/kuhonnye-prinadlezhnosti-30711/"
    },
    {
      "root": "Unknown",
      "name": "Ножи и разделочные доски",
      "url": "https://www.ozon.ru/category/nozhi-i-razdelochnye-doski-19006/"
    },
    {
      "root": "Unknown",
      "name": "Столовая посуда",
      "url": "https://www.ozon.ru/category/stolovaya-posuda-19013/"
    },
    {
      "root": "Unknown",
      "name": "Чайники и кофейники",
      "url": "https://www.ozon.ru/category/chayniki-i-kofeyniki-30814/"
    },
    {
      "root": "Unknown",
      "name": "Бар",
      "url": "https://www.ozon.ru/category/bar-14525/"
    },
    {
      "root": "Unknown",
      "name": "Столовые приборы",
      "url": "https://www.ozon.ru/category/stolovye-pribory-14545/"
    },
    {
      "root": "Unknown",
      "name": "Предметы для сервировки стола",
      "url": "https://www.ozon.ru/category/predmety-dlya-servirovki-stola-39162/"
    },
    {
      "root": "Unknown",
      "name": "Товары для консервирования",
      "url": "https://www.ozon.ru/category/tovary-dlya-konservirovaniya-19023/"
    },
    {
      "root": "Unknown",
      "name": "Термосы и термокружки",
      "url": "https://www.ozon.ru/category/termosy-i-termokruzhki-14853/"
    },
    {
      "root": "Unknown",
      "name": "Хранение продуктов",
      "url": "https://www.ozon.ru/category/hranenie-produktov-14552/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для детей",
      "url": "https://www.ozon.ru/category/detskaya-posuda-31029/"
    },
    {
      "root": "Unknown",
      "name": "Одноразовая посуда и скатерти",
      "url": "https://www.ozon.ru/category/odnorazovaya-posuda-14559/"
    },
    {
      "root": "Unknown",
      "name": "Фильтры для воды",
      "url": "https://www.ozon.ru/category/filtry-dlya-vody-14560/"
    },
    {
      "root": "Unknown",
      "name": "Текстиль",
      "url": "https://www.ozon.ru/category/tekstil-15078/"
    },
    {
      "root": "Unknown",
      "name": "Шторы и карнизы",
      "url": "https://www.ozon.ru/category/shtory-i-zhalyuzi-15073/"
    },
    {
      "root": "Unknown",
      "name": "Постельное белье",
      "url": "https://www.ozon.ru/category/postelnoe-bele-15085/"
    },
    {
      "root": "Unknown",
      "name": "Подушки",
      "url": "https://www.ozon.ru/category/podushki-31147/"
    },
    {
      "root": "Unknown",
      "name": "Одеяла",
      "url": "https://www.ozon.ru/category/odeyala-15081/"
    },
    {
      "root": "Unknown",
      "name": "Пледы и покрывала",
      "url": "https://www.ozon.ru/category/pledy-i-pokryvala-15082/"
    },
    {
      "root": "Unknown",
      "name": "Текстиль с электроподогревом",
      "url": "https://www.ozon.ru/category/tekstil-s-elektropodogrevom-15091/"
    },
    {
      "root": "Unknown",
      "name": "Ковры и ковровые дорожки",
      "url": "https://www.ozon.ru/category/kovry-i-kovrovye-dorozhki-15055/"
    },
    {
      "root": "Unknown",
      "name": "Полотенца",
      "url": "https://www.ozon.ru/category/polotentsa-15084/"
    },
    {
      "root": "Unknown",
      "name": "Кухонный текстиль",
      "url": "https://www.ozon.ru/category/kuhonnyy-tekstil-31158/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы для мебели",
      "url": "https://www.ozon.ru/category/chehly-dlya-mebeli-15095/"
    },
    {
      "root": "Unknown",
      "name": "Наматрасники",
      "url": "https://www.ozon.ru/category/namatrasniki-i-chehly-dlya-matrasov-15080/"
    },
    {
      "root": "Unknown",
      "name": "Ткани",
      "url": "https://www.ozon.ru/category/tkani-mebelnye-34771/"
    },
    {
      "root": "Unknown",
      "name": "Фиксаторы для текстиля",
      "url": "https://www.ozon.ru/category/fiksatory-domashnego-tekstilya-41314/"
    },
    {
      "root": "Unknown",
      "name": "Освещение",
      "url": "https://www.ozon.ru/category/osveshchenie-15096/"
    },
    {
      "root": "Unknown",
      "name": "Потолочные и подвесные светильники",
      "url": "https://www.ozon.ru/category/potolochnye-svetilniki-31143/"
    },
    {
      "root": "Unknown",
      "name": "Напольные и настольные светильники",
      "url": "https://www.ozon.ru/category/napolnye-i-nastolnye-svetilniki-31145/"
    },
    {
      "root": "Unknown",
      "name": "Настенные светильники",
      "url": "https://www.ozon.ru/category/nastennye-svetilniki-31144/"
    },
    {
      "root": "Unknown",
      "name": "Уличные светильники",
      "url": "https://www.ozon.ru/category/ulichnye-svetilniki-15110/"
    },
    {
      "root": "Unknown",
      "name": "Светодиодные ленты",
      "url": "https://www.ozon.ru/category/svetodiodnye-lenty-15107/"
    },
    {
      "root": "Unknown",
      "name": "Споты и трековые светильники",
      "url": "https://www.ozon.ru/category/spoty-i-trekovye-svetilniki-31550/"
    },
    {
      "root": "Unknown",
      "name": "Рабочее освещение",
      "url": "https://www.ozon.ru/category/avariynye-svetilniki-35095/"
    },
    {
      "root": "Unknown",
      "name": "Лампочки",
      "url": "https://www.ozon.ru/category/lampochki-15101/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для освещения",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-osveshcheniya-15136/"
    },
    {
      "root": "Unknown",
      "name": "Декор и интерьер",
      "url": "https://www.ozon.ru/category/dekor-i-interer-15044/"
    },
    {
      "root": "Unknown",
      "name": "Оформление интерьера",
      "url": "https://www.ozon.ru/category/oformlenie-interera-14915/"
    },
    {
      "root": "Unknown",
      "name": "Зеркала",
      "url": "https://www.ozon.ru/category/zerkala-15051/"
    },
    {
      "root": "Unknown",
      "name": "Картины и панно",
      "url": "https://www.ozon.ru/category/kartiny-i-panno-15152/"
    },
    {
      "root": "Unknown",
      "name": "Фоторамки и фотоальбомы",
      "url": "https://www.ozon.ru/category/fotoramki-i-fotoalbomy-14637/"
    },
    {
      "root": "Unknown",
      "name": "Свечи и подсвечники",
      "url": "https://www.ozon.ru/category/svechi-i-podsvechniki-15153/"
    },
    {
      "root": "Unknown",
      "name": "Ароматы для дома",
      "url": "https://www.ozon.ru/category/aromaty-dlya-doma-30931/"
    },
    {
      "root": "Unknown",
      "name": "Часы и метеостанции",
      "url": "https://www.ozon.ru/category/chasy-i-meteostantsii-14647/"
    },
    {
      "root": "Unknown",
      "name": "Копилки",
      "url": "https://www.ozon.ru/category/kopilki-15056/"
    },
    {
      "root": "Unknown",
      "name": "Держатели и подставки интерьерные",
      "url": "https://www.ozon.ru/category/derzhateli-podstavki-i-podnosy-15114/"
    },
    {
      "root": "Unknown",
      "name": "Таблички и крепления",
      "url": "https://www.ozon.ru/category/tablichki-nomera-i-kryuchki-30520/"
    },
    {
      "root": "Unknown",
      "name": "Изделия декора из драгоценных металлов",
      "url": "https://www.ozon.ru/category/izdeliya-dekora-iz-dragotsennyh-metallov-37727/"
    },
    {
      "root": "Unknown",
      "name": "Дача и сад",
      "url": "https://www.ozon.ru/category/tovary-dlya-dachi-14633/"
    },
    {
      "root": "Unknown",
      "name": "Садовая техника",
      "url": "https://www.ozon.ru/category/sadovaya-tehnika-14692/"
    },
    {
      "root": "Unknown",
      "name": "Садовый инструмент",
      "url": "https://www.ozon.ru/category/sadovyy-inventar-i-instrumenty-14722/"
    },
    {
      "root": "Unknown",
      "name": "Садовая мебель",
      "url": "https://www.ozon.ru/category/sadovaya-mebel-14678/"
    },
    {
      "root": "Unknown",
      "name": "Парники и теплицы",
      "url": "https://www.ozon.ru/category/parniki-i-teplitsy-14742/"
    },
    {
      "root": "Unknown",
      "name": "Дачные постройки",
      "url": "https://www.ozon.ru/category/dachnye-postroyki-37455/"
    },
    {
      "root": "Unknown",
      "name": "Садовый декор",
      "url": "https://www.ozon.ru/category/sadovyy-dekor-14715/"
    },
    {
      "root": "Unknown",
      "name": "Водоснабжение для дачи",
      "url": "https://www.ozon.ru/category/vodosnabzhenie-dlya-dachi-36073/"
    },
    {
      "root": "Unknown",
      "name": "Бассейны и аксессуары",
      "url": "https://www.ozon.ru/category/basseyny-i-aksessuary-14642/"
    },
    {
      "root": "Unknown",
      "name": "Биотуалеты и септики",
      "url": "https://www.ozon.ru/category/biotualety-i-aksessuary-14659/"
    },
    {
      "root": "Unknown",
      "name": "Отпугиватели животных и насекомых",
      "url": "https://www.ozon.ru/category/otpugivateli-zhivotnyh-i-nasekomyh-38295/"
    },
    {
      "root": "Unknown",
      "name": "Отдых и пикник",
      "url": "https://www.ozon.ru/category/otdyh-i-piknik-14666/"
    },
    {
      "root": "Unknown",
      "name": "Уборка снега",
      "url": "https://www.ozon.ru/category/uborka-snega-14730/"
    },
    {
      "root": "Unknown",
      "name": "Цветы, растения и горшки",
      "url": "https://www.ozon.ru/category/tsvety-i-rasteniya-14884/"
    },
    {
      "root": "Unknown",
      "name": "Грунты, удобрения и садовая химия",
      "url": "https://www.ozon.ru/category/udobreniya-i-grunty-14746/"
    },
    {
      "root": "Unknown",
      "name": "Защита и уход за растениями",
      "url": "https://www.ozon.ru/category/zashchita-i-uhod-za-rasteniyami-14749/"
    },
    {
      "root": "Unknown",
      "name": "Цветы",
      "url": "https://www.ozon.ru/category/zhivye-tsvety-i-bukety-14951/"
    },
    {
      "root": "Unknown",
      "name": "Горшки и кашпо",
      "url": "https://www.ozon.ru/category/gorshki-podstavki-dlya-rasteniy-14756/"
    },
    {
      "root": "Unknown",
      "name": "Лейки и пульверизаторы",
      "url": "https://www.ozon.ru/category/leyki-i-opryskivateli-31648/"
    },
    {
      "root": "Unknown",
      "name": "Подставки и крепления",
      "url": "https://www.ozon.ru/category/podstavki-i-krepleniya-dlya-rasteniy-14930/"
    },
    {
      "root": "Unknown",
      "name": "Семена и саженцы",
      "url": "https://www.ozon.ru/category/semena-i-sazhentsy-14745/"
    },
    {
      "root": "Unknown",
      "name": "Хозяйственные товары",
      "url": "https://www.ozon.ru/category/hozyaystvennye-tovary-14593/"
    },
    {
      "root": "Unknown",
      "name": "Инвентарь для уборки",
      "url": "https://www.ozon.ru/category/inventar-dlya-uborki-14610/"
    },
    {
      "root": "Unknown",
      "name": "Мусорные ведра и баки",
      "url": "https://www.ozon.ru/category/musornye-vedra-i-baki-14614/"
    },
    {
      "root": "Unknown",
      "name": "Уход за одеждой и обувью",
      "url": "https://www.ozon.ru/category/uhod-za-odezhdoy-i-obuvyu-14619/"
    },
    {
      "root": "Unknown",
      "name": "Упаковка и переезд",
      "url": "https://www.ozon.ru/category/tovary-dlya-upakovki-i-pereezda-34780/"
    },
    {
      "root": "Unknown",
      "name": "Сумки хозяйственные",
      "url": "https://www.ozon.ru/category/sumki-hozyaystvennye-7817/"
    },
    {
      "root": "Unknown",
      "name": "Сумки-тележки",
      "url": "https://www.ozon.ru/category/sumki-telezhki-7821/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для стирки",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-stirki-31130/"
    },
    {
      "root": "Unknown",
      "name": "Хранение вещей",
      "url": "https://www.ozon.ru/category/hranenie-veshchey-14759/"
    },
    {
      "root": "Unknown",
      "name": "Вешалки",
      "url": "https://www.ozon.ru/category/veshalki-dlya-odezhdy-14763/"
    },
    {
      "root": "Unknown",
      "name": "Органайзеры и разделители",
      "url": "https://www.ozon.ru/category/organayzery-i-razdeliteli-14988/"
    },
    {
      "root": "Unknown",
      "name": "Коробки и контейнеры",
      "url": "https://www.ozon.ru/category/korobki-i-konteynery-31128/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы для одежды",
      "url": "https://www.ozon.ru/category/chehly-dlya-odezhdy-14764/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы для обуви",
      "url": "https://www.ozon.ru/category/chehly-dlya-obuvi-7776/"
    },
    {
      "root": "Unknown",
      "name": "Вакуумные пакеты",
      "url": "https://www.ozon.ru/category/vakuumnye-pakety-14760/"
    },
    {
      "root": "Unknown",
      "name": "Мешочки и пакеты",
      "url": "https://www.ozon.ru/category/meshki-dlya-veshchey-19052/"
    },
    {
      "root": "Unknown",
      "name": "Корзины для белья",
      "url": "https://www.ozon.ru/category/baki-dlya-belya-14987/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для ванной",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-vannoy-14594/"
    },
    {
      "root": "Unknown",
      "name": "Шторы и карнизы",
      "url": "https://www.ozon.ru/category/shtory-i-karnizy-dlya-vannoy-15015/"
    },
    {
      "root": "Unknown",
      "name": "Диспенсеры и дозаторы",
      "url": "https://www.ozon.ru/category/dispensery-31134/"
    },
    {
      "root": "Unknown",
      "name": "Полки",
      "url": "https://www.ozon.ru/category/polki-dlya-vannoy-14598/"
    },
    {
      "root": "Unknown",
      "name": "Держатели",
      "url": "https://www.ozon.ru/category/derzhateli-dlya-vannoy-komnaty-14600/"
    },
    {
      "root": "Unknown",
      "name": "Крючки, рейлинги",
      "url": "https://www.ozon.ru/category/kryuchki-dlya-vannoy-14968/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для ванной комнаты",
      "url": "https://www.ozon.ru/category/nabory-dlya-vannoy-komnaty-14976/"
    },
    {
      "root": "Unknown",
      "name": "Пробки",
      "url": "https://www.ozon.ru/category/probki-dlya-vanny-14908/"
    },
    {
      "root": "Unknown",
      "name": "Подушки",
      "url": "https://www.ozon.ru/category/podushki-dlya-vanny-14975/"
    },
    {
      "root": "Unknown",
      "name": "Ковшики",
      "url": "https://www.ozon.ru/category/kovshiki-dlya-vannoy-30579/"
    },
    {
      "root": "Unknown",
      "name": "Мыльницы",
      "url": "https://www.ozon.ru/category/mylnitsy-i-derzhateli-14597/"
    },
    {
      "root": "Unknown",
      "name": "Ершики для унитаза",
      "url": "https://www.ozon.ru/category/ershiki-dlya-unitaza-14595/"
    },
    {
      "root": "Unknown",
      "name": "Товары для бань и саун",
      "url": "https://www.ozon.ru/category/tovary-dlya-bani-i-sauny-14860/"
    },
    {
      "root": "Unknown",
      "name": "Банный текстиль",
      "url": "https://www.ozon.ru/category/bannyy-tekstil-14650/"
    },
    {
      "root": "Unknown",
      "name": "Предметы интерьера бани",
      "url": "https://www.ozon.ru/category/predmety-interera-bani-14928/"
    },
    {
      "root": "Unknown",
      "name": "Ковши, ушаты и ведра для бань",
      "url": "https://www.ozon.ru/category/kovshi-dlya-ban-14958/"
    },
    {
      "root": "Unknown",
      "name": "Веники, опахало для бани",
      "url": "https://www.ozon.ru/category/veniki-dlya-ban-14861/"
    },
    {
      "root": "Unknown",
      "name": "Запарки, соль и ароматизаторы для бани",
      "url": "https://www.ozon.ru/category/zaparki-dlya-ban-i-saun-14869/"
    },
    {
      "root": "Unknown",
      "name": "Купели",
      "url": "https://www.ozon.ru/category/kupeli-dlya-bani-34880/"
    },
    {
      "root": "Unknown",
      "name": "Сувениры и подарки",
      "url": "https://www.ozon.ru/category/suveniry-15061/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные наборы",
      "url": "https://www.ozon.ru/category/podarki-s-prikolami-15142/"
    },
    {
      "root": "Unknown",
      "name": "Флаги",
      "url": "https://www.ozon.ru/category/flagi-35086/"
    },
    {
      "root": "Unknown",
      "name": "Сувениры",
      "url": "https://www.ozon.ru/category/suveniry-34279/"
    },
    {
      "root": "Unknown",
      "name": "Сувенирное оружие",
      "url": "https://www.ozon.ru/category/suvenirnoe-oruzhie-15065/"
    },
    {
      "root": "Unknown",
      "name": "Матрешки",
      "url": "https://www.ozon.ru/category/matreshki-15063/"
    },
    {
      "root": "Unknown",
      "name": "Магниты на холодильник",
      "url": "https://www.ozon.ru/category/magnity-15062/"
    },
    {
      "root": "Unknown",
      "name": "Сувенирные деньги",
      "url": "https://www.ozon.ru/category/suvenirnye-dengi-15149/"
    },
    {
      "root": "Unknown",
      "name": "Вееры",
      "url": "https://www.ozon.ru/category/veery-30917/"
    },
    {
      "root": "Unknown",
      "name": "Сувенирное мыло",
      "url": "https://www.ozon.ru/category/suvenirnoe-mylo-32087/"
    },
    {
      "root": "Unknown",
      "name": "Шары со снегом",
      "url": "https://www.ozon.ru/category/shary-so-snegom-30771/"
    },
    {
      "root": "Unknown",
      "name": "Товары для праздников",
      "url": "https://www.ozon.ru/category/tovary-dlya-prazdnikov-14793/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные упаковки",
      "url": "https://www.ozon.ru/category/podarochnaya-upakovka-14809/"
    },
    {
      "root": "Unknown",
      "name": "Праздничный декор",
      "url": "https://www.ozon.ru/category/ukrasheniya-i-figurki-14973/"
    },
    {
      "root": "Unknown",
      "name": "Воздушные шары и аксессуары",
      "url": "https://www.ozon.ru/category/vozdushnye-shary-31240/"
    },
    {
      "root": "Unknown",
      "name": "Мыльные пузыри",
      "url": "https://www.ozon.ru/category/mylnye-puzyri-14822/"
    },
    {
      "root": "Unknown",
      "name": "Свадебные товары",
      "url": "https://www.ozon.ru/category/svadebnye-tovary-1736/"
    },
    {
      "root": "Unknown",
      "name": "Украшения на машину",
      "url": "https://www.ozon.ru/category/aksessuary-na-limuzin-30627/"
    },
    {
      "root": "Unknown",
      "name": "Открытки",
      "url": "https://www.ozon.ru/category/otkrytki-14875/"
    },
    {
      "root": "Unknown",
      "name": "Свечи для торта",
      "url": "https://www.ozon.ru/category/svechi-dlya-torta-14844/"
    },
    {
      "root": "Unknown",
      "name": "Топперы для торта",
      "url": "https://www.ozon.ru/category/toppery-dlya-torta-31858/"
    },
    {
      "root": "Unknown",
      "name": "Фотобутафория",
      "url": "https://www.ozon.ru/category/fotobutaforiya-14818/"
    },
    {
      "root": "Unknown",
      "name": "Награды и кубки",
      "url": "https://www.ozon.ru/category/priglasheniya-na-prazdniki-19057/"
    },
    {
      "root": "Unknown",
      "name": "Китайские фонарики",
      "url": "https://www.ozon.ru/category/kitayskie-fonariki-14828/"
    },
    {
      "root": "Unknown",
      "name": "Карнавальные товары",
      "url": "https://www.ozon.ru/category/karnavalnye-tovary-31239/"
    },
    {
      "root": "Unknown",
      "name": "Краски Холи",
      "url": "https://www.ozon.ru/category/kraski-holi-32928/"
    },
    {
      "root": "Unknown",
      "name": "Фейерверки и салюты",
      "url": "https://www.ozon.ru/category/feyerverki-i-salyuty-14823/"
    },
    {
      "root": "Unknown",
      "name": "Религиозные предметы",
      "url": "https://www.ozon.ru/category/ritualnye-tovary-32805/"
    },
    {
      "root": "Unknown",
      "name": "Иконы и панно",
      "url": "https://www.ozon.ru/category/ikony-1725/"
    },
    {
      "root": "Unknown",
      "name": "Церковная утварь",
      "url": "https://www.ozon.ru/category/ritualnye-prinadlezhnosti-37285/"
    },
    {
      "root": "Unknown",
      "name": "Свечи церковные",
      "url": "https://www.ozon.ru/category/svechi-ritualnye-37286/"
    },
    {
      "root": "Unknown",
      "name": "Одежда и аксессуары для крещения",
      "url": "https://www.ozon.ru/category/odezhda-dlya-kreshcheniya-38027/"
    },
    {
      "root": "Unknown",
      "name": "Товары к Пасхе",
      "url": "https://www.ozon.ru/category/tovary-k-pashe-15161/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары религиозные",
      "url": "https://www.ozon.ru/category/aksessuary-religioznye-37946/"
    },
    {
      "root": "Unknown",
      "name": "Коврики для намаза",
      "url": "https://www.ozon.ru/category/kovriki-dlya-namaza-32659/"
    },
    {
      "root": "Unknown",
      "name": "Ритуальные товары",
      "url": "https://www.ozon.ru/category/ritualnye-tovary-39215/"
    },
    {
      "root": "Unknown",
      "name": "Оформление могилы",
      "url": "https://www.ozon.ru/category/korziny-ritualnye-34546/"
    },
    {
      "root": "Unknown",
      "name": "Памятники и ограды на могилу",
      "url": "https://www.ozon.ru/category/pamyatniki-na-mogilu-34557/"
    },
    {
      "root": "Unknown",
      "name": "Цветы для кладбища",
      "url": "https://www.ozon.ru/category/bukety-traurnye-37282/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 118,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Товары для школы и обучения",
      "url": "https://www.ozon.ru/category/tovary-dlya-shkoly-7182/"
    },
    {
      "root": "Unknown",
      "name": "Рюкзаки, ранцы, сумки",
      "url": "https://www.ozon.ru/category/ryukzaki-rantsy-sumki-dlya-shkoly-7201/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские принадлежности",
      "url": "https://www.ozon.ru/category/kantselyarskie-prinadlezhnosti-7184/"
    },
    {
      "root": "Unknown",
      "name": "Письменные принадлежности",
      "url": "https://www.ozon.ru/category/pismennye-prinadlezhnosti-7192/"
    },
    {
      "root": "Unknown",
      "name": "Чертежные принадлежности",
      "url": "https://www.ozon.ru/category/chertezhnye-prinadlezhnosti-dlya-shkoly-39784/"
    },
    {
      "root": "Unknown",
      "name": "Глобусы и астропланетарии",
      "url": "https://www.ozon.ru/category/globusy-7183/"
    },
    {
      "root": "Unknown",
      "name": "Обучающие материалы и пособия",
      "url": "https://www.ozon.ru/category/obuchayushchie-plakaty-7106/"
    },
    {
      "root": "Unknown",
      "name": "Счетный материал",
      "url": "https://www.ozon.ru/category/igrushki-dlya-scheta-7263/"
    },
    {
      "root": "Unknown",
      "name": "Творчество в школе",
      "url": "https://www.ozon.ru/category/tvorchestvo-v-shkole-31470/"
    },
    {
      "root": "Unknown",
      "name": "Тетради, блокноты и дневники",
      "url": "https://www.ozon.ru/category/tetradi-bloknoty-dnevniki-7205/"
    },
    {
      "root": "Unknown",
      "name": "Электронные карты и браслеты",
      "url": "https://www.ozon.ru/category/elektronnye-karty-i-braslety-shkolnika-31967/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки и игры",
      "url": "https://www.ozon.ru/category/igrushki-i-igry-7108/"
    },
    {
      "root": "Unknown",
      "name": "Мягкие игрушки",
      "url": "https://www.ozon.ru/category/myagkie-igrushki-7175/"
    },
    {
      "root": "Unknown",
      "name": "Игрушечное оружие",
      "url": "https://www.ozon.ru/category/igrushechnoe-oruzhie-i-blastery-7141/"
    },
    {
      "root": "Unknown",
      "name": "Конструкторы",
      "url": "https://www.ozon.ru/category/konstruktory-7174/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки для малышей",
      "url": "https://www.ozon.ru/category/igrushki-dlya-malyshey-7119/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки для ванной",
      "url": "https://www.ozon.ru/category/igrushki-dlya-vannoy-7121/"
    },
    {
      "root": "Unknown",
      "name": "Куклы и аксессуары",
      "url": "https://www.ozon.ru/category/kukly-i-aksessuary-31272/"
    },
    {
      "root": "Unknown",
      "name": "Фигурки и аксессуары",
      "url": "https://www.ozon.ru/category/figurki-i-aksessuary-7169/"
    },
    {
      "root": "Unknown",
      "name": "Сюжетно-ролевые игрушки",
      "url": "https://www.ozon.ru/category/syuzhetno-rolevye-igrushki-7112/"
    },
    {
      "root": "Unknown",
      "name": "Игрушечный транспорт",
      "url": "https://www.ozon.ru/category/igrushechnye-mashinki-i-tehnika-7142/"
    },
    {
      "root": "Unknown",
      "name": "Радиоуправляемые игрушки",
      "url": "https://www.ozon.ru/category/radioupravlyaemye-igrushki-7149/"
    },
    {
      "root": "Unknown",
      "name": "Интерактивные и электронные игрушки",
      "url": "https://www.ozon.ru/category/interaktivnye-igrushki-30148/"
    },
    {
      "root": "Unknown",
      "name": "Роботы и трансформеры",
      "url": "https://www.ozon.ru/category/roboty-i-transformery-7167/"
    },
    {
      "root": "Unknown",
      "name": "Развивающие игры",
      "url": "https://www.ozon.ru/category/razvivayushchie-i-obuchayushchie-igrushki-7176/"
    },
    {
      "root": "Unknown",
      "name": "Настольные игры",
      "url": "https://www.ozon.ru/category/nastolnye-igry-dlya-detey-7172/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки-антистресс",
      "url": "https://www.ozon.ru/category/igrushki-antistress-7181/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные наборы",
      "url": "https://www.ozon.ru/category/podarochnye-nabory-igrushek-35388/"
    },
    {
      "root": "Unknown",
      "name": "Авторские игрушки",
      "url": "https://www.ozon.ru/category/avtorskie-igrushki-35343/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и игры на улице",
      "url": "https://www.ozon.ru/category/sport-i-igry-na-ulitse-30726/"
    },
    {
      "root": "Unknown",
      "name": "Детский транспорт",
      "url": "https://www.ozon.ru/category/detskiy-transport-1746/"
    },
    {
      "root": "Unknown",
      "name": "Игры на улице",
      "url": "https://www.ozon.ru/category/igry-na-ulitse-7218/"
    },
    {
      "root": "Unknown",
      "name": "Игровые и спортивные комплексы",
      "url": "https://www.ozon.ru/category/igrovye-kompleksy-dlya-ulitsy-34267/"
    },
    {
      "root": "Unknown",
      "name": "Плавание и игры на воде",
      "url": "https://www.ozon.ru/category/plavanie-i-igry-na-vode-31052/"
    },
    {
      "root": "Unknown",
      "name": "Спортивная защита",
      "url": "https://www.ozon.ru/category/sportivnaya-zashchita-dlya-detey-31019/"
    },
    {
      "root": "Unknown",
      "name": "Зимние товары",
      "url": "https://www.ozon.ru/category/zimnie-tovary-30983/"
    },
    {
      "root": "Unknown",
      "name": "Подгузники и гигиена",
      "url": "https://www.ozon.ru/category/podguzniki-i-gigiena-7058/"
    },
    {
      "root": "Unknown",
      "name": "Подгузники и трусики",
      "url": "https://www.ozon.ru/category/podguzniki-i-trusiki-30749/"
    },
    {
      "root": "Unknown",
      "name": "Пеленки и клеенки",
      "url": "https://www.ozon.ru/category/pelenki-detskie-7063/"
    },
    {
      "root": "Unknown",
      "name": "Горшки и сиденья детские",
      "url": "https://www.ozon.ru/category/gorshki-i-sidenya-7060/"
    },
    {
      "root": "Unknown",
      "name": "Детская косметика",
      "url": "https://www.ozon.ru/category/detskaya-kosmetika-30748/"
    },
    {
      "root": "Unknown",
      "name": "Здоровье и уход за ребенком",
      "url": "https://www.ozon.ru/category/zdorove-i-uhod-za-rebenkom-7012/"
    },
    {
      "root": "Unknown",
      "name": "Купание ребенка",
      "url": "https://www.ozon.ru/category/kupanie-rebenka-7002/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия",
      "url": "https://www.ozon.ru/category/detskaya-bytovaya-himiya-30750/"
    },
    {
      "root": "Unknown",
      "name": "Детская комната",
      "url": "https://www.ozon.ru/category/detskaya-komnata-7041/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/detskaya-mebel-30883/"
    },
    {
      "root": "Unknown",
      "name": "Все для сна",
      "url": "https://www.ozon.ru/category/vse-dlya-sna-30882/"
    },
    {
      "root": "Unknown",
      "name": "Активность и игры в комнате",
      "url": "https://www.ozon.ru/category/aktivnost-i-igry-v-komnate-30884/"
    },
    {
      "root": "Unknown",
      "name": "Безопасность ребенка",
      "url": "https://www.ozon.ru/category/bezopasnost-rebenka-7055/"
    },
    {
      "root": "Unknown",
      "name": "Декор",
      "url": "https://www.ozon.ru/category/dekor-dlya-detskoy-komnaty-30885/"
    },
    {
      "root": "Unknown",
      "name": "Коляски и автокресла",
      "url": "https://www.ozon.ru/category/kolyaski-i-avtokresla-30482/"
    },
    {
      "root": "Unknown",
      "name": "Коляски",
      "url": "https://www.ozon.ru/category/detskie-kolyaski-7071/"
    },
    {
      "root": "Unknown",
      "name": "Автокресла",
      "url": "https://www.ozon.ru/category/detskie-avtokresla-7066/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для колясок",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-kolyasok-7067/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для автокресел",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-detskih-avtokresel-7070/"
    },
    {
      "root": "Unknown",
      "name": "Детское питание",
      "url": "https://www.ozon.ru/category/detskoe-pitanie-7030/"
    },
    {
      "root": "Unknown",
      "name": "Молочные смеси",
      "url": "https://www.ozon.ru/category/smesi-i-zameniteli-grudnogo-moloka-7034/"
    },
    {
      "root": "Unknown",
      "name": "Пюре",
      "url": "https://www.ozon.ru/category/pyure-1653/"
    },
    {
      "root": "Unknown",
      "name": "Каши",
      "url": "https://www.ozon.ru/category/kashi-7031/"
    },
    {
      "root": "Unknown",
      "name": "Десерты",
      "url": "https://www.ozon.ru/category/deserty-detskie-34589/"
    },
    {
      "root": "Unknown",
      "name": "Молочные продукты",
      "url": "https://www.ozon.ru/category/molochnye-produkty-dlya-detey-7032/"
    },
    {
      "root": "Unknown",
      "name": "Вода и напитки",
      "url": "https://www.ozon.ru/category/voda-detskaya-7038/"
    },
    {
      "root": "Unknown",
      "name": "Готовые блюда",
      "url": "https://www.ozon.ru/category/gotovye-blyuda-detskie-7039/"
    },
    {
      "root": "Unknown",
      "name": "Товары для кормления",
      "url": "https://www.ozon.ru/category/tovary-dlya-kormleniya-7019/"
    },
    {
      "root": "Unknown",
      "name": "Пустышки и аксессуары",
      "url": "https://www.ozon.ru/category/pustyshki-i-aksessuary-7025/"
    },
    {
      "root": "Unknown",
      "name": "Бутылочки",
      "url": "https://www.ozon.ru/category/butylochki-7020/"
    },
    {
      "root": "Unknown",
      "name": "Соски для бутылочек",
      "url": "https://www.ozon.ru/category/soski-dlya-butylochek-7026/"
    },
    {
      "root": "Unknown",
      "name": "Подогреватели бутылочек",
      "url": "https://www.ozon.ru/category/podogrevateli-butylochek-7022/"
    },
    {
      "root": "Unknown",
      "name": "Стерилизаторы",
      "url": "https://www.ozon.ru/category/sterilizatory-7027/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для бутылочек",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-butylochek-i-niblerov-7226/"
    },
    {
      "root": "Unknown",
      "name": "Поильники",
      "url": "https://www.ozon.ru/category/poilniki-7023/"
    },
    {
      "root": "Unknown",
      "name": "Ниблеры",
      "url": "https://www.ozon.ru/category/niblery-i-prorezyvateli-30781/"
    },
    {
      "root": "Unknown",
      "name": "Товары для грудного вскармливания",
      "url": "https://www.ozon.ru/category/tovary-dlya-grudnogo-vskarmlivaniya-30782/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для кормления",
      "url": "https://www.ozon.ru/category/posuda-dlya-kormleniya-7024/"
    },
    {
      "root": "Unknown",
      "name": "Блендеры-пароварки",
      "url": "https://www.ozon.ru/category/blendery-parovarki-31243/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для детей от 3х лет",
      "url": "https://www.ozon.ru/category/detskaya-posuda-1649/"
    },
    {
      "root": "Unknown",
      "name": "Столовые приборы для кормления",
      "url": "https://www.ozon.ru/category/stolovye-pribory-dlya-kormleniya-1698/"
    },
    {
      "root": "Unknown",
      "name": "Нагрудники и слюнявчики",
      "url": "https://www.ozon.ru/category/nagrudniki-i-slyunyavchiki-7021/"
    },
    {
      "root": "Unknown",
      "name": "Стульчики для кормления",
      "url": "https://www.ozon.ru/category/stulchiki-dlya-kormleniya-30997/"
    },
    {
      "root": "Unknown",
      "name": "Товары для мам",
      "url": "https://www.ozon.ru/category/tovary-dlya-mam-7077/"
    },
    {
      "root": "Unknown",
      "name": "Переноски для детей",
      "url": "https://www.ozon.ru/category/perenoski-dlya-detey-7065/"
    },
    {
      "root": "Unknown",
      "name": "Рюкзаки и сумки",
      "url": "https://www.ozon.ru/category/ryukzaki-dlya-mam-32020/"
    },
    {
      "root": "Unknown",
      "name": "Наборы в роддом",
      "url": "https://www.ozon.ru/category/nabory-v-roddom-32706/"
    },
    {
      "root": "Unknown",
      "name": "Подушки для беременных",
      "url": "https://www.ozon.ru/category/podushki-dlya-beremennyh-i-kormyashchih-7085/"
    },
    {
      "root": "Unknown",
      "name": "Бандажи",
      "url": "https://www.ozon.ru/category/bandazhi-dlya-beremennyh-7078/"
    },
    {
      "root": "Unknown",
      "name": "Косметика и уход",
      "url": "https://www.ozon.ru/category/kosmetika-i-uhod-dlya-mam-30700/"
    },
    {
      "root": "Unknown",
      "name": "Питание для мам",
      "url": "https://www.ozon.ru/category/pitanie-dlya-mam-7084/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 137,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Уход за волосами",
      "url": "https://www.ozon.ru/category/uhod-za-volosami-6584/"
    },
    {
      "root": "Unknown",
      "name": "Шампуни и кондиционеры",
      "url": "https://www.ozon.ru/category/shampuni-i-konditsionery-35438/"
    },
    {
      "root": "Unknown",
      "name": "Масла и сыворотки",
      "url": "https://www.ozon.ru/category/maski-i-syvorotki-6587/"
    },
    {
      "root": "Unknown",
      "name": "Средства для укладки",
      "url": "https://www.ozon.ru/category/sredstva-dlya-ukladki-volos-6601/"
    },
    {
      "root": "Unknown",
      "name": "Расчески и щетки",
      "url": "https://www.ozon.ru/category/rascheski-i-shchetki-6629/"
    },
    {
      "root": "Unknown",
      "name": "Окрашивание и химическая завивка",
      "url": "https://www.ozon.ru/category/okrashivanie-i-himicheskaya-zavivka-6616/"
    },
    {
      "root": "Unknown",
      "name": "Косметические наборы",
      "url": "https://www.ozon.ru/category/kosmeticheskie-nabory-dlya-volos-6682/"
    },
    {
      "root": "Unknown",
      "name": "Наращивание волос",
      "url": "https://www.ozon.ru/category/snyatie-narashchennyh-volos-32123/"
    },
    {
      "root": "Unknown",
      "name": "Шапочки для душа",
      "url": "https://www.ozon.ru/category/flakony-dorozhnye-6691/"
    },
    {
      "root": "Unknown",
      "name": "Бигуди",
      "url": "https://www.ozon.ru/category/bigudi-6635/"
    },
    {
      "root": "Unknown",
      "name": "Парики и шиньоны",
      "url": "https://www.ozon.ru/category/pariki-i-shinony-6636/"
    },
    {
      "root": "Unknown",
      "name": "Профессиональные инструменты парикмахера",
      "url": "https://www.ozon.ru/category/professionalnye-instrumenty-parikmahera-30674/"
    },
    {
      "root": "Unknown",
      "name": "Уход за лицом",
      "url": "https://www.ozon.ru/category/uhod-za-litsom-6559/"
    },
    {
      "root": "Unknown",
      "name": "Очищение и умывание",
      "url": "https://www.ozon.ru/category/ochishchenie-6560/"
    },
    {
      "root": "Unknown",
      "name": "Скрабы и пилинги",
      "url": "https://www.ozon.ru/category/skraby-dlya-litsa-6583/"
    },
    {
      "root": "Unknown",
      "name": "Увлажнение и питание",
      "url": "https://www.ozon.ru/category/uvlazhnenie-i-pitanie-6561/"
    },
    {
      "root": "Unknown",
      "name": "Маски",
      "url": "https://www.ozon.ru/category/maski-dlya-litsa-30937/"
    },
    {
      "root": "Unknown",
      "name": "Патчи",
      "url": "https://www.ozon.ru/category/patchi-kosmeticheskie-6577/"
    },
    {
      "root": "Unknown",
      "name": "Средства для проблемной кожи",
      "url": "https://www.ozon.ru/category/sredstva-dlya-problemnoy-kozhi-6581/"
    },
    {
      "root": "Unknown",
      "name": "Антивозрастной уход",
      "url": "https://www.ozon.ru/category/antivozrastnoy-uhod-38000/"
    },
    {
      "root": "Unknown",
      "name": "Наборы средств для лица",
      "url": "https://www.ozon.ru/category/nabory-sredstv-dlya-litsa-30521/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты косметологические",
      "url": "https://www.ozon.ru/category/instrumenty-kosmetologicheskie-31614/"
    },
    {
      "root": "Unknown",
      "name": "Уход за телом",
      "url": "https://www.ozon.ru/category/uhod-za-telom-6637/"
    },
    {
      "root": "Unknown",
      "name": "Кремы",
      "url": "https://www.ozon.ru/category/kremy-dlya-tela-6648/"
    },
    {
      "root": "Unknown",
      "name": "Увлажнение и питание",
      "url": "https://www.ozon.ru/category/uvlazhnenie-i-pitanie-dlya-tela-31294/"
    },
    {
      "root": "Unknown",
      "name": "Средства для душа",
      "url": "https://www.ozon.ru/category/geli-dlya-dusha-6638/"
    },
    {
      "root": "Unknown",
      "name": "Мыло",
      "url": "https://www.ozon.ru/category/mylo-6639/"
    },
    {
      "root": "Unknown",
      "name": "Мочалки",
      "url": "https://www.ozon.ru/category/mochalki-6661/"
    },
    {
      "root": "Unknown",
      "name": "Скрабы и пилинги",
      "url": "https://www.ozon.ru/category/skraby-i-pilingi-6574/"
    },
    {
      "root": "Unknown",
      "name": "Средства для принятия ванны",
      "url": "https://www.ozon.ru/category/sredstva-dlya-prinyatiya-vanny-37954/"
    },
    {
      "root": "Unknown",
      "name": "Дезодоранты",
      "url": "https://www.ozon.ru/category/dezodoranty-6647/"
    },
    {
      "root": "Unknown",
      "name": "Средства против целлюлита и растяжек",
      "url": "https://www.ozon.ru/category/antitsellyulitnye-sredstva-31976/"
    },
    {
      "root": "Unknown",
      "name": "Щетки для сухого массажа",
      "url": "https://www.ozon.ru/category/shchetki-dlya-suhogo-massazha-30638/"
    },
    {
      "root": "Unknown",
      "name": "Депиляция и эпиляция",
      "url": "https://www.ozon.ru/category/depilyatsiya-i-epilyatsiya-6640/"
    },
    {
      "root": "Unknown",
      "name": "Наборы косметики",
      "url": "https://www.ozon.ru/category/nabory-kosmetiki-dlya-uhoda-za-kozhey-6582/"
    },
    {
      "root": "Unknown",
      "name": "Стики для тела",
      "url": "https://www.ozon.ru/category/stiki-dlya-tela-6704/"
    },
    {
      "root": "Unknown",
      "name": "Макияж",
      "url": "https://www.ozon.ru/category/makiyazh-6501/"
    },
    {
      "root": "Unknown",
      "name": "Лицо",
      "url": "https://www.ozon.ru/category/litso-6502/"
    },
    {
      "root": "Unknown",
      "name": "Глаза",
      "url": "https://www.ozon.ru/category/kosmetika-dlya-glaz-6516/"
    },
    {
      "root": "Unknown",
      "name": "Губы",
      "url": "https://www.ozon.ru/category/guby-6512/"
    },
    {
      "root": "Unknown",
      "name": "Брови",
      "url": "https://www.ozon.ru/category/brovi-6521/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для макияжа",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-makiyazha-6551/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для макияжа",
      "url": "https://www.ozon.ru/category/nabory-dlya-makiyazha-6550/"
    },
    {
      "root": "Unknown",
      "name": "Атомайзеры и флаконы",
      "url": "https://www.ozon.ru/category/atomayzery-6700/"
    },
    {
      "root": "Unknown",
      "name": "Перманентный макияж",
      "url": "https://www.ozon.ru/category/permanentnyy-makiyazh-34911/"
    },
    {
      "root": "Unknown",
      "name": "Временные татуировки и стразы",
      "url": "https://www.ozon.ru/category/perevodnye-tatu-6723/"
    },
    {
      "root": "Unknown",
      "name": "Маникюр и педикюр",
      "url": "https://www.ozon.ru/category/nogti-6526/"
    },
    {
      "root": "Unknown",
      "name": "Лаки и гели для ногтей",
      "url": "https://www.ozon.ru/category/gel-laki-i-gelevye-sistemy-38765/"
    },
    {
      "root": "Unknown",
      "name": "Дизайн ногтей",
      "url": "https://www.ozon.ru/category/dizayn-nogtey-6530/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты и аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-manikyura-i-pedikyura-6534/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для маникюра и педикюра",
      "url": "https://www.ozon.ru/category/apparaty-dlya-manikyura-i-pedikyura-6337/"
    },
    {
      "root": "Unknown",
      "name": "Типсы и формы для наращивания",
      "url": "https://www.ozon.ru/category/nakladnye-nogti-tipsy-6546/"
    },
    {
      "root": "Unknown",
      "name": "Уход за кожей и ногтями",
      "url": "https://www.ozon.ru/category/uhod-za-nogtyami-35492/"
    },
    {
      "root": "Unknown",
      "name": "Антисептические средства",
      "url": "https://www.ozon.ru/category/antibakterialnye-sredstva-33252/"
    },
    {
      "root": "Unknown",
      "name": "Ванночки и парафинотерапия",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-manikyura-i-pedikyura-35464/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмерия",
      "url": "https://www.ozon.ru/category/parfyumeriya-6662/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмерная вода",
      "url": "https://www.ozon.ru/category/parfyumernaya-voda-6663/"
    },
    {
      "root": "Unknown",
      "name": "Туалетная вода",
      "url": "https://www.ozon.ru/category/tualetnaya-voda-6664/"
    },
    {
      "root": "Unknown",
      "name": "Духи",
      "url": "https://www.ozon.ru/category/duhi-6666/"
    },
    {
      "root": "Unknown",
      "name": "Духи сухие и масляные",
      "url": "https://www.ozon.ru/category/duhi-suhie-i-maslyanye-33245/"
    },
    {
      "root": "Unknown",
      "name": "Нишевая парфюмерия",
      "url": "https://www.ozon.ru/category/nishevaya-parfyumeriya-1587/"
    },
    {
      "root": "Unknown",
      "name": "Дымки и вуали",
      "url": "https://www.ozon.ru/category/dymki-i-vuali-dlya-volos-38055/"
    },
    {
      "root": "Unknown",
      "name": "Наливная парфюмерия",
      "url": "https://www.ozon.ru/category/nalivnaya-parfyumeriya-33037/"
    },
    {
      "root": "Unknown",
      "name": "Одеколоны",
      "url": "https://www.ozon.ru/category/odekolony-6665/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмированный набор",
      "url": "https://www.ozon.ru/category/parfyumirovannyy-nabor-6668/"
    },
    {
      "root": "Unknown",
      "name": "Загар и защита от солнца",
      "url": "https://www.ozon.ru/category/zagar-i-zashchita-ot-solntsa-6651/"
    },
    {
      "root": "Unknown",
      "name": "Солнцезащитные средства",
      "url": "https://www.ozon.ru/category/solntsezashchitnye-sredstva-6656/"
    },
    {
      "root": "Unknown",
      "name": "Косметика для ухода с SPF",
      "url": "https://www.ozon.ru/category/solntsezashchitnye-sredstva-dlya-litsa-38024/"
    },
    {
      "root": "Unknown",
      "name": "Средства для загара",
      "url": "https://www.ozon.ru/category/sredstva-dlya-zagara-36201/"
    },
    {
      "root": "Unknown",
      "name": "Средства после загара",
      "url": "https://www.ozon.ru/category/sredstva-posle-zagara-6655/"
    },
    {
      "root": "Unknown",
      "name": "Средства для солярия",
      "url": "https://www.ozon.ru/category/sredstva-dlya-solyariya-6653/"
    },
    {
      "root": "Unknown",
      "name": "Автозагар",
      "url": "https://www.ozon.ru/category/avtozagar-6652/"
    },
    {
      "root": "Unknown",
      "name": "Мужская косметика",
      "url": "https://www.ozon.ru/category/muzhskaya-kosmetika-35504/"
    },
    {
      "root": "Unknown",
      "name": "Бритье и уход за бородой",
      "url": "https://www.ozon.ru/category/britvy-i-sredstva-dlya-britya-6685/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмерия",
      "url": "https://www.ozon.ru/category/muzhskaya-parfyumeriya-35513/"
    },
    {
      "root": "Unknown",
      "name": "Для волос",
      "url": "https://www.ozon.ru/category/muzhskaya-kosmetika-dlya-volos-35506/"
    },
    {
      "root": "Unknown",
      "name": "Гели для душа",
      "url": "https://www.ozon.ru/category/geli-dlya-dusha-muzhskie-39216/"
    },
    {
      "root": "Unknown",
      "name": "Дезодоранты",
      "url": "https://www.ozon.ru/category/dezodoranty-muzhskie-35505/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для гигиены",
      "url": "https://www.ozon.ru/category/nabory-dlya-gigieny-muzhskie-39217/"
    },
    {
      "root": "Unknown",
      "name": "Детская косметика и парфюмерия",
      "url": "https://www.ozon.ru/category/detskaya-kosmetika-35584/"
    },
    {
      "root": "Unknown",
      "name": "Декоративная косметика",
      "url": "https://www.ozon.ru/category/makiyazh-detskiy-35587/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмерия",
      "url": "https://www.ozon.ru/category/detskiy-parfyum-35590/"
    },
    {
      "root": "Unknown",
      "name": "Средства для купания",
      "url": "https://www.ozon.ru/category/sredstva-dlya-kupaniya-39495/"
    },
    {
      "root": "Unknown",
      "name": "Средства для укладки волос",
      "url": "https://www.ozon.ru/category/detskie-sredstva-dlya-ukladki-volos-33257/"
    },
    {
      "root": "Unknown",
      "name": "Маникюр",
      "url": "https://www.ozon.ru/category/detskiy-manikyur-35585/"
    },
    {
      "root": "Unknown",
      "name": "Беременным и кормящим",
      "url": "https://www.ozon.ru/category/kosmetika-dlya-beremennyh-i-kormyashchih-33251/"
    },
    {
      "root": "Unknown",
      "name": "Аппаратная косметология и массаж",
      "url": "https://www.ozon.ru/category/apparatnaya-kosmetologiya-6325/"
    },
    {
      "root": "Unknown",
      "name": "Массажеры",
      "url": "https://www.ozon.ru/category/massazhery-34220/"
    },
    {
      "root": "Unknown",
      "name": "Косметологические аппараты",
      "url": "https://www.ozon.ru/category/kosmetologicheskie-apparaty-6326/"
    },
    {
      "root": "Unknown",
      "name": "Эпиляторы",
      "url": "https://www.ozon.ru/category/epilyatory-32708/"
    },
    {
      "root": "Unknown",
      "name": "Контактные гели",
      "url": "https://www.ozon.ru/category/kontaktnye-geli-33153/"
    },
    {
      "root": "Unknown",
      "name": "Ароматерапия",
      "url": "https://www.ozon.ru/category/aromaterapiya-6671/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование и материалы для тату-салона",
      "url": "https://www.ozon.ru/category/oborudovanie-i-materialy-dlya-tatu-31987/"
    },
    {
      "root": "Unknown",
      "name": "Тату-машинки и аксессуары",
      "url": "https://www.ozon.ru/category/tatu-mashinki-i-aksessuary-31989/"
    },
    {
      "root": "Unknown",
      "name": "Краски и расходники",
      "url": "https://www.ozon.ru/category/kraski-dlya-tatuirovok-31991/"
    },
    {
      "root": "Unknown",
      "name": "Уход за татуировками",
      "url": "https://www.ozon.ru/category/uhod-za-tatuirovkami-31990/"
    },
    {
      "root": "Unknown",
      "name": "Тату-наборы",
      "url": "https://www.ozon.ru/category/tatu-nabory-31994/"
    },
    {
      "root": "Unknown",
      "name": "Удаления татуировок",
      "url": "https://www.ozon.ru/category/tovary-dlya-udaleniya-tatuirovok-34774/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты для пирсинга",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-pirsinga-31992/"
    },
    {
      "root": "Unknown",
      "name": "Мебель и оборудование для салонов красоты",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-salonov-krasoty-34940/"
    },
    {
      "root": "Unknown",
      "name": "Массажное оборудование",
      "url": "https://www.ozon.ru/category/massazhnoe-oborudovanie-34221/"
    },
    {
      "root": "Unknown",
      "name": "Для кабинетов маникюра и педикюра",
      "url": "https://www.ozon.ru/category/mebel-i-oborudovanie-dlya-kabinetov-manikyura-i-pedikyura-39014/"
    },
    {
      "root": "Unknown",
      "name": "Для парикмахеров",
      "url": "https://www.ozon.ru/category/mebel-i-oborudovanie-dlya-parikmaherov-39544/"
    },
    {
      "root": "Unknown",
      "name": "Для косметологов",
      "url": "https://www.ozon.ru/category/mebel-i-oborudovanie-dlya-kosmetologov-39015/"
    },
    {
      "root": "Unknown",
      "name": "Для визажистов",
      "url": "https://www.ozon.ru/category/mebel-i-oborudovanie-dlya-vizazhistov-39017/"
    },
    {
      "root": "Unknown",
      "name": "Стулья мастеров для салонов красоты",
      "url": "https://www.ozon.ru/category/stulya-masterov-dlya-salonov-krasoty-39018/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 102,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Крупная бытовая техника",
      "url": "https://www.ozon.ru/category/krupnaya-bytovaya-tehnika-10501/"
    },
    {
      "root": "Unknown",
      "name": "Холодильники",
      "url": "https://www.ozon.ru/category/holodilniki-10502/"
    },
    {
      "root": "Unknown",
      "name": "Морозильные камеры",
      "url": "https://www.ozon.ru/category/morozilnye-kamery-10504/"
    },
    {
      "root": "Unknown",
      "name": "Стиральные машины",
      "url": "https://www.ozon.ru/category/stiralnye-mashiny-10507/"
    },
    {
      "root": "Unknown",
      "name": "Стиральные машины с сушкой",
      "url": "https://www.ozon.ru/category/stiralnye-mashiny-s-sushkoy-39815/"
    },
    {
      "root": "Unknown",
      "name": "Сушильные машины для белья",
      "url": "https://www.ozon.ru/category/sushilnye-mashiny-10508/"
    },
    {
      "root": "Unknown",
      "name": "Варочные панели",
      "url": "https://www.ozon.ru/category/varochnye-paneli-10511/"
    },
    {
      "root": "Unknown",
      "name": "Плиты",
      "url": "https://www.ozon.ru/category/plity-10509/"
    },
    {
      "root": "Unknown",
      "name": "Духовые шкафы",
      "url": "https://www.ozon.ru/category/duhovye-shkafy-10510/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные вытяжки и аксессуары",
      "url": "https://www.ozon.ru/category/kuhonnye-vytyazhki-10512/"
    },
    {
      "root": "Unknown",
      "name": "Посудомоечные машины",
      "url": "https://www.ozon.ru/category/posudomoechnye-mashiny-10515/"
    },
    {
      "root": "Unknown",
      "name": "Кулеры для воды",
      "url": "https://www.ozon.ru/category/kulery-dlya-vody-i-aksessuary-10516/"
    },
    {
      "root": "Unknown",
      "name": "Винные и сигарные шкафы",
      "url": "https://www.ozon.ru/category/vinnye-shkafy-10506/"
    },
    {
      "root": "Unknown",
      "name": "Подогреватели посуды",
      "url": "https://www.ozon.ru/category/vstraivaemye-podogrevateli-posudy-37173/"
    },
    {
      "root": "Unknown",
      "name": "Измельчители отходов",
      "url": "https://www.ozon.ru/category/vstraivaemye-izmelchiteli-bytovyh-othodov-32683/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты встраиваемой техники",
      "url": "https://www.ozon.ru/category/duhovoy-shkaf-varochnaya-panel-35364/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-krupnoy-bytovoy-tehniki-10794/"
    },
    {
      "root": "Unknown",
      "name": "Техника для кухни",
      "url": "https://www.ozon.ru/category/tehnika-dlya-kuhni-10523/"
    },
    {
      "root": "Unknown",
      "name": "Кофеварки и кофемашины",
      "url": "https://www.ozon.ru/category/kofevarki-i-kofemashiny-10530/"
    },
    {
      "root": "Unknown",
      "name": "Электрические чайники и термопоты",
      "url": "https://www.ozon.ru/category/elektricheskie-chayniki-i-termopoty-10524/"
    },
    {
      "root": "Unknown",
      "name": "Блендеры, измельчители и миксеры",
      "url": "https://www.ozon.ru/category/miksery-blendery-i-izmelchiteli-10580/"
    },
    {
      "root": "Unknown",
      "name": "Печи и грили",
      "url": "https://www.ozon.ru/category/pechi-i-grili-10545/"
    },
    {
      "root": "Unknown",
      "name": "Настольные плиты",
      "url": "https://www.ozon.ru/category/nastolnye-plity-1610/"
    },
    {
      "root": "Unknown",
      "name": "Соковыжималки",
      "url": "https://www.ozon.ru/category/sokovyzhimalki-10592/"
    },
    {
      "root": "Unknown",
      "name": "Мультиварки и техника для варки",
      "url": "https://www.ozon.ru/category/multivarki-i-tehnika-dlya-varki-10562/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные комбайны и машины",
      "url": "https://www.ozon.ru/category/kuhonnye-mashiny-i-kombayny-33128/"
    },
    {
      "root": "Unknown",
      "name": "Мясорубки и насадки",
      "url": "https://www.ozon.ru/category/myasorubki-i-kuhonnye-kombayny-10593/"
    },
    {
      "root": "Unknown",
      "name": "Техника для приготовления десертов",
      "url": "https://www.ozon.ru/category/tehnika-dlya-prigotovleniya-desertov-10600/"
    },
    {
      "root": "Unknown",
      "name": "Техника для приготовления блюд",
      "url": "https://www.ozon.ru/category/tehnika-dlya-prigotovleniya-blyud-10612/"
    },
    {
      "root": "Unknown",
      "name": "Прочая кухонная техника",
      "url": "https://www.ozon.ru/category/prochaya-kuhonnaya-tehnika-10620/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-kuhonnoy-tehniki-10640/"
    },
    {
      "root": "Unknown",
      "name": "Техника для дома",
      "url": "https://www.ozon.ru/category/tehnika-dlya-doma-10647/"
    },
    {
      "root": "Unknown",
      "name": "Пылесосы",
      "url": "https://www.ozon.ru/category/pylesosy-i-aksessuary-10648/"
    },
    {
      "root": "Unknown",
      "name": "Утюги и отпариватели",
      "url": "https://www.ozon.ru/category/utyugi-i-otparivateli-10679/"
    },
    {
      "root": "Unknown",
      "name": "Аппараты для мойки окон и полов",
      "url": "https://www.ozon.ru/category/stekloochistiteli-10678/"
    },
    {
      "root": "Unknown",
      "name": "Пароочистители и паровые швабры",
      "url": "https://www.ozon.ru/category/paroochistiteli-10685/"
    },
    {
      "root": "Unknown",
      "name": "Швейные и вышивальные машины",
      "url": "https://www.ozon.ru/category/shveynye-mashiny-i-aksessuary-10687/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти",
      "url": "https://www.ozon.ru/category/aksessuary-i-zapchasti-k-tehnike-dlya-doma-39598/"
    },
    {
      "root": "Unknown",
      "name": "Климатическая техника",
      "url": "https://www.ozon.ru/category/klimaticheskaya-tehnika-10711/"
    },
    {
      "root": "Unknown",
      "name": "Водонагреватели",
      "url": "https://www.ozon.ru/category/vodonagrevateli-10719/"
    },
    {
      "root": "Unknown",
      "name": "Обогреватели и тепловентиляторы",
      "url": "https://www.ozon.ru/category/obogrevateli-i-teploventilyatory-10712/"
    },
    {
      "root": "Unknown",
      "name": "Кондиционеры и сплит-системы",
      "url": "https://www.ozon.ru/category/konditsionery-i-split-sistemy-10726/"
    },
    {
      "root": "Unknown",
      "name": "Вентиляторы",
      "url": "https://www.ozon.ru/category/ventilyatory-10724/"
    },
    {
      "root": "Unknown",
      "name": "Увлажнители воздуха и аромадиффузоры",
      "url": "https://www.ozon.ru/category/uvlazhniteli-vozduha-i-aromadiffuzory-10723/"
    },
    {
      "root": "Unknown",
      "name": "Очистители и мойки воздуха",
      "url": "https://www.ozon.ru/category/ochistiteli-vozduha-10725/"
    },
    {
      "root": "Unknown",
      "name": "Портативные кондиционеры",
      "url": "https://www.ozon.ru/category/ohladiteli-vozduha-1648/"
    },
    {
      "root": "Unknown",
      "name": "Осушители воздуха",
      "url": "https://www.ozon.ru/category/osushiteli-vozduha-10717/"
    },
    {
      "root": "Unknown",
      "name": "Погодные станции и датчики",
      "url": "https://www.ozon.ru/category/pogodnye-stantsii-i-datchiki-10730/"
    },
    {
      "root": "Unknown",
      "name": "Сушилки для рук и тела",
      "url": "https://www.ozon.ru/category/sushilki-dlya-ruk-10710/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-klimaticheskoy-tehniki-10734/"
    },
    {
      "root": "Unknown",
      "name": "Техника для красоты и здоровья",
      "url": "https://www.ozon.ru/category/tehnika-dlya-krasoty-i-zdorovya-10737/"
    },
    {
      "root": "Unknown",
      "name": "Массажное оборудование и аксессуары",
      "url": "https://www.ozon.ru/category/massazhnoe-oborudovanie-i-aksessuary-10777/"
    },
    {
      "root": "Unknown",
      "name": "Весы напольные",
      "url": "https://www.ozon.ru/category/napolnye-vesy-10792/"
    },
    {
      "root": "Unknown",
      "name": "Фены и аксессуары",
      "url": "https://www.ozon.ru/category/feny-i-termoshchetki-10738/"
    },
    {
      "root": "Unknown",
      "name": "Приборы для завивки и аксессуары",
      "url": "https://www.ozon.ru/category/shchiptsy-dlya-zavivki-i-aksessuary-10744/"
    },
    {
      "root": "Unknown",
      "name": "Выпрямители для волос и термощетки",
      "url": "https://www.ozon.ru/category/vypryamiteli-10743/"
    },
    {
      "root": "Unknown",
      "name": "Триммеры для волос",
      "url": "https://www.ozon.ru/category/trimmery-dlya-volos-10765/"
    },
    {
      "root": "Unknown",
      "name": "Электробритвы и аксессуары",
      "url": "https://www.ozon.ru/category/elektrobritvy-i-aksessuary-10759/"
    },
    {
      "root": "Unknown",
      "name": "Машинки для стрижки волос и аксессуары",
      "url": "https://www.ozon.ru/category/mashinki-dlya-strizhki-volos-i-aksessuary-10755/"
    },
    {
      "root": "Unknown",
      "name": "Эпиляторы и аксессуары",
      "url": "https://www.ozon.ru/category/epilyatory-i-aksessuary-10749/"
    },
    {
      "root": "Unknown",
      "name": "Электрические зубные щетки и аксессуары",
      "url": "https://www.ozon.ru/category/elektricheskie-zubnye-shchetki-i-aksessuary-10771/"
    },
    {
      "root": "Unknown",
      "name": "Ирригаторы и аксессуары",
      "url": "https://www.ozon.ru/category/irrigatory-i-aksessuary-36933/"
    },
    {
      "root": "Unknown",
      "name": "Техника для общепита",
      "url": "https://www.ozon.ru/category/tehnika-dlya-obshchepita-35374/"
    },
    {
      "root": "Unknown",
      "name": "Холодильное оборудование",
      "url": "https://www.ozon.ru/category/holodilnye-vitriny-10503/"
    },
    {
      "root": "Unknown",
      "name": "Жарочное оборудование",
      "url": "https://www.ozon.ru/category/shkafy-i-pechi-pekarskie-35911/"
    },
    {
      "root": "Unknown",
      "name": "Тепловое оборудование",
      "url": "https://www.ozon.ru/category/teplovye-vitriny-i-podogrevateli-35375/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для приготовления напитков",
      "url": "https://www.ozon.ru/category/kipyatilniki-protochnye-38045/"
    },
    {
      "root": "Unknown",
      "name": "Кондитерское и пекарское оборудование",
      "url": "https://www.ozon.ru/category/pekarskoe-oborudovanie-37986/"
    },
    {
      "root": "Unknown",
      "name": "Электромеханическое оборудование",
      "url": "https://www.ozon.ru/category/elektromehanicheskoe-oborudovanie-37186/"
    },
    {
      "root": "Unknown",
      "name": "Вендинговые аппараты",
      "url": "https://www.ozon.ru/category/torgovye-avtomaty-34996/"
    },
    {
      "root": "Unknown",
      "name": "Для оборудования общепита",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-oborudovaniya-obshchepita-35115/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 195,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Спортивное питание",
      "url": "https://www.ozon.ru/category/sportivnoe-pitanie-11650/"
    },
    {
      "root": "Unknown",
      "name": "Протеины, гейнеры, углеводы",
      "url": "https://www.ozon.ru/category/proteiny-11675/"
    },
    {
      "root": "Unknown",
      "name": "Витамины и минералы",
      "url": "https://www.ozon.ru/category/vitaminno-mineralnye-kompleksy-11656/"
    },
    {
      "root": "Unknown",
      "name": "Аминокислоты",
      "url": "https://www.ozon.ru/category/aminokisloty-11661/"
    },
    {
      "root": "Unknown",
      "name": "Средства для снижения веса",
      "url": "https://www.ozon.ru/category/sredstva-dlya-snizheniya-vesa-31101/"
    },
    {
      "root": "Unknown",
      "name": "Креатины",
      "url": "https://www.ozon.ru/category/kreatiny-11667/"
    },
    {
      "root": "Unknown",
      "name": "Фитнес-питание",
      "url": "https://www.ozon.ru/category/fitnes-pitanie-11676/"
    },
    {
      "root": "Unknown",
      "name": "Энергетики и изотоники",
      "url": "https://www.ozon.ru/category/sportivnye-energetiki-i-izotoniki-31103/"
    },
    {
      "root": "Unknown",
      "name": "Анаболики и тестостероны",
      "url": "https://www.ozon.ru/category/testosteronovye-bustery-11681/"
    },
    {
      "root": "Unknown",
      "name": "Шейкеры",
      "url": "https://www.ozon.ru/category/sheykery-sportivnye-i-butylki-11689/"
    },
    {
      "root": "Unknown",
      "name": "Тренировочные комплексы и релаксанты",
      "url": "https://www.ozon.ru/category/trenirovochnye-kompleksy-31102/"
    },
    {
      "root": "Unknown",
      "name": "Батончики",
      "url": "https://www.ozon.ru/category/batonchiki-sportivnye-1693/"
    },
    {
      "root": "Unknown",
      "name": "Препараты для связок и суставов",
      "url": "https://www.ozon.ru/category/preparaty-dlya-svyazok-i-sustavov-11674/"
    },
    {
      "root": "Unknown",
      "name": "Ферменты и антиоксиданты",
      "url": "https://www.ozon.ru/category/antioksidanty-11653/"
    },
    {
      "root": "Unknown",
      "name": "Жирные кислоты",
      "url": "https://www.ozon.ru/category/omega-3-i-kompleksy-zhirov-11687/"
    },
    {
      "root": "Unknown",
      "name": "Велоспорт",
      "url": "https://www.ozon.ru/category/velosipedy-ekipirovka-i-zapchasti-11001/"
    },
    {
      "root": "Unknown",
      "name": "Велосипеды",
      "url": "https://www.ozon.ru/category/velosipedy-11002/"
    },
    {
      "root": "Unknown",
      "name": "Велозапчасти",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-velosipedov-11012/"
    },
    {
      "root": "Unknown",
      "name": "Колеса",
      "url": "https://www.ozon.ru/category/kolesa-velosipednye-1734/"
    },
    {
      "root": "Unknown",
      "name": "Покрышки и камеры",
      "url": "https://www.ozon.ru/category/pokryshki-i-kamery-dlya-velosipedov-11048/"
    },
    {
      "root": "Unknown",
      "name": "Седла",
      "url": "https://www.ozon.ru/category/sedlo-velosipednoe-8508/"
    },
    {
      "root": "Unknown",
      "name": "Крылья и брызговики",
      "url": "https://www.ozon.ru/category/krylya-dlya-velosipedov-11037/"
    },
    {
      "root": "Unknown",
      "name": "Грипсы и ручки",
      "url": "https://www.ozon.ru/category/gripsy-i-ruchki-11025/"
    },
    {
      "root": "Unknown",
      "name": "Тормоза",
      "url": "https://www.ozon.ru/category/tormoza-dlya-velosipedov-11058/"
    },
    {
      "root": "Unknown",
      "name": "Велокосметика и средства для ухода",
      "url": "https://www.ozon.ru/category/velokosmetika-i-sredstva-dlya-uhoda-11017/"
    },
    {
      "root": "Unknown",
      "name": "Цепи",
      "url": "https://www.ozon.ru/category/tsepi-dlya-velosipedov-11063/"
    },
    {
      "root": "Unknown",
      "name": "Велосумки",
      "url": "https://www.ozon.ru/category/velosumki-11020/"
    },
    {
      "root": "Unknown",
      "name": "Велоодежда и велотуфли",
      "url": "https://www.ozon.ru/category/ekipirovka-dlya-velosipedistov-11003/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/akssesuary-dlya-velosipedov-31111/"
    },
    {
      "root": "Unknown",
      "name": "Велокресла",
      "url": "https://www.ozon.ru/category/velosipednye-kresla-7069/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для велокресел",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-velokresel-34449/"
    },
    {
      "root": "Unknown",
      "name": "Водный спорт и отдых на воде",
      "url": "https://www.ozon.ru/category/vodnyy-sport-i-otdyh-na-vode-34408/"
    },
    {
      "root": "Unknown",
      "name": "SUP-доски и аксессуары",
      "url": "https://www.ozon.ru/category/sup-serfing-34409/"
    },
    {
      "root": "Unknown",
      "name": "Плавание",
      "url": "https://www.ozon.ru/category/plavanie-11181/"
    },
    {
      "root": "Unknown",
      "name": "Гидрокостюмы",
      "url": "https://www.ozon.ru/category/gidrokostyumy-11215/"
    },
    {
      "root": "Unknown",
      "name": "Оружие для охоты",
      "url": "https://www.ozon.ru/category/oruzhie-dlya-podvodnoy-ohoty-31878/"
    },
    {
      "root": "Unknown",
      "name": "Дайвинг",
      "url": "https://www.ozon.ru/category/dayving-11214/"
    },
    {
      "root": "Unknown",
      "name": "Каякинг",
      "url": "https://www.ozon.ru/category/kayaking-34413/"
    },
    {
      "root": "Unknown",
      "name": "Аквафитнес и водное поло",
      "url": "https://www.ozon.ru/category/akvafitnes-33767/"
    },
    {
      "root": "Unknown",
      "name": "Ватрушки и баллоны",
      "url": "https://www.ozon.ru/category/vatrushki-i-ballony-38353/"
    },
    {
      "root": "Unknown",
      "name": "Серфинг, виндсерфинг и водные лыжи",
      "url": "https://www.ozon.ru/category/serfing-i-vodnyy-sport-38772/"
    },
    {
      "root": "Unknown",
      "name": "Бассейны",
      "url": "https://www.ozon.ru/category/basseyny-35372/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для водных видов спорта",
      "url": "https://www.ozon.ru/category/prochie-aksessuary-dlya-plavaniya-11189/"
    },
    {
      "root": "Unknown",
      "name": "Самокаты и аксессуары",
      "url": "https://www.ozon.ru/category/samokaty-giroskutery-i-monokolesa-11069/"
    },
    {
      "root": "Unknown",
      "name": "Самокаты",
      "url": "https://www.ozon.ru/category/samokaty-11068/"
    },
    {
      "root": "Unknown",
      "name": "Электросамокаты",
      "url": "https://www.ozon.ru/category/elektrosamokaty-38264/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для самокатов",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-samokatov-37362/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для электросамокатов",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-elektrosamokatov-37434/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-samokatov-37361/"
    },
    {
      "root": "Unknown",
      "name": "Электротранспорт",
      "url": "https://www.ozon.ru/category/elektrotransport-38259/"
    },
    {
      "root": "Unknown",
      "name": "Электроскутеры",
      "url": "https://www.ozon.ru/category/elektroskutery-34036/"
    },
    {
      "root": "Unknown",
      "name": "Гироскутеры и гироролики",
      "url": "https://www.ozon.ru/category/giroskutery-11070/"
    },
    {
      "root": "Unknown",
      "name": "Электровелосипеды",
      "url": "https://www.ozon.ru/category/elektrovelosipedy-38260/"
    },
    {
      "root": "Unknown",
      "name": "Электросамокаты",
      "url": "https://www.ozon.ru/category/elektrosamokaty-11071/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для электротранспорта",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-giroskuterov-11074/"
    },
    {
      "root": "Unknown",
      "name": "Роликовые коньки",
      "url": "https://www.ozon.ru/category/rolikovye-konki-ekipirovka-i-zapchasti-11086/"
    },
    {
      "root": "Unknown",
      "name": "Роликовые коньки",
      "url": "https://www.ozon.ru/category/rolikovye-konki-11088/"
    },
    {
      "root": "Unknown",
      "name": "Лыжероллеры",
      "url": "https://www.ozon.ru/category/lyzherollery-38243/"
    },
    {
      "root": "Unknown",
      "name": "Защита",
      "url": "https://www.ozon.ru/category/zashchita-dlya-rolikov-34662/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти для роликовых коньков",
      "url": "https://www.ozon.ru/category/aksessuary-i-zapchasti-dlya-rolikovyh-konkov-11092/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для лыжероллеров",
      "url": "https://www.ozon.ru/category/lyzherollery-11104/"
    },
    {
      "root": "Unknown",
      "name": "Скейтбординг",
      "url": "https://www.ozon.ru/category/skeytbording-11075/"
    },
    {
      "root": "Unknown",
      "name": "Круизеры, пенни борды и роллерсерфы",
      "url": "https://www.ozon.ru/category/kruizery-11080/"
    },
    {
      "root": "Unknown",
      "name": "Скейтборды",
      "url": "https://www.ozon.ru/category/skeytbordy-11077/"
    },
    {
      "root": "Unknown",
      "name": "Лонгборды",
      "url": "https://www.ozon.ru/category/longbordy-11078/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти",
      "url": "https://www.ozon.ru/category/deki-dlya-skeytborda-11084/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы и сумки",
      "url": "https://www.ozon.ru/category/chehly-i-sumki-dlya-skeytbordov-31953/"
    },
    {
      "root": "Unknown",
      "name": "Теннис и бадминтон",
      "url": "https://www.ozon.ru/category/tennis-i-badminton-11276/"
    },
    {
      "root": "Unknown",
      "name": "Большой теннис",
      "url": "https://www.ozon.ru/category/bolshoy-tennis-11277/"
    },
    {
      "root": "Unknown",
      "name": "Настольный теннис",
      "url": "https://www.ozon.ru/category/nastolnyy-tennis-11286/"
    },
    {
      "root": "Unknown",
      "name": "Бадминтон",
      "url": "https://www.ozon.ru/category/badminton-11293/"
    },
    {
      "root": "Unknown",
      "name": "Сквош, падел, спидрол",
      "url": "https://www.ozon.ru/category/skvosh-32652/"
    },
    {
      "root": "Unknown",
      "name": "Бег",
      "url": "https://www.ozon.ru/category/beg-11847/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы, гольфы, перчатки",
      "url": "https://www.ozon.ru/category/odezhda-dlya-bega-30235/"
    },
    {
      "root": "Unknown",
      "name": "Обувь и аксессуары для легкой атлетики",
      "url": "https://www.ozon.ru/category/obuv-dlya-bega-i-aksessuary-33692/"
    },
    {
      "root": "Unknown",
      "name": "Поясные сумки и рюкзаки-гидраторы для бега",
      "url": "https://www.ozon.ru/category/sumki-dlya-bega-33698/"
    },
    {
      "root": "Unknown",
      "name": "Спортивные бутылки",
      "url": "https://www.ozon.ru/category/sportivnye-butylki-1718/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для бега",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-bega-33696/"
    },
    {
      "root": "Unknown",
      "name": "Виды спорта",
      "url": "https://www.ozon.ru/category/vidy-sporta-8811/"
    },
    {
      "root": "Unknown",
      "name": "Футбол",
      "url": "https://www.ozon.ru/category/futbol-11227/"
    },
    {
      "root": "Unknown",
      "name": "Баскетбол",
      "url": "https://www.ozon.ru/category/basketbol-11252/"
    },
    {
      "root": "Unknown",
      "name": "Волейбол",
      "url": "https://www.ozon.ru/category/voleybol-11257/"
    },
    {
      "root": "Unknown",
      "name": "Художественная гимнастика",
      "url": "https://www.ozon.ru/category/hudozhestvennaya-gimnastika-i-tantsy-11764/"
    },
    {
      "root": "Unknown",
      "name": "Спортивная гимнастика",
      "url": "https://www.ozon.ru/category/sportivnaya-gimnastika-32950/"
    },
    {
      "root": "Unknown",
      "name": "Конный спорт",
      "url": "https://www.ozon.ru/category/konnyy-sport-33980/"
    },
    {
      "root": "Unknown",
      "name": "Тяжелая атлетика",
      "url": "https://www.ozon.ru/category/ekipirovka-dlya-tyazheloy-atletiki-11848/"
    },
    {
      "root": "Unknown",
      "name": "Бейсбол",
      "url": "https://www.ozon.ru/category/beysbol-11260/"
    },
    {
      "root": "Unknown",
      "name": "Регби, гандбол и американский футбол",
      "url": "https://www.ozon.ru/category/regbi-i-amerikanskiy-futbol-11264/"
    },
    {
      "root": "Unknown",
      "name": "Пейнтбол",
      "url": "https://www.ozon.ru/category/peyntbol-32834/"
    },
    {
      "root": "Unknown",
      "name": "Гольф",
      "url": "https://www.ozon.ru/category/golf-38247/"
    },
    {
      "root": "Unknown",
      "name": "Фехтование",
      "url": "https://www.ozon.ru/category/fehtovanie-37571/"
    },
    {
      "root": "Unknown",
      "name": "Атрибутика и аксессуары",
      "url": "https://www.ozon.ru/category/sportivnaya-atributika-11887/"
    },
    {
      "root": "Unknown",
      "name": "Активные виды отдыха",
      "url": "https://www.ozon.ru/category/aktivnye-vidy-otdyha-8787/"
    },
    {
      "root": "Unknown",
      "name": "Батуты",
      "url": "https://www.ozon.ru/category/batuty-11748/"
    },
    {
      "root": "Unknown",
      "name": "Палки для спортивной ходьбы и аксессуары",
      "url": "https://www.ozon.ru/category/palki-dlya-skandinavskoy-hodby-11633/"
    },
    {
      "root": "Unknown",
      "name": "Дартс",
      "url": "https://www.ozon.ru/category/darts-11318/"
    },
    {
      "root": "Unknown",
      "name": "Бильярд",
      "url": "https://www.ozon.ru/category/bilyard-11302/"
    },
    {
      "root": "Unknown",
      "name": "Игровые столы",
      "url": "https://www.ozon.ru/category/nastolnye-sportivnye-igry-11325/"
    },
    {
      "root": "Unknown",
      "name": "Инвентарь для активного отдыха",
      "url": "https://www.ozon.ru/category/florbol-34927/"
    },
    {
      "root": "Unknown",
      "name": "Джамперы и погостики",
      "url": "https://www.ozon.ru/category/dzhampery-i-pogostiki-11105/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для батутов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-batutov-11749/"
    },
    {
      "root": "Unknown",
      "name": "Фитнес и йога",
      "url": "https://www.ozon.ru/category/fitnes-i-yoga-38647/"
    },
    {
      "root": "Unknown",
      "name": "Фитнес",
      "url": "https://www.ozon.ru/category/fitnes-11716/"
    },
    {
      "root": "Unknown",
      "name": "Йога и пилатес",
      "url": "https://www.ozon.ru/category/yoga-i-pilates-11734/"
    },
    {
      "root": "Unknown",
      "name": "Спортивные комплексы и шведские стенки",
      "url": "https://www.ozon.ru/category/gimnasticheskie-snaryady-shvedskie-stenki-i-sportivnye-kompleksy-11750/"
    },
    {
      "root": "Unknown",
      "name": "Спортивные массажеры",
      "url": "https://www.ozon.ru/category/sportivnye-massazhery-34245/"
    },
    {
      "root": "Unknown",
      "name": "Утяжелители",
      "url": "https://www.ozon.ru/category/utyazheliteli-11722/"
    },
    {
      "root": "Unknown",
      "name": "Одежда, пояса и пластыри для похудения",
      "url": "https://www.ozon.ru/category/odezhda-i-poyasa-dlya-pohudeniya-6293/"
    },
    {
      "root": "Unknown",
      "name": "Смарт-часы",
      "url": "https://www.ozon.ru/category/smart-chasy-41310/"
    },
    {
      "root": "Unknown",
      "name": "Ремешки для смарт-часов и фитнес-браслетов",
      "url": "https://www.ozon.ru/category/remeshki-dlya-smart-chasov-i-fitnes-brasletov-39671/"
    },
    {
      "root": "Unknown",
      "name": "Гаджеты для фитнеса",
      "url": "https://www.ozon.ru/category/gadzhety-dlya-fitnesa-11728/"
    },
    {
      "root": "Unknown",
      "name": "Петли, лестницы и тумбы",
      "url": "https://www.ozon.ru/category/krossfit-35324/"
    },
    {
      "root": "Unknown",
      "name": "Тренажеры",
      "url": "https://www.ozon.ru/category/trenazhery-i-fitnes-11638/"
    },
    {
      "root": "Unknown",
      "name": "Скамьи и стойки",
      "url": "https://www.ozon.ru/category/atleticheskie-skami-32530/"
    },
    {
      "root": "Unknown",
      "name": "Мини-тренажеры",
      "url": "https://www.ozon.ru/category/mini-trenazhery-11709/"
    },
    {
      "root": "Unknown",
      "name": "Степперы",
      "url": "https://www.ozon.ru/category/steppery-11694/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-trenazherov-38646/"
    },
    {
      "root": "Unknown",
      "name": "Кардиотренажеры",
      "url": "https://www.ozon.ru/category/kardiotrenazhery-32524/"
    },
    {
      "root": "Unknown",
      "name": "Беговые дорожки",
      "url": "https://www.ozon.ru/category/begovye-dorozhki-11691/"
    },
    {
      "root": "Unknown",
      "name": "Велотренажеры",
      "url": "https://www.ozon.ru/category/velotrenazhery-11692/"
    },
    {
      "root": "Unknown",
      "name": "Эллиптические тренажеры",
      "url": "https://www.ozon.ru/category/ellipticheskie-trenazhery-11695/"
    },
    {
      "root": "Unknown",
      "name": "Гребные тренажеры",
      "url": "https://www.ozon.ru/category/grebnye-trenazhery-11697/"
    },
    {
      "root": "Unknown",
      "name": "Бокс и единоборства",
      "url": "https://www.ozon.ru/category/boks-i-edinoborstva-11778/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки",
      "url": "https://www.ozon.ru/category/bokserskie-perchatki-11780/"
    },
    {
      "root": "Unknown",
      "name": "Груши и мешки",
      "url": "https://www.ozon.ru/category/bokserskie-grushi-11784/"
    },
    {
      "root": "Unknown",
      "name": "Защита тела",
      "url": "https://www.ozon.ru/category/zashchita-dlya-boksa-i-edinoborstv-32759/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-dlya-boksa-37414/"
    },
    {
      "root": "Unknown",
      "name": "Кимоно",
      "url": "https://www.ozon.ru/category/kimono-dlya-karate-30165/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-dlya-boksa-37415/"
    },
    {
      "root": "Unknown",
      "name": "Капы",
      "url": "https://www.ozon.ru/category/bokserskie-kapy-11781/"
    },
    {
      "root": "Unknown",
      "name": "Оружие",
      "url": "https://www.ozon.ru/category/oruzhie-dlya-edinoborstv-34852/"
    },
    {
      "root": "Unknown",
      "name": "Инвентарь",
      "url": "https://www.ozon.ru/category/inventar-dlya-borby-34871/"
    },
    {
      "root": "Unknown",
      "name": "Зимний спорт",
      "url": "https://www.ozon.ru/category/zimniy-sport-11108/"
    },
    {
      "root": "Unknown",
      "name": "Хоккей",
      "url": "https://www.ozon.ru/category/hokkey-11232/"
    },
    {
      "root": "Unknown",
      "name": "Беговые лыжи",
      "url": "https://www.ozon.ru/category/begovye-lyzhi-11136/"
    },
    {
      "root": "Unknown",
      "name": "Сноуборды",
      "url": "https://www.ozon.ru/category/snoubordy-11159/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для лыж и сноубординга",
      "url": "https://www.ozon.ru/category/odezhda-dlya-begovyh-lyzh-30300/"
    },
    {
      "root": "Unknown",
      "name": "Ботинки и крепления для лыж и сноубордов",
      "url": "https://www.ozon.ru/category/lyzhnye-botinki-11141/"
    },
    {
      "root": "Unknown",
      "name": "Маски и очки",
      "url": "https://www.ozon.ru/category/maski-i-ochki-dlya-gornyh-lyzh-11118/"
    },
    {
      "root": "Unknown",
      "name": "Обработка лыж и сноубордов",
      "url": "https://www.ozon.ru/category/stanki-profili-dlya-lyzh-11155/"
    },
    {
      "root": "Unknown",
      "name": "Лыжные палки",
      "url": "https://www.ozon.ru/category/lyzhnye-palki-11140/"
    },
    {
      "root": "Unknown",
      "name": "Коньки прогулочные",
      "url": "https://www.ozon.ru/category/konki-11110/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для фигурного катания",
      "url": "https://www.ozon.ru/category/odezhda-dlya-figurnogo-kataniya-33923/"
    },
    {
      "root": "Unknown",
      "name": "Снегоходы и мотобуксировщики",
      "url": "https://www.ozon.ru/category/snegohody-i-motobuksirovshchiki-38121/"
    },
    {
      "root": "Unknown",
      "name": "Тюбинги",
      "url": "https://www.ozon.ru/category/tyubingi-39545/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и чехлы для лыж, сноубордов и ботинок",
      "url": "https://www.ozon.ru/category/chehly-dlya-begovyh-lyzh-11144/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы, сумки, аксессуары для коньков",
      "url": "https://www.ozon.ru/category/chehly-dlya-konkov-11111/"
    },
    {
      "root": "Unknown",
      "name": "Спортивная защита и экипировка",
      "url": "https://www.ozon.ru/category/sportivnaya-zashchita-i-ekipirovka-11836/"
    },
    {
      "root": "Unknown",
      "name": "Защита тела",
      "url": "https://www.ozon.ru/category/sportivnaya-zashchita-11837/"
    },
    {
      "root": "Unknown",
      "name": "Шлемы и маски",
      "url": "https://www.ozon.ru/category/zashchitnye-shlemy-11840/"
    },
    {
      "root": "Unknown",
      "name": "Тейпы",
      "url": "https://www.ozon.ru/category/kinezioteypy-11843/"
    },
    {
      "root": "Unknown",
      "name": "Компрессионные повязки и рукава",
      "url": "https://www.ozon.ru/category/kompressionnye-povyazki-i-rukava-6289/"
    },
    {
      "root": "Unknown",
      "name": "Очки",
      "url": "https://www.ozon.ru/category/ochki-sportivnye-11841/"
    },
    {
      "root": "Unknown",
      "name": "Сумки",
      "url": "https://www.ozon.ru/category/sportivnye-sumki-11856/"
    },
    {
      "root": "Unknown",
      "name": "Товары для самообороны",
      "url": "https://www.ozon.ru/category/tovary-dlya-samooborony-32022/"
    },
    {
      "root": "Unknown",
      "name": "Жезлы ДПС",
      "url": "https://www.ozon.ru/category/zhezly-dps-38623/"
    },
    {
      "root": "Unknown",
      "name": "Свободные веса",
      "url": "https://www.ozon.ru/category/svobodnye-vesa-38639/"
    },
    {
      "root": "Unknown",
      "name": "Гантели",
      "url": "https://www.ozon.ru/category/ganteli-11641/"
    },
    {
      "root": "Unknown",
      "name": "Гири",
      "url": "https://www.ozon.ru/category/giri-11643/"
    },
    {
      "root": "Unknown",
      "name": "Штанги",
      "url": "https://www.ozon.ru/category/shtangi-11642/"
    },
    {
      "root": "Unknown",
      "name": "Турники и брусья",
      "url": "https://www.ozon.ru/category/turniki-i-brusya-11698/"
    },
    {
      "root": "Unknown",
      "name": "Диски и блины",
      "url": "https://www.ozon.ru/category/diski-dlya-shtang-11644/"
    },
    {
      "root": "Unknown",
      "name": "Грифы",
      "url": "https://www.ozon.ru/category/grify-dlya-shtang-11645/"
    },
    {
      "root": "Unknown",
      "name": "Планерный спорт",
      "url": "https://www.ozon.ru/category/planernyy-sport-39936/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 194,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-remonta-i-stroitelstva-9856/"
    },
    {
      "root": "Unknown",
      "name": "Электроинструменты",
      "url": "https://www.ozon.ru/category/elektroinstrumenty-9857/"
    },
    {
      "root": "Unknown",
      "name": "Пневмоинструменты",
      "url": "https://www.ozon.ru/category/pnevmoinstrumenty-9989/"
    },
    {
      "root": "Unknown",
      "name": "Сварочное оборудование",
      "url": "https://www.ozon.ru/category/svarochnoe-oborudovanie-10046/"
    },
    {
      "root": "Unknown",
      "name": "Паяльное оборудование",
      "url": "https://www.ozon.ru/category/payalnoe-oborudovanie-10053/"
    },
    {
      "root": "Unknown",
      "name": "Измерительные инструменты",
      "url": "https://www.ozon.ru/category/izmeritelnye-instrumenty-10075/"
    },
    {
      "root": "Unknown",
      "name": "Режущие и пильные инструменты",
      "url": "https://www.ozon.ru/category/rezhushchiy-i-pilnyy-31814/"
    },
    {
      "root": "Unknown",
      "name": "Малярные и отделочные инструменты",
      "url": "https://www.ozon.ru/category/malyarnyy-i-otdelochnyy-31817/"
    },
    {
      "root": "Unknown",
      "name": "Монтажные и крепежные инструменты",
      "url": "https://www.ozon.ru/category/montazhnyy-i-krepezhnyy-31816/"
    },
    {
      "root": "Unknown",
      "name": "Ключи и отвертки",
      "url": "https://www.ozon.ru/category/klyuchi-i-otvertki-31813/"
    },
    {
      "root": "Unknown",
      "name": "Ударные и рычажные инструменты",
      "url": "https://www.ozon.ru/category/udarnyy-i-rychazhnyy-31815/"
    },
    {
      "root": "Unknown",
      "name": "Слесарные инструменты",
      "url": "https://www.ozon.ru/category/slesarnye-instrumenty-9917/"
    },
    {
      "root": "Unknown",
      "name": "Специальные инструменты",
      "url": "https://www.ozon.ru/category/spetsialnyy-instrument-36072/"
    },
    {
      "root": "Unknown",
      "name": "Наборы инструментов",
      "url": "https://www.ozon.ru/category/nabory-instrumentov-31107/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти и аксессуары",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-instrumentov-32788/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для мастерской",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-masterskoy-31818/"
    },
    {
      "root": "Unknown",
      "name": "Расходные материалы и оснастка",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-i-osnastka-dlya-instrumentov-10110/"
    },
    {
      "root": "Unknown",
      "name": "Оснастка",
      "url": "https://www.ozon.ru/category/osnastka-dlya-instrumenta-39512/"
    },
    {
      "root": "Unknown",
      "name": "Для дрелей, гравёров и шуруповертов",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-dreley-i-shurupovertov-10117/"
    },
    {
      "root": "Unknown",
      "name": "Круги и диски",
      "url": "https://www.ozon.ru/category/krugi-i-diski-39006/"
    },
    {
      "root": "Unknown",
      "name": "Для шлифовальных машин",
      "url": "https://www.ozon.ru/category/osnastka-dlya-shlifovalnyh-mashin-10146/"
    },
    {
      "root": "Unknown",
      "name": "Для ремонта",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-remonta-39513/"
    },
    {
      "root": "Unknown",
      "name": "Сантехника",
      "url": "https://www.ozon.ru/category/santehnika-i-vodosnabzhenie-10255/"
    },
    {
      "root": "Unknown",
      "name": "Смесители и комплектующие",
      "url": "https://www.ozon.ru/category/smesiteli-i-komplektuyushchie-31849/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные мойки",
      "url": "https://www.ozon.ru/category/kuhonnye-moyki-10264/"
    },
    {
      "root": "Unknown",
      "name": "Раковины, умывальники и пьедесталы",
      "url": "https://www.ozon.ru/category/rakoviny-umyvalniki-i-pedestaly-10257/"
    },
    {
      "root": "Unknown",
      "name": "Души и душевые кабины",
      "url": "https://www.ozon.ru/category/dushi-i-dushevye-kabiny-10266/"
    },
    {
      "root": "Unknown",
      "name": "Душевое оборудование",
      "url": "https://www.ozon.ru/category/dushevoe-oborudovanie-31851/"
    },
    {
      "root": "Unknown",
      "name": "Унитазы и инсталляции",
      "url": "https://www.ozon.ru/category/unitazy-i-bede-31850/"
    },
    {
      "root": "Unknown",
      "name": "Ванны и комплектующие",
      "url": "https://www.ozon.ru/category/vanny-i-komplektuyushchie-31848/"
    },
    {
      "root": "Unknown",
      "name": "Арматура и аксессуары для сантехники",
      "url": "https://www.ozon.ru/category/armatura-i-aksessuary-dlya-santehniki-10310/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты сантехники",
      "url": "https://www.ozon.ru/category/komplekty-santehniki-33841/"
    },
    {
      "root": "Unknown",
      "name": "Водоснабжение",
      "url": "https://www.ozon.ru/category/vodosnabzhenie-31846/"
    },
    {
      "root": "Unknown",
      "name": "Водоочистка и фильтры",
      "url": "https://www.ozon.ru/category/vodoochistka-i-filtry-10292/"
    },
    {
      "root": "Unknown",
      "name": "Трубы и водоснабжение",
      "url": "https://www.ozon.ru/category/truby-i-vodosnabzhenie-10281/"
    },
    {
      "root": "Unknown",
      "name": "Водоотведение и канализация",
      "url": "https://www.ozon.ru/category/vodootvedenie-i-kanalizatsiya-34558/"
    },
    {
      "root": "Unknown",
      "name": "Запорная и регулирующая арматура",
      "url": "https://www.ozon.ru/category/zapornaya-armatura-31847/"
    },
    {
      "root": "Unknown",
      "name": "Предохранительная арматура",
      "url": "https://www.ozon.ru/category/predohranitelnaya-armatura-34561/"
    },
    {
      "root": "Unknown",
      "name": "Счетчики воды и монтажные комплекты",
      "url": "https://www.ozon.ru/category/schetchiki-vody-i-montazhnye-komplekty-38842/"
    },
    {
      "root": "Unknown",
      "name": "Гидроаккумуляторы",
      "url": "https://www.ozon.ru/category/gidroakkumulyatory-35087/"
    },
    {
      "root": "Unknown",
      "name": "Насосные группы",
      "url": "https://www.ozon.ru/category/tsirkulyatsionnye-nasosy-34110/"
    },
    {
      "root": "Unknown",
      "name": "Ревизионные люки",
      "url": "https://www.ozon.ru/category/revizionnye-lyuki-10309/"
    },
    {
      "root": "Unknown",
      "name": "Расходные материалы для сантехники",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-santehniki-30356/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты для труб",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-trub-34560/"
    },
    {
      "root": "Unknown",
      "name": "Лакокрасочные материалы",
      "url": "https://www.ozon.ru/category/kraski-laki-i-rastvoriteli-9804/"
    },
    {
      "root": "Unknown",
      "name": "Клеи и герметики",
      "url": "https://www.ozon.ru/category/klei-i-germetiki-9821/"
    },
    {
      "root": "Unknown",
      "name": "Краски",
      "url": "https://www.ozon.ru/category/kraski-dlya-vnutrennih-rabot-34494/"
    },
    {
      "root": "Unknown",
      "name": "Краска колерованная",
      "url": "https://www.ozon.ru/category/kraska-kolerovannaya-39969/"
    },
    {
      "root": "Unknown",
      "name": "Эмали",
      "url": "https://www.ozon.ru/category/emali-9806/"
    },
    {
      "root": "Unknown",
      "name": "Лаки строительные",
      "url": "https://www.ozon.ru/category/laki-dlya-stroitelstva-i-remonta-9807/"
    },
    {
      "root": "Unknown",
      "name": "Аэрозольные краски",
      "url": "https://www.ozon.ru/category/aerozolnye-kraski-9814/"
    },
    {
      "root": "Unknown",
      "name": "Покрытия для дерева",
      "url": "https://www.ozon.ru/category/pokrytiya-dlya-dereva-34471/"
    },
    {
      "root": "Unknown",
      "name": "Пропитки",
      "url": "https://www.ozon.ru/category/propitki-9811/"
    },
    {
      "root": "Unknown",
      "name": "Грунтовки",
      "url": "https://www.ozon.ru/category/gruntovki-9808/"
    },
    {
      "root": "Unknown",
      "name": "Растворители и очистители",
      "url": "https://www.ozon.ru/category/rastvoriteli-i-ochistiteli-9815/"
    },
    {
      "root": "Unknown",
      "name": "Колеры",
      "url": "https://www.ozon.ru/category/kolery-9813/"
    },
    {
      "root": "Unknown",
      "name": "Функциональные добавки к ЛКМ",
      "url": "https://www.ozon.ru/category/funktsionalnye-dobavki-k-lkm-37996/"
    },
    {
      "root": "Unknown",
      "name": "Малярные ленты",
      "url": "https://www.ozon.ru/category/malyarnye-lenty-10038/"
    },
    {
      "root": "Unknown",
      "name": "Материалы для реставрации",
      "url": "https://www.ozon.ru/category/materialy-restavratsionnye-dlya-remonta-36893/"
    },
    {
      "root": "Unknown",
      "name": "Каталоги, тестеры и комплекты ЛКМ",
      "url": "https://www.ozon.ru/category/katalog-krasok-34193/"
    },
    {
      "root": "Unknown",
      "name": "Отделочные материалы",
      "url": "https://www.ozon.ru/category/otdelochnye-materialy-9721/"
    },
    {
      "root": "Unknown",
      "name": "Обои и сопутствующие материалы",
      "url": "https://www.ozon.ru/category/oboi-i-pokrytiya-9730/"
    },
    {
      "root": "Unknown",
      "name": "Напольные покрытия",
      "url": "https://www.ozon.ru/category/napolnye-pokrytiya-9737/"
    },
    {
      "root": "Unknown",
      "name": "Стеновые панели",
      "url": "https://www.ozon.ru/category/stenovye-paneli-31845/"
    },
    {
      "root": "Unknown",
      "name": "Самоклеящаяся пленка",
      "url": "https://www.ozon.ru/category/samokleyushchiesya-plenki-dlya-mebeli-32098/"
    },
    {
      "root": "Unknown",
      "name": "Плитка и керамогранит",
      "url": "https://www.ozon.ru/category/plitka-i-keramogranit-9722/"
    },
    {
      "root": "Unknown",
      "name": "Кирпичи и камень для отделки",
      "url": "https://www.ozon.ru/category/kirpichi-dlya-oblitsovki-i-otdelki-9726/"
    },
    {
      "root": "Unknown",
      "name": "Декор и лепнина",
      "url": "https://www.ozon.ru/category/dekor-i-lepnina-33935/"
    },
    {
      "root": "Unknown",
      "name": "Подвесной потолок и комплектующие",
      "url": "https://www.ozon.ru/category/podvesnye-potolki-32896/"
    },
    {
      "root": "Unknown",
      "name": "Мебельные наполнители",
      "url": "https://www.ozon.ru/category/mebelnye-napolniteli-33765/"
    },
    {
      "root": "Unknown",
      "name": "Армирующие ленты",
      "url": "https://www.ozon.ru/category/armiruyushchie-lenty-9769/"
    },
    {
      "root": "Unknown",
      "name": "Строительные материалы",
      "url": "https://www.ozon.ru/category/stroitelnye-i-otdelochnye-materialy-9701/"
    },
    {
      "root": "Unknown",
      "name": "Строительные смеси",
      "url": "https://www.ozon.ru/category/stroitelnye-smesi-9702/"
    },
    {
      "root": "Unknown",
      "name": "Изоляционные покрытия и материалы",
      "url": "https://www.ozon.ru/category/izolyatsionnye-pokrytiya-i-materialy-9735/"
    },
    {
      "root": "Unknown",
      "name": "Кровля и комплектующие",
      "url": "https://www.ozon.ru/category/krovlya-30342/"
    },
    {
      "root": "Unknown",
      "name": "Водосточные системы",
      "url": "https://www.ozon.ru/category/vodostochnye-sistemy-34983/"
    },
    {
      "root": "Unknown",
      "name": "Облицовочные материалы",
      "url": "https://www.ozon.ru/category/oblitsovochnye-materialy-34476/"
    },
    {
      "root": "Unknown",
      "name": "Металлопрокат и металлоконструкции",
      "url": "https://www.ozon.ru/category/metalloprokat-31463/"
    },
    {
      "root": "Unknown",
      "name": "Двери, окна, лестницы и комплектующие",
      "url": "https://www.ozon.ru/category/dveri-okna-elementy-domov-9746/"
    },
    {
      "root": "Unknown",
      "name": "Двери",
      "url": "https://www.ozon.ru/category/dveri-34488/"
    },
    {
      "root": "Unknown",
      "name": "Ручки, замки и фурнитура",
      "url": "https://www.ozon.ru/category/ruchki-zamki-i-furnitura-9755/"
    },
    {
      "root": "Unknown",
      "name": "Дверные звонки и комплектующие",
      "url": "https://www.ozon.ru/category/zvonki-dvernye-38984/"
    },
    {
      "root": "Unknown",
      "name": "Окна",
      "url": "https://www.ozon.ru/category/okna-34037/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие к окнам и дверям",
      "url": "https://www.ozon.ru/category/komplektuyushchie-k-oknam-39268/"
    },
    {
      "root": "Unknown",
      "name": "Рольставни",
      "url": "https://www.ozon.ru/category/rolstavni-37487/"
    },
    {
      "root": "Unknown",
      "name": "Крыльцо и козырьки",
      "url": "https://www.ozon.ru/category/kozyrki-nad-dvermi-31966/"
    },
    {
      "root": "Unknown",
      "name": "Межэтажные лестницы и комплектующие",
      "url": "https://www.ozon.ru/category/marshevye-lestnitsy-32034/"
    },
    {
      "root": "Unknown",
      "name": "Крепеж и фурнитура",
      "url": "https://www.ozon.ru/category/krepezh-i-furnitura-9767/"
    },
    {
      "root": "Unknown",
      "name": "Фурнитура и комплектующие для мебели",
      "url": "https://www.ozon.ru/category/furnitura-dlya-mebeli-15035/"
    },
    {
      "root": "Unknown",
      "name": "Крепежные изделия и метизы",
      "url": "https://www.ozon.ru/category/krepezhnye-izdeliya-metizy-31883/"
    },
    {
      "root": "Unknown",
      "name": "Такелаж",
      "url": "https://www.ozon.ru/category/takelazh-9791/"
    },
    {
      "root": "Unknown",
      "name": "Кованые элементы",
      "url": "https://www.ozon.ru/category/kovanye-elementy-38770/"
    },
    {
      "root": "Unknown",
      "name": "Опечатывание и пломбирование",
      "url": "https://www.ozon.ru/category/plomby-30778/"
    },
    {
      "root": "Unknown",
      "name": "Неодимовые магниты",
      "url": "https://www.ozon.ru/category/neodimovye-magnity-10399/"
    },
    {
      "root": "Unknown",
      "name": "Система Джокер",
      "url": "https://www.ozon.ru/category/soediniteli-trub-9787/"
    },
    {
      "root": "Unknown",
      "name": "Тарная фурнитура",
      "url": "https://www.ozon.ru/category/tarnaya-furnitura-34970/"
    },
    {
      "root": "Unknown",
      "name": "Почтовые ящики",
      "url": "https://www.ozon.ru/category/pochtovye-yashchiki-9754/"
    },
    {
      "root": "Unknown",
      "name": "Электрика",
      "url": "https://www.ozon.ru/category/elektrika-9826/"
    },
    {
      "root": "Unknown",
      "name": "Розетки, вилки и выключатели",
      "url": "https://www.ozon.ru/category/rozetki-i-vyklyuchateli-9827/"
    },
    {
      "root": "Unknown",
      "name": "Кабели и провода",
      "url": "https://www.ozon.ru/category/kabeli-i-provod-34460/"
    },
    {
      "root": "Unknown",
      "name": "Кабеленесущие системы",
      "url": "https://www.ozon.ru/category/kabelenesushchie-sistemy-34465/"
    },
    {
      "root": "Unknown",
      "name": "Распределительные щиты и боксы",
      "url": "https://www.ozon.ru/category/raspredelitelnye-shchity-9847/"
    },
    {
      "root": "Unknown",
      "name": "Стабилизаторы напряжения",
      "url": "https://www.ozon.ru/category/stabilizatory-napryazheniya-9832/"
    },
    {
      "root": "Unknown",
      "name": "Автоматика",
      "url": "https://www.ozon.ru/category/avtomaticheskie-vyklyuchateli-uzo-difavtomaty-9839/"
    },
    {
      "root": "Unknown",
      "name": "Коммутационное оборудование",
      "url": "https://www.ozon.ru/category/kommutatsionnoe-oborudovanie-34935/"
    },
    {
      "root": "Unknown",
      "name": "Трансформаторы",
      "url": "https://www.ozon.ru/category/transformatory-34467/"
    },
    {
      "root": "Unknown",
      "name": "Изоляционные материалы",
      "url": "https://www.ozon.ru/category/izolyatsionnye-materialy-9854/"
    },
    {
      "root": "Unknown",
      "name": "Солнечные панели",
      "url": "https://www.ozon.ru/category/solnechnye-paneli-i-batarei-31336/"
    },
    {
      "root": "Unknown",
      "name": "Отопление",
      "url": "https://www.ozon.ru/category/otoplenie-10198/"
    },
    {
      "root": "Unknown",
      "name": "Радиаторы",
      "url": "https://www.ozon.ru/category/radiatory-10200/"
    },
    {
      "root": "Unknown",
      "name": "Отопительные котлы",
      "url": "https://www.ozon.ru/category/otopitelnye-kotly-10211/"
    },
    {
      "root": "Unknown",
      "name": "Полотенцесушители",
      "url": "https://www.ozon.ru/category/polotentsesushiteli-10216/"
    },
    {
      "root": "Unknown",
      "name": "Теплые полы",
      "url": "https://www.ozon.ru/category/elektricheskie-teplye-poly-10217/"
    },
    {
      "root": "Unknown",
      "name": "Камины и порталы",
      "url": "https://www.ozon.ru/category/kaminy-i-portaly-10207/"
    },
    {
      "root": "Unknown",
      "name": "Отопительные конвекторы",
      "url": "https://www.ozon.ru/category/konvektory-10199/"
    },
    {
      "root": "Unknown",
      "name": "Тепловые пушки и аксессуары",
      "url": "https://www.ozon.ru/category/teplovye-pushki-10716/"
    },
    {
      "root": "Unknown",
      "name": "Греющие кабели",
      "url": "https://www.ozon.ru/category/greyushchiesya-kabeli-30796/"
    },
    {
      "root": "Unknown",
      "name": "Печи и комплектующие",
      "url": "https://www.ozon.ru/category/pechi-10342/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для котлов",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-kotlov-10212/"
    },
    {
      "root": "Unknown",
      "name": "Датчики и регуляторы",
      "url": "https://www.ozon.ru/category/datchiki-regulyatory-dlya-teplyh-polov-31840/"
    },
    {
      "root": "Unknown",
      "name": "Теплоносители, промывки и герметизаторы",
      "url": "https://www.ozon.ru/category/teplonositeli-i-promyvka-sistem-otopleniya-32004/"
    },
    {
      "root": "Unknown",
      "name": "Элементы систем отопления",
      "url": "https://www.ozon.ru/category/rasshiritelnye-baki-dlya-otopleniya-35320/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-konvektorov-i-radiatorov-10201/"
    },
    {
      "root": "Unknown",
      "name": "Вентиляция",
      "url": "https://www.ozon.ru/category/ventilyatsiya-10218/"
    },
    {
      "root": "Unknown",
      "name": "Дымоходы и комплектующие",
      "url": "https://www.ozon.ru/category/dymohody-i-komplektuyushchie-10244/"
    },
    {
      "root": "Unknown",
      "name": "Вентиляторы и дефлекторы вентиляционные",
      "url": "https://www.ozon.ru/category/ventilyatsionnye-ustanovki-10221/"
    },
    {
      "root": "Unknown",
      "name": "Вентиляционное оборудование",
      "url": "https://www.ozon.ru/category/ventilyatsionnoe-oborudovanie-10223/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие и запчасти",
      "url": "https://www.ozon.ru/category/komplektuyushchie-i-zapchasti-dlya-ventilyatsii-10231/"
    },
    {
      "root": "Unknown",
      "name": "Газоснабжение",
      "url": "https://www.ozon.ru/category/gazosnabzhenie-37995/"
    },
    {
      "root": "Unknown",
      "name": "Средства защиты и пожаротушения",
      "url": "https://www.ozon.ru/category/sredstva-individualnoy-zashchity-33126/"
    },
    {
      "root": "Unknown",
      "name": "Защита органов дыхания",
      "url": "https://www.ozon.ru/category/zashchita-organov-dyhaniya-34500/"
    },
    {
      "root": "Unknown",
      "name": "Защита органов зрения",
      "url": "https://www.ozon.ru/category/zashchita-organov-zreniya-34501/"
    },
    {
      "root": "Unknown",
      "name": "Защита органов слуха",
      "url": "https://www.ozon.ru/category/zashchita-organov-sluha-34503/"
    },
    {
      "root": "Unknown",
      "name": "Защита рук",
      "url": "https://www.ozon.ru/category/zashchita-ruk-34502/"
    },
    {
      "root": "Unknown",
      "name": "Защита ног",
      "url": "https://www.ozon.ru/category/zashchita-nog-34971/"
    },
    {
      "root": "Unknown",
      "name": "Каски строительные",
      "url": "https://www.ozon.ru/category/stroitelnye-kaski-10195/"
    },
    {
      "root": "Unknown",
      "name": "Химзащита",
      "url": "https://www.ozon.ru/category/odezhda-dlya-himzashchity-33158/"
    },
    {
      "root": "Unknown",
      "name": "Страховка на высоте",
      "url": "https://www.ozon.ru/category/strahovochnye-poyasa-10197/"
    },
    {
      "root": "Unknown",
      "name": "Пожарное оборудование",
      "url": "https://www.ozon.ru/category/pozharnoe-oborudovanie-34992/"
    },
    {
      "root": "Unknown",
      "name": "Аварийные ограждения",
      "url": "https://www.ozon.ru/category/signalnye-lenty-9785/"
    },
    {
      "root": "Unknown",
      "name": "Силовая техника и оборудование",
      "url": "https://www.ozon.ru/category/silovaya-tehnika-i-oborudovanie-31810/"
    },
    {
      "root": "Unknown",
      "name": "Электрогенераторы",
      "url": "https://www.ozon.ru/category/elektrogeneratory-9834/"
    },
    {
      "root": "Unknown",
      "name": "Станки",
      "url": "https://www.ozon.ru/category/stanki-31811/"
    },
    {
      "root": "Unknown",
      "name": "Частотные преобразователи",
      "url": "https://www.ozon.ru/category/preobrazovateli-chastoty-9835/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие для ЧПУ",
      "url": "https://www.ozon.ru/category/komplektuyushchie-dlya-chpu-36215/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для клининга",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-klininga-38269/"
    },
    {
      "root": "Unknown",
      "name": "Бетономешалки и растворосмесители",
      "url": "https://www.ozon.ru/category/betonosmesiteli-10411/"
    },
    {
      "root": "Unknown",
      "name": "Виброоборудование",
      "url": "https://www.ozon.ru/category/vibrooborudovanie-38397/"
    },
    {
      "root": "Unknown",
      "name": "Малая строительная техника",
      "url": "https://www.ozon.ru/category/malaya-stroitelnaya-tehnika-9883/"
    },
    {
      "root": "Unknown",
      "name": "Малярно-отделочное оборудование",
      "url": "https://www.ozon.ru/category/malyarno-otdelochnoe-oborudovanie-39514/"
    },
    {
      "root": "Unknown",
      "name": "Промышленные электродвигатели",
      "url": "https://www.ozon.ru/category/promyshlennye-elektrodvigateli-35627/"
    },
    {
      "root": "Unknown",
      "name": "Промышленные насосы",
      "url": "https://www.ozon.ru/category/promyshlennye-nasosy-33801/"
    },
    {
      "root": "Unknown",
      "name": "Промышленное оборудование и комплектующие",
      "url": "https://www.ozon.ru/category/komplektuyushchie-dlya-promyshlennogo-oborudovaniya-37420/"
    },
    {
      "root": "Unknown",
      "name": "Сауны и бани",
      "url": "https://www.ozon.ru/category/sauny-i-bani-10338/"
    },
    {
      "root": "Unknown",
      "name": "Дровяные печи",
      "url": "https://www.ozon.ru/category/drovyanye-pechi-10341/"
    },
    {
      "root": "Unknown",
      "name": "Электрокаменки",
      "url": "https://www.ozon.ru/category/elektrokamenki-34247/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-saun-i-ban-10346/"
    },
    {
      "root": "Unknown",
      "name": "Камни",
      "url": "https://www.ozon.ru/category/kamni-dlya-bani-38379/"
    },
    {
      "root": "Unknown",
      "name": "Двери",
      "url": "https://www.ozon.ru/category/dveri-dlya-sauny-i-bani-39239/"
    },
    {
      "root": "Unknown",
      "name": "Дома, бани и гаражи",
      "url": "https://www.ozon.ru/category/gotovye-doma-bani-i-garazhi-37598/"
    },
    {
      "root": "Unknown",
      "name": "Проекты",
      "url": "https://www.ozon.ru/category/gotovye-proekty-domov-31436/"
    },
    {
      "root": "Unknown",
      "name": "Дома",
      "url": "https://www.ozon.ru/category/gotovye-doma-37599/"
    },
    {
      "root": "Unknown",
      "name": "Гаражи",
      "url": "https://www.ozon.ru/category/garazhi-37600/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 174,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Чай, кофе и какао",
      "url": "https://www.ozon.ru/category/chay-kofe-kakao-9370/"
    },
    {
      "root": "Unknown",
      "name": "Кофе",
      "url": "https://www.ozon.ru/category/kofe-9372/"
    },
    {
      "root": "Unknown",
      "name": "Чай",
      "url": "https://www.ozon.ru/category/chay-9373/"
    },
    {
      "root": "Unknown",
      "name": "Какао и горячий шоколад",
      "url": "https://www.ozon.ru/category/kakao-goryachiy-shokolad-9371/"
    },
    {
      "root": "Unknown",
      "name": "Цикорий и кэроб",
      "url": "https://www.ozon.ru/category/tsikoriy-kerob-9374/"
    },
    {
      "root": "Unknown",
      "name": "Кофейные напитки",
      "url": "https://www.ozon.ru/category/kofeynye-napitki-9493/"
    },
    {
      "root": "Unknown",
      "name": "Фильтры для заваривания чая",
      "url": "https://www.ozon.ru/category/filtry-dlya-zavarivaniya-chaya-1588/"
    },
    {
      "root": "Unknown",
      "name": "Выпечка и сладости",
      "url": "https://www.ozon.ru/category/konditerskie-izdeliya-9378/"
    },
    {
      "root": "Unknown",
      "name": "Конфеты",
      "url": "https://www.ozon.ru/category/konfety-30695/"
    },
    {
      "root": "Unknown",
      "name": "Мармелад",
      "url": "https://www.ozon.ru/category/marmelad-9390/"
    },
    {
      "root": "Unknown",
      "name": "Шоколад и шоколадные батончики",
      "url": "https://www.ozon.ru/category/shokolad-i-shokoladnye-batonchiki-9393/"
    },
    {
      "root": "Unknown",
      "name": "Шоколадная и ореховая пасты",
      "url": "https://www.ozon.ru/category/shokoladnaya-i-orehovaya-pasty-9397/"
    },
    {
      "root": "Unknown",
      "name": "Печенье, пряники и вафли",
      "url": "https://www.ozon.ru/category/pechene-pryaniki-i-vafli-9381/"
    },
    {
      "root": "Unknown",
      "name": "Выпечка и сдоба",
      "url": "https://www.ozon.ru/category/vypechka-i-sdoba-9376/"
    },
    {
      "root": "Unknown",
      "name": "Зефир и пастила",
      "url": "https://www.ozon.ru/category/zefir-pastila-9388/"
    },
    {
      "root": "Unknown",
      "name": "Восточные сладости",
      "url": "https://www.ozon.ru/category/vostochnye-sladosti-nuga-9379/"
    },
    {
      "root": "Unknown",
      "name": "Жевательная резинка",
      "url": "https://www.ozon.ru/category/zhevatelnaya-rezinka-9380/"
    },
    {
      "root": "Unknown",
      "name": "Торты и пирожные",
      "url": "https://www.ozon.ru/category/torty-i-pirozhnye-39097/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные наборы",
      "url": "https://www.ozon.ru/category/podarochnye-nabory-konfet-9394/"
    },
    {
      "root": "Unknown",
      "name": "Хлеб, лаваши и лепешки",
      "url": "https://www.ozon.ru/category/hleb-lavashi-lepeshki-9377/"
    },
    {
      "root": "Unknown",
      "name": "Соки, воды и напитки",
      "url": "https://www.ozon.ru/category/soki-vody-napitki-9467/"
    },
    {
      "root": "Unknown",
      "name": "Вода",
      "url": "https://www.ozon.ru/category/voda-pitevaya-i-mineralnaya-9468/"
    },
    {
      "root": "Unknown",
      "name": "Лимонады и газированные напитки",
      "url": "https://www.ozon.ru/category/limonady-i-gazirovannye-napitki-9470/"
    },
    {
      "root": "Unknown",
      "name": "Соки и нектары",
      "url": "https://www.ozon.ru/category/soki-nektary-morsy-9471/"
    },
    {
      "root": "Unknown",
      "name": "Энергетические напитки",
      "url": "https://www.ozon.ru/category/energeticheskie-napitki-9473/"
    },
    {
      "root": "Unknown",
      "name": "Квас",
      "url": "https://www.ozon.ru/category/kvas-9469/"
    },
    {
      "root": "Unknown",
      "name": "Холодный чай и кофе",
      "url": "https://www.ozon.ru/category/holodnyy-chay-9472/"
    },
    {
      "root": "Unknown",
      "name": "Компоты, морсы и кисели",
      "url": "https://www.ozon.ru/category/kiseli-39264/"
    },
    {
      "root": "Unknown",
      "name": "Безалкогольное пиво, вино и шампанское",
      "url": "https://www.ozon.ru/category/bezalkogolnoe-pivo-vina-i-shampanskoe-1687/"
    },
    {
      "root": "Unknown",
      "name": "Растворимые напитки",
      "url": "https://www.ozon.ru/category/rastvorimye-napitki-31644/"
    },
    {
      "root": "Unknown",
      "name": "Орехи и снеки",
      "url": "https://www.ozon.ru/category/sneki-suhariki-chipsy-9355/"
    },
    {
      "root": "Unknown",
      "name": "Орехи",
      "url": "https://www.ozon.ru/category/orehi-31485/"
    },
    {
      "root": "Unknown",
      "name": "Сухофрукты и цукаты",
      "url": "https://www.ozon.ru/category/suhofrukty-31486/"
    },
    {
      "root": "Unknown",
      "name": "Смеси сухофруктов и орехов",
      "url": "https://www.ozon.ru/category/smesi-suhofruktov-i-orehov-32041/"
    },
    {
      "root": "Unknown",
      "name": "Снеки и закуски",
      "url": "https://www.ozon.ru/category/sneki-zakuski-9358/"
    },
    {
      "root": "Unknown",
      "name": "Батончики",
      "url": "https://www.ozon.ru/category/batonchiki-i-myusli-9356/"
    },
    {
      "root": "Unknown",
      "name": "Батончики спортивные",
      "url": "https://www.ozon.ru/category/batonchiki-sportivnye-38920/"
    },
    {
      "root": "Unknown",
      "name": "Сушеная и вяленая рыба",
      "url": "https://www.ozon.ru/category/sushenaya-i-vyalenaya-ryba-9322/"
    },
    {
      "root": "Unknown",
      "name": "Хлебцы и соломка",
      "url": "https://www.ozon.ru/category/hlebtsy-9359/"
    },
    {
      "root": "Unknown",
      "name": "Семечки",
      "url": "https://www.ozon.ru/category/semechki-30157/"
    },
    {
      "root": "Unknown",
      "name": "Суперфудс",
      "url": "https://www.ozon.ru/category/superfuds-1617/"
    },
    {
      "root": "Unknown",
      "name": "Молочные продукты, сыры и яйца",
      "url": "https://www.ozon.ru/category/moloko-syr-yaytsa-9276/"
    },
    {
      "root": "Unknown",
      "name": "Сыр и сырные продукты",
      "url": "https://www.ozon.ru/category/syr-i-syrnye-produkty-9289/"
    },
    {
      "root": "Unknown",
      "name": "Молоко",
      "url": "https://www.ozon.ru/category/moloko-9283/"
    },
    {
      "root": "Unknown",
      "name": "Сливки",
      "url": "https://www.ozon.ru/category/slivki-9284/"
    },
    {
      "root": "Unknown",
      "name": "Растительные продукты",
      "url": "https://www.ozon.ru/category/rastitelnoe-moloko-30844/"
    },
    {
      "root": "Unknown",
      "name": "Яйца",
      "url": "https://www.ozon.ru/category/yaytsa-9290/"
    },
    {
      "root": "Unknown",
      "name": "Закваски",
      "url": "https://www.ozon.ru/category/zakvaski-9292/"
    },
    {
      "root": "Unknown",
      "name": "Творог",
      "url": "https://www.ozon.ru/category/tvorog-i-tvorozhnye-produkty-9278/"
    },
    {
      "root": "Unknown",
      "name": "Масло, маргарин и спред",
      "url": "https://www.ozon.ru/category/maslo-margarin-spred-9287/"
    },
    {
      "root": "Unknown",
      "name": "Сгущённое молоко",
      "url": "https://www.ozon.ru/category/molochnye-konservy-9291/"
    },
    {
      "root": "Unknown",
      "name": "Йогурты, творожки и пудинги",
      "url": "https://www.ozon.ru/category/yogurty-9277/"
    },
    {
      "root": "Unknown",
      "name": "Питьевые йогурты и молочные напитки",
      "url": "https://www.ozon.ru/category/molochnye-napitki-9285/"
    },
    {
      "root": "Unknown",
      "name": "Бисквиты, десерты и сырки",
      "url": "https://www.ozon.ru/category/deserty-pudingi-kremy-zhele-9435/"
    },
    {
      "root": "Unknown",
      "name": "Сметана",
      "url": "https://www.ozon.ru/category/smetana-9288/"
    },
    {
      "root": "Unknown",
      "name": "Майонез",
      "url": "https://www.ozon.ru/category/mayonez-9286/"
    },
    {
      "root": "Unknown",
      "name": "Кефир, биолакт и ацидофилин",
      "url": "https://www.ozon.ru/category/kefir-bifidok-atsidofilin-9280/"
    },
    {
      "root": "Unknown",
      "name": "Ряженка, варенец и простокваша",
      "url": "https://www.ozon.ru/category/ryazhenka-varenets-prostokvasha-9282/"
    },
    {
      "root": "Unknown",
      "name": "Тан и айран",
      "url": "https://www.ozon.ru/category/tan-ayran-9476/"
    },
    {
      "root": "Unknown",
      "name": "Кумыс, катык и мацони",
      "url": "https://www.ozon.ru/category/kumys-katyk-matsoni-9281/"
    },
    {
      "root": "Unknown",
      "name": "Масла, соусы и специи",
      "url": "https://www.ozon.ru/category/masla-sousy-spetsii-30701/"
    },
    {
      "root": "Unknown",
      "name": "Специи, семена и сушеные овощи",
      "url": "https://www.ozon.ru/category/spetsii-pripravy-i-pryanosti-9411/"
    },
    {
      "root": "Unknown",
      "name": "Добавки для приготовления блюд",
      "url": "https://www.ozon.ru/category/spetsii-i-dobavki-9399/"
    },
    {
      "root": "Unknown",
      "name": "Сиропы и топпинги",
      "url": "https://www.ozon.ru/category/siropy-i-toppingi-9412/"
    },
    {
      "root": "Unknown",
      "name": "Соусы",
      "url": "https://www.ozon.ru/category/sousy-9368/"
    },
    {
      "root": "Unknown",
      "name": "Масла",
      "url": "https://www.ozon.ru/category/masla-9354/"
    },
    {
      "root": "Unknown",
      "name": "Сахар",
      "url": "https://www.ozon.ru/category/sahar-9401/"
    },
    {
      "root": "Unknown",
      "name": "Соль",
      "url": "https://www.ozon.ru/category/sol-9403/"
    },
    {
      "root": "Unknown",
      "name": "Макароны, крупы и мука",
      "url": "https://www.ozon.ru/category/makarony-krupy-muka-30699/"
    },
    {
      "root": "Unknown",
      "name": "Макаронные изделия",
      "url": "https://www.ozon.ru/category/makaronnye-izdeliya-9353/"
    },
    {
      "root": "Unknown",
      "name": "Мука",
      "url": "https://www.ozon.ru/category/muka-9351/"
    },
    {
      "root": "Unknown",
      "name": "Блюда быстрого приготовления",
      "url": "https://www.ozon.ru/category/blyuda-bystrogo-prigotovleniya-9327/"
    },
    {
      "root": "Unknown",
      "name": "Крупы",
      "url": "https://www.ozon.ru/category/krupy-35647/"
    },
    {
      "root": "Unknown",
      "name": "Бобовые",
      "url": "https://www.ozon.ru/category/bobovye-35648/"
    },
    {
      "root": "Unknown",
      "name": "Хлопья",
      "url": "https://www.ozon.ru/category/hlopya-35652/"
    },
    {
      "root": "Unknown",
      "name": "Смеси для супов и гарниров",
      "url": "https://www.ozon.ru/category/smesi-dlya-supov-i-garnirov-9349/"
    },
    {
      "root": "Unknown",
      "name": "Зерна для проращивания",
      "url": "https://www.ozon.ru/category/zerna-dlya-prorashchivaniya-9338/"
    },
    {
      "root": "Unknown",
      "name": "Консервация",
      "url": "https://www.ozon.ru/category/konservatsiya-9413/"
    },
    {
      "root": "Unknown",
      "name": "Мед и варенья",
      "url": "https://www.ozon.ru/category/med-i-varenya-9432/"
    },
    {
      "root": "Unknown",
      "name": "Овощи консервированные",
      "url": "https://www.ozon.ru/category/ovoshchi-konservirovannye-9423/"
    },
    {
      "root": "Unknown",
      "name": "Мясные консервы",
      "url": "https://www.ozon.ru/category/myasnye-konservy-9414/"
    },
    {
      "root": "Unknown",
      "name": "Рыбные консервы",
      "url": "https://www.ozon.ru/category/rybnye-konservy-9418/"
    },
    {
      "root": "Unknown",
      "name": "Грибы консервированные",
      "url": "https://www.ozon.ru/category/griby-konservirovannye-9424/"
    },
    {
      "root": "Unknown",
      "name": "Паштеты и холодцы",
      "url": "https://www.ozon.ru/category/pashtety-holodtsy-zeltsy-9315/"
    },
    {
      "root": "Unknown",
      "name": "Фруктовые консервы",
      "url": "https://www.ozon.ru/category/fruktovye-konservy-9430/"
    },
    {
      "root": "Unknown",
      "name": "Сухие пайки",
      "url": "https://www.ozon.ru/category/suhie-payki-30516/"
    },
    {
      "root": "Unknown",
      "name": "Готовые блюда",
      "url": "https://www.ozon.ru/category/blyuda-gotovye-konservirovannye-9415/"
    },
    {
      "root": "Unknown",
      "name": "Соленья и квашения",
      "url": "https://www.ozon.ru/category/solenya-kvasheniya-9436/"
    },
    {
      "root": "Unknown",
      "name": "Замороженные продукты",
      "url": "https://www.ozon.ru/category/zamorozhennye-produkty-9437/"
    },
    {
      "root": "Unknown",
      "name": "Мороженое и десерты",
      "url": "https://www.ozon.ru/category/morozhenoe-deserty-9464/"
    },
    {
      "root": "Unknown",
      "name": "Овощи, фрукты, ягоды",
      "url": "https://www.ozon.ru/category/ovoshchi-frukty-yagody-9438/"
    },
    {
      "root": "Unknown",
      "name": "Полуфабрикаты",
      "url": "https://www.ozon.ru/category/zamorozhennye-polufabrikaty-9443/"
    },
    {
      "root": "Unknown",
      "name": "Готовые блюда",
      "url": "https://www.ozon.ru/category/zamorozhennye-gotovye-blyuda-30133/"
    },
    {
      "root": "Unknown",
      "name": "Морепродукты",
      "url": "https://www.ozon.ru/category/zamorozhennye-moreprodukty-9442/"
    },
    {
      "root": "Unknown",
      "name": "Рыба",
      "url": "https://www.ozon.ru/category/zamorozhennaya-ryba-32037/"
    },
    {
      "root": "Unknown",
      "name": "Мясо",
      "url": "https://www.ozon.ru/category/zamorozhennoe-myaso-32038/"
    },
    {
      "root": "Unknown",
      "name": "Птица",
      "url": "https://www.ozon.ru/category/zamorozhennaya-ptitsa-32039/"
    },
    {
      "root": "Unknown",
      "name": "Субпродукты",
      "url": "https://www.ozon.ru/category/zamorozhennye-subprodukty-32040/"
    },
    {
      "root": "Unknown",
      "name": "Тесто, хлеб, выпечка",
      "url": "https://www.ozon.ru/category/testo-osnova-dlya-pitstsy-9462/"
    },
    {
      "root": "Unknown",
      "name": "Лёд",
      "url": "https://www.ozon.ru/category/led-pishchevoy-36909/"
    },
    {
      "root": "Unknown",
      "name": "Мясо и птица",
      "url": "https://www.ozon.ru/category/myaso-i-ptitsa-9293/"
    },
    {
      "root": "Unknown",
      "name": "Курица",
      "url": "https://www.ozon.ru/category/kuritsa-9297/"
    },
    {
      "root": "Unknown",
      "name": "Индейка",
      "url": "https://www.ozon.ru/category/indeyka-9298/"
    },
    {
      "root": "Unknown",
      "name": "Говядина",
      "url": "https://www.ozon.ru/category/govyadina-9294/"
    },
    {
      "root": "Unknown",
      "name": "Свинина",
      "url": "https://www.ozon.ru/category/svinina-9295/"
    },
    {
      "root": "Unknown",
      "name": "Баранина",
      "url": "https://www.ozon.ru/category/baranina-9296/"
    },
    {
      "root": "Unknown",
      "name": "Телятина, ягнятина и кролик",
      "url": "https://www.ozon.ru/category/telyatina-yagnyatina-krolik-9299/"
    },
    {
      "root": "Unknown",
      "name": "Субпродукты",
      "url": "https://www.ozon.ru/category/subprodukty-9300/"
    },
    {
      "root": "Unknown",
      "name": "Фарш и полуфабрикаты",
      "url": "https://www.ozon.ru/category/farsh-polufabrikaty-9302/"
    },
    {
      "root": "Unknown",
      "name": "Соевое и растительное мясо",
      "url": "https://www.ozon.ru/category/soevoe-myaso-31936/"
    },
    {
      "root": "Unknown",
      "name": "Рыба и морепродукты",
      "url": "https://www.ozon.ru/category/ryba-moreprodukty-9317/"
    },
    {
      "root": "Unknown",
      "name": "Соленая и копченая рыба",
      "url": "https://www.ozon.ru/category/solenaya-i-kopchenaya-ryba-9321/"
    },
    {
      "root": "Unknown",
      "name": "Рыба",
      "url": "https://www.ozon.ru/category/ryba-9318/"
    },
    {
      "root": "Unknown",
      "name": "Пресервы рыбные",
      "url": "https://www.ozon.ru/category/preservy-32042/"
    },
    {
      "root": "Unknown",
      "name": "Икра",
      "url": "https://www.ozon.ru/category/ikra-9320/"
    },
    {
      "root": "Unknown",
      "name": "Крабовое мясо и палочки",
      "url": "https://www.ozon.ru/category/krabovoe-myaso-i-palochki-9323/"
    },
    {
      "root": "Unknown",
      "name": "Морепродукты",
      "url": "https://www.ozon.ru/category/moreprodukty-9325/"
    },
    {
      "root": "Unknown",
      "name": "Морские водоросли",
      "url": "https://www.ozon.ru/category/morskie-vodorosli-9499/"
    },
    {
      "root": "Unknown",
      "name": "Колбасы, сосиски и деликатесы",
      "url": "https://www.ozon.ru/category/kolbasy-sosiski-delikatesy-9312/"
    },
    {
      "root": "Unknown",
      "name": "Колбасы",
      "url": "https://www.ozon.ru/category/kolbasy-9314/"
    },
    {
      "root": "Unknown",
      "name": "Сосиски, сардельки и колбаски для гриля",
      "url": "https://www.ozon.ru/category/sosiski-sardelki-kolbaski-dlya-grilya-9316/"
    },
    {
      "root": "Unknown",
      "name": "Деликатесы мясные и копчености",
      "url": "https://www.ozon.ru/category/delikatesy-kopchenosti-9313/"
    },
    {
      "root": "Unknown",
      "name": "Ветчина",
      "url": "https://www.ozon.ru/category/vetchina-i-rulety-9512/"
    },
    {
      "root": "Unknown",
      "name": "Бекон и сало",
      "url": "https://www.ozon.ru/category/shpik-i-bekon-9513/"
    },
    {
      "root": "Unknown",
      "name": "Овощи, фрукты и зелень",
      "url": "https://www.ozon.ru/category/ovoshchi-frukty-zelen-9201/"
    },
    {
      "root": "Unknown",
      "name": "Овощи",
      "url": "https://www.ozon.ru/category/ovoshchi-9202/"
    },
    {
      "root": "Unknown",
      "name": "Зелень, салатные смеси",
      "url": "https://www.ozon.ru/category/zelen-salatnye-smesi-9247/"
    },
    {
      "root": "Unknown",
      "name": "Грибы",
      "url": "https://www.ozon.ru/category/griby-9253/"
    },
    {
      "root": "Unknown",
      "name": "Фрукты",
      "url": "https://www.ozon.ru/category/frukty-9230/"
    },
    {
      "root": "Unknown",
      "name": "Ягоды",
      "url": "https://www.ozon.ru/category/yagody-9254/"
    },
    {
      "root": "Unknown",
      "name": "Фруктово-овощные наборы",
      "url": "https://www.ozon.ru/category/fruktovo-ovoshchnye-nabory-34104/"
    },
    {
      "root": "Unknown",
      "name": "Готовые блюда",
      "url": "https://www.ozon.ru/category/gotovye-blyuda-9521/"
    },
    {
      "root": "Unknown",
      "name": "Завтраки",
      "url": "https://www.ozon.ru/category/zavtraki-34428/"
    },
    {
      "root": "Unknown",
      "name": "Вторые блюда",
      "url": "https://www.ozon.ru/category/vtorye-blyuda-34431/"
    },
    {
      "root": "Unknown",
      "name": "Супы",
      "url": "https://www.ozon.ru/category/supy-34430/"
    },
    {
      "root": "Unknown",
      "name": "Салаты",
      "url": "https://www.ozon.ru/category/salaty-39077/"
    },
    {
      "root": "Unknown",
      "name": "Закуски",
      "url": "https://www.ozon.ru/category/salaty-i-zakuski-34429/"
    },
    {
      "root": "Unknown",
      "name": "Бургеры, сэндвичи",
      "url": "https://www.ozon.ru/category/burgery-sendvichi-ohlazhdennye-34498/"
    },
    {
      "root": "Unknown",
      "name": "Тесто и полуфабрикаты",
      "url": "https://www.ozon.ru/category/testo-9459/"
    },
    {
      "root": "Unknown",
      "name": "Сухие завтраки, мюсли и каши",
      "url": "https://www.ozon.ru/category/gotovye-zavtraki-i-kashi-9328/"
    },
    {
      "root": "Unknown",
      "name": "Каши",
      "url": "https://www.ozon.ru/category/kashi-9330/"
    },
    {
      "root": "Unknown",
      "name": "Сухие завтраки",
      "url": "https://www.ozon.ru/category/gotovye-zavtraki-9329/"
    },
    {
      "root": "Unknown",
      "name": "Мюсли и гранола",
      "url": "https://www.ozon.ru/category/myusli-i-granola-9331/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 158,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Лекарственные средства",
      "url": "https://www.ozon.ru/category/lekarstvennye-sredstva-30000/"
    },
    {
      "root": "Unknown",
      "name": "При простуде и гриппе",
      "url": "https://www.ozon.ru/category/prostuda-gripp-30006/"
    },
    {
      "root": "Unknown",
      "name": "Иммуностимуляторы",
      "url": "https://www.ozon.ru/category/immunitet-30015/"
    },
    {
      "root": "Unknown",
      "name": "Желудок, кишечник, печень",
      "url": "https://www.ozon.ru/category/zheludok-kishechnik-pechen-30032/"
    },
    {
      "root": "Unknown",
      "name": "Препараты при дерматологических нарушениях",
      "url": "https://www.ozon.ru/category/kozha-volosy-nogti-32097/"
    },
    {
      "root": "Unknown",
      "name": "При нарушениях опорно-двигательного аппарата",
      "url": "https://www.ozon.ru/category/lekarstva-ot-bolezni-sustavov-30103/"
    },
    {
      "root": "Unknown",
      "name": "Сердечно-сосудистые",
      "url": "https://www.ozon.ru/category/serdechno-sosudistye-zabolevaniya-30007/"
    },
    {
      "root": "Unknown",
      "name": "При неврологических нарушениях",
      "url": "https://www.ozon.ru/category/nevrologiya-30081/"
    },
    {
      "root": "Unknown",
      "name": "Препараты при аллергии",
      "url": "https://www.ozon.ru/category/lekarstva-ot-allergii-30014/"
    },
    {
      "root": "Unknown",
      "name": "При нарушении обмена веществ",
      "url": "https://www.ozon.ru/category/narushenie-obmena-veshchestv-6118/"
    },
    {
      "root": "Unknown",
      "name": "Витаминные препараты",
      "url": "https://www.ozon.ru/category/vitaminnye-preparaty-35301/"
    },
    {
      "root": "Unknown",
      "name": "При воспалениях и инфекциях",
      "url": "https://www.ozon.ru/category/vospalenie-i-infektsii-30435/"
    },
    {
      "root": "Unknown",
      "name": "При курении и алкоголизме",
      "url": "https://www.ozon.ru/category/vrednye-privychki-6134/"
    },
    {
      "root": "Unknown",
      "name": "При гинекологических нарушениях",
      "url": "https://www.ozon.ru/category/akusherstvo-i-ginekologiya-30048/"
    },
    {
      "root": "Unknown",
      "name": "Болеутоляющие",
      "url": "https://www.ozon.ru/category/boleutolyayushchie-preparaty-30002/"
    },
    {
      "root": "Unknown",
      "name": "При нарушениях мочеполовой системы",
      "url": "https://www.ozon.ru/category/mochepolovaya-sistema-30044/"
    },
    {
      "root": "Unknown",
      "name": "При нарушениях работы зрения",
      "url": "https://www.ozon.ru/category/lekarstva-dlya-glaz-30063/"
    },
    {
      "root": "Unknown",
      "name": "При гормональных нарушениях",
      "url": "https://www.ozon.ru/category/endokrinologiya-30096/"
    },
    {
      "root": "Unknown",
      "name": "Для зубов и десен",
      "url": "https://www.ozon.ru/category/stomatologiya-30062/"
    },
    {
      "root": "Unknown",
      "name": "Препараты при бронхиальной астме",
      "url": "https://www.ozon.ru/category/bronhialnaya-astma-30025/"
    },
    {
      "root": "Unknown",
      "name": "Препараты при онкологии",
      "url": "https://www.ozon.ru/category/lekarstvennye-sredstva-pri-onkologii-39585/"
    },
    {
      "root": "Unknown",
      "name": "Витамины и БАДы",
      "url": "https://www.ozon.ru/category/vitaminy-bady-i-pishchevye-dobavki-6164/"
    },
    {
      "root": "Unknown",
      "name": "БАД",
      "url": "https://www.ozon.ru/category/bady-6183/"
    },
    {
      "root": "Unknown",
      "name": "Витамины и витаминно-минеральные комплексы",
      "url": "https://www.ozon.ru/category/vitaminy-i-vitaminnye-kompleksy-6166/"
    },
    {
      "root": "Unknown",
      "name": "Парафармацевтика",
      "url": "https://www.ozon.ru/category/parafarmatsevticheskie-sredstva-39537/"
    },
    {
      "root": "Unknown",
      "name": "Лечебные средства",
      "url": "https://www.ozon.ru/category/gomeopatiya-6162/"
    },
    {
      "root": "Unknown",
      "name": "Средства профилактики",
      "url": "https://www.ozon.ru/category/uho-gorlo-nos-30021/"
    },
    {
      "root": "Unknown",
      "name": "Диабетические товары",
      "url": "https://www.ozon.ru/category/diabet-30069/"
    },
    {
      "root": "Unknown",
      "name": "Комплексные пищевые добавки",
      "url": "https://www.ozon.ru/category/kompleksnye-pishchevye-dobavki-38313/"
    },
    {
      "root": "Unknown",
      "name": "Специализированное питание",
      "url": "https://www.ozon.ru/category/spetsializirovannoe-pitanie-30938/"
    },
    {
      "root": "Unknown",
      "name": "Дыхательные смеси",
      "url": "https://www.ozon.ru/category/dyhatelnye-smesi-6198/"
    },
    {
      "root": "Unknown",
      "name": "Оптика",
      "url": "https://www.ozon.ru/category/linzy-ochki-aksessuary-6295/"
    },
    {
      "root": "Unknown",
      "name": "Контактные линзы",
      "url": "https://www.ozon.ru/category/kontaktnye-linzy-i-aksessuary-6296/"
    },
    {
      "root": "Unknown",
      "name": "Растворы для линз",
      "url": "https://www.ozon.ru/category/rastvory-dlya-linz-6300/"
    },
    {
      "root": "Unknown",
      "name": "Линзы для очков",
      "url": "https://www.ozon.ru/category/komplektuyushchie-dlya-ochkov-38607/"
    },
    {
      "root": "Unknown",
      "name": "Оправы для очков",
      "url": "https://www.ozon.ru/category/opravy-dlya-ochkov-39942/"
    },
    {
      "root": "Unknown",
      "name": "Очки для зрения",
      "url": "https://www.ozon.ru/category/ochki-dlya-zreniya-6303/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и комплектующие для линз и очков",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-linz-6302/"
    },
    {
      "root": "Unknown",
      "name": "Капли для глаз",
      "url": "https://www.ozon.ru/category/uvlazhnyayushchie-kapli-6301/"
    },
    {
      "root": "Unknown",
      "name": "Медицинские приборы",
      "url": "https://www.ozon.ru/category/meditsinskie-pribory-6254/"
    },
    {
      "root": "Unknown",
      "name": "Тонометры, пульсоксиметры и термометры",
      "url": "https://www.ozon.ru/category/tonometry-6261/"
    },
    {
      "root": "Unknown",
      "name": "Стетоскопы",
      "url": "https://www.ozon.ru/category/stetoskopy-6241/"
    },
    {
      "root": "Unknown",
      "name": "Термометры медицинские",
      "url": "https://www.ozon.ru/category/termometry-meditsinskie-6260/"
    },
    {
      "root": "Unknown",
      "name": "Глюкометры и анализаторы",
      "url": "https://www.ozon.ru/category/glyukometry-i-analizatory-krovi-6257/"
    },
    {
      "root": "Unknown",
      "name": "Инфузионные и инсулиновые помпы",
      "url": "https://www.ozon.ru/category/insulinovye-pompy-i-aksessuary-31457/"
    },
    {
      "root": "Unknown",
      "name": "Ингаляторы, устройства от насморка и аллергии",
      "url": "https://www.ozon.ru/category/ingalyatory-i-aksessuary-35039/"
    },
    {
      "root": "Unknown",
      "name": "Слуховые аппараты и усилители звука",
      "url": "https://www.ozon.ru/category/sluhovye-apparaty-30987/"
    },
    {
      "root": "Unknown",
      "name": "Кварцевые лампы, рециркуляторы и облучатели",
      "url": "https://www.ozon.ru/category/kvartsevye-lampy-6268/"
    },
    {
      "root": "Unknown",
      "name": "Концентраторы кислорода",
      "url": "https://www.ozon.ru/category/kontsentratory-kisloroda-34271/"
    },
    {
      "root": "Unknown",
      "name": "Активаторы воды",
      "url": "https://www.ozon.ru/category/aktivatory-vody-6262/"
    },
    {
      "root": "Unknown",
      "name": "Стерилизаторы и дезинфекторы",
      "url": "https://www.ozon.ru/category/sterilizatory-6279/"
    },
    {
      "root": "Unknown",
      "name": "Очки, осветители и рефлекторы",
      "url": "https://www.ozon.ru/category/osvetiteli-i-reflektory-meditsinskie-31329/"
    },
    {
      "root": "Unknown",
      "name": "Приборы для контроля сна, антихрап",
      "url": "https://www.ozon.ru/category/pribory-dlya-kontrolya-sna-38583/"
    },
    {
      "root": "Unknown",
      "name": "Нейростимуляторы",
      "url": "https://www.ozon.ru/category/neyrostimulyatory-30976/"
    },
    {
      "root": "Unknown",
      "name": "Свинг-машины",
      "url": "https://www.ozon.ru/category/sving-mashiny-6274/"
    },
    {
      "root": "Unknown",
      "name": "Медицинское оборудование",
      "url": "https://www.ozon.ru/category/professionalnoe-meditsinskoe-oborudovanie-37654/"
    },
    {
      "root": "Unknown",
      "name": "Медицинский осмотр",
      "url": "https://www.ozon.ru/category/apparaty-dlya-provedeniya-meditsinskogo-osmotra-39185/"
    },
    {
      "root": "Unknown",
      "name": "Лабораторное оборудование и материалы",
      "url": "https://www.ozon.ru/category/laboratornoe-oborudovanie-i-materialy-37238/"
    },
    {
      "root": "Unknown",
      "name": "Для ортодонтии и стоматологии",
      "url": "https://www.ozon.ru/category/ortodonticheskie-pribory-39603/"
    },
    {
      "root": "Unknown",
      "name": "Для физиотерапии",
      "url": "https://www.ozon.ru/category/fizioterapevticheskie-apparaty-6278/"
    },
    {
      "root": "Unknown",
      "name": "Учебное медицинское оборудование",
      "url": "https://www.ozon.ru/category/uchebnoe-meditsinskoe-oborudovanie-38948/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и комплектующие",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-meditsinskoy-tehniki-i-priborov-39853/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-meditsinskoy-tehniki-6280/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие",
      "url": "https://www.ozon.ru/category/komplektuyushchie-dlya-meditsinskoy-tehniki-39918/"
    },
    {
      "root": "Unknown",
      "name": "Медицинские изделия и расходные материалы",
      "url": "https://www.ozon.ru/category/meditsinskie-izdeliya-6209/"
    },
    {
      "root": "Unknown",
      "name": "Контейнеры для анализов и пакеты для стерилизации",
      "url": "https://www.ozon.ru/category/konteynery-dlya-analizov-30511/"
    },
    {
      "root": "Unknown",
      "name": "Кровоостанавливающие средства",
      "url": "https://www.ozon.ru/category/krovoostanavlivayushchie-gubki-30670/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки, маски, бахилы и шапочки",
      "url": "https://www.ozon.ru/category/perchatki-meditsinskie-6212/"
    },
    {
      "root": "Unknown",
      "name": "Перевязочные материалы",
      "url": "https://www.ozon.ru/category/perevyazochnye-materialy-35152/"
    },
    {
      "root": "Unknown",
      "name": "Пипетки, дозаторы, спринцовки и клизмы",
      "url": "https://www.ozon.ru/category/sprintsovki-6242/"
    },
    {
      "root": "Unknown",
      "name": "Пессарии и уринаторы",
      "url": "https://www.ozon.ru/category/pessarii-30912/"
    },
    {
      "root": "Unknown",
      "name": "Шприцы, иглы и инъекторы",
      "url": "https://www.ozon.ru/category/shpritsy-6214/"
    },
    {
      "root": "Unknown",
      "name": "Таблетницы",
      "url": "https://www.ozon.ru/category/konteynery-dlya-tabletok-6362/"
    },
    {
      "root": "Unknown",
      "name": "Аптечки",
      "url": "https://www.ozon.ru/category/aptechki-6215/"
    },
    {
      "root": "Unknown",
      "name": "Диагностические тесты",
      "url": "https://www.ozon.ru/category/diagnosticheskie-testy-6239/"
    },
    {
      "root": "Unknown",
      "name": "Средства для процедур и дезинфекции",
      "url": "https://www.ozon.ru/category/dezinfitsiruyushchie-meditsinskie-sredstva-33249/"
    },
    {
      "root": "Unknown",
      "name": "Грелки",
      "url": "https://www.ozon.ru/category/grelki-32170/"
    },
    {
      "root": "Unknown",
      "name": "Одежда и текстиль медицинские",
      "url": "https://www.ozon.ru/category/odezhda-i-tekstil-meditsinskie-39939/"
    },
    {
      "root": "Unknown",
      "name": "Текстиль",
      "url": "https://www.ozon.ru/category/tekstil-meditsinskiy-39940/"
    },
    {
      "root": "Unknown",
      "name": "Одежда медицинская и послеоперационная",
      "url": "https://www.ozon.ru/category/odezhda-meditsinskaya-odnorazovaya-39941/"
    },
    {
      "root": "Unknown",
      "name": "Адаптивная одежда",
      "url": "https://www.ozon.ru/category/adaptivnaya-odezhda-37439/"
    },
    {
      "root": "Unknown",
      "name": "Медицинские инструменты",
      "url": "https://www.ozon.ru/category/meditsinskie-instrumenty-31231/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент для биопсии",
      "url": "https://www.ozon.ru/category/hirurgicheskie-instrumenty-32173/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент гинекологический",
      "url": "https://www.ozon.ru/category/ginekologicheskie-instrumenty-32172/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент для оториноларингологии",
      "url": "https://www.ozon.ru/category/lor-instrumenty-32175/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент для неврологии",
      "url": "https://www.ozon.ru/category/nevrologicheskie-instrumenty-32174/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент для хирургии",
      "url": "https://www.ozon.ru/category/instrument-dlya-hirurgii-39850/"
    },
    {
      "root": "Unknown",
      "name": "Инструмент стоматологический",
      "url": "https://www.ozon.ru/category/instrumenty-stomatologicheskie-37019/"
    },
    {
      "root": "Unknown",
      "name": "Товары стоматологические",
      "url": "https://www.ozon.ru/category/instrumenty-i-materialy-stomatologicheskie-31441/"
    },
    {
      "root": "Unknown",
      "name": "Материалы и средства",
      "url": "https://www.ozon.ru/category/materialy-stomatologicheskie-37020/"
    },
    {
      "root": "Unknown",
      "name": "Имплантаты и компоненты",
      "url": "https://www.ozon.ru/category/implantaty-i-komponenty-39851/"
    },
    {
      "root": "Unknown",
      "name": "Капа, трейнер",
      "url": "https://www.ozon.ru/category/kapy-stomatologicheskie-31246/"
    },
    {
      "root": "Unknown",
      "name": "Товары для гигиены",
      "url": "https://www.ozon.ru/category/lichnaya-gigiena-30397/"
    },
    {
      "root": "Unknown",
      "name": "Презервативы и лубриканты",
      "url": "https://www.ozon.ru/category/prezervativy-i-lubrikanty-1751/"
    },
    {
      "root": "Unknown",
      "name": "Антисептические средства",
      "url": "https://www.ozon.ru/category/antibakterialnye-sredstva-6199/"
    },
    {
      "root": "Unknown",
      "name": "Ирригаторы и аксессуары",
      "url": "https://www.ozon.ru/category/irrigatory-i-aksessuary-35159/"
    },
    {
      "root": "Unknown",
      "name": "Уход за полостью рта и отбеливание зубов",
      "url": "https://www.ozon.ru/category/tovary-dlya-otbelivaniya-zubov-36974/"
    },
    {
      "root": "Unknown",
      "name": "Прокладки урологические",
      "url": "https://www.ozon.ru/category/prokladki-urologicheskie-30404/"
    },
    {
      "root": "Unknown",
      "name": "Менструальные чаши",
      "url": "https://www.ozon.ru/category/menstrualnye-chashi-30941/"
    },
    {
      "root": "Unknown",
      "name": "Вкладыши для груди и одежды",
      "url": "https://www.ozon.ru/category/prokladki-dlya-podmyshek-30503/"
    },
    {
      "root": "Unknown",
      "name": "Товары для зубных протезов",
      "url": "https://www.ozon.ru/category/uhod-za-zubnymi-protezami-6344/"
    },
    {
      "root": "Unknown",
      "name": "Товары для чистки ушей, носа",
      "url": "https://www.ozon.ru/category/pribory-dlya-chistki-ushey-7015/"
    },
    {
      "root": "Unknown",
      "name": "Здоровье и гигиена малыша",
      "url": "https://www.ozon.ru/category/zdorove-i-gigiena-malysha-39553/"
    },
    {
      "root": "Unknown",
      "name": "Товары для реабилитации",
      "url": "https://www.ozon.ru/category/sredstva-dlya-reabilitatsii-6249/"
    },
    {
      "root": "Unknown",
      "name": "Товары по уходу за больными",
      "url": "https://www.ozon.ru/category/credstva-po-uhodu-za-bolnymi-6243/"
    },
    {
      "root": "Unknown",
      "name": "Костыли, трости и ходунки",
      "url": "https://www.ozon.ru/category/kostyli-trosti-kolyaski-35153/"
    },
    {
      "root": "Unknown",
      "name": "Бытовые приспособления",
      "url": "https://www.ozon.ru/category/prisposobleniya-dlya-lyudey-s-ogranichennymi-vozmozhnostyami-37860/"
    },
    {
      "root": "Unknown",
      "name": "Коляски инвалидные, пандусы",
      "url": "https://www.ozon.ru/category/kolyaski-invalidnye-pandusy-37674/"
    },
    {
      "root": "Unknown",
      "name": "Параподиумы, вертикализаторы и подъемники",
      "url": "https://www.ozon.ru/category/parapodiumy-vertikalizatory-i-podemniki-37861/"
    },
    {
      "root": "Unknown",
      "name": "Товары для ухода за стомой",
      "url": "https://www.ozon.ru/category/tovary-dlya-uhoda-za-stomoy-39576/"
    },
    {
      "root": "Unknown",
      "name": "Протезы и аксессуары",
      "url": "https://www.ozon.ru/category/protezy-34808/"
    },
    {
      "root": "Unknown",
      "name": "Реабилитационные тренажеры и оборудование",
      "url": "https://www.ozon.ru/category/reabilitatsionnye-trenazhery-i-oborudovanie-37857/"
    },
    {
      "root": "Unknown",
      "name": "Детская реабилитация",
      "url": "https://www.ozon.ru/category/tovary-dlya-detey-s-dtsp-37852/"
    },
    {
      "root": "Unknown",
      "name": "Ортопедия",
      "url": "https://www.ozon.ru/category/ortopediya-6285/"
    },
    {
      "root": "Unknown",
      "name": "Бандажи и ортезы",
      "url": "https://www.ozon.ru/category/bandazhi-i-ortezy-6286/"
    },
    {
      "root": "Unknown",
      "name": "Корсеты, корректоры осанки и пояса",
      "url": "https://www.ozon.ru/category/korsety-i-korrektory-osanki-6290/"
    },
    {
      "root": "Unknown",
      "name": "Компрессионное белье",
      "url": "https://www.ozon.ru/category/kompressionnoe-bele-zhenskoe-7527/"
    },
    {
      "root": "Unknown",
      "name": "Ортопедические стельки",
      "url": "https://www.ozon.ru/category/ortopedicheskie-stelki-6294/"
    },
    {
      "root": "Unknown",
      "name": "Корректоры ног и стопы",
      "url": "https://www.ozon.ru/category/korrektory-stopy-6288/"
    },
    {
      "root": "Unknown",
      "name": "Бинты эластичные и шины",
      "url": "https://www.ozon.ru/category/binty-elastichnye-6287/"
    },
    {
      "root": "Unknown",
      "name": "Ортопедическая обувь",
      "url": "https://www.ozon.ru/category/ortopedicheskaya-obuv-6292/"
    },
    {
      "root": "Unknown",
      "name": "Ручные массажеры и аппликаторы",
      "url": "https://www.ozon.ru/category/ruchnye-massazhery-i-ipplikatory-30529/"
    },
    {
      "root": "Unknown",
      "name": "Массажеры и банки",
      "url": "https://www.ozon.ru/category/ruchnye-massazhery-10789/"
    },
    {
      "root": "Unknown",
      "name": "Массажные и ортопедические коврики",
      "url": "https://www.ozon.ru/category/massazhnye-kovriki-31872/"
    },
    {
      "root": "Unknown",
      "name": "Рефлекторные тапочки",
      "url": "https://www.ozon.ru/category/reflektornye-tapochki-10790/"
    },
    {
      "root": "Unknown",
      "name": "Акупунктурные иглы и браслеты",
      "url": "https://www.ozon.ru/category/tibetskie-ipplikatory-10791/"
    },
    {
      "root": "Unknown",
      "name": "Мебель медицинская",
      "url": "https://www.ozon.ru/category/mebel-meditsinskaya-35290/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 110,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Для кошек",
      "url": "https://www.ozon.ru/category/dlya-koshek-12347/"
    },
    {
      "root": "Unknown",
      "name": "Корма и лакомства",
      "url": "https://www.ozon.ru/category/korm-dlya-koshek-12348/"
    },
    {
      "root": "Unknown",
      "name": "Туалеты и наполнители",
      "url": "https://www.ozon.ru/category/tualety-12365/"
    },
    {
      "root": "Unknown",
      "name": "Когтеточки и игровые комплексы",
      "url": "https://www.ozon.ru/category/kogtetochki-i-igrovye-kompleksy-30230/"
    },
    {
      "root": "Unknown",
      "name": "Домики",
      "url": "https://www.ozon.ru/category/domiki-dlya-koshek-12361/"
    },
    {
      "root": "Unknown",
      "name": "Лежанки",
      "url": "https://www.ozon.ru/category/lezhaki-i-krovati-dlya-koshek-12379/"
    },
    {
      "root": "Unknown",
      "name": "Переноски",
      "url": "https://www.ozon.ru/category/perenoski-dlya-koshek-34579/"
    },
    {
      "root": "Unknown",
      "name": "Клетки и ограждения",
      "url": "https://www.ozon.ru/category/kletki-dlya-sobak-i-koshek-32012/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки",
      "url": "https://www.ozon.ru/category/igrushki-dlya-koshek-12359/"
    },
    {
      "root": "Unknown",
      "name": "Ошейники и поводки",
      "url": "https://www.ozon.ru/category/osheyniki-i-povodki-dlya-koshek-12355/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для кошек",
      "url": "https://www.ozon.ru/category/posuda-dlya-koshek-38324/"
    },
    {
      "root": "Unknown",
      "name": "Груминг",
      "url": "https://www.ozon.ru/category/gruming-12372/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода",
      "url": "https://www.ozon.ru/category/preparaty-dlya-koshek-12405/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-dlya-koshek-34930/"
    },
    {
      "root": "Unknown",
      "name": "Коррекция поведения",
      "url": "https://www.ozon.ru/category/sredstva-dlya-korrektsii-povedeniya-koshek-38952/"
    },
    {
      "root": "Unknown",
      "name": "Ритуальные товары",
      "url": "https://www.ozon.ru/category/ritualnye-tovary-dlya-koshek-36564/"
    },
    {
      "root": "Unknown",
      "name": "Для собак",
      "url": "https://www.ozon.ru/category/dlya-sobak-12301/"
    },
    {
      "root": "Unknown",
      "name": "Корма и лакомства",
      "url": "https://www.ozon.ru/category/korm-dlya-sobak-12302/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки",
      "url": "https://www.ozon.ru/category/igrushki-dlya-sobak-12308/"
    },
    {
      "root": "Unknown",
      "name": "Амуниция",
      "url": "https://www.ozon.ru/category/amunitsiya-12309/"
    },
    {
      "root": "Unknown",
      "name": "Лежаки и домики",
      "url": "https://www.ozon.ru/category/matrasy-i-lezhaki-dlya-sobak-12337/"
    },
    {
      "root": "Unknown",
      "name": "Посуда",
      "url": "https://www.ozon.ru/category/posuda-dlya-sobak-38325/"
    },
    {
      "root": "Unknown",
      "name": "Груминг",
      "url": "https://www.ozon.ru/category/gruming-12315/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода",
      "url": "https://www.ozon.ru/category/preparaty-dlya-sobak-12393/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-dlya-sobak-12325/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-dlya-sobak-12332/"
    },
    {
      "root": "Unknown",
      "name": "Переноски",
      "url": "https://www.ozon.ru/category/perenoski-i-sumki-12362/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для перевозки",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-perevozki-sobak-12340/"
    },
    {
      "root": "Unknown",
      "name": "Туалеты и пеленки",
      "url": "https://www.ozon.ru/category/tualety-12341/"
    },
    {
      "root": "Unknown",
      "name": "Вольеры и будки",
      "url": "https://www.ozon.ru/category/volery-i-budki-dlya-sobak-12333/"
    },
    {
      "root": "Unknown",
      "name": "Дрессировка собак",
      "url": "https://www.ozon.ru/category/dressirovka-sobak-12346/"
    },
    {
      "root": "Unknown",
      "name": "Средства для коррекции поведения",
      "url": "https://www.ozon.ru/category/sredstva-dlya-korrektsii-povedeniya-sobak-39234/"
    },
    {
      "root": "Unknown",
      "name": "Ритуальные товары",
      "url": "https://www.ozon.ru/category/ritualnye-tovary-dlya-sobak-36663/"
    },
    {
      "root": "Unknown",
      "name": "Для грызунов и хорьков",
      "url": "https://www.ozon.ru/category/dlya-gryzunov-12429/"
    },
    {
      "root": "Unknown",
      "name": "Корма и лакомства",
      "url": "https://www.ozon.ru/category/korma-dlya-gryzunov-12442/"
    },
    {
      "root": "Unknown",
      "name": "Клетки",
      "url": "https://www.ozon.ru/category/kletki-dlya-gryzunov-12435/"
    },
    {
      "root": "Unknown",
      "name": "Переноски",
      "url": "https://www.ozon.ru/category/perenoski-dlya-gryzunov-12432/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки",
      "url": "https://www.ozon.ru/category/igrushki-dlya-gryzunov-12434/"
    },
    {
      "root": "Unknown",
      "name": "Домики и лежаки",
      "url": "https://www.ozon.ru/category/domiki-dlya-gryzunov-12431/"
    },
    {
      "root": "Unknown",
      "name": "Туалеты и наполнители",
      "url": "https://www.ozon.ru/category/tualety-i-napolniteli-dlya-gryzunov-12444/"
    },
    {
      "root": "Unknown",
      "name": "Миски, поилки",
      "url": "https://www.ozon.ru/category/miski-poilki-dlya-gryzunov-12441/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода",
      "url": "https://www.ozon.ru/category/preparaty-dlya-gryzunov-12390/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты для ухода",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-uhoda-za-gryzunami-12433/"
    },
    {
      "root": "Unknown",
      "name": "Шлейки и амуниция",
      "url": "https://www.ozon.ru/category/shleyki-dlya-gryzunov-12430/"
    },
    {
      "root": "Unknown",
      "name": "Для птиц",
      "url": "https://www.ozon.ru/category/dlya-ptits-12416/"
    },
    {
      "root": "Unknown",
      "name": "Корма и лакомства",
      "url": "https://www.ozon.ru/category/korma-dlya-ptits-12427/"
    },
    {
      "root": "Unknown",
      "name": "Клетки",
      "url": "https://www.ozon.ru/category/kletki-dlya-ptits-12422/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки",
      "url": "https://www.ozon.ru/category/igrushki-dlya-ptits-12421/"
    },
    {
      "root": "Unknown",
      "name": "Поилки, кормушки",
      "url": "https://www.ozon.ru/category/poilki-kormushki-dlya-ptits-12426/"
    },
    {
      "root": "Unknown",
      "name": "Купалки и песок",
      "url": "https://www.ozon.ru/category/kupalki-i-pesok-dlya-ptits-12428/"
    },
    {
      "root": "Unknown",
      "name": "Светильники и лампы",
      "url": "https://www.ozon.ru/category/svetilniki-i-lampy-dlya-ptits-37712/"
    },
    {
      "root": "Unknown",
      "name": "Переноски",
      "url": "https://www.ozon.ru/category/perevozki-12418/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-dlya-ptits-38356/"
    },
    {
      "root": "Unknown",
      "name": "Дрессировка и воспитание",
      "url": "https://www.ozon.ru/category/sredstva-dlya-dressirovki-i-vospitaniya-ptits-38953/"
    },
    {
      "root": "Unknown",
      "name": "Скворечники и гнезда",
      "url": "https://www.ozon.ru/category/skvorechniki-12419/"
    },
    {
      "root": "Unknown",
      "name": "Для рыб и рептилий",
      "url": "https://www.ozon.ru/category/akvariumistika-12446/"
    },
    {
      "root": "Unknown",
      "name": "Аквариумы и аксессуары",
      "url": "https://www.ozon.ru/category/akvariumy-i-aksessuary-34214/"
    },
    {
      "root": "Unknown",
      "name": "Террариумы и аксессуары",
      "url": "https://www.ozon.ru/category/terrariumy-i-aksessuary-34651/"
    },
    {
      "root": "Unknown",
      "name": "Корма для рыб",
      "url": "https://www.ozon.ru/category/korma-dlya-ryb-32260/"
    },
    {
      "root": "Unknown",
      "name": "Корма для рептилий и других насекомоядных",
      "url": "https://www.ozon.ru/category/korma-dlya-ryb-i-reptiliy-12449/"
    },
    {
      "root": "Unknown",
      "name": "Муравьиные фермы",
      "url": "https://www.ozon.ru/category/muravinye-fermy-38936/"
    },
    {
      "root": "Unknown",
      "name": "Для лошадей",
      "url": "https://www.ozon.ru/category/dlya-loshadey-12454/"
    },
    {
      "root": "Unknown",
      "name": "Корм для лошадей",
      "url": "https://www.ozon.ru/category/korm-dlya-loshadey-32447/"
    },
    {
      "root": "Unknown",
      "name": "Амуниция для лошадей",
      "url": "https://www.ozon.ru/category/amunitsiya-dlya-loshadey-33823/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода",
      "url": "https://www.ozon.ru/category/preparaty-dlya-loshadey-12415/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для конюшни",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-konyushni-35094/"
    },
    {
      "root": "Unknown",
      "name": "Подковы и инструменты для ковки",
      "url": "https://www.ozon.ru/category/podkovy-12455/"
    },
    {
      "root": "Unknown",
      "name": "Ветаптека",
      "url": "https://www.ozon.ru/category/veterinarnaya-apteka-12387/"
    },
    {
      "root": "Unknown",
      "name": "Лекарственные препараты",
      "url": "https://www.ozon.ru/category/lekarstvennye-sredstva-dlya-zhivotnyh-31674/"
    },
    {
      "root": "Unknown",
      "name": "Парафармацевтика",
      "url": "https://www.ozon.ru/category/parafarmatsevtika-39414/"
    },
    {
      "root": "Unknown",
      "name": "Медицинские инструменты и оборудование",
      "url": "https://www.ozon.ru/category/meditsinskie-instrumenty-dlya-zhivotnyh-35078/"
    },
    {
      "root": "Unknown",
      "name": "Расходные материалы",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-lecheniya-zhivotnyh-39431/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных-инвалидов",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-invalidov-39433/"
    },
    {
      "root": "Unknown",
      "name": "Фермерское хозяйство",
      "url": "https://www.ozon.ru/category/tovary-dlya-fermerskogo-hozyaystva-34997/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-ptitsevodstva-i-zhivotnovodstva-34998/"
    },
    {
      "root": "Unknown",
      "name": "Содержание с/х животных и птиц",
      "url": "https://www.ozon.ru/category/soderzhanie-uhod-ptitsy-i-selskohozyaystvennyh-zhivotnyh-34999/"
    },
    {
      "root": "Unknown",
      "name": "Корма и добавки",
      "url": "https://www.ozon.ru/category/korma-i-dobavki-dlya-ptitsevodstva-i-zhivotnovodstva-35000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для пчеловодства",
      "url": "https://www.ozon.ru/category/tovary-dlya-pchelovodstva-14766/"
    },
    {
      "root": "Unknown",
      "name": "Ветеринарное оборудование",
      "url": "https://www.ozon.ru/category/professionalnoe-veterinarnoe-oborudovanie-37990/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 82,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Нехудожественная литература",
      "url": "https://www.ozon.ru/category/nehudozhestvennaya-literatura-16511/"
    },
    {
      "root": "Unknown",
      "name": "Бизнес",
      "url": "https://www.ozon.ru/category/biznes-literatura-40024/"
    },
    {
      "root": "Unknown",
      "name": "Саморазвитие и психология",
      "url": "https://www.ozon.ru/category/samorazvitie-32618/"
    },
    {
      "root": "Unknown",
      "name": "Научная и научно-популярная литература",
      "url": "https://www.ozon.ru/category/nauchnaya-literatura-40021/"
    },
    {
      "root": "Unknown",
      "name": "Медицина",
      "url": "https://www.ozon.ru/category/meditsina-16551/"
    },
    {
      "root": "Unknown",
      "name": "Юридическая литература",
      "url": "https://www.ozon.ru/category/pravo-40022/"
    },
    {
      "root": "Unknown",
      "name": "Искусство и культура",
      "url": "https://www.ozon.ru/category/iskusstvo-i-fotografiya-40013/"
    },
    {
      "root": "Unknown",
      "name": "История",
      "url": "https://www.ozon.ru/category/istoriya-16552/"
    },
    {
      "root": "Unknown",
      "name": "Военное дело",
      "url": "https://www.ozon.ru/category/voennoe-delo-34066/"
    },
    {
      "root": "Unknown",
      "name": "Политика и политология",
      "url": "https://www.ozon.ru/category/politologiya-33927/"
    },
    {
      "root": "Unknown",
      "name": "Публицистика",
      "url": "https://www.ozon.ru/category/publitsistika-16518/"
    },
    {
      "root": "Unknown",
      "name": "Эзотерика и спиритизм",
      "url": "https://www.ozon.ru/category/ezoterika-i-spiritizm-40016/"
    },
    {
      "root": "Unknown",
      "name": "Кулинария",
      "url": "https://www.ozon.ru/category/kulinarnye-knigi-40018/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/rukodelie-i-tvorchestvo-33802/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-hobbi-40019/"
    },
    {
      "root": "Unknown",
      "name": "Красота, здоровье и спорт",
      "url": "https://www.ozon.ru/category/krasota-zdorove-i-sport-40012/"
    },
    {
      "root": "Unknown",
      "name": "Религия",
      "url": "https://www.ozon.ru/category/religiya-40015/"
    },
    {
      "root": "Unknown",
      "name": "Компьютерные технологии",
      "url": "https://www.ozon.ru/category/kompyuternye-tehnologii-40020/"
    },
    {
      "root": "Unknown",
      "name": "Энциклопедии и справочники",
      "url": "https://www.ozon.ru/category/entsiklopedii-spravochniki-40017/"
    },
    {
      "root": "Unknown",
      "name": "Путешествия. Путеводители",
      "url": "https://www.ozon.ru/category/puteshestviya-putevoditeli-40028/"
    },
    {
      "root": "Unknown",
      "name": "Художественная литература",
      "url": "https://www.ozon.ru/category/hudozhestvennaya-literatura-16501/"
    },
    {
      "root": "Unknown",
      "name": "Проза",
      "url": "https://www.ozon.ru/category/proza-35410/"
    },
    {
      "root": "Unknown",
      "name": "Детективы",
      "url": "https://www.ozon.ru/category/detektivy-trillery-40003/"
    },
    {
      "root": "Unknown",
      "name": "Фэнтези",
      "url": "https://www.ozon.ru/category/fentezi-33046/"
    },
    {
      "root": "Unknown",
      "name": "Фантастика",
      "url": "https://www.ozon.ru/category/fantastika-i-fentezi-40002/"
    },
    {
      "root": "Unknown",
      "name": "Подростковая литература",
      "url": "https://www.ozon.ru/category/literatura-dlya-podrostkov-33015/"
    },
    {
      "root": "Unknown",
      "name": "Ужасы и триллеры",
      "url": "https://www.ozon.ru/category/uzhasy-trillery-32998/"
    },
    {
      "root": "Unknown",
      "name": "Любовные романы",
      "url": "https://www.ozon.ru/category/romany-40005/"
    },
    {
      "root": "Unknown",
      "name": "Фольклор",
      "url": "https://www.ozon.ru/category/folklor-35412/"
    },
    {
      "root": "Unknown",
      "name": "Поэзия",
      "url": "https://www.ozon.ru/category/poeziya-40007/"
    },
    {
      "root": "Unknown",
      "name": "Приключения",
      "url": "https://www.ozon.ru/category/priklyucheniya-33098/"
    },
    {
      "root": "Unknown",
      "name": "Боевики",
      "url": "https://www.ozon.ru/category/knigi-boeviki-35414/"
    },
    {
      "root": "Unknown",
      "name": "Драматургия",
      "url": "https://www.ozon.ru/category/pesy-i-dramaturgiya-35413/"
    },
    {
      "root": "Unknown",
      "name": "Детям и родителям",
      "url": "https://www.ozon.ru/category/detyam-i-roditelyam-40025/"
    },
    {
      "root": "Unknown",
      "name": "Художественная литература",
      "url": "https://www.ozon.ru/category/hudozhestvennaya-literatura-40046/"
    },
    {
      "root": "Unknown",
      "name": "Развитие детей",
      "url": "https://www.ozon.ru/category/razvitie-rebenka-40044/"
    },
    {
      "root": "Unknown",
      "name": "Познавательная литература",
      "url": "https://www.ozon.ru/category/poznavatelnaya-literatura-40041/"
    },
    {
      "root": "Unknown",
      "name": "Досуг и творчество",
      "url": "https://www.ozon.ru/category/dosug-i-tvorchestvo-detey-40035/"
    },
    {
      "root": "Unknown",
      "name": "Комиксы",
      "url": "https://www.ozon.ru/category/komiksy-40038/"
    },
    {
      "root": "Unknown",
      "name": "Учебная литература",
      "url": "https://www.ozon.ru/category/uchebnaya-literatura-40026/"
    },
    {
      "root": "Unknown",
      "name": "Изучение иностранных языков",
      "url": "https://www.ozon.ru/category/izuchenie-inostrannyh-yazykov-40029/"
    },
    {
      "root": "Unknown",
      "name": "Пособия для школы",
      "url": "https://www.ozon.ru/category/uchebniki-dlya-1-klassa-40080/"
    },
    {
      "root": "Unknown",
      "name": "Подготовка к экзаменам",
      "url": "https://www.ozon.ru/category/posobiya-dlya-podgotovki-k-ege-40092/"
    },
    {
      "root": "Unknown",
      "name": "Абитуриентам, студентам и аспирантам",
      "url": "https://www.ozon.ru/category/uchebniik-dlya-abiturientov-i-studentov-40094/"
    },
    {
      "root": "Unknown",
      "name": "Педагогика и логопедия",
      "url": "https://www.ozon.ru/category/pedagogika-33894/"
    },
    {
      "root": "Unknown",
      "name": "Комиксы",
      "url": "https://www.ozon.ru/category/komiksy-manga-40027/"
    },
    {
      "root": "Unknown",
      "name": "Манга",
      "url": "https://www.ozon.ru/category/manga-32576/"
    },
    {
      "root": "Unknown",
      "name": "Журналы и газеты",
      "url": "https://www.ozon.ru/category/zhurnaly-gazety-34105/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные издания книг",
      "url": "https://www.ozon.ru/category/podarochnye-izdaniya-16547/"
    },
    {
      "root": "Unknown",
      "name": "Антикварные книги",
      "url": "https://www.ozon.ru/category/antikvarnye-knigi-30963/"
    },
    {
      "root": "Unknown",
      "name": "Подписки на электронные книги и аудиокниги",
      "url": "https://www.ozon.ru/category/podpiski-na-elektronnye-knigi-i-audioknigi-34457/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 99,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Туризм и отдых на природе",
      "url": "https://www.ozon.ru/category/turizm-i-otdyh-na-prirode-11424/"
    },
    {
      "root": "Unknown",
      "name": "Палатки, тенты и шатры",
      "url": "https://www.ozon.ru/category/palatki-tenty-i-shatry-11425/"
    },
    {
      "root": "Unknown",
      "name": "Ножи, лопаты и пилы",
      "url": "https://www.ozon.ru/category/nozhi-i-aksessuary-11463/"
    },
    {
      "root": "Unknown",
      "name": "Туристическая мебель",
      "url": "https://www.ozon.ru/category/skladnaya-pohodnaya-mebel-32938/"
    },
    {
      "root": "Unknown",
      "name": "Фонари и аксессуары",
      "url": "https://www.ozon.ru/category/fonari-i-laytstiki-11448/"
    },
    {
      "root": "Unknown",
      "name": "Насосы",
      "url": "https://www.ozon.ru/category/nasosy-dlya-naduvnyh-matrasov-1716/"
    },
    {
      "root": "Unknown",
      "name": "Спальные мешки",
      "url": "https://www.ozon.ru/category/spalnye-meshki-11434/"
    },
    {
      "root": "Unknown",
      "name": "Коврики",
      "url": "https://www.ozon.ru/category/kovriki-turisticheskie-11520/"
    },
    {
      "root": "Unknown",
      "name": "Горелки, походные печи и газовые обогреватели",
      "url": "https://www.ozon.ru/category/gorelki-zazhigalki-i-prinadlezhnosti-11545/"
    },
    {
      "root": "Unknown",
      "name": "Термосы, фляги и питьевые системы",
      "url": "https://www.ozon.ru/category/termosy-i-termokruzhki-33774/"
    },
    {
      "root": "Unknown",
      "name": "Металлоискатели и аксессуары",
      "url": "https://www.ozon.ru/category/metalloiskateli-i-aksessuary-11497/"
    },
    {
      "root": "Unknown",
      "name": "Рюкзаки и сумки",
      "url": "https://www.ozon.ru/category/turisticheskie-ryukzaki-i-sumki-11435/"
    },
    {
      "root": "Unknown",
      "name": "Термосумки и аксессуары",
      "url": "https://www.ozon.ru/category/sumki-holodilniki-11521/"
    },
    {
      "root": "Unknown",
      "name": "Походная посуда",
      "url": "https://www.ozon.ru/category/turisticheskaya-posuda-11526/"
    },
    {
      "root": "Unknown",
      "name": "Тактическая одежда",
      "url": "https://www.ozon.ru/category/takticheskie-kostyumy-38981/"
    },
    {
      "root": "Unknown",
      "name": "Дождевики",
      "url": "https://www.ozon.ru/category/dozhdeviki-7793/"
    },
    {
      "root": "Unknown",
      "name": "Альпинизм и скалолазание",
      "url": "https://www.ozon.ru/category/alpinizm-32415/"
    },
    {
      "root": "Unknown",
      "name": "Компасы и курвиметры",
      "url": "https://www.ozon.ru/category/kompasy-11461/"
    },
    {
      "root": "Unknown",
      "name": "Тросы",
      "url": "https://www.ozon.ru/category/trosy-dlya-turizma-11598/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для туризма",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-turizma-11576/"
    },
    {
      "root": "Unknown",
      "name": "Рыбалка",
      "url": "https://www.ozon.ru/category/rybalka-33152/"
    },
    {
      "root": "Unknown",
      "name": "Удочки, удилища и спиннинги",
      "url": "https://www.ozon.ru/category/udochki-udilishcha-i-spinningi-11327/"
    },
    {
      "root": "Unknown",
      "name": "Катушки",
      "url": "https://www.ozon.ru/category/katushki-rybolovnye-11376/"
    },
    {
      "root": "Unknown",
      "name": "Приманки и снасти",
      "url": "https://www.ozon.ru/category/primanki-11362/"
    },
    {
      "root": "Unknown",
      "name": "Лески и плетеные шнуры",
      "url": "https://www.ozon.ru/category/leski-i-pletenye-shnury-11383/"
    },
    {
      "root": "Unknown",
      "name": "Эхолоты, подводные камеры и аксессуары",
      "url": "https://www.ozon.ru/category/eholoty-i-aksessuary-11336/"
    },
    {
      "root": "Unknown",
      "name": "Хранение и переноски",
      "url": "https://www.ozon.ru/category/hranenie-i-perenoski-31455/"
    },
    {
      "root": "Unknown",
      "name": "Прикормки, насадки и ароматизаторы",
      "url": "https://www.ozon.ru/category/prikormki-i-aromatizatory-31453/"
    },
    {
      "root": "Unknown",
      "name": "Грузила",
      "url": "https://www.ozon.ru/category/gruzila-i-kryuchki-11370/"
    },
    {
      "root": "Unknown",
      "name": "Ледобуры и аксессуары",
      "url": "https://www.ozon.ru/category/ledobury-i-aksessuary-30568/"
    },
    {
      "root": "Unknown",
      "name": "Снаряжение",
      "url": "https://www.ozon.ru/category/snaryazhenie-dlya-zimney-rybalki-32445/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары рыболовные",
      "url": "https://www.ozon.ru/category/aksessuary-i-prinadlezhnosti-dlya-rybalki-11340/"
    },
    {
      "root": "Unknown",
      "name": "Товары для охоты",
      "url": "https://www.ozon.ru/category/aksessuary-i-prinadlezhnosti-dlya-ohoty-11408/"
    },
    {
      "root": "Unknown",
      "name": "Пневматическое оружие",
      "url": "https://www.ozon.ru/category/pnevmaticheskoe-oruzhie-11804/"
    },
    {
      "root": "Unknown",
      "name": "Оптика",
      "url": "https://www.ozon.ru/category/optika-dlya-ohoty-i-sporta-33134/"
    },
    {
      "root": "Unknown",
      "name": "Снаряжение для охоты",
      "url": "https://www.ozon.ru/category/snaryazhenie-dlya-ohoty-33149/"
    },
    {
      "root": "Unknown",
      "name": "Страйкбольное оружие",
      "url": "https://www.ozon.ru/category/straykbolnoe-oruzhie-11816/"
    },
    {
      "root": "Unknown",
      "name": "Луки и арбалеты",
      "url": "https://www.ozon.ru/category/sportivnye-luki-i-arbalety-11825/"
    },
    {
      "root": "Unknown",
      "name": "Спортивная стрельба",
      "url": "https://www.ozon.ru/category/sportivnaya-strelba-11803/"
    },
    {
      "root": "Unknown",
      "name": "Рогатки",
      "url": "https://www.ozon.ru/category/rogatki-11596/"
    },
    {
      "root": "Unknown",
      "name": "Средства связи для охоты",
      "url": "https://www.ozon.ru/category/sredstva-svyazi-dlya-ohoty-34938/"
    },
    {
      "root": "Unknown",
      "name": "Оформления трофеев",
      "url": "https://www.ozon.ru/category/obrabotka-ohotnichih-trofeev-35386/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и хранение оружия",
      "url": "https://www.ozon.ru/category/aksessuary-i-hranenie-oruzhiya-33147/"
    },
    {
      "root": "Unknown",
      "name": "Лодки и лодочные моторы",
      "url": "https://www.ozon.ru/category/lodki-i-lodochnye-motory-11190/"
    },
    {
      "root": "Unknown",
      "name": "Лодки, байдарки и каяки",
      "url": "https://www.ozon.ru/category/lodki-34600/"
    },
    {
      "root": "Unknown",
      "name": "Моторы",
      "url": "https://www.ozon.ru/category/lodochnye-motory-11192/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти и аксессуары для моторов",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-lodochnyh-motorov-11200/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для лодок",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-lodok-11196/"
    },
    {
      "root": "Unknown",
      "name": "Спасательные жилеты",
      "url": "https://www.ozon.ru/category/spasatelnye-zhilety-11206/"
    },
    {
      "root": "Unknown",
      "name": "Средства спасения",
      "url": "https://www.ozon.ru/category/sredstva-spaseniya-32919/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-yaht-38820/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для рыбалки и охоты",
      "url": "https://www.ozon.ru/category/odezhda-dlya-rybalki-11334/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы",
      "url": "https://www.ozon.ru/category/kostyumy-dlya-rybalki-32132/"
    },
    {
      "root": "Unknown",
      "name": "Полукомбинезоны",
      "url": "https://www.ozon.ru/category/polukombinezony-dlya-rybalki-32133/"
    },
    {
      "root": "Unknown",
      "name": "Верхняя одежда",
      "url": "https://www.ozon.ru/category/verhnyaya-odezhda-dlya-rybalki-32134/"
    },
    {
      "root": "Unknown",
      "name": "Брюки",
      "url": "https://www.ozon.ru/category/shtany-rybolovnye-32135/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки, варежки и носки",
      "url": "https://www.ozon.ru/category/perchatki-i-varezhki-rybolovnye-32136/"
    },
    {
      "root": "Unknown",
      "name": "Головные уборы и очки",
      "url": "https://www.ozon.ru/category/golovnye-ubory-dlya-ohoty-i-rybalki-35121/"
    },
    {
      "root": "Unknown",
      "name": "Рубашки, футболки и худи",
      "url": "https://www.ozon.ru/category/rubashki-dlya-rybalki-37865/"
    },
    {
      "root": "Unknown",
      "name": "Одежда для зимней рыбалки",
      "url": "https://www.ozon.ru/category/odezhda-dlya-zimney-rybalki-32157/"
    },
    {
      "root": "Unknown",
      "name": "Обувь для рыбалки и охоты",
      "url": "https://www.ozon.ru/category/obuv-dlya-rybalki-11335/"
    },
    {
      "root": "Unknown",
      "name": "Тактическая одежда и аксессуары",
      "url": "https://www.ozon.ru/category/takticheskaya-odezhda-i-aksessuary-38392/"
    },
    {
      "root": "Unknown",
      "name": "Бронежилеты и бронешлемы",
      "url": "https://www.ozon.ru/category/bronezhilety-33900/"
    },
    {
      "root": "Unknown",
      "name": "Ремни и разгрузочные системы",
      "url": "https://www.ozon.ru/category/takticheskie-remni-11886/"
    },
    {
      "root": "Unknown",
      "name": "Тактическая одежда",
      "url": "https://www.ozon.ru/category/kamuflyazhnye-kostyumy-7822/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки",
      "url": "https://www.ozon.ru/category/takticheskie-perchatki-38394/"
    },
    {
      "root": "Unknown",
      "name": "Сумки и рюкзаки",
      "url": "https://www.ozon.ru/category/turisticheskie-bauly-11875/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для выживания",
      "url": "https://www.ozon.ru/category/nabory-dlya-vyzhivaniya-11583/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 197,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для легковых авто",
      "url": "https://www.ozon.ru/category/avtozapchasti-8678/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для ТО",
      "url": "https://www.ozon.ru/category/katalog-to-8603/"
    },
    {
      "root": "Unknown",
      "name": "Автосвет",
      "url": "https://www.ozon.ru/category/avtosvet-8679/"
    },
    {
      "root": "Unknown",
      "name": "Двигатель",
      "url": "https://www.ozon.ru/category/dvigatel-8814/"
    },
    {
      "root": "Unknown",
      "name": "Подвеска",
      "url": "https://www.ozon.ru/category/podveska-34348/"
    },
    {
      "root": "Unknown",
      "name": "Трансмиссия",
      "url": "https://www.ozon.ru/category/transmissiya-8704/"
    },
    {
      "root": "Unknown",
      "name": "Тормозная система",
      "url": "https://www.ozon.ru/category/tormoznaya-sistema-8703/"
    },
    {
      "root": "Unknown",
      "name": "Система очистки стекол и фар",
      "url": "https://www.ozon.ru/category/sistemy-ochistki-stekol-i-far-34196/"
    },
    {
      "root": "Unknown",
      "name": "Топливная система",
      "url": "https://www.ozon.ru/category/toplivnaya-sistema-8702/"
    },
    {
      "root": "Unknown",
      "name": "Система выпуска",
      "url": "https://www.ozon.ru/category/sistemy-vypuska-otrabotavshih-gazov-1683/"
    },
    {
      "root": "Unknown",
      "name": "Система питания",
      "url": "https://www.ozon.ru/category/sistema-pitaniya-34376/"
    },
    {
      "root": "Unknown",
      "name": "Система зажигания",
      "url": "https://www.ozon.ru/category/sistema-zazhiganiya-8700/"
    },
    {
      "root": "Unknown",
      "name": "Рулевое управление",
      "url": "https://www.ozon.ru/category/rulevoe-upravlenie-8696/"
    },
    {
      "root": "Unknown",
      "name": "Электрооборудование",
      "url": "https://www.ozon.ru/category/elektrooborudovanie-avtomobilya-33899/"
    },
    {
      "root": "Unknown",
      "name": "Кузовные запчасти",
      "url": "https://www.ozon.ru/category/kuzovnye-zapchasti-32469/"
    },
    {
      "root": "Unknown",
      "name": "Отопители и кондиционирование",
      "url": "https://www.ozon.ru/category/otopitel-i-konditsionirovanie-34340/"
    },
    {
      "root": "Unknown",
      "name": "Подшипники",
      "url": "https://www.ozon.ru/category/podshipniki-avtomobilnye-38999/"
    },
    {
      "root": "Unknown",
      "name": "Детали салона",
      "url": "https://www.ozon.ru/category/detali-salona-39587/"
    },
    {
      "root": "Unknown",
      "name": "Прочие запчасти",
      "url": "https://www.ozon.ru/category/avtozpchastii-avtomobilnye-34605/"
    },
    {
      "root": "Unknown",
      "name": "Автоаксессуары и принадлежности",
      "url": "https://www.ozon.ru/category/avtoaksessuary-i-oborudovanie-8608/"
    },
    {
      "root": "Unknown",
      "name": "Интерьер автомобиля",
      "url": "https://www.ozon.ru/category/obustroystvo-salona-8633/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы и накидки на сиденья",
      "url": "https://www.ozon.ru/category/chehly-i-nakidki-na-sidenya-8640/"
    },
    {
      "root": "Unknown",
      "name": "Ковры автомобильные",
      "url": "https://www.ozon.ru/category/kovry-avtomobilnye-34455/"
    },
    {
      "root": "Unknown",
      "name": "Экстерьер автомобиля",
      "url": "https://www.ozon.ru/category/tyuning-i-vneshniy-dekor-8815/"
    },
    {
      "root": "Unknown",
      "name": "Изоляционные материалы",
      "url": "https://www.ozon.ru/category/izolyatsionnye-materialy-dlya-avtomobiley-31771/"
    },
    {
      "root": "Unknown",
      "name": "Защита кузова",
      "url": "https://www.ozon.ru/category/zashchita-i-vneshniy-tyuning-8615/"
    },
    {
      "root": "Unknown",
      "name": "Перевозка багажа",
      "url": "https://www.ozon.ru/category/bagazhnye-sistemy-8610/"
    },
    {
      "root": "Unknown",
      "name": "Органайзеры и сумки в багажник",
      "url": "https://www.ozon.ru/category/organayzery-i-sumki-8804/"
    },
    {
      "root": "Unknown",
      "name": "Автохолодильники",
      "url": "https://www.ozon.ru/category/avtoholodilniki-8609/"
    },
    {
      "root": "Unknown",
      "name": "Сувениры для автомобилистов",
      "url": "https://www.ozon.ru/category/podarochnye-nabory-dlya-avtomobilistov-30896/"
    },
    {
      "root": "Unknown",
      "name": "Аварийные принадлежности",
      "url": "https://www.ozon.ru/category/avariynye-prinadlezhnosti-30291/"
    },
    {
      "root": "Unknown",
      "name": "Противоугонные устройства и блокираторы",
      "url": "https://www.ozon.ru/category/mehanicheskie-blokiratory-8734/"
    },
    {
      "root": "Unknown",
      "name": "Подстаканники",
      "url": "https://www.ozon.ru/category/termokruzhki-i-podstakanniki-avtomobilnye-31508/"
    },
    {
      "root": "Unknown",
      "name": "Масла и автохимия",
      "url": "https://www.ozon.ru/category/masla-i-avtohimiya-8514/"
    },
    {
      "root": "Unknown",
      "name": "Моторные масла",
      "url": "https://www.ozon.ru/category/motornye-masla-8517/"
    },
    {
      "root": "Unknown",
      "name": "Трансмиссионные масла",
      "url": "https://www.ozon.ru/category/transmissionnye-masla-8516/"
    },
    {
      "root": "Unknown",
      "name": "Специальные масла",
      "url": "https://www.ozon.ru/category/spetsialnye-masla-8520/"
    },
    {
      "root": "Unknown",
      "name": "Смазки",
      "url": "https://www.ozon.ru/category/smazki-8519/"
    },
    {
      "root": "Unknown",
      "name": "Антикоры",
      "url": "https://www.ozon.ru/category/antikory-8559/"
    },
    {
      "root": "Unknown",
      "name": "Присадки и добавки",
      "url": "https://www.ozon.ru/category/prisadki-i-dobavki-31089/"
    },
    {
      "root": "Unknown",
      "name": "Антифризы",
      "url": "https://www.ozon.ru/category/antifriz-8515/"
    },
    {
      "root": "Unknown",
      "name": "Промывки и очистители",
      "url": "https://www.ozon.ru/category/promyvki-i-ochistiteli-8530/"
    },
    {
      "root": "Unknown",
      "name": "Клей и герметики",
      "url": "https://www.ozon.ru/category/kley-i-germetiki-8533/"
    },
    {
      "root": "Unknown",
      "name": "Жидкости омывателя",
      "url": "https://www.ozon.ru/category/zhidkosti-omyvatelya-8569/"
    },
    {
      "root": "Unknown",
      "name": "Тормозные жидкости",
      "url": "https://www.ozon.ru/category/tormoznye-zhidkosti-8521/"
    },
    {
      "root": "Unknown",
      "name": "Дистиллированная вода и электролиты",
      "url": "https://www.ozon.ru/category/distillirovannaya-voda-30599/"
    },
    {
      "root": "Unknown",
      "name": "Жидкости для гидроусилителя",
      "url": "https://www.ozon.ru/category/gidravlicheskie-masla-34151/"
    },
    {
      "root": "Unknown",
      "name": "Моторное топливо",
      "url": "https://www.ozon.ru/category/motornye-topliva-39797/"
    },
    {
      "root": "Unknown",
      "name": "Средства для очистки рук",
      "url": "https://www.ozon.ru/category/sredstva-dlya-ochistki-ruk-8553/"
    },
    {
      "root": "Unknown",
      "name": "Наборы автохимии",
      "url": "https://www.ozon.ru/category/nabory-avtohimii-30628/"
    },
    {
      "root": "Unknown",
      "name": "Шины и диски",
      "url": "https://www.ozon.ru/category/shiny-i-diski-8501/"
    },
    {
      "root": "Unknown",
      "name": "Шины",
      "url": "https://www.ozon.ru/category/shiny-8502/"
    },
    {
      "root": "Unknown",
      "name": "Мотошины",
      "url": "https://www.ozon.ru/category/motoshiny-39926/"
    },
    {
      "root": "Unknown",
      "name": "Диски",
      "url": "https://www.ozon.ru/category/kolesnye-diski-8504/"
    },
    {
      "root": "Unknown",
      "name": "Камеры",
      "url": "https://www.ozon.ru/category/kamery-avtomobilnye-30247/"
    },
    {
      "root": "Unknown",
      "name": "Колпаки на диски",
      "url": "https://www.ozon.ru/category/kolpaki-na-diski-8621/"
    },
    {
      "root": "Unknown",
      "name": "Ниппели, вентили и секретки",
      "url": "https://www.ozon.ru/category/kolpachki-na-nipel-8712/"
    },
    {
      "root": "Unknown",
      "name": "Заглушки для дисков",
      "url": "https://www.ozon.ru/category/emblemy-na-kolesnye-diski-8667/"
    },
    {
      "root": "Unknown",
      "name": "Центровочные кольца и проставки",
      "url": "https://www.ozon.ru/category/prostavki-dlya-kolesnyh-diskov-35338/"
    },
    {
      "root": "Unknown",
      "name": "Уход за шинами и дисками",
      "url": "https://www.ozon.ru/category/uhod-za-shinami-i-diskami-8572/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы для колес",
      "url": "https://www.ozon.ru/category/chehly-dlya-avtomobilnyh-koles-31961/"
    },
    {
      "root": "Unknown",
      "name": "Цепи и ленты антипробуксовочные",
      "url": "https://www.ozon.ru/category/tsepi-i-lenty-antiprobuksovochnye-8642/"
    },
    {
      "root": "Unknown",
      "name": "Автозвук",
      "url": "https://www.ozon.ru/category/avtozvuk-8733/"
    },
    {
      "root": "Unknown",
      "name": "Автомагнитолы",
      "url": "https://www.ozon.ru/category/avtomagnitoly-8742/"
    },
    {
      "root": "Unknown",
      "name": "Головные устройства",
      "url": "https://www.ozon.ru/category/golovnye-ustroystva-8740/"
    },
    {
      "root": "Unknown",
      "name": "Колонки",
      "url": "https://www.ozon.ru/category/kolonki-dlya-avto-8738/"
    },
    {
      "root": "Unknown",
      "name": "Сабвуферы для автомобиля",
      "url": "https://www.ozon.ru/category/sabvufery-dlya-avto-8739/"
    },
    {
      "root": "Unknown",
      "name": "Усилители",
      "url": "https://www.ozon.ru/category/usiliteli-dlya-avto-8747/"
    },
    {
      "root": "Unknown",
      "name": "FM-трансмиттеры",
      "url": "https://www.ozon.ru/category/fm-transmittery-8737/"
    },
    {
      "root": "Unknown",
      "name": "Антенны",
      "url": "https://www.ozon.ru/category/avtomobilnye-antenny-8745/"
    },
    {
      "root": "Unknown",
      "name": "Установка автозвука",
      "url": "https://www.ozon.ru/category/komplekty-ustanovki-avtozvuka-8750/"
    },
    {
      "root": "Unknown",
      "name": "Транспортные средства",
      "url": "https://www.ozon.ru/category/transportnye-sredstva-39798/"
    },
    {
      "root": "Unknown",
      "name": "Мототехника",
      "url": "https://www.ozon.ru/category/mototehnika-38600/"
    },
    {
      "root": "Unknown",
      "name": "Спецтехника",
      "url": "https://www.ozon.ru/category/spetstehnika-39801/"
    },
    {
      "root": "Unknown",
      "name": "Прицепы",
      "url": "https://www.ozon.ru/category/pritsepy-37235/"
    },
    {
      "root": "Unknown",
      "name": "Уход за автомобилем",
      "url": "https://www.ozon.ru/category/uhod-za-avtomobilem-8523/"
    },
    {
      "root": "Unknown",
      "name": "Ароматизаторы автомобильные",
      "url": "https://www.ozon.ru/category/aromatizatory-i-neytralizatory-zapaha-8524/"
    },
    {
      "root": "Unknown",
      "name": "Воски и полироли",
      "url": "https://www.ozon.ru/category/voski-i-poliroli-8562/"
    },
    {
      "root": "Unknown",
      "name": "Краски и грунтовки",
      "url": "https://www.ozon.ru/category/kraski-i-gruntovki-8525/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ремонта царапин",
      "url": "https://www.ozon.ru/category/sredstva-dlya-remonta-tsarapin-30458/"
    },
    {
      "root": "Unknown",
      "name": "Чистящие средства для автомобиля",
      "url": "https://www.ozon.ru/category/chistyashchie-sredstva-dlya-avtomobilya-8534/"
    },
    {
      "root": "Unknown",
      "name": "Щетки, губки и салфетки",
      "url": "https://www.ozon.ru/category/shchetki-gubki-salfetki-31092/"
    },
    {
      "root": "Unknown",
      "name": "Пылесосы автомобильные",
      "url": "https://www.ozon.ru/category/avtomobilnye-pylesosy-10652/"
    },
    {
      "root": "Unknown",
      "name": "Мойки высокого давления и аксессуары",
      "url": "https://www.ozon.ru/category/moyki-vysokogo-davleniya-i-aksessuary-39531/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы и утеплители",
      "url": "https://www.ozon.ru/category/chehly-i-utepliteli-8555/"
    },
    {
      "root": "Unknown",
      "name": "Уход за стеклами и фарами",
      "url": "https://www.ozon.ru/category/uhod-za-steklami-i-farami-8566/"
    },
    {
      "root": "Unknown",
      "name": "Антигравий",
      "url": "https://www.ozon.ru/category/antigraviy-8558/"
    },
    {
      "root": "Unknown",
      "name": "Размораживатели замков и стекол",
      "url": "https://www.ozon.ru/category/razmorazhivateli-zamkov-i-stekol-8773/"
    },
    {
      "root": "Unknown",
      "name": "Электроника для автомобиля",
      "url": "https://www.ozon.ru/category/elektronika-dlya-avto-8751/"
    },
    {
      "root": "Unknown",
      "name": "Видеорегистраторы",
      "url": "https://www.ozon.ru/category/videoregistratory-8755/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти для видеорегистраторов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-videoregistratorov-34604/"
    },
    {
      "root": "Unknown",
      "name": "Камеры обзора",
      "url": "https://www.ozon.ru/category/kamery-zadnego-vida-8756/"
    },
    {
      "root": "Unknown",
      "name": "Автосигнализации и брелоки",
      "url": "https://www.ozon.ru/category/avtosignalizatsii-8731/"
    },
    {
      "root": "Unknown",
      "name": "Радар-детекторы",
      "url": "https://www.ozon.ru/category/radar-detektory-8758/"
    },
    {
      "root": "Unknown",
      "name": "Розетки и разветвители прикуривателя",
      "url": "https://www.ozon.ru/category/rozetki-i-razvetviteli-prikurivatelya-8759/"
    },
    {
      "root": "Unknown",
      "name": "Выключатели зажигания",
      "url": "https://www.ozon.ru/category/vyklyuchateli-zazhiganiya-30828/"
    },
    {
      "root": "Unknown",
      "name": "Алкотестеры",
      "url": "https://www.ozon.ru/category/alkotestery-6256/"
    },
    {
      "root": "Unknown",
      "name": "Парктроники и комплектующие",
      "url": "https://www.ozon.ru/category/parktroniki-8757/"
    },
    {
      "root": "Unknown",
      "name": "Транспондеры",
      "url": "https://www.ozon.ru/category/transpondery-8672/"
    },
    {
      "root": "Unknown",
      "name": "Вентиляторы и увлажнители воздуха",
      "url": "https://www.ozon.ru/category/ventilyatory-i-uvlazhniteli-vozduha-8736/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника для автомобиля",
      "url": "https://www.ozon.ru/category/kipyatilniki-v-prikurivatel-32046/"
    },
    {
      "root": "Unknown",
      "name": "Бортовые компьютеры",
      "url": "https://www.ozon.ru/category/bortovye-kompyutery-30993/"
    },
    {
      "root": "Unknown",
      "name": "Мониторы для салона автомобиля",
      "url": "https://www.ozon.ru/category/avtomobilnye-monitory-8743/"
    },
    {
      "root": "Unknown",
      "name": "Автомобильная громкая связь",
      "url": "https://www.ozon.ru/category/avtomobilnaya-gromkaya-svyaz-8760/"
    },
    {
      "root": "Unknown",
      "name": "Тахографы и аксессуары",
      "url": "https://www.ozon.ru/category/bumaga-dlya-tahografov-8677/"
    },
    {
      "root": "Unknown",
      "name": "Устройства ограничения скорости",
      "url": "https://www.ozon.ru/category/ustroystva-ogranicheniya-skorosti-36347/"
    },
    {
      "root": "Unknown",
      "name": "Нагревательные элементы",
      "url": "https://www.ozon.ru/category/nagrevatelnye-elementy-8715/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты и оборудование",
      "url": "https://www.ozon.ru/category/avtomobilnye-instrumenty-8576/"
    },
    {
      "root": "Unknown",
      "name": "Домкраты",
      "url": "https://www.ozon.ru/category/domkraty-8587/"
    },
    {
      "root": "Unknown",
      "name": "Лебедки",
      "url": "https://www.ozon.ru/category/lebedki-avtomobilnye-8632/"
    },
    {
      "root": "Unknown",
      "name": "Ручные инструменты",
      "url": "https://www.ozon.ru/category/ruchnye-instrumenty-dlya-avto-30298/"
    },
    {
      "root": "Unknown",
      "name": "Компрессоры и комплектующие",
      "url": "https://www.ozon.ru/category/avtomobilnye-kompressory-i-komplektuyushchie-38783/"
    },
    {
      "root": "Unknown",
      "name": "Манометры",
      "url": "https://www.ozon.ru/category/manometry-avtomobilnye-8584/"
    },
    {
      "root": "Unknown",
      "name": "Пневмоинструменты",
      "url": "https://www.ozon.ru/category/pnevmoinstrumenty-dlya-avto-30299/"
    },
    {
      "root": "Unknown",
      "name": "Крепеж",
      "url": "https://www.ozon.ru/category/krepezh-i-osnastka-8579/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для автоинструмента",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-hodovoy-chasti-i-tormozov-8597/"
    },
    {
      "root": "Unknown",
      "name": "Фаркопы",
      "url": "https://www.ozon.ru/category/farkopy-8614/"
    },
    {
      "root": "Unknown",
      "name": "Гараж и автосервис",
      "url": "https://www.ozon.ru/category/garazh-i-avtoservis-34163/"
    },
    {
      "root": "Unknown",
      "name": "Специнструменты для слесарных работ",
      "url": "https://www.ozon.ru/category/spetsinstrumenty-dlya-slesarnyh-rabot-8600/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты для кузовных работ",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-kuzovnyh-rabot-8586/"
    },
    {
      "root": "Unknown",
      "name": "Диагностическое оборудование",
      "url": "https://www.ozon.ru/category/diagnosticheskoe-i-izmeritelnoe-oborudovanie-8581/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для авторемонта",
      "url": "https://www.ozon.ru/category/vspomogatelnye-instrumenty-8578/"
    },
    {
      "root": "Unknown",
      "name": "Замена жидкостей автомобиля",
      "url": "https://www.ozon.ru/category/zamena-zhidkostey-avtomobilya-34164/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для парковки",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-parkovki-34242/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для автомойки",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-avtomoek-35658/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для отвода выхлопных газов",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-otvoda-vyhlopnyh-gazov-39276/"
    },
    {
      "root": "Unknown",
      "name": "Подъемники для моторемонта",
      "url": "https://www.ozon.ru/category/podemniki-dlya-motoremonta-34770/"
    },
    {
      "root": "Unknown",
      "name": "Аппараты для химчистки",
      "url": "https://www.ozon.ru/category/tornadory-31303/"
    },
    {
      "root": "Unknown",
      "name": "Ремонтные лежаки и сиденья",
      "url": "https://www.ozon.ru/category/remontnye-lezhaki-8670/"
    },
    {
      "root": "Unknown",
      "name": "Хранение колес",
      "url": "https://www.ozon.ru/category/hranenie-avtomobilnyh-koles-34199/"
    },
    {
      "root": "Unknown",
      "name": "Пасты для ремонтных работ",
      "url": "https://www.ozon.ru/category/pasty-avtomobilnye-dlya-remontnyh-rabot-41315/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторы и аксессуары",
      "url": "https://www.ozon.ru/category/akkumulyatory-i-aksessuary-8685/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторные батареи",
      "url": "https://www.ozon.ru/category/akkumulyatornye-batarei-8686/"
    },
    {
      "root": "Unknown",
      "name": "Зарядные устройства для АКБ",
      "url": "https://www.ozon.ru/category/zaryadnye-ustroystva-dlya-akkumulyatorov-8687/"
    },
    {
      "root": "Unknown",
      "name": "Принадлежности для АКБ",
      "url": "https://www.ozon.ru/category/kronshteyny-dlya-akb-30381/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторные клеммы",
      "url": "https://www.ozon.ru/category/klemmy-akkumulyatornye-30317/"
    },
    {
      "root": "Unknown",
      "name": "Провода прикуривания",
      "url": "https://www.ozon.ru/category/provoda-prikurivaniya-8688/"
    },
    {
      "root": "Unknown",
      "name": "Зарядные станции для электромобилей",
      "url": "https://www.ozon.ru/category/zaryadnye-stantsii-dlya-elektromobiley-34689/"
    },
    {
      "root": "Unknown",
      "name": "Мототовары",
      "url": "https://www.ozon.ru/category/mototehnika-i-ekipirovka-8719/"
    },
    {
      "root": "Unknown",
      "name": "Мотозапчасти",
      "url": "https://www.ozon.ru/category/motozapchasti-38599/"
    },
    {
      "root": "Unknown",
      "name": "Мотошины",
      "url": "https://www.ozon.ru/category/motoshiny-8505/"
    },
    {
      "root": "Unknown",
      "name": "Мотоэкипировка",
      "url": "https://www.ozon.ru/category/ekipirovka-dlya-mototsiklistov-1692/"
    },
    {
      "root": "Unknown",
      "name": "Экипировка для картинга",
      "url": "https://www.ozon.ru/category/ekipirovka-dlya-kartinga-38567/"
    },
    {
      "root": "Unknown",
      "name": "Экипировка для снегоходов",
      "url": "https://www.ozon.ru/category/ekipirovka-dlya-snegohodov-33162/"
    },
    {
      "root": "Unknown",
      "name": "Мотоаксессуары",
      "url": "https://www.ozon.ru/category/moto-aksessuary-8720/"
    },
    {
      "root": "Unknown",
      "name": "Мотохимия",
      "url": "https://www.ozon.ru/category/motohimiya-38601/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для грузовиков и спецтехники",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-spetstehniki-37159/"
    },
    {
      "root": "Unknown",
      "name": "Оптика для грузовиков",
      "url": "https://www.ozon.ru/category/optika-dlya-gruzovyh-avtomobiley-39946/"
    },
    {
      "root": "Unknown",
      "name": "Двигатели для грузовиков",
      "url": "https://www.ozon.ru/category/dvigateli-gruzovyh-avtomobiley-39947/"
    },
    {
      "root": "Unknown",
      "name": "Крепежные детали для грузовиков",
      "url": "https://www.ozon.ru/category/krepezhnye-detali-gruzovyh-avtomobiley-39948/"
    },
    {
      "root": "Unknown",
      "name": "Кузовные детали для грузовиков",
      "url": "https://www.ozon.ru/category/kuzovnye-detali-gruzovyh-avtomobiley-39949/"
    },
    {
      "root": "Unknown",
      "name": "Подвеска для грузовиков",
      "url": "https://www.ozon.ru/category/podveska-gruzovyh-avtomobiley-39951/"
    },
    {
      "root": "Unknown",
      "name": "Рулевое управление для грузовиков",
      "url": "https://www.ozon.ru/category/rulevoe-upravlenie-gruzovyh-avtomobiley-39952/"
    },
    {
      "root": "Unknown",
      "name": "Система выпуска для грузовиков",
      "url": "https://www.ozon.ru/category/sistema-vypuska-gruzovyh-avtomobiley-39953/"
    },
    {
      "root": "Unknown",
      "name": "Система зажигания для грузовиков",
      "url": "https://www.ozon.ru/category/sistema-zazhiganiya-gruzovyh-avtomobiley-39954/"
    },
    {
      "root": "Unknown",
      "name": "Система отопления, охлаждения для грузовиков",
      "url": "https://www.ozon.ru/category/sistema-otopleniya-ohlazhdeniya-gruzovyh-avtomobiley-39955/"
    },
    {
      "root": "Unknown",
      "name": "Система очистки стекол и фар для грузовиков",
      "url": "https://www.ozon.ru/category/sistema-ochistki-stekol-i-far-gruzovyh-avtomobiley-39956/"
    },
    {
      "root": "Unknown",
      "name": "Система питания для грузовиков",
      "url": "https://www.ozon.ru/category/sistema-pitaniya-gruzovyh-avtomobiley-39957/"
    },
    {
      "root": "Unknown",
      "name": "Тормозная система для грузовиков",
      "url": "https://www.ozon.ru/category/tormoznaya-sistema-gruzovyh-avtomobiley-39958/"
    },
    {
      "root": "Unknown",
      "name": "Трансмиссия для грузовиков",
      "url": "https://www.ozon.ru/category/transmissiya-gruzovyh-avtomobiley-39959/"
    },
    {
      "root": "Unknown",
      "name": "Универсальные детали для грузовиков",
      "url": "https://www.ozon.ru/category/universalnye-detali-gruzovyh-avtomobiley-39960/"
    },
    {
      "root": "Unknown",
      "name": "Фильтры для грузовиков",
      "url": "https://www.ozon.ru/category/filtry-gruzovyh-avtomobiley-39961/"
    },
    {
      "root": "Unknown",
      "name": "Электрооборудование для грузовиков",
      "url": "https://www.ozon.ru/category/elektrooborudovanie-gruzovyh-avtomobiley-39962/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для спецтехники",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-spetstehniki-39998/"
    },
    {
      "root": "Unknown",
      "name": "Автолитература",
      "url": "https://www.ozon.ru/category/avtoliteratura-37492/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти авиационные",
      "url": "https://www.ozon.ru/category/zapchasti-aviatsionnye-39991/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 112,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Садовая мебель",
      "url": "https://www.ozon.ru/category/sadovaya-mebel-15155/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты мебели",
      "url": "https://www.ozon.ru/category/komplekty-sadovoy-mebeli-33746/"
    },
    {
      "root": "Unknown",
      "name": "Столы",
      "url": "https://www.ozon.ru/category/stoly-dlya-sada-39532/"
    },
    {
      "root": "Unknown",
      "name": "Диваны",
      "url": "https://www.ozon.ru/category/divany-sadovye-39533/"
    },
    {
      "root": "Unknown",
      "name": "Стулья и кресла",
      "url": "https://www.ozon.ru/category/stulya-i-kresla-sadovye-33341/"
    },
    {
      "root": "Unknown",
      "name": "Скамейки",
      "url": "https://www.ozon.ru/category/skameyki-34063/"
    },
    {
      "root": "Unknown",
      "name": "Тенты и шатры",
      "url": "https://www.ozon.ru/category/tenty-i-shatry-39565/"
    },
    {
      "root": "Unknown",
      "name": "Качели-гнезда и гамаки",
      "url": "https://www.ozon.ru/category/kacheli-i-gamaki-39518/"
    },
    {
      "root": "Unknown",
      "name": "Кресла подвесные садовые",
      "url": "https://www.ozon.ru/category/podvesnye-kresla-33701/"
    },
    {
      "root": "Unknown",
      "name": "Качели садовые",
      "url": "https://www.ozon.ru/category/sadovye-kacheli-i-aksessuary-39515/"
    },
    {
      "root": "Unknown",
      "name": "Лежаки и шезлонги",
      "url": "https://www.ozon.ru/category/lezhaki-i-shezlongi-39516/"
    },
    {
      "root": "Unknown",
      "name": "Шкафы и тумбы",
      "url": "https://www.ozon.ru/category/shkafy-i-tumby-sadovye-39566/"
    },
    {
      "root": "Unknown",
      "name": "Фурнитура",
      "url": "https://www.ozon.ru/category/furnitura-dlya-sadovoy-mebeli-38565/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы, сетки и матрасы",
      "url": "https://www.ozon.ru/category/chehly-i-setki-dlya-sadovoy-mebeli-38566/"
    },
    {
      "root": "Unknown",
      "name": "Компьютерная и офисная мебель",
      "url": "https://www.ozon.ru/category/kompyuternaya-i-ofisnaya-mebel-38449/"
    },
    {
      "root": "Unknown",
      "name": "Столы письменные и компьютерные",
      "url": "https://www.ozon.ru/category/kompyuternye-i-pismennye-stoly-38454/"
    },
    {
      "root": "Unknown",
      "name": "Кресла офисные и компьютерные",
      "url": "https://www.ozon.ru/category/kompyuternye-i-ofisnye-kresla-38450/"
    },
    {
      "root": "Unknown",
      "name": "Стулья офисные",
      "url": "https://www.ozon.ru/category/ofisnye-kresla-38451/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для рабочего места",
      "url": "https://www.ozon.ru/category/podstavki-pod-nogi-30491/"
    },
    {
      "root": "Unknown",
      "name": "Мягкая мебель",
      "url": "https://www.ozon.ru/category/myagkaya-mebel-15017/"
    },
    {
      "root": "Unknown",
      "name": "Диваны",
      "url": "https://www.ozon.ru/category/divany-i-kushetki-15018/"
    },
    {
      "root": "Unknown",
      "name": "Кресла",
      "url": "https://www.ozon.ru/category/kresla-15019/"
    },
    {
      "root": "Unknown",
      "name": "Кресла-качалки",
      "url": "https://www.ozon.ru/category/kresla-kachalki-36812/"
    },
    {
      "root": "Unknown",
      "name": "Пуфы и банкетки",
      "url": "https://www.ozon.ru/category/pufiki-15031/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты мягкой мебели",
      "url": "https://www.ozon.ru/category/komplekty-myagkoy-mebeli-15021/"
    },
    {
      "root": "Unknown",
      "name": "Столы и стулья",
      "url": "https://www.ozon.ru/category/stoly-stulya-i-kresla-15027/"
    },
    {
      "root": "Unknown",
      "name": "Столы",
      "url": "https://www.ozon.ru/category/kuhonnye-stoly-i-barnye-stoyki-38439/"
    },
    {
      "root": "Unknown",
      "name": "Стулья",
      "url": "https://www.ozon.ru/category/stulya-taburetki-15033/"
    },
    {
      "root": "Unknown",
      "name": "Табуреты",
      "url": "https://www.ozon.ru/category/taburetki-i-banketki-15034/"
    },
    {
      "root": "Unknown",
      "name": "Туалетные столики и консоли",
      "url": "https://www.ozon.ru/category/tualetnye-stoliki-15133/"
    },
    {
      "root": "Unknown",
      "name": "Обеденные группы",
      "url": "https://www.ozon.ru/category/obedennye-gruppy-38464/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие для столов и стульев",
      "url": "https://www.ozon.ru/category/sidenya-stulev-34892/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для хранения",
      "url": "https://www.ozon.ru/category/shkafy-komody-polki-15036/"
    },
    {
      "root": "Unknown",
      "name": "Вешалки",
      "url": "https://www.ozon.ru/category/veshalki-v-prihozhuyu-32947/"
    },
    {
      "root": "Unknown",
      "name": "Гардеробные системы",
      "url": "https://www.ozon.ru/category/garderobnye-sistemy-15126/"
    },
    {
      "root": "Unknown",
      "name": "Для гостиной",
      "url": "https://www.ozon.ru/category/komplekty-mebeli-dlya-gostinoy-38537/"
    },
    {
      "root": "Unknown",
      "name": "Для прихожей",
      "url": "https://www.ozon.ru/category/komplekty-mebeli-dlya-prihozhey-38538/"
    },
    {
      "root": "Unknown",
      "name": "Мебельные модули",
      "url": "https://www.ozon.ru/category/mebelnye-moduli-31437/"
    },
    {
      "root": "Unknown",
      "name": "Комоды и тумбы",
      "url": "https://www.ozon.ru/category/tumby-15041/"
    },
    {
      "root": "Unknown",
      "name": "Обувницы",
      "url": "https://www.ozon.ru/category/obuvnitsy-15038/"
    },
    {
      "root": "Unknown",
      "name": "Полки",
      "url": "https://www.ozon.ru/category/polki-i-stelazhi-31649/"
    },
    {
      "root": "Unknown",
      "name": "Стеллажи",
      "url": "https://www.ozon.ru/category/stellazhi-15040/"
    },
    {
      "root": "Unknown",
      "name": "Шкафы",
      "url": "https://www.ozon.ru/category/shkafy-38531/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для спальни и комплектующие",
      "url": "https://www.ozon.ru/category/mebel-dlya-spalni-15009/"
    },
    {
      "root": "Unknown",
      "name": "Кровати",
      "url": "https://www.ozon.ru/category/krovati-15010/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие для кровати",
      "url": "https://www.ozon.ru/category/osnovaniya-dlya-matrasov-15012/"
    },
    {
      "root": "Unknown",
      "name": "Матрасы",
      "url": "https://www.ozon.ru/category/matrasy-15011/"
    },
    {
      "root": "Unknown",
      "name": "Раскладушки",
      "url": "https://www.ozon.ru/category/raskladushki-11514/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты мебели для спальни",
      "url": "https://www.ozon.ru/category/komplekty-mebeli-dlya-spalni-38235/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для кухни",
      "url": "https://www.ozon.ru/category/mebel-dlya-kuhni-15008/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные уголки",
      "url": "https://www.ozon.ru/category/kuhonnye-ugolki-15128/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные гарнитуры",
      "url": "https://www.ozon.ru/category/obedennye-gruppy-15131/"
    },
    {
      "root": "Unknown",
      "name": "Кухонные модули",
      "url": "https://www.ozon.ru/category/kuhonnye-moduli-37569/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие",
      "url": "https://www.ozon.ru/category/plintus-dlya-stoleshnitsy-37495/"
    },
    {
      "root": "Unknown",
      "name": "Наполнения для кухонных модулей",
      "url": "https://www.ozon.ru/category/poddony-kuhonnye-37009/"
    },
    {
      "root": "Unknown",
      "name": "Столешницы для кухни",
      "url": "https://www.ozon.ru/category/stoleshnitsy-34680/"
    },
    {
      "root": "Unknown",
      "name": "Фартуки для кухни",
      "url": "https://www.ozon.ru/category/fartuki-dlya-kuhni-31926/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для ванной",
      "url": "https://www.ozon.ru/category/mebel-dlya-vannoy-15013/"
    },
    {
      "root": "Unknown",
      "name": "Тумбы",
      "url": "https://www.ozon.ru/category/tumby-dlya-vannoy-34522/"
    },
    {
      "root": "Unknown",
      "name": "Шкафы и пеналы",
      "url": "https://www.ozon.ru/category/shkafy-i-penaly-dlya-vannoy-34523/"
    },
    {
      "root": "Unknown",
      "name": "Бескаркасная мебель",
      "url": "https://www.ozon.ru/category/beskarkasnaya-mebel-35621/"
    },
    {
      "root": "Unknown",
      "name": "Диваны и пуфы бескаркасные",
      "url": "https://www.ozon.ru/category/beskarkasnye-divany-35623/"
    },
    {
      "root": "Unknown",
      "name": "Кресла-мешки",
      "url": "https://www.ozon.ru/category/kresla-meshki-15020/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие для бескаркасной мебели",
      "url": "https://www.ozon.ru/category/napolniteli-dlya-kresla-meshka-38041/"
    },
    {
      "root": "Unknown",
      "name": "Детская мебель",
      "url": "https://www.ozon.ru/category/detskaya-mebel-15001/"
    },
    {
      "root": "Unknown",
      "name": "Диваны",
      "url": "https://www.ozon.ru/category/detskie-divany-39488/"
    },
    {
      "root": "Unknown",
      "name": "Кресла",
      "url": "https://www.ozon.ru/category/detskie-kresla-39489/"
    },
    {
      "root": "Unknown",
      "name": "Кровати",
      "url": "https://www.ozon.ru/category/detskie-krovati-39487/"
    },
    {
      "root": "Unknown",
      "name": "Колыбели",
      "url": "https://www.ozon.ru/category/kolybeli-detskie-31223/"
    },
    {
      "root": "Unknown",
      "name": "Парты и столы",
      "url": "https://www.ozon.ru/category/party-i-stoly-30998/"
    },
    {
      "root": "Unknown",
      "name": "Наборы детской мебели",
      "url": "https://www.ozon.ru/category/nabory-detskoy-mebeli-31002/"
    },
    {
      "root": "Unknown",
      "name": "Стулья и табуреты",
      "url": "https://www.ozon.ru/category/detskie-stulya-i-taburety-30999/"
    },
    {
      "root": "Unknown",
      "name": "Пеленальные комоды и столики",
      "url": "https://www.ozon.ru/category/pelenalnye-komody-i-stoliki-31017/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для бизнеса",
      "url": "https://www.ozon.ru/category/mebel-dlya-biznesa-34225/"
    },
    {
      "root": "Unknown",
      "name": "Для торгового зала",
      "url": "https://www.ozon.ru/category/mebel-dlya-torgovogo-zala-34226/"
    },
    {
      "root": "Unknown",
      "name": "Для салонов красоты",
      "url": "https://www.ozon.ru/category/mebel-dlya-salonov-krasoty-34227/"
    },
    {
      "root": "Unknown",
      "name": "Для производства",
      "url": "https://www.ozon.ru/category/mebel-dlya-proizvodstva-36339/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для ПВЗ",
      "url": "https://www.ozon.ru/category/mebel-dlya-pvz-37535/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для мероприятий",
      "url": "https://www.ozon.ru/category/mebel-dlya-meropriyatiy-38365/"
    },
    {
      "root": "Unknown",
      "name": "Мебель для швей",
      "url": "https://www.ozon.ru/category/mebel-dlya-shitya-37472/"
    },
    {
      "root": "Unknown",
      "name": "Сейфы и архивные шкафы",
      "url": "https://www.ozon.ru/category/seyfy-15158/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 161,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Рукоделие",
      "url": "https://www.ozon.ru/category/rukodelie-13586/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и материалы",
      "url": "https://www.ozon.ru/category/aksessuary-i-materialy-dlya-rukodeliya-13646/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты и инвентарь",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-rukodeliya-13617/"
    },
    {
      "root": "Unknown",
      "name": "Валяние",
      "url": "https://www.ozon.ru/category/valyanie-13607/"
    },
    {
      "root": "Unknown",
      "name": "Выжигание и поделки из дерева",
      "url": "https://www.ozon.ru/category/vyzhiganie-podelki-iz-dereva-13722/"
    },
    {
      "root": "Unknown",
      "name": "Вышивание",
      "url": "https://www.ozon.ru/category/vyshivanie-13587/"
    },
    {
      "root": "Unknown",
      "name": "Вязание",
      "url": "https://www.ozon.ru/category/vyazanie-13588/"
    },
    {
      "root": "Unknown",
      "name": "Декупаж",
      "url": "https://www.ozon.ru/category/dekupazh-13574/"
    },
    {
      "root": "Unknown",
      "name": "Заготовки для декорирования",
      "url": "https://www.ozon.ru/category/zagotovki-dlya-dekorirovaniya-13576/"
    },
    {
      "root": "Unknown",
      "name": "Изготовление игрушек",
      "url": "https://www.ozon.ru/category/nabory-dlya-izgotovleniya-igrushek-13834/"
    },
    {
      "root": "Unknown",
      "name": "Изготовление ножей",
      "url": "https://www.ozon.ru/category/izgotovlenie-nozhey-39393/"
    },
    {
      "root": "Unknown",
      "name": "Кожевенное дело",
      "url": "https://www.ozon.ru/category/kozhevennoe-delo-34023/"
    },
    {
      "root": "Unknown",
      "name": "Лэмпворк",
      "url": "https://www.ozon.ru/category/lempvork-37063/"
    },
    {
      "root": "Unknown",
      "name": "Мыловарение",
      "url": "https://www.ozon.ru/category/mylovarenie-13822/"
    },
    {
      "root": "Unknown",
      "name": "Плетение",
      "url": "https://www.ozon.ru/category/pletenie-13721/"
    },
    {
      "root": "Unknown",
      "name": "Пэчворк и квилтинг",
      "url": "https://www.ozon.ru/category/pechvork-i-kvilting-13614/"
    },
    {
      "root": "Unknown",
      "name": "Реставрация и золочение",
      "url": "https://www.ozon.ru/category/restavratsiya-i-zolochenie-34676/"
    },
    {
      "root": "Unknown",
      "name": "Скрапбукинг",
      "url": "https://www.ozon.ru/category/skrapbuking-13573/"
    },
    {
      "root": "Unknown",
      "name": "Гобелены и стринг-арт",
      "url": "https://www.ozon.ru/category/sozdanie-gobelenov-13613/"
    },
    {
      "root": "Unknown",
      "name": "Создание украшений",
      "url": "https://www.ozon.ru/category/nabory-dlya-sozdaniya-ukrasheniy-13837/"
    },
    {
      "root": "Unknown",
      "name": "Ткачество и прядение",
      "url": "https://www.ozon.ru/category/tkachestvo-i-pryadeniye-38197/"
    },
    {
      "root": "Unknown",
      "name": "Флористика",
      "url": "https://www.ozon.ru/category/floristicheskie-peny-13711/"
    },
    {
      "root": "Unknown",
      "name": "Шитье",
      "url": "https://www.ozon.ru/category/shite-13596/"
    },
    {
      "root": "Unknown",
      "name": "Материалы и инструменты для ювелиров",
      "url": "https://www.ozon.ru/category/materialy-i-instrumenty-dlya-yuvelirov-39791/"
    },
    {
      "root": "Unknown",
      "name": "Настольные и карточные игры",
      "url": "https://www.ozon.ru/category/nastolnye-i-kartochnye-igry-13506/"
    },
    {
      "root": "Unknown",
      "name": "Настольные игры",
      "url": "https://www.ozon.ru/category/nastolnye-igry-13507/"
    },
    {
      "root": "Unknown",
      "name": "Ходилки",
      "url": "https://www.ozon.ru/category/nastolnye-igry-hodilki-39336/"
    },
    {
      "root": "Unknown",
      "name": "Cпортивные игры",
      "url": "https://www.ozon.ru/category/nastolnyy-futbol-hokkey-bilyard-7173/"
    },
    {
      "root": "Unknown",
      "name": "Трансформационные психологические игры",
      "url": "https://www.ozon.ru/category/transformatsionnye-igry-34939/"
    },
    {
      "root": "Unknown",
      "name": "Карточные игры",
      "url": "https://www.ozon.ru/category/kartochnye-igry-39337/"
    },
    {
      "root": "Unknown",
      "name": "Игры в рулетку",
      "url": "https://www.ozon.ru/category/igry-v-ruletku-39335/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для покера",
      "url": "https://www.ozon.ru/category/nabory-dlya-pokera-13518/"
    },
    {
      "root": "Unknown",
      "name": "Игральные карты",
      "url": "https://www.ozon.ru/category/igralnye-karty-13517/"
    },
    {
      "root": "Unknown",
      "name": "Шахматы",
      "url": "https://www.ozon.ru/category/shahmaty-13509/"
    },
    {
      "root": "Unknown",
      "name": "Нарды",
      "url": "https://www.ozon.ru/category/nardy-13511/"
    },
    {
      "root": "Unknown",
      "name": "Шашки",
      "url": "https://www.ozon.ru/category/shashki-13510/"
    },
    {
      "root": "Unknown",
      "name": "Лото",
      "url": "https://www.ozon.ru/category/loto-13513/"
    },
    {
      "root": "Unknown",
      "name": "Домино и маджонг",
      "url": "https://www.ozon.ru/category/domino-13512/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-nastolnyh-igr-13523/"
    },
    {
      "root": "Unknown",
      "name": "Дополнения к настольным играм",
      "url": "https://www.ozon.ru/category/dopolneniya-k-nastolnym-igram-39343/"
    },
    {
      "root": "Unknown",
      "name": "Пазлы и головоломки",
      "url": "https://www.ozon.ru/category/pazly-i-golovolomki-13501/"
    },
    {
      "root": "Unknown",
      "name": "Пазлы",
      "url": "https://www.ozon.ru/category/pazly-13502/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-pazlov-13504/"
    },
    {
      "root": "Unknown",
      "name": "Головоломки",
      "url": "https://www.ozon.ru/category/golovolomki-7177/"
    },
    {
      "root": "Unknown",
      "name": "Неокубы",
      "url": "https://www.ozon.ru/category/neokuby-39814/"
    },
    {
      "root": "Unknown",
      "name": "Музыкальные инструменты",
      "url": "https://www.ozon.ru/category/muzykalnye-instrumenty-13917/"
    },
    {
      "root": "Unknown",
      "name": "Гитары и оборудование",
      "url": "https://www.ozon.ru/category/gitary-i-aksessuary-13924/"
    },
    {
      "root": "Unknown",
      "name": "Струнные инструменты",
      "url": "https://www.ozon.ru/category/strunnye-instrumenty-13951/"
    },
    {
      "root": "Unknown",
      "name": "Клавишные инструменты",
      "url": "https://www.ozon.ru/category/klavishnye-instrumenty-13918/"
    },
    {
      "root": "Unknown",
      "name": "Ударные и перкуссия",
      "url": "https://www.ozon.ru/category/udarnye-i-perkussiya-13959/"
    },
    {
      "root": "Unknown",
      "name": "Духовые инструменты",
      "url": "https://www.ozon.ru/category/duhovye-instrumenty-13932/"
    },
    {
      "root": "Unknown",
      "name": "Смычковые инструменты",
      "url": "https://www.ozon.ru/category/smychkovye-instrumenty-39992/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары к музыкальным инструментам",
      "url": "https://www.ozon.ru/category/aksessuary-k-muzykalnym-instrumentam-13968/"
    },
    {
      "root": "Unknown",
      "name": "Уход за музыкальными инструментами",
      "url": "https://www.ozon.ru/category/uhod-za-muzykalnymi-instrumentami-37518/"
    },
    {
      "root": "Unknown",
      "name": "Рисование",
      "url": "https://www.ozon.ru/category/risovanie-13528/"
    },
    {
      "root": "Unknown",
      "name": "Холсты, артборды и картон грунтованный",
      "url": "https://www.ozon.ru/category/holsty-36228/"
    },
    {
      "root": "Unknown",
      "name": "Бумага для черчения и рисования",
      "url": "https://www.ozon.ru/category/bumaga-dlya-chercheniya-i-risovaniya-39580/"
    },
    {
      "root": "Unknown",
      "name": "Мольберты и этюдники",
      "url": "https://www.ozon.ru/category/molberty-13529/"
    },
    {
      "root": "Unknown",
      "name": "Скетчбуки",
      "url": "https://www.ozon.ru/category/sketchbuki-14017/"
    },
    {
      "root": "Unknown",
      "name": "Краски",
      "url": "https://www.ozon.ru/category/kraski-dlya-risovaniya-13530/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для рисования",
      "url": "https://www.ozon.ru/category/nabory-dlya-risovaniya-13544/"
    },
    {
      "root": "Unknown",
      "name": "Пастель",
      "url": "https://www.ozon.ru/category/pastel-13547/"
    },
    {
      "root": "Unknown",
      "name": "Пигменты",
      "url": "https://www.ozon.ru/category/pigmenty-13539/"
    },
    {
      "root": "Unknown",
      "name": "Глиттеры",
      "url": "https://www.ozon.ru/category/glittery-hudozhestvennye-13541/"
    },
    {
      "root": "Unknown",
      "name": "Уголь, сангина, сепия и соус",
      "url": "https://www.ozon.ru/category/ugol-dlya-risovaniya-13550/"
    },
    {
      "root": "Unknown",
      "name": "Средства для очищения кистей",
      "url": "https://www.ozon.ru/category/sredstva-dlya-ochishcheniya-kistey-38044/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-i-prinadlezhnosti-13551/"
    },
    {
      "root": "Unknown",
      "name": "Экраны и проекторы",
      "url": "https://www.ozon.ru/category/ekrany-dlya-risovaniya-13560/"
    },
    {
      "root": "Unknown",
      "name": "Штампы и губки",
      "url": "https://www.ozon.ru/category/shtampy-i-trafarety-13548/"
    },
    {
      "root": "Unknown",
      "name": "Разбавители, загустители и грунты",
      "url": "https://www.ozon.ru/category/razbaviteli-zagustiteli-i-grunty-dlya-risovaniya-35383/"
    },
    {
      "root": "Unknown",
      "name": "Рисование на воде Эбру",
      "url": "https://www.ozon.ru/category/risovanie-na-vode-ebru-34967/"
    },
    {
      "root": "Unknown",
      "name": "Рисование жидким акрилом (Флюид-арт)",
      "url": "https://www.ozon.ru/category/risovanie-zhidkim-akrilom-flyuid-art-37560/"
    },
    {
      "root": "Unknown",
      "name": "Раскрашивание и роспись",
      "url": "https://www.ozon.ru/category/raskrashivanie-i-rospis-13524/"
    },
    {
      "root": "Unknown",
      "name": "Раскраски",
      "url": "https://www.ozon.ru/category/raskraski-13525/"
    },
    {
      "root": "Unknown",
      "name": "Аэрография",
      "url": "https://www.ozon.ru/category/aerografiya-dlya-tvorchestva-34907/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для росписи",
      "url": "https://www.ozon.ru/category/nabory-dlya-rospisi-13527/"
    },
    {
      "root": "Unknown",
      "name": "Шелкография",
      "url": "https://www.ozon.ru/category/shelkografiya-34904/"
    },
    {
      "root": "Unknown",
      "name": "Картины по номерам",
      "url": "https://www.ozon.ru/category/kartiny-po-nomeram-34021/"
    },
    {
      "root": "Unknown",
      "name": "Создание картин и фоторамок",
      "url": "https://www.ozon.ru/category/sozdanie-kartin-fotoramok-otkrytok-13567/"
    },
    {
      "root": "Unknown",
      "name": "Картины по номерам",
      "url": "https://www.ozon.ru/category/kartiny-po-nomeram-13568/"
    },
    {
      "root": "Unknown",
      "name": "Картины из эпоксидной смолы",
      "url": "https://www.ozon.ru/category/nabory-dlya-kartin-iz-epoksidnoy-smoly-35045/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для создания фоторамок",
      "url": "https://www.ozon.ru/category/nabory-dlya-sozdaniya-fotoramok-13572/"
    },
    {
      "root": "Unknown",
      "name": "Мозаики и фрески",
      "url": "https://www.ozon.ru/category/mozaika-i-freska-13561/"
    },
    {
      "root": "Unknown",
      "name": "Алмазные мозаики",
      "url": "https://www.ozon.ru/category/almaznye-mozaiki-13563/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для рисования песком",
      "url": "https://www.ozon.ru/category/freski-13564/"
    },
    {
      "root": "Unknown",
      "name": "Барельефы и витражи",
      "url": "https://www.ozon.ru/category/barelefy-i-vitrazhi-13566/"
    },
    {
      "root": "Unknown",
      "name": "Гравюры",
      "url": "https://www.ozon.ru/category/gravyury-13565/"
    },
    {
      "root": "Unknown",
      "name": "Лепка и скульптура",
      "url": "https://www.ozon.ru/category/lepka-13723/"
    },
    {
      "root": "Unknown",
      "name": "Пластилин",
      "url": "https://www.ozon.ru/category/plastilin-13734/"
    },
    {
      "root": "Unknown",
      "name": "Глина для лепки",
      "url": "https://www.ozon.ru/category/glina-polimernaya-13725/"
    },
    {
      "root": "Unknown",
      "name": "Клеи и лак для полимерной глины",
      "url": "https://www.ozon.ru/category/klei-i-lak-dlya-polimernoy-gliny-36257/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для создания слепков",
      "url": "https://www.ozon.ru/category/nabory-dlya-sozdaniya-slepkov-13729/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для лепки",
      "url": "https://www.ozon.ru/category/nabory-dlya-lepki-13728/"
    },
    {
      "root": "Unknown",
      "name": "Слаймы",
      "url": "https://www.ozon.ru/category/sozdanie-slaymov-34884/"
    },
    {
      "root": "Unknown",
      "name": "Масса и тесто для лепки",
      "url": "https://www.ozon.ru/category/massa-dlya-lepki-36252/"
    },
    {
      "root": "Unknown",
      "name": "Инструменты",
      "url": "https://www.ozon.ru/category/instrumenty-dlya-lepki-13730/"
    },
    {
      "root": "Unknown",
      "name": "Гипс",
      "url": "https://www.ozon.ru/category/gips-13724/"
    },
    {
      "root": "Unknown",
      "name": "Песок кинетический и цветной",
      "url": "https://www.ozon.ru/category/kineticheskiy-pesok-13726/"
    },
    {
      "root": "Unknown",
      "name": "Гончарное дело",
      "url": "https://www.ozon.ru/category/goncharnoe-delo-37760/"
    },
    {
      "root": "Unknown",
      "name": "Моделизм",
      "url": "https://www.ozon.ru/category/modelirovanie-13738/"
    },
    {
      "root": "Unknown",
      "name": "Принадлежности",
      "url": "https://www.ozon.ru/category/prinadlezhnosti-dlya-modelirovaniya-13749/"
    },
    {
      "root": "Unknown",
      "name": "Интерьерные миниатюры и сборка зданий",
      "url": "https://www.ozon.ru/category/interernye-miniatyury-13746/"
    },
    {
      "root": "Unknown",
      "name": "Военная техника и оружие",
      "url": "https://www.ozon.ru/category/modeli-voennoy-tehniki-13744/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили и мотоциклы",
      "url": "https://www.ozon.ru/category/modeli-avtomobiley-13740/"
    },
    {
      "root": "Unknown",
      "name": "Самолеты и космические корабли",
      "url": "https://www.ozon.ru/category/modeli-samoletov-13741/"
    },
    {
      "root": "Unknown",
      "name": "Корабли и подводные лодки",
      "url": "https://www.ozon.ru/category/modeli-korabley-i-podvodnyh-lodok-13743/"
    },
    {
      "root": "Unknown",
      "name": "Модели из дерева",
      "url": "https://www.ozon.ru/category/modeli-iz-dereva-13742/"
    },
    {
      "root": "Unknown",
      "name": "Фигурки",
      "url": "https://www.ozon.ru/category/modeli-dlya-sborki-14016/"
    },
    {
      "root": "Unknown",
      "name": "Дополнения",
      "url": "https://www.ozon.ru/category/dopolneniya-dlya-sbornyh-modeley-32787/"
    },
    {
      "root": "Unknown",
      "name": "3D-ручки и аксессуары",
      "url": "https://www.ozon.ru/category/3d-ruchki-i-aksessuary-39200/"
    },
    {
      "root": "Unknown",
      "name": "3D ручки",
      "url": "https://www.ozon.ru/category/3d-ruchki-15775/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-3d-ruchek-39201/"
    },
    {
      "root": "Unknown",
      "name": "Оригами и поделки из бумаги",
      "url": "https://www.ozon.ru/category/origami-i-podelki-iz-bumagi-36265/"
    },
    {
      "root": "Unknown",
      "name": "Аппликации",
      "url": "https://www.ozon.ru/category/applikatsii-13719/"
    },
    {
      "root": "Unknown",
      "name": "Оригами",
      "url": "https://www.ozon.ru/category/origami-13720/"
    },
    {
      "root": "Unknown",
      "name": "Поделки из бумаги",
      "url": "https://www.ozon.ru/category/sozdanie-podelok-iz-bumagi-36267/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для квиллинга",
      "url": "https://www.ozon.ru/category/nabory-dlya-kvillinga-14013/"
    },
    {
      "root": "Unknown",
      "name": "Изготовление косметики и духов",
      "url": "https://www.ozon.ru/category/izgotovlenie-kosmetiki-i-duhov-13830/"
    },
    {
      "root": "Unknown",
      "name": "Изготовление косметики",
      "url": "https://www.ozon.ru/category/izgotovlenie-kosmetiki-39316/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для создания духов",
      "url": "https://www.ozon.ru/category/nabory-dlya-sozdaniya-duhov-13832/"
    },
    {
      "root": "Unknown",
      "name": "Изготовление свечей и саше",
      "url": "https://www.ozon.ru/category/izgotovlenie-svechey-13829/"
    },
    {
      "root": "Unknown",
      "name": "Фокусы",
      "url": "https://www.ozon.ru/category/fokusy-13840/"
    },
    {
      "root": "Unknown",
      "name": "Гадания и эзотерика",
      "url": "https://www.ozon.ru/category/gadaniya-i-ezoterika-13841/"
    },
    {
      "root": "Unknown",
      "name": "Карты Таро",
      "url": "https://www.ozon.ru/category/karty-taro-13843/"
    },
    {
      "root": "Unknown",
      "name": "Амулеты, талисманы и ловцы снов",
      "url": "https://www.ozon.ru/category/amulety-oberegi-i-talismany-13856/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и атрибутика для гаданий",
      "url": "https://www.ozon.ru/category/aksessuary-i-atributika-dlya-gadaniy-13846/"
    },
    {
      "root": "Unknown",
      "name": "Руны",
      "url": "https://www.ozon.ru/category/runy-13844/"
    },
    {
      "root": "Unknown",
      "name": "Магические аксессуары и материалы",
      "url": "https://www.ozon.ru/category/magicheskie-aksessuary-i-materialy-13868/"
    },
    {
      "root": "Unknown",
      "name": "Цветотипирование",
      "url": "https://www.ozon.ru/category/tovary-dlya-tsvetotipirovaniya-37209/"
    },
    {
      "root": "Unknown",
      "name": "Театральные бинокли",
      "url": "https://www.ozon.ru/category/teatralnye-binokli-33333/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 60,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Кольца",
      "url": "https://www.ozon.ru/category/koltsa-yuvelirnye-50002/"
    },
    {
      "root": "Unknown",
      "name": "Золотые",
      "url": "https://www.ozon.ru/category/zolotye-koltsa-39610/"
    },
    {
      "root": "Unknown",
      "name": "Серебряные",
      "url": "https://www.ozon.ru/category/serebryanye-koltsa-39611/"
    },
    {
      "root": "Unknown",
      "name": "С бриллиантами",
      "url": "https://www.ozon.ru/category/koltsa-s-brilliantami-39613/"
    },
    {
      "root": "Unknown",
      "name": "Обручальные",
      "url": "https://www.ozon.ru/category/obruchalnye-koltsa-39614/"
    },
    {
      "root": "Unknown",
      "name": "Помолвочные",
      "url": "https://www.ozon.ru/category/pomolvochnye-koltsa-39615/"
    },
    {
      "root": "Unknown",
      "name": "Серьги",
      "url": "https://www.ozon.ru/category/sergi-yuvelirnye-50003/"
    },
    {
      "root": "Unknown",
      "name": "Золотые",
      "url": "https://www.ozon.ru/category/zolotye-sergi-39616/"
    },
    {
      "root": "Unknown",
      "name": "Серебряные",
      "url": "https://www.ozon.ru/category/serebryanye-sergi-39617/"
    },
    {
      "root": "Unknown",
      "name": "Платиновые",
      "url": "https://www.ozon.ru/category/platinovye-sergi-39618/"
    },
    {
      "root": "Unknown",
      "name": "С бриллиантами",
      "url": "https://www.ozon.ru/category/sergi-s-brilliantami-39619/"
    },
    {
      "root": "Unknown",
      "name": "Браслеты",
      "url": "https://www.ozon.ru/category/braslety-yuvelirnye-50011/"
    },
    {
      "root": "Unknown",
      "name": "Золотые",
      "url": "https://www.ozon.ru/category/zolotye-braslety-39620/"
    },
    {
      "root": "Unknown",
      "name": "Серебряные",
      "url": "https://www.ozon.ru/category/serebryanye-braslety-39621/"
    },
    {
      "root": "Unknown",
      "name": "Украшения на шею",
      "url": "https://www.ozon.ru/category/ukrasheniya-na-sheyu-50004/"
    },
    {
      "root": "Unknown",
      "name": "Золотые",
      "url": "https://www.ozon.ru/category/zolotye-ukrasheniya-na-sheyu-39626/"
    },
    {
      "root": "Unknown",
      "name": "Серебряные",
      "url": "https://www.ozon.ru/category/serebryanye-ukrasheniya-na-sheyu-39631/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты украшений",
      "url": "https://www.ozon.ru/category/komplekty-yuvelirnyh-ukrasheniy-50013/"
    },
    {
      "root": "Unknown",
      "name": "Шармы",
      "url": "https://www.ozon.ru/category/sharmy-yuvelirnye-50015/"
    },
    {
      "root": "Unknown",
      "name": "Броши и значки",
      "url": "https://www.ozon.ru/category/broshi-yuvelirnye-50014/"
    },
    {
      "root": "Unknown",
      "name": "Пирсинг",
      "url": "https://www.ozon.ru/category/pirsing-yuvelirnyy-50018/"
    },
    {
      "root": "Unknown",
      "name": "Часы",
      "url": "https://www.ozon.ru/category/chasy-yuvelirnye-50012/"
    },
    {
      "root": "Unknown",
      "name": "Золотые",
      "url": "https://www.ozon.ru/category/zolotye-chasy-39623/"
    },
    {
      "root": "Unknown",
      "name": "Серебряные",
      "url": "https://www.ozon.ru/category/serebryanye-chasy-39624/"
    },
    {
      "root": "Unknown",
      "name": "Детские украшения",
      "url": "https://www.ozon.ru/category/detskie-yuvelirnye-izdeliya-50024/"
    },
    {
      "root": "Unknown",
      "name": "Запонки и зажимы",
      "url": "https://www.ozon.ru/category/zaponki-yuvelirnye-50016/"
    },
    {
      "root": "Unknown",
      "name": "Сувениры",
      "url": "https://www.ozon.ru/category/suveniry-yuvelirnye-31652/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для волос",
      "url": "https://www.ozon.ru/category/zakolki-dlya-volos-yuvelirnye-50030/"
    },
    {
      "root": "Unknown",
      "name": "Религиозные украшения",
      "url": "https://www.ozon.ru/category/religioznye-yuvelirnye-izdeliya-50025/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 73,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Женские аксессуары",
      "url": "https://www.ozon.ru/category/zhenskie-aksessuary-17000/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для волос",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-volos-zhenskie-17047/"
    },
    {
      "root": "Unknown",
      "name": "Бижутерия",
      "url": "https://www.ozon.ru/category/bizhuternye-ukrasheniya-zhenskie-17022/"
    },
    {
      "root": "Unknown",
      "name": "Галстуки и бабочки",
      "url": "https://www.ozon.ru/category/galstuki-i-babochki-zhenskie-35308/"
    },
    {
      "root": "Unknown",
      "name": "Головные уборы",
      "url": "https://www.ozon.ru/category/golovnye-ubory-zhenskie-17011/"
    },
    {
      "root": "Unknown",
      "name": "Зонты",
      "url": "https://www.ozon.ru/category/zonty-i-chehly-zhenskie-39417/"
    },
    {
      "root": "Unknown",
      "name": "Кошельки, ключницы и визитницы",
      "url": "https://www.ozon.ru/category/koshelki-klyuchnitsy-i-vizitnitsy-zhenskie-17041/"
    },
    {
      "root": "Unknown",
      "name": "Носовые платки",
      "url": "https://www.ozon.ru/category/nosovye-platki-zhenskie-17059/"
    },
    {
      "root": "Unknown",
      "name": "Обложки для документов",
      "url": "https://www.ozon.ru/category/oblozhki-dlya-dokumentov-zhenskie-17058/"
    },
    {
      "root": "Unknown",
      "name": "Очки",
      "url": "https://www.ozon.ru/category/ochki-zhenskie-17018/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки и варежки",
      "url": "https://www.ozon.ru/category/perchatki-i-varezhki-zhenskie-17060/"
    },
    {
      "root": "Unknown",
      "name": "Платки и шарфы",
      "url": "https://www.ozon.ru/category/platki-i-sharfy-zhenskie-17054/"
    },
    {
      "root": "Unknown",
      "name": "Повязки на лицо",
      "url": "https://www.ozon.ru/category/povyazki-na-litso-zhenskie-32990/"
    },
    {
      "root": "Unknown",
      "name": "Ремни, пояса и портупеи",
      "url": "https://www.ozon.ru/category/remni-poyasa-i-portupei-zhenskie-31983/"
    },
    {
      "root": "Unknown",
      "name": "Сумки и рюкзаки",
      "url": "https://www.ozon.ru/category/sumki-zhenskie-17001/"
    },
    {
      "root": "Unknown",
      "name": "Часы и аксессуары",
      "url": "https://www.ozon.ru/category/chasy-zhenskie-17037/"
    },
    {
      "root": "Unknown",
      "name": "Спортивные аксессуары",
      "url": "https://www.ozon.ru/category/sportivnye-aksessuary-zhenskie-33020/"
    },
    {
      "root": "Unknown",
      "name": "Свадебные аксессуары",
      "url": "https://www.ozon.ru/category/svadebnye-aksessuary-32988/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для военной формы",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-voennoy-formy-zhenskie-38006/"
    },
    {
      "root": "Unknown",
      "name": "Мужские аксессуары",
      "url": "https://www.ozon.ru/category/muzhskie-aksessuary-17063/"
    },
    {
      "root": "Unknown",
      "name": "Бижутерия",
      "url": "https://www.ozon.ru/category/bizhuternye-ukrasheniya-muzhskie-17083/"
    },
    {
      "root": "Unknown",
      "name": "Галстуки и бабочки",
      "url": "https://www.ozon.ru/category/galstuki-i-babochki-muzhskie-17102/"
    },
    {
      "root": "Unknown",
      "name": "Головные уборы",
      "url": "https://www.ozon.ru/category/golovnye-ubory-muzhskie-17073/"
    },
    {
      "root": "Unknown",
      "name": "Зонты",
      "url": "https://www.ozon.ru/category/zonty-i-chehly-muzhskie-39418/"
    },
    {
      "root": "Unknown",
      "name": "Кошельки, ключницы и визитницы",
      "url": "https://www.ozon.ru/category/koshelki-klyuchnitsy-i-vizitnitsy-muzhskie-17093/"
    },
    {
      "root": "Unknown",
      "name": "Носовые платки",
      "url": "https://www.ozon.ru/category/nosovye-platki-muzhskie-17103/"
    },
    {
      "root": "Unknown",
      "name": "Обложки для документов",
      "url": "https://www.ozon.ru/category/oblozhki-dlya-dokumentov-muzhskie-17101/"
    },
    {
      "root": "Unknown",
      "name": "Очки",
      "url": "https://www.ozon.ru/category/ochki-muzhskie-17079/"
    },
    {
      "root": "Unknown",
      "name": "Перчатки и варежки",
      "url": "https://www.ozon.ru/category/perchatki-i-varezhki-muzhskie-17104/"
    },
    {
      "root": "Unknown",
      "name": "Платки и шарфы",
      "url": "https://www.ozon.ru/category/platki-i-sharfy-muzhskie-17100/"
    },
    {
      "root": "Unknown",
      "name": "Повязки на лицо",
      "url": "https://www.ozon.ru/category/povyazki-na-litso-muzhskie-33773/"
    },
    {
      "root": "Unknown",
      "name": "Ремни и подтяжки",
      "url": "https://www.ozon.ru/category/remni-i-podtyazhki-muzhskie-31984/"
    },
    {
      "root": "Unknown",
      "name": "Спортивные аксессуары",
      "url": "https://www.ozon.ru/category/sportivnye-aksessuary-33004/"
    },
    {
      "root": "Unknown",
      "name": "Сумки и рюкзаки",
      "url": "https://www.ozon.ru/category/sumki-muzhskie-17064/"
    },
    {
      "root": "Unknown",
      "name": "Часы и аксессуары",
      "url": "https://www.ozon.ru/category/chasy-i-remeshki-muzhskie-17089/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для военной формы",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-voennoy-formy-32933/"
    },
    {
      "root": "Unknown",
      "name": "Детские аксессуары",
      "url": "https://www.ozon.ru/category/detskie-aksessuary-17108/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для девочек",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-devochek-17109/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для мальчиков",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-malchikov-17139/"
    },
    {
      "root": "Unknown",
      "name": "Путешествия",
      "url": "https://www.ozon.ru/category/puteshestviya-8511/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для путешествий",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-puteshestviy-11600/"
    },
    {
      "root": "Unknown",
      "name": "Багаж",
      "url": "https://www.ozon.ru/category/bagazh-7707/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 71,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "PlayStation",
      "url": "https://www.ozon.ru/category/playstation-31719/"
    },
    {
      "root": "Unknown",
      "name": "Игровые консоли",
      "url": "https://www.ozon.ru/category/konsoli-playstation-31751/"
    },
    {
      "root": "Unknown",
      "name": "Игры для PlayStation 5",
      "url": "https://www.ozon.ru/category/igry-dlya-playstation-5-38457/"
    },
    {
      "root": "Unknown",
      "name": "Игры для PlayStation 4",
      "url": "https://www.ozon.ru/category/igry-dlya-playstation-4-38456/"
    },
    {
      "root": "Unknown",
      "name": "Игры для PlayStation 2/3",
      "url": "https://www.ozon.ru/category/igry-dlya-playstation-3-13303/"
    },
    {
      "root": "Unknown",
      "name": "Игры для PlayStation Portable/Vita",
      "url": "https://www.ozon.ru/category/igry-dlya-playstation-portable-13305/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-ps-31752/"
    },
    {
      "root": "Unknown",
      "name": "Nintendo",
      "url": "https://www.ozon.ru/category/nintendo-switch-31721/"
    },
    {
      "root": "Unknown",
      "name": "Консоли",
      "url": "https://www.ozon.ru/category/konsoli-nintendo-switch-31761/"
    },
    {
      "root": "Unknown",
      "name": "Игры для Nintendo Switch",
      "url": "https://www.ozon.ru/category/igry-dlya-nintendo-switch-13309/"
    },
    {
      "root": "Unknown",
      "name": "Игры для Nintendo Wii/3DS",
      "url": "https://www.ozon.ru/category/igry-dlya-nintendo-wii-13310/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-nintendo-switch-31762/"
    },
    {
      "root": "Unknown",
      "name": "Xbox",
      "url": "https://www.ozon.ru/category/xbox-31720/"
    },
    {
      "root": "Unknown",
      "name": "Консоли",
      "url": "https://www.ozon.ru/category/konsoli-xbox-series-x-34802/"
    },
    {
      "root": "Unknown",
      "name": "Игры для Xbox One",
      "url": "https://www.ozon.ru/category/igry-dlya-xbox-one-13307/"
    },
    {
      "root": "Unknown",
      "name": "Игры для Xbox 360",
      "url": "https://www.ozon.ru/category/igry-dlya-xbox-360-13308/"
    },
    {
      "root": "Unknown",
      "name": "Игры для Xbox Series",
      "url": "https://www.ozon.ru/category/igry-dlya-xbox-series-38520/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-xbox-one-31757/"
    },
    {
      "root": "Unknown",
      "name": "Игровые приставки",
      "url": "https://www.ozon.ru/category/igrovye-pristavki-15801/"
    },
    {
      "root": "Unknown",
      "name": "PC",
      "url": "https://www.ozon.ru/category/pc-31718/"
    },
    {
      "root": "Unknown",
      "name": "Компьютерные комплектующие",
      "url": "https://www.ozon.ru/category/kompyuternye-komplektuyushchie-31735/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-pk-31726/"
    },
    {
      "root": "Unknown",
      "name": "Игровые ноутбуки",
      "url": "https://www.ozon.ru/category/igrovye-noutbuki-31292/"
    },
    {
      "root": "Unknown",
      "name": "Игры",
      "url": "https://www.ozon.ru/category/kompyuternye-igry-13313/"
    },
    {
      "root": "Unknown",
      "name": "Mobile gaming",
      "url": "https://www.ozon.ru/category/mobile-gaming-31932/"
    },
    {
      "root": "Unknown",
      "name": "Игровые планшеты",
      "url": "https://www.ozon.ru/category/igrovye-planshety-31928/"
    },
    {
      "root": "Unknown",
      "name": "Геймпады и джойстики",
      "url": "https://www.ozon.ru/category/geympady-i-dzhoystiki-dlya-smartfonov-31933/"
    },
    {
      "root": "Unknown",
      "name": "Игры для ретро консолей",
      "url": "https://www.ozon.ru/category/igry-dlya-pristavok-13301/"
    },
    {
      "root": "Unknown",
      "name": "Ретро-консоли",
      "url": "https://www.ozon.ru/category/retro-konsoli-31722/"
    },
    {
      "root": "Unknown",
      "name": "Игровые картриджи",
      "url": "https://www.ozon.ru/category/igrovye-kartridzhi-15814/"
    },
    {
      "root": "Unknown",
      "name": "Фигурки по видеоиграм",
      "url": "https://www.ozon.ru/category/igrovaya-atributika-1672/"
    },
    {
      "root": "Unknown",
      "name": "Игровые наушники",
      "url": "https://www.ozon.ru/category/igrovye-naushniki-35137/"
    },
    {
      "root": "Unknown",
      "name": "Геймпады",
      "url": "https://www.ozon.ru/category/geympady-15823/"
    },
    {
      "root": "Unknown",
      "name": "Очки виртуальной реальности",
      "url": "https://www.ozon.ru/category/ochki-virtualnoy-realnosti-dlya-igr-15825/"
    },
    {
      "root": "Unknown",
      "name": "Рули и педали",
      "url": "https://www.ozon.ru/category/igrovye-ruli-i-pedali-15829/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для игровых приставок",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-igrovyh-pristavok-15810/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для киберспорта",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-kibersporta-39237/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторы и зарядки",
      "url": "https://www.ozon.ru/category/akkumulyatory-i-zaryadki-dlya-igrovoy-pristavki-15818/"
    },
    {
      "root": "Unknown",
      "name": "Сумки и чехлы",
      "url": "https://www.ozon.ru/category/chehly-dlya-igrovyh-pristavok-15905/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для игровых консолей",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-igrovyh-konsoley-37161/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 148,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Письменные принадлежности",
      "url": "https://www.ozon.ru/category/pismennye-prinadlezhnosti-18015/"
    },
    {
      "root": "Unknown",
      "name": "Ручки",
      "url": "https://www.ozon.ru/category/ruchki-18016/"
    },
    {
      "root": "Unknown",
      "name": "Маркеры",
      "url": "https://www.ozon.ru/category/markery-18019/"
    },
    {
      "root": "Unknown",
      "name": "Карандаши",
      "url": "https://www.ozon.ru/category/karandashi-7193/"
    },
    {
      "root": "Unknown",
      "name": "Фломастеры",
      "url": "https://www.ozon.ru/category/flomastery-18020/"
    },
    {
      "root": "Unknown",
      "name": "Кисти",
      "url": "https://www.ozon.ru/category/kisti-18021/"
    },
    {
      "root": "Unknown",
      "name": "Ластики",
      "url": "https://www.ozon.ru/category/lastiki-18093/"
    },
    {
      "root": "Unknown",
      "name": "Мелки и пастель",
      "url": "https://www.ozon.ru/category/melki-i-pastel-18024/"
    },
    {
      "root": "Unknown",
      "name": "Перья",
      "url": "https://www.ozon.ru/category/perya-18022/"
    },
    {
      "root": "Unknown",
      "name": "Принадлежности по Брайлю",
      "url": "https://www.ozon.ru/category/pismennye-prinadlezhnosti-po-braylyu-37228/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские наборы",
      "url": "https://www.ozon.ru/category/kantselyarskie-nabory-18023/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и расходники для карандашей",
      "url": "https://www.ozon.ru/category/aksessuary-i-rashodniki-dlya-karandashey-30398/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и расходники для ручек",
      "url": "https://www.ozon.ru/category/aksessuary-i-rashodniki-dlya-ruchek-18017/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и расходники для маркеров",
      "url": "https://www.ozon.ru/category/aksessuary-i-rashodniki-dlya-markerov-38003/"
    },
    {
      "root": "Unknown",
      "name": "Бумага",
      "url": "https://www.ozon.ru/category/bumaga-18001/"
    },
    {
      "root": "Unknown",
      "name": "Бумага для печати",
      "url": "https://www.ozon.ru/category/bumaga-dlya-pechati-18002/"
    },
    {
      "root": "Unknown",
      "name": "Фотобумага",
      "url": "https://www.ozon.ru/category/fotobumaga-18005/"
    },
    {
      "root": "Unknown",
      "name": "Черчение и рисование",
      "url": "https://www.ozon.ru/category/bumaga-dlya-chercheniya-i-risovaniya-18008/"
    },
    {
      "root": "Unknown",
      "name": "Альбомы для рисования",
      "url": "https://www.ozon.ru/category/albom-dlya-risovaniya-31475/"
    },
    {
      "root": "Unknown",
      "name": "Стикеры",
      "url": "https://www.ozon.ru/category/stikery-18006/"
    },
    {
      "root": "Unknown",
      "name": "Бумага цветная",
      "url": "https://www.ozon.ru/category/bumaga-tsvetnaya-18013/"
    },
    {
      "root": "Unknown",
      "name": "Бумажная продукция",
      "url": "https://www.ozon.ru/category/bumazhnaya-produktsiya-18025/"
    },
    {
      "root": "Unknown",
      "name": "Тетради",
      "url": "https://www.ozon.ru/category/tetradi-7268/"
    },
    {
      "root": "Unknown",
      "name": "Блокноты",
      "url": "https://www.ozon.ru/category/bloknoty-18026/"
    },
    {
      "root": "Unknown",
      "name": "Еженедельники и ежедневники",
      "url": "https://www.ozon.ru/category/ezhenedelniki-i-ezhednevniki-18028/"
    },
    {
      "root": "Unknown",
      "name": "Дневники",
      "url": "https://www.ozon.ru/category/dnevniki-7208/"
    },
    {
      "root": "Unknown",
      "name": "Анкеты и дневники личные",
      "url": "https://www.ozon.ru/category/dnevniki-lichnye-18027/"
    },
    {
      "root": "Unknown",
      "name": "Записные книжки",
      "url": "https://www.ozon.ru/category/zapisnye-knizhki-18029/"
    },
    {
      "root": "Unknown",
      "name": "Планинги",
      "url": "https://www.ozon.ru/category/planingi-18031/"
    },
    {
      "root": "Unknown",
      "name": "Наклейки",
      "url": "https://www.ozon.ru/category/nakleyki-13821/"
    },
    {
      "root": "Unknown",
      "name": "Закладки",
      "url": "https://www.ozon.ru/category/zakladki-18043/"
    },
    {
      "root": "Unknown",
      "name": "Классные журналы",
      "url": "https://www.ozon.ru/category/klassnye-zhurnaly-7240/"
    },
    {
      "root": "Unknown",
      "name": "Трудовые книжки и удостоверения",
      "url": "https://www.ozon.ru/category/trudovye-knizhki-30659/"
    },
    {
      "root": "Unknown",
      "name": "Телефонные книги",
      "url": "https://www.ozon.ru/category/telefonnye-knigi-18030/"
    },
    {
      "root": "Unknown",
      "name": "Книги учета",
      "url": "https://www.ozon.ru/category/knigi-ucheta-18120/"
    },
    {
      "root": "Unknown",
      "name": "Родословные книги",
      "url": "https://www.ozon.ru/category/rodoslovnye-knigi-15170/"
    },
    {
      "root": "Unknown",
      "name": "Книги пожеланий",
      "url": "https://www.ozon.ru/category/knigi-pozhelaniy-30830/"
    },
    {
      "root": "Unknown",
      "name": "Книги для записи рецептов",
      "url": "https://www.ozon.ru/category/knigi-dlya-zapisi-retseptov-33271/"
    },
    {
      "root": "Unknown",
      "name": "Медкарты и сертификаты",
      "url": "https://www.ozon.ru/category/meditsinskie-karty-32631/"
    },
    {
      "root": "Unknown",
      "name": "Бланки, визитки и сертификаты",
      "url": "https://www.ozon.ru/category/blanki-18011/"
    },
    {
      "root": "Unknown",
      "name": "Календари",
      "url": "https://www.ozon.ru/category/kalendari-30838/"
    },
    {
      "root": "Unknown",
      "name": "Коробки почтовые",
      "url": "https://www.ozon.ru/category/korobki-pochtovye-31911/"
    },
    {
      "root": "Unknown",
      "name": "Конверты",
      "url": "https://www.ozon.ru/category/konverty-18097/"
    },
    {
      "root": "Unknown",
      "name": "Карты мира",
      "url": "https://www.ozon.ru/category/karty-mira-32752/"
    },
    {
      "root": "Unknown",
      "name": "Этикетки",
      "url": "https://www.ozon.ru/category/etiketki-18121/"
    },
    {
      "root": "Unknown",
      "name": "Пленка самоклеящаяся",
      "url": "https://www.ozon.ru/category/plenka-samokleyashchayasya-18117/"
    },
    {
      "root": "Unknown",
      "name": "Папки и файлы",
      "url": "https://www.ozon.ru/category/papki-i-fayly-30106/"
    },
    {
      "root": "Unknown",
      "name": "Папки для бумаги",
      "url": "https://www.ozon.ru/category/papki-dlya-bumagi-1694/"
    },
    {
      "root": "Unknown",
      "name": "Файлы, разделители и сшиватели",
      "url": "https://www.ozon.ru/category/fayly-i-razdeliteli-7190/"
    },
    {
      "root": "Unknown",
      "name": "Пленки для ламинирования",
      "url": "https://www.ozon.ru/category/plenki-dlya-laminirovaniya-15694/"
    },
    {
      "root": "Unknown",
      "name": "Обложки для переплета",
      "url": "https://www.ozon.ru/category/oblozhki-dlya-perepleta-15695/"
    },
    {
      "root": "Unknown",
      "name": "Пружины для переплета",
      "url": "https://www.ozon.ru/category/pruzhiny-dlya-perepleta-15698/"
    },
    {
      "root": "Unknown",
      "name": "Обложки",
      "url": "https://www.ozon.ru/category/oblozhki-7210/"
    },
    {
      "root": "Unknown",
      "name": "Демонстрационные доски",
      "url": "https://www.ozon.ru/category/demonstratsionnye-doski-18095/"
    },
    {
      "root": "Unknown",
      "name": "Маркерные доски",
      "url": "https://www.ozon.ru/category/markernye-doski-18116/"
    },
    {
      "root": "Unknown",
      "name": "Доски для заметок",
      "url": "https://www.ozon.ru/category/probkovye-doski-18096/"
    },
    {
      "root": "Unknown",
      "name": "Доски меловые",
      "url": "https://www.ozon.ru/category/doski-melovye-14022/"
    },
    {
      "root": "Unknown",
      "name": "Флипчарты",
      "url": "https://www.ozon.ru/category/flipcharty-18114/"
    },
    {
      "root": "Unknown",
      "name": "Магнитные доски",
      "url": "https://www.ozon.ru/category/magnitnye-doski-30507/"
    },
    {
      "root": "Unknown",
      "name": "Текстильные доски",
      "url": "https://www.ozon.ru/category/podvesnye-sistemy-1661/"
    },
    {
      "root": "Unknown",
      "name": "Указки",
      "url": "https://www.ozon.ru/category/ukazki-32058/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для досок и флипчартов",
      "url": "https://www.ozon.ru/category/stirateli-dlya-doski-18113/"
    },
    {
      "root": "Unknown",
      "name": "Магниты для досок",
      "url": "https://www.ozon.ru/category/magnity-dlya-dosok-18118/"
    },
    {
      "root": "Unknown",
      "name": "Наборы для досок и флипчартов",
      "url": "https://www.ozon.ru/category/nabory-dlya-dosok-i-flipchartov-18112/"
    },
    {
      "root": "Unknown",
      "name": "Офисные принадлежности",
      "url": "https://www.ozon.ru/category/ofisnye-prinadlezhnosti-30107/"
    },
    {
      "root": "Unknown",
      "name": "Клейкая лента",
      "url": "https://www.ozon.ru/category/kleykaya-lenta-kantselyarskaya-18072/"
    },
    {
      "root": "Unknown",
      "name": "Лупы",
      "url": "https://www.ozon.ru/category/lupy-18039/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские ножницы и ножи",
      "url": "https://www.ozon.ru/category/kantselyarskie-nozhnitsy-i-nozhi-18081/"
    },
    {
      "root": "Unknown",
      "name": "Клей",
      "url": "https://www.ozon.ru/category/kley-18045/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские мелочи",
      "url": "https://www.ozon.ru/category/kantselyarskie-melochi-18032/"
    },
    {
      "root": "Unknown",
      "name": "Степлеры и скобы",
      "url": "https://www.ozon.ru/category/steplery-i-skoby-18053/"
    },
    {
      "root": "Unknown",
      "name": "Лотки и накопители для бумаг",
      "url": "https://www.ozon.ru/category/lotki-i-nakopiteli-dlya-bumag-18079/"
    },
    {
      "root": "Unknown",
      "name": "Коврики на стол",
      "url": "https://www.ozon.ru/category/kovriki-na-stol-18078/"
    },
    {
      "root": "Unknown",
      "name": "Корректоры для текста",
      "url": "https://www.ozon.ru/category/korrektory-dlya-teksta-18071/"
    },
    {
      "root": "Unknown",
      "name": "Корзины для бумаг",
      "url": "https://www.ozon.ru/category/korziny-dlya-bumag-18080/"
    },
    {
      "root": "Unknown",
      "name": "Дыроколы",
      "url": "https://www.ozon.ru/category/dyrokoly-18057/"
    },
    {
      "root": "Unknown",
      "name": "Бейджи и аксессуары",
      "url": "https://www.ozon.ru/category/beydzhi-i-aksessuary-1656/"
    },
    {
      "root": "Unknown",
      "name": "Подставки и визитницы",
      "url": "https://www.ozon.ru/category/nastolnye-podstavki-i-vizitnitsy-18073/"
    },
    {
      "root": "Unknown",
      "name": "Подставки для канцелярии",
      "url": "https://www.ozon.ru/category/podstavki-dlya-karandashey-i-ruchek-18074/"
    },
    {
      "root": "Unknown",
      "name": "Подставки для книг",
      "url": "https://www.ozon.ru/category/podstavki-dlya-knig-7187/"
    },
    {
      "root": "Unknown",
      "name": "Визитницы настольные",
      "url": "https://www.ozon.ru/category/vizitnitsy-18076/"
    },
    {
      "root": "Unknown",
      "name": "Держатели для бумаг",
      "url": "https://www.ozon.ru/category/derzhateli-dlya-bumag-30929/"
    },
    {
      "root": "Unknown",
      "name": "Сменные блоки для визитниц",
      "url": "https://www.ozon.ru/category/smennye-bloki-dlya-vizitnits-30637/"
    },
    {
      "root": "Unknown",
      "name": "Печати и штампы",
      "url": "https://www.ozon.ru/category/pechati-i-shtampy-18063/"
    },
    {
      "root": "Unknown",
      "name": "Штампы",
      "url": "https://www.ozon.ru/category/shtampy-18064/"
    },
    {
      "root": "Unknown",
      "name": "Подушки штемпельные",
      "url": "https://www.ozon.ru/category/podushki-shtempelnye-18069/"
    },
    {
      "root": "Unknown",
      "name": "Краски",
      "url": "https://www.ozon.ru/category/kraski-shtempelnye-18070/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/datery-18066/"
    },
    {
      "root": "Unknown",
      "name": "Печати канцелярские",
      "url": "https://www.ozon.ru/category/pechati-kantselyarskie-18068/"
    },
    {
      "root": "Unknown",
      "name": "Расходные материалы",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-shtempelnye-37301/"
    },
    {
      "root": "Unknown",
      "name": "Калькуляторы",
      "url": "https://www.ozon.ru/category/kalkulyatory-18058/"
    },
    {
      "root": "Unknown",
      "name": "Картриджи для лазерных принтеров",
      "url": "https://www.ozon.ru/category/kartridzhi-dlya-lazernyh-printerov-31920/"
    },
    {
      "root": "Unknown",
      "name": "Картриджи для струйных принтеров",
      "url": "https://www.ozon.ru/category/kartridzhi-dlya-struynyh-printerov-31921/"
    },
    {
      "root": "Unknown",
      "name": "Чертежные принадлежности",
      "url": "https://www.ozon.ru/category/chertezhnye-prinadlezhnosti-18084/"
    },
    {
      "root": "Unknown",
      "name": "Чертежные доски и кульманы",
      "url": "https://www.ozon.ru/category/chertezhnye-doski-i-kulmany-34187/"
    },
    {
      "root": "Unknown",
      "name": "Линейки",
      "url": "https://www.ozon.ru/category/lineyki-18087/"
    },
    {
      "root": "Unknown",
      "name": "Циркули",
      "url": "https://www.ozon.ru/category/tsirkuli-18089/"
    },
    {
      "root": "Unknown",
      "name": "Грифели для циркулей",
      "url": "https://www.ozon.ru/category/grifeli-dlya-tsirkuley-36830/"
    },
    {
      "root": "Unknown",
      "name": "Готовальни",
      "url": "https://www.ozon.ru/category/gotovalni-18090/"
    },
    {
      "root": "Unknown",
      "name": "Угольники",
      "url": "https://www.ozon.ru/category/ugolniki-18085/"
    },
    {
      "root": "Unknown",
      "name": "Транспортиры",
      "url": "https://www.ozon.ru/category/transportiry-18086/"
    },
    {
      "root": "Unknown",
      "name": "Геометрические наборы",
      "url": "https://www.ozon.ru/category/geometricheskie-nabory-18092/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование и принадлежности для торговли",
      "url": "https://www.ozon.ru/category/oborudovanie-dlya-torgovli-32303/"
    },
    {
      "root": "Unknown",
      "name": "Информационное оборудование",
      "url": "https://www.ozon.ru/category/informatsionnoe-oborudovanie-dlya-torgovogo-zala-32304/"
    },
    {
      "root": "Unknown",
      "name": "Этикет-пистолеты и счетчики",
      "url": "https://www.ozon.ru/category/etiket-pistolety-18115/"
    },
    {
      "root": "Unknown",
      "name": "Лототроны и промоящики",
      "url": "https://www.ozon.ru/category/lototrony-promoyashchiki-34888/"
    },
    {
      "root": "Unknown",
      "name": "Корзины и тележки",
      "url": "https://www.ozon.ru/category/korziny-telezhki-dlya-torgovli-34966/"
    },
    {
      "root": "Unknown",
      "name": "Палатки",
      "url": "https://www.ozon.ru/category/torgovye-palatki-37566/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для выкладки",
      "url": "https://www.ozon.ru/category/razdeliteli-i-stellazhi-dlya-torgovli-32307/"
    },
    {
      "root": "Unknown",
      "name": "Контрольные браслеты",
      "url": "https://www.ozon.ru/category/kontrolnye-braslety-37138/"
    },
    {
      "root": "Unknown",
      "name": "Торговые манекены",
      "url": "https://www.ozon.ru/category/torgovye-manekeny-38294/"
    },
    {
      "root": "Unknown",
      "name": "Механические торговые автоматы",
      "url": "https://www.ozon.ru/category/mehanicheskie-torgovye-avtomaty-37187/"
    },
    {
      "root": "Unknown",
      "name": "Упаковочное оборудование для торговли",
      "url": "https://www.ozon.ru/category/stanki-dlya-bumazhnoy-upakovki-38839/"
    },
    {
      "root": "Unknown",
      "name": "Монетницы",
      "url": "https://www.ozon.ru/category/monetnitsa-32306/"
    },
    {
      "root": "Unknown",
      "name": "Макеты телефонов",
      "url": "https://www.ozon.ru/category/makety-telefonov-35950/"
    },
    {
      "root": "Unknown",
      "name": "Полиграфическое оборудование",
      "url": "https://www.ozon.ru/category/poligraficheskoe-oborudovanie-36351/"
    },
    {
      "root": "Unknown",
      "name": "Сублимационная печать",
      "url": "https://www.ozon.ru/category/sublimatsionnaya-pechat-38924/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 65,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Секс игрушки",
      "url": "https://www.ozon.ru/category/ceks-igrushki-9024/"
    },
    {
      "root": "Unknown",
      "name": "Вибраторы и вибромассажеры",
      "url": "https://www.ozon.ru/category/vibratory-i-vibromassazhery-9051/"
    },
    {
      "root": "Unknown",
      "name": "Мастурбаторы",
      "url": "https://www.ozon.ru/category/masturbatory-9036/"
    },
    {
      "root": "Unknown",
      "name": "Фаллоимитаторы",
      "url": "https://www.ozon.ru/category/falloimitatory-9048/"
    },
    {
      "root": "Unknown",
      "name": "Куклы для секса",
      "url": "https://www.ozon.ru/category/kukly-dlya-seksa-9034/"
    },
    {
      "root": "Unknown",
      "name": "Плаги и пробки анальные",
      "url": "https://www.ozon.ru/category/plagi-probki-9040/"
    },
    {
      "root": "Unknown",
      "name": "Анальные стимуляторы",
      "url": "https://www.ozon.ru/category/analnye-stimulyatory-9025/"
    },
    {
      "root": "Unknown",
      "name": "Вагинальные шарики и тренажеры",
      "url": "https://www.ozon.ru/category/vaginalnye-shariki-i-trenazhery-9029/"
    },
    {
      "root": "Unknown",
      "name": "Страпоны",
      "url": "https://www.ozon.ru/category/strapony-9045/"
    },
    {
      "root": "Unknown",
      "name": "Насадки и удлинители",
      "url": "https://www.ozon.ru/category/nasadki-na-chlen-9038/"
    },
    {
      "root": "Unknown",
      "name": "Эрекционное кольцо, утяжка и лассо",
      "url": "https://www.ozon.ru/category/erektsionnye-koltsa-9050/"
    },
    {
      "root": "Unknown",
      "name": "Эротические помпы",
      "url": "https://www.ozon.ru/category/vakuumnye-pompy-9030/"
    },
    {
      "root": "Unknown",
      "name": "Эротическое белье и костюмы",
      "url": "https://www.ozon.ru/category/eroticheskoe-bele-i-kostyumy-9015/"
    },
    {
      "root": "Unknown",
      "name": "Эротическое белье",
      "url": "https://www.ozon.ru/category/eroticheskoe-bele-9020/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы для ролевых игр",
      "url": "https://www.ozon.ru/category/kostyumy-dlya-rolevyh-igr-9022/"
    },
    {
      "root": "Unknown",
      "name": "Платья гоу-гоу",
      "url": "https://www.ozon.ru/category/platya-gou-gou-9067/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/poyasa-dlya-chulok-9059/"
    },
    {
      "root": "Unknown",
      "name": "Товары для БДСМ",
      "url": "https://www.ozon.ru/category/tovary-dlya-bdsm-9056/"
    },
    {
      "root": "Unknown",
      "name": "Наборы",
      "url": "https://www.ozon.ru/category/nabory-dlya-bdsm-32957/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-vzroslyh-9057/"
    },
    {
      "root": "Unknown",
      "name": "Наручники и фиксаторы",
      "url": "https://www.ozon.ru/category/naruchniki-i-fiksatory-dlya-bdsm-32964/"
    },
    {
      "root": "Unknown",
      "name": "Расширители",
      "url": "https://www.ozon.ru/category/rasshiriteli-uretralnye-32014/"
    },
    {
      "root": "Unknown",
      "name": "Плетки и стеки",
      "url": "https://www.ozon.ru/category/pletki-i-steki-32963/"
    },
    {
      "root": "Unknown",
      "name": "Секс-машины",
      "url": "https://www.ozon.ru/category/seks-mashiny-38106/"
    },
    {
      "root": "Unknown",
      "name": "Мебель и подушки для секса",
      "url": "https://www.ozon.ru/category/mebel-dlya-seksa-32978/"
    },
    {
      "root": "Unknown",
      "name": "Костюмы",
      "url": "https://www.ozon.ru/category/kostyumy-dlya-bdsm-32958/"
    },
    {
      "root": "Unknown",
      "name": "Интимная косметика",
      "url": "https://www.ozon.ru/category/intimnaya-kosmetika-9005/"
    },
    {
      "root": "Unknown",
      "name": "Возбуждающие средства и пролонгаторы",
      "url": "https://www.ozon.ru/category/vozbuzhdayushchie-sredstva-9007/"
    },
    {
      "root": "Unknown",
      "name": "Парфюмерия с феромонами",
      "url": "https://www.ozon.ru/category/duhi-s-feromonami-9006/"
    },
    {
      "root": "Unknown",
      "name": "Уход и хранение секс-игрушек",
      "url": "https://www.ozon.ru/category/sredstva-dlya-chistki-igrushek-9012/"
    },
    {
      "root": "Unknown",
      "name": "Презервативы и лубриканты",
      "url": "https://www.ozon.ru/category/prezervativy-i-lubrikanty-32959/"
    },
    {
      "root": "Unknown",
      "name": "Презервативы",
      "url": "https://www.ozon.ru/category/prezervativy-32226/"
    },
    {
      "root": "Unknown",
      "name": "Лубриканты",
      "url": "https://www.ozon.ru/category/lubrikanty-32227/"
    },
    {
      "root": "Unknown",
      "name": "Эротические сувениры и игры",
      "url": "https://www.ozon.ru/category/eroticheskie-suveniry-9061/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 74,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Коллекционирование",
      "url": "https://www.ozon.ru/category/kollektsionirovanie-13755/"
    },
    {
      "root": "Unknown",
      "name": "Банкноты",
      "url": "https://www.ozon.ru/category/banknoty-13778/"
    },
    {
      "root": "Unknown",
      "name": "Билеты",
      "url": "https://www.ozon.ru/category/kollektsionnye-bilety-37461/"
    },
    {
      "root": "Unknown",
      "name": "Жетоны",
      "url": "https://www.ozon.ru/category/ekzonumiya-13790/"
    },
    {
      "root": "Unknown",
      "name": "Журналы и наклейки",
      "url": "https://www.ozon.ru/category/kollektsionirovanie-zhurnalov-i-nakleek-13813/"
    },
    {
      "root": "Unknown",
      "name": "Значки",
      "url": "https://www.ozon.ru/category/znachki-13795/"
    },
    {
      "root": "Unknown",
      "name": "Карточки",
      "url": "https://www.ozon.ru/category/kartochki-kollektsionnye-32948/"
    },
    {
      "root": "Unknown",
      "name": "Насекомые",
      "url": "https://www.ozon.ru/category/entomologiya-37448/"
    },
    {
      "root": "Unknown",
      "name": "Куклы",
      "url": "https://www.ozon.ru/category/kukly-kollektsionnye-39578/"
    },
    {
      "root": "Unknown",
      "name": "Марки",
      "url": "https://www.ozon.ru/category/marki-13757/"
    },
    {
      "root": "Unknown",
      "name": "Минералы и окаменелости",
      "url": "https://www.ozon.ru/category/kollektsionirovanie-mineralov-34667/"
    },
    {
      "root": "Unknown",
      "name": "Модели и фигурки",
      "url": "https://www.ozon.ru/category/kollektsionirovanie-modeley-13812/"
    },
    {
      "root": "Unknown",
      "name": "Монеты",
      "url": "https://www.ozon.ru/category/monety-13765/"
    },
    {
      "root": "Unknown",
      "name": "Наборы",
      "url": "https://www.ozon.ru/category/kollektsionnye-nabory-13819/"
    },
    {
      "root": "Unknown",
      "name": "Наперстки",
      "url": "https://www.ozon.ru/category/kollektsionirovanie-naperstkov-13807/"
    },
    {
      "root": "Unknown",
      "name": "Открытки и конверты",
      "url": "https://www.ozon.ru/category/filokartiya-13799/"
    },
    {
      "root": "Unknown",
      "name": "Средства для ухода",
      "url": "https://www.ozon.ru/category/uhod-za-kollektsiyami-39577/"
    },
    {
      "root": "Unknown",
      "name": "Хранение коллекций",
      "url": "https://www.ozon.ru/category/holdery-13772/"
    },
    {
      "root": "Unknown",
      "name": "Ценные бумаги",
      "url": "https://www.ozon.ru/category/tsennye-bumagi-13786/"
    },
    {
      "root": "Unknown",
      "name": "Этикетки и пробки",
      "url": "https://www.ozon.ru/category/etiketki-butylki-probki-39189/"
    },
    {
      "root": "Unknown",
      "name": "Живопись и графика",
      "url": "https://www.ozon.ru/category/antikvarnye-plakaty-gravyury-i-otkrytki-8027/"
    },
    {
      "root": "Unknown",
      "name": "Плакаты, журналы и фотографии",
      "url": "https://www.ozon.ru/category/plakaty-i-postery-8032/"
    },
    {
      "root": "Unknown",
      "name": "Посуда и утварь",
      "url": "https://www.ozon.ru/category/posuda-i-servirovka-8001/"
    },
    {
      "root": "Unknown",
      "name": "Посуда для чая и кофе",
      "url": "https://www.ozon.ru/category/vse-dlya-chaya-i-kofe-8002/"
    },
    {
      "root": "Unknown",
      "name": "Предметы сервировки",
      "url": "https://www.ozon.ru/category/servirovka-stola-8004/"
    },
    {
      "root": "Unknown",
      "name": "Сервизы",
      "url": "https://www.ozon.ru/category/servizy-8045/"
    },
    {
      "root": "Unknown",
      "name": "Кухонная утварь",
      "url": "https://www.ozon.ru/category/vintazhnye-aksessuary-dlya-hraneniya-produktov-8008/"
    },
    {
      "root": "Unknown",
      "name": "Предметы военной истории",
      "url": "https://www.ozon.ru/category/voennaya-atributika-37035/"
    },
    {
      "root": "Unknown",
      "name": "Предметы интерьера",
      "url": "https://www.ozon.ru/category/predmety-interera-8009/"
    },
    {
      "root": "Unknown",
      "name": "Скульптуры и статуэтки",
      "url": "https://www.ozon.ru/category/skulptury-i-statuetki-8016/"
    },
    {
      "root": "Unknown",
      "name": "Вазы, кашпо",
      "url": "https://www.ozon.ru/category/antikvarnye-vazy-8010/"
    },
    {
      "root": "Unknown",
      "name": "Элементы интерьера",
      "url": "https://www.ozon.ru/category/elementy-interera-8019/"
    },
    {
      "root": "Unknown",
      "name": "Освещение",
      "url": "https://www.ozon.ru/category/svetilniki-i-lampy-8015/"
    },
    {
      "root": "Unknown",
      "name": "Предметы быта",
      "url": "https://www.ozon.ru/category/antikvarnye-predmety-byta-39592/"
    },
    {
      "root": "Unknown",
      "name": "Игрушки и игры",
      "url": "https://www.ozon.ru/category/igrushki-8037/"
    },
    {
      "root": "Unknown",
      "name": "Бытовые товары",
      "url": "https://www.ozon.ru/category/antikvarnye-bytovye-tovary-39593/"
    },
    {
      "root": "Unknown",
      "name": "Украшения",
      "url": "https://www.ozon.ru/category/ukrasheniya-vintazhnye-8080/"
    },
    {
      "root": "Unknown",
      "name": "Часы наручные",
      "url": "https://www.ozon.ru/category/karmannye-chasy-antikvarnye-30703/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярия",
      "url": "https://www.ozon.ru/category/antikvarnye-kantselyarskie-tovary-8038/"
    },
    {
      "root": "Unknown",
      "name": "Приборы и инструменты",
      "url": "https://www.ozon.ru/category/pribory-i-instrumenty-8040/"
    },
    {
      "root": "Unknown",
      "name": "Галантерея",
      "url": "https://www.ozon.ru/category/galantereya-8026/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения",
      "url": "https://www.ozon.ru/category/tovary-dlya-kureniya-8042/"
    },
    {
      "root": "Unknown",
      "name": "Религиозная атрибутика",
      "url": "https://www.ozon.ru/category/starinnye-ikony-32189/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 63,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Электронные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-32060/"
    },
    {
      "root": "Unknown",
      "name": "Электронные сертификаты OZON",
      "url": "https://www.ozon.ru/category/elektronnye-sertifikaty-ozon-41317/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/sertifikaty-na-yuvelirnye-ukrasheniya-40279/"
    },
    {
      "root": "Unknown",
      "name": "Одежда, обувь, аксессуары",
      "url": "https://www.ozon.ru/category/sertifikaty-na-odezhdu-obuv-aksessuary-40284/"
    },
    {
      "root": "Unknown",
      "name": "Другое",
      "url": "https://www.ozon.ru/category/drugie-sertifikaty-40291/"
    },
    {
      "root": "Unknown",
      "name": "Благотворительные сертификаты",
      "url": "https://www.ozon.ru/category/blagotvoritelnye-elektronnye-sertifikaty-39219/"
    },
    {
      "root": "Unknown",
      "name": "Детям и взрослым",
      "url": "https://www.ozon.ru/category/blagotvoritelnye-elektronnye-sertifikaty-37233/"
    },
    {
      "root": "Unknown",
      "name": "Животным",
      "url": "https://www.ozon.ru/category/pomoshch-zhivotnym-39220/"
    },
    {
      "root": "Unknown",
      "name": "Природоохранным организациям",
      "url": "https://www.ozon.ru/category/blagotvoritelnyy-vznos-v-pomoshch-prirodoohrannym-organizatsiyam-42368/"
    },
    {
      "root": "Unknown",
      "name": "Сложные жизненные ситуации",
      "url": "https://www.ozon.ru/category/elektronnye-sertifikaty-pomoshchi-39945/"
    },
    {
      "root": "Unknown",
      "name": "Мобильная связь",
      "url": "https://www.ozon.ru/category/mobilnaya-svyaz-40285/"
    },
    {
      "root": "Unknown",
      "name": "Мобильные тарифы eSIM",
      "url": "https://www.ozon.ru/category/mobilnye-tarify-esim-37457/"
    },
    {
      "root": "Unknown",
      "name": "Онлайн-подписки",
      "url": "https://www.ozon.ru/category/podpiski-na-filmy-i-muzyku-35607/"
    },
    {
      "root": "Unknown",
      "name": "Музыка",
      "url": "https://www.ozon.ru/category/muzykalnye-podpiski-34045/"
    },
    {
      "root": "Unknown",
      "name": "Онлайн-кинотеатры",
      "url": "https://www.ozon.ru/category/podpiski-na-onlayn-kinoteatry-32061/"
    },
    {
      "root": "Unknown",
      "name": "Электронные и аудиокниги",
      "url": "https://www.ozon.ru/category/podpiski-na-knigi-i-audioknigi-34453/"
    },
    {
      "root": "Unknown",
      "name": "Подписки на нейросети",
      "url": "https://www.ozon.ru/category/podpiski-na-neyroseti-41318/"
    },
    {
      "root": "Unknown",
      "name": "Игры и игровые подписки",
      "url": "https://www.ozon.ru/category/tsifrovye-igry-i-igrovye-podpiski-35606/"
    },
    {
      "root": "Unknown",
      "name": "Игровая валюта",
      "url": "https://www.ozon.ru/category/igrovaya-valyuta-34048/"
    },
    {
      "root": "Unknown",
      "name": "PlayStation",
      "url": "https://www.ozon.ru/category/dopolneniya-dlya-igr-i-podpiski-na-playstation-37304/"
    },
    {
      "root": "Unknown",
      "name": "Xbox",
      "url": "https://www.ozon.ru/category/tsifrovye-igry-i-podpiski-xbox-37303/"
    },
    {
      "root": "Unknown",
      "name": "Steam",
      "url": "https://www.ozon.ru/category/tsifrovye-igry-i-podpiski-dlya-steam-40290/"
    },
    {
      "root": "Unknown",
      "name": "Nintendo",
      "url": "https://www.ozon.ru/category/dopolneniya-dlya-igr-i-podpiski-na-nintendo-37306/"
    },
    {
      "root": "Unknown",
      "name": "PC",
      "url": "https://www.ozon.ru/category/tsifrovye-igry-i-podpiski-dlya-pc-37305/"
    },
    {
      "root": "Unknown",
      "name": "Мобильные платформы",
      "url": "https://www.ozon.ru/category/tsifrovye-igry-dlya-mobilnyh-platform-39596/"
    },
    {
      "root": "Unknown",
      "name": "Программное обеспечение",
      "url": "https://www.ozon.ru/category/antivirusy-i-programmnoe-obespechenie-32086/"
    },
    {
      "root": "Unknown",
      "name": "Антивирусы и безопасность",
      "url": "https://www.ozon.ru/category/antivirusy-32647/"
    },
    {
      "root": "Unknown",
      "name": "Операционные системы и приложения",
      "url": "https://www.ozon.ru/category/prikladnye-i-sistemnye-programmy-32656/"
    },
    {
      "root": "Unknown",
      "name": "Облачные хранилища",
      "url": "https://www.ozon.ru/category/oblachnye-hranilishcha-34872/"
    },
    {
      "root": "Unknown",
      "name": "Электронные лотерейные билеты",
      "url": "https://www.ozon.ru/category/elektronnye-lotereynye-bilety-39391/"
    },
    {
      "root": "Unknown",
      "name": "Услуги",
      "url": "https://www.ozon.ru/category/meditsinskie-uslugi-38022/"
    },
    {
      "root": "Unknown",
      "name": "Сервисные услуги",
      "url": "https://www.ozon.ru/category/servisnye-uslugi-38310/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 48,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-36861/"
    },
    {
      "root": "Unknown",
      "name": "Средства для стирки",
      "url": "https://www.ozon.ru/category/sredstva-dlya-stirki-14580/"
    },
    {
      "root": "Unknown",
      "name": "Чистящие средства",
      "url": "https://www.ozon.ru/category/chistyashchie-sredstva-14587/"
    },
    {
      "root": "Unknown",
      "name": "Средства для посудомоечных машин",
      "url": "https://www.ozon.ru/category/sredstva-dlya-posudomoechnyh-mashin-32310/"
    },
    {
      "root": "Unknown",
      "name": "Средства для мытья посуды",
      "url": "https://www.ozon.ru/category/sredstva-dlya-mytya-posudy-14591/"
    },
    {
      "root": "Unknown",
      "name": "Для бытовой техники",
      "url": "https://www.ozon.ru/category/sredstva-dlya-uhoda-za-bytovoy-tehnikoy-14573/"
    },
    {
      "root": "Unknown",
      "name": "Освежители воздуха и нейтрализаторы запахов",
      "url": "https://www.ozon.ru/category/osvezhiteli-i-aromatizatory-14579/"
    },
    {
      "root": "Unknown",
      "name": "Защита от насекомых",
      "url": "https://www.ozon.ru/category/sredstva-ot-nasekomyh-34955/"
    },
    {
      "root": "Unknown",
      "name": "Средства от грызунов",
      "url": "https://www.ozon.ru/category/sredstva-ot-gryzunov-34961/"
    },
    {
      "root": "Unknown",
      "name": "Личная гигиена",
      "url": "https://www.ozon.ru/category/lichnaya-gigiena-6310/"
    },
    {
      "root": "Unknown",
      "name": "Гигиена полости рта",
      "url": "https://www.ozon.ru/category/gigiena-polosti-rta-6318/"
    },
    {
      "root": "Unknown",
      "name": "Гигиена тела",
      "url": "https://www.ozon.ru/category/tovary-dlya-gigieny-tela-36848/"
    },
    {
      "root": "Unknown",
      "name": "Уход за волосами",
      "url": "https://www.ozon.ru/category/tovary-dlya-uhoda-za-volosami-36847/"
    },
    {
      "root": "Unknown",
      "name": "Интимная гигиена",
      "url": "https://www.ozon.ru/category/intimnaya-gigiena-32177/"
    },
    {
      "root": "Unknown",
      "name": "Товары для мужского бритья",
      "url": "https://www.ozon.ru/category/tovary-dlya-britya-36855/"
    },
    {
      "root": "Unknown",
      "name": "Детская гигиена",
      "url": "https://www.ozon.ru/category/tovary-dlya-detskoy-gigieny-36849/"
    },
    {
      "root": "Unknown",
      "name": "Ватно-бумажная продукция",
      "url": "https://www.ozon.ru/category/bumazhnaya-produktsiya-dlya-doma-14854/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 52,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Музыка",
      "url": "https://www.ozon.ru/category/muzyka-34944/"
    },
    {
      "root": "Unknown",
      "name": "Детская музыка",
      "url": "https://www.ozon.ru/category/detskaya-muzyka-13173/"
    },
    {
      "root": "Unknown",
      "name": "Поп-музыка",
      "url": "https://www.ozon.ru/category/pop-muzyka-13101/"
    },
    {
      "root": "Unknown",
      "name": "Рок",
      "url": "https://www.ozon.ru/category/rok-13108/"
    },
    {
      "root": "Unknown",
      "name": "Джаз и блюз",
      "url": "https://www.ozon.ru/category/dzhaz-i-blyuz-13160/"
    },
    {
      "root": "Unknown",
      "name": "Электронная музыка",
      "url": "https://www.ozon.ru/category/elektronnaya-muzyka-13138/"
    },
    {
      "root": "Unknown",
      "name": "Метал",
      "url": "https://www.ozon.ru/category/metal-38030/"
    },
    {
      "root": "Unknown",
      "name": "Рэп и R&B",
      "url": "https://www.ozon.ru/category/rep-i-r-b-13133/"
    },
    {
      "root": "Unknown",
      "name": "Музыка мира",
      "url": "https://www.ozon.ru/category/muzyka-mira-13181/"
    },
    {
      "root": "Unknown",
      "name": "Саундтреки",
      "url": "https://www.ozon.ru/category/saundtreki-13176/"
    },
    {
      "root": "Unknown",
      "name": "Классическая музыка",
      "url": "https://www.ozon.ru/category/klassicheskaya-muzyka-13148/"
    },
    {
      "root": "Unknown",
      "name": "Авторская песня",
      "url": "https://www.ozon.ru/category/avtorskaya-pesnya-13174/"
    },
    {
      "root": "Unknown",
      "name": "Романс и шансон",
      "url": "https://www.ozon.ru/category/shanson-13175/"
    },
    {
      "root": "Unknown",
      "name": "Видео",
      "url": "https://www.ozon.ru/category/video-13000/"
    },
    {
      "root": "Unknown",
      "name": "Документальные фильмы",
      "url": "https://www.ozon.ru/category/dokumentalnye-filmy-13041/"
    },
    {
      "root": "Unknown",
      "name": "Художественные фильмы",
      "url": "https://www.ozon.ru/category/hudozhestvennye-filmy-13001/"
    },
    {
      "root": "Unknown",
      "name": "Мультфильмы",
      "url": "https://www.ozon.ru/category/multfilmy-13033/"
    },
    {
      "root": "Unknown",
      "name": "Сериалы",
      "url": "https://www.ozon.ru/category/serialy-13021/"
    },
    {
      "root": "Unknown",
      "name": "Концерты, клипы и театральные постановки",
      "url": "https://www.ozon.ru/category/kontserty-myuzikly-videoklipy-13064/"
    },
    {
      "root": "Unknown",
      "name": "Телевизионные программы и видеоуроки",
      "url": "https://www.ozon.ru/category/televizionnye-programmy-i-videouroki-13053/"
    },
    {
      "root": "Unknown",
      "name": "Виниловые пластинки",
      "url": "https://www.ozon.ru/category/vinilovye-plastinki-31667/"
    }
  ]
}

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 41,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для электронных сигарет и систем нагревания",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-sistemy-nagrevaniya-31917/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для электронных сигарет",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-elektronnyh-sigaret-35671/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для систем нагревания",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-sistem-nagrevaniya-15959/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения",
      "url": "https://www.ozon.ru/category/tovary-dlya-kureniya-32628/"
    },
    {
      "root": "Unknown",
      "name": "Зажигалки, спички и аксессуары",
      "url": "https://www.ozon.ru/category/zazhigalki-i-aksessuary-35663/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для курения",
      "url": "https://www.ozon.ru/category/tovary-dlya-samokrutok-34696/"
    },
    {
      "root": "Unknown",
      "name": "Для сигар",
      "url": "https://www.ozon.ru/category/dlya-sigar-39263/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и комплектующие для кальянов",
      "url": "https://www.ozon.ru/category/kalyany-i-aksessuary-32629/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-kalyana-39358/"
    },
    {
      "root": "Unknown",
      "name": "Уголь, розжиг и плитка",
      "url": "https://www.ozon.ru/category/ugol-rozzhig-plitka-dlya-kalyana-39356/"
    }
  ]
}

## Raw payload: Electronics 196 links

```json
{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 196,
  "categories": [
    {
      "root": "Unknown",
      "name": "Ozon fresh",
      "url": "https://www.ozon.ru/category/supermarket-25000/"
    },
    {
      "root": "Unknown",
      "name": "Одежда",
      "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"
    },
    {
      "root": "Unknown",
      "name": "Электроника",
      "url": "https://www.ozon.ru/category/elektronika-15500/"
    },
    {
      "root": "Unknown",
      "name": "Дом и сад",
      "url": "https://www.ozon.ru/category/dom-i-sad-14500/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Обувь",
      "url": "https://www.ozon.ru/category/obuv-17777/"
    },
    {
      "root": "Unknown",
      "name": "Детские товары",
      "url": "https://www.ozon.ru/category/detskie-tovary-7000/"
    },
    {
      "root": "Unknown",
      "name": "Красота и здоровье",
      "url": "https://www.ozon.ru/category/krasota-i-zdorove-6500/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая техника",
      "url": "https://www.ozon.ru/category/bytovaya-tehnika-10500/"
    },
    {
      "root": "Unknown",
      "name": "Спорт и отдых",
      "url": "https://www.ozon.ru/category/sport-i-otdyh-11000/"
    },
    {
      "root": "Unknown",
      "name": "Строительство и ремонт",
      "url": "https://www.ozon.ru/category/stroitelstvo-i-remont-9700/"
    },
    {
      "root": "Unknown",
      "name": "Продукты питания",
      "url": "https://www.ozon.ru/category/produkty-pitaniya-9200/"
    },
    {
      "root": "Unknown",
      "name": "Аптека",
      "url": "https://www.ozon.ru/category/apteka-6000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для животных",
      "url": "https://www.ozon.ru/category/tovary-dlya-zhivotnyh-12300/"
    },
    {
      "root": "Unknown",
      "name": "Книги",
      "url": "https://www.ozon.ru/category/knigi-16500/"
    },
    {
      "root": "Unknown",
      "name": "Туризм, рыбалка, охота",
      "url": "https://www.ozon.ru/category/ohota-rybalka-turizm-33332/"
    },
    {
      "root": "Unknown",
      "name": "Автотовары",
      "url": "https://www.ozon.ru/category/avtotovary-8500/"
    },
    {
      "root": "Unknown",
      "name": "Мебель",
      "url": "https://www.ozon.ru/category/mebel-15000/"
    },
    {
      "root": "Unknown",
      "name": "Хобби и творчество",
      "url": "https://www.ozon.ru/category/hobbi-i-tvorchestvo-13500/"
    },
    {
      "root": "Unknown",
      "name": "Ювелирные украшения",
      "url": "https://www.ozon.ru/category/yuvelirnye-ukrasheniya-50001/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-7697/"
    },
    {
      "root": "Unknown",
      "name": "Игры и консоли",
      "url": "https://www.ozon.ru/category/igry-i-soft-13300/"
    },
    {
      "root": "Unknown",
      "name": "Канцелярские товары",
      "url": "https://www.ozon.ru/category/kantselyarskie-tovary-18000/"
    },
    {
      "root": "Unknown",
      "name": "Товары для взрослых",
      "url": "https://www.ozon.ru/category/tovary-dlya-vzroslyh-9000/"
    },
    {
      "root": "Unknown",
      "name": "Антиквариат и коллекционирование",
      "url": "https://www.ozon.ru/category/antikvariat-vintazh-iskusstvo-8000/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые товары",
      "url": "https://www.ozon.ru/category/tsifrovye-tovary-32056/"
    },
    {
      "root": "Unknown",
      "name": "Подарочные сертификаты OZON",
      "url": "https://www.ozon.ru/category/podarochnye-sertifikaty-37234/"
    },
    {
      "root": "Unknown",
      "name": "Бытовая химия и гигиена",
      "url": "https://www.ozon.ru/category/bytovaya-himiya-14572/"
    },
    {
      "root": "Unknown",
      "name": "Музыка и видео",
      "url": "https://www.ozon.ru/category/muzyka-i-video-13100/"
    },
    {
      "root": "Unknown",
      "name": "Автомобили",
      "url": "https://www.ozon.ru/category/avtomobili-39803/"
    },
    {
      "root": "Unknown",
      "name": "Товары для курения и аксессуары",
      "url": "https://www.ozon.ru/category/elektronnye-sigarety-i-tovary-dlya-kureniya-35659/"
    },
    {
      "root": "Unknown",
      "name": "Телефоны и смарт-часы",
      "url": "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/"
    },
    {
      "root": "Unknown",
      "name": "Смартфоны",
      "url": "https://www.ozon.ru/category/smartfony-15502/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для смартфонов и телефонов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-telefonov-15511/"
    },
    {
      "root": "Unknown",
      "name": "Смарт-часы",
      "url": "https://www.ozon.ru/category/umnye-chasy-15516/"
    },
    {
      "root": "Unknown",
      "name": "Фитнес-браслеты",
      "url": "https://www.ozon.ru/category/fitnes-braslety-15519/"
    },
    {
      "root": "Unknown",
      "name": "Ремешки для смарт-часов и фитнес-браслетов",
      "url": "https://www.ozon.ru/category/remeshki-dlya-smart-chasov-15517/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для смарт-часов и фитнес-браслетов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-umnyh-chasov-i-fitnes-brasletov-30739/"
    },
    {
      "root": "Unknown",
      "name": "Мобильные телефоны",
      "url": "https://www.ozon.ru/category/mobilnye-telefony-15503/"
    },
    {
      "root": "Unknown",
      "name": "SIM-карты",
      "url": "https://www.ozon.ru/category/sim-karty-15514/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-smartfonov-31566/"
    },
    {
      "root": "Unknown",
      "name": "Проводные и радиотелефоны",
      "url": "https://www.ozon.ru/category/dect-telefony-15504/"
    },
    {
      "root": "Unknown",
      "name": "Ноутбуки, планшеты и электронные книги",
      "url": "https://www.ozon.ru/category/noutbuki-planshety-i-elektronnye-knigi-8730/"
    },
    {
      "root": "Unknown",
      "name": "Ноутбуки",
      "url": "https://www.ozon.ru/category/noutbuki-15692/"
    },
    {
      "root": "Unknown",
      "name": "Игровые ноутбуки",
      "url": "https://www.ozon.ru/category/igrovye-noutbuki-15821/"
    },
    {
      "root": "Unknown",
      "name": "Планшеты",
      "url": "https://www.ozon.ru/category/planshety-15525/"
    },
    {
      "root": "Unknown",
      "name": "Электронные книги",
      "url": "https://www.ozon.ru/category/elektronnye-knigi-15526/"
    },
    {
      "root": "Unknown",
      "name": "Графические планшеты",
      "url": "https://www.ozon.ru/category/graficheskie-planshety-15745/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы и подставки для планшетов",
      "url": "https://www.ozon.ru/category/chehly-dlya-planshetov-15893/"
    },
    {
      "root": "Unknown",
      "name": "Стилусы",
      "url": "https://www.ozon.ru/category/stilusy-dlya-planshetov-15932/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для ноутбуков",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-noutbukov-15693/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-noutbukov-31902/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторы для ноутбуков",
      "url": "https://www.ozon.ru/category/akkumulyatory-dlya-noutbukov-15885/"
    },
    {
      "root": "Unknown",
      "name": "Зарядные устройства",
      "url": "https://www.ozon.ru/category/zaryadnye-ustroystva-dlya-noutbukov-15924/"
    },
    {
      "root": "Unknown",
      "name": "Чехлы для электронных книг",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-elektronnyh-knig-15895/"
    },
    {
      "root": "Unknown",
      "name": "Переводчики и словари",
      "url": "https://www.ozon.ru/category/elektronnye-perevodchiki-i-slovari-1646/"
    },
    {
      "root": "Unknown",
      "name": "Оптические приборы",
      "url": "https://www.ozon.ru/category/opticheskie-pribory-15984/"
    },
    {
      "root": "Unknown",
      "name": "Телескопы",
      "url": "https://www.ozon.ru/category/teleskopy-15985/"
    },
    {
      "root": "Unknown",
      "name": "Микроскопы",
      "url": "https://www.ozon.ru/category/mikroskopy-15986/"
    },
    {
      "root": "Unknown",
      "name": "Окуляры",
      "url": "https://www.ozon.ru/category/okulyary-dlya-teleskopov-15988/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для телескопов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-teleskopov-15987/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для микроскопов",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-mikroskopov-16010/"
    },
    {
      "root": "Unknown",
      "name": "Наушники и аудиотехника",
      "url": "https://www.ozon.ru/category/audiotehnika-15543/"
    },
    {
      "root": "Unknown",
      "name": "Наушники",
      "url": "https://www.ozon.ru/category/naushniki-15547/"
    },
    {
      "root": "Unknown",
      "name": "Беспроводные колонки",
      "url": "https://www.ozon.ru/category/portativnaya-akustika-15588/"
    },
    {
      "root": "Unknown",
      "name": "Умные колонки",
      "url": "https://www.ozon.ru/category/umnye-kolonki-31337/"
    },
    {
      "root": "Unknown",
      "name": "Акустические системы",
      "url": "https://www.ozon.ru/category/akustika-i-kolonki-15584/"
    },
    {
      "root": "Unknown",
      "name": "Студийное и сценическое оборудование",
      "url": "https://www.ozon.ru/category/studiynoe-i-stsenicheskoe-oborudovanie-15937/"
    },
    {
      "root": "Unknown",
      "name": "Микрофоны",
      "url": "https://www.ozon.ru/category/mikrofony-15556/"
    },
    {
      "root": "Unknown",
      "name": "Рации и радиостанции",
      "url": "https://www.ozon.ru/category/ratsii-i-radiostantsii-8753/"
    },
    {
      "root": "Unknown",
      "name": "Радиоприемники",
      "url": "https://www.ozon.ru/category/radiopriemniki-15563/"
    },
    {
      "root": "Unknown",
      "name": "Виниловые проигрыватели и аксессуары",
      "url": "https://www.ozon.ru/category/vinilovye-proigryvateli-15572/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для наушников",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-naushnikov-1740/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для аудиотехники",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-audiotehniki-15607/"
    },
    {
      "root": "Unknown",
      "name": "Усилители, ресиверы и ЦАПы",
      "url": "https://www.ozon.ru/category/usiliteli-resivery-i-tsapy-15593/"
    },
    {
      "root": "Unknown",
      "name": "MP3-плееры",
      "url": "https://www.ozon.ru/category/mp3-pleery-15544/"
    },
    {
      "root": "Unknown",
      "name": "Диктофоны",
      "url": "https://www.ozon.ru/category/diktofony-15561/"
    },
    {
      "root": "Unknown",
      "name": "Комплектующие для ПК",
      "url": "https://www.ozon.ru/category/kompyuternye-komplektuyushchie-15709/"
    },
    {
      "root": "Unknown",
      "name": "Видеокарты и графические ускорители",
      "url": "https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/"
    },
    {
      "root": "Unknown",
      "name": "Жесткие диски, SSD и сетевые накопители",
      "url": "https://www.ozon.ru/category/zhestkie-diski-ssd-i-setevye-nakopiteli-15710/"
    },
    {
      "root": "Unknown",
      "name": "Процессоры",
      "url": "https://www.ozon.ru/category/protsessory-15726/"
    },
    {
      "root": "Unknown",
      "name": "Материнские платы",
      "url": "https://www.ozon.ru/category/materinskie-platy-15725/"
    },
    {
      "root": "Unknown",
      "name": "Оперативная память",
      "url": "https://www.ozon.ru/category/operativnaya-pamyat-15724/"
    },
    {
      "root": "Unknown",
      "name": "Системы охлаждения",
      "url": "https://www.ozon.ru/category/sistemy-ohlazhdeniya-dlya-kompyuterov-15729/"
    },
    {
      "root": "Unknown",
      "name": "Блоки питания",
      "url": "https://www.ozon.ru/category/bloki-pitaniya-15727/"
    },
    {
      "root": "Unknown",
      "name": "Корпуса",
      "url": "https://www.ozon.ru/category/korpusa-dlya-kompyuterov-15734/"
    },
    {
      "root": "Unknown",
      "name": "Звуковые карты",
      "url": "https://www.ozon.ru/category/zvukovye-karty-15728/"
    },
    {
      "root": "Unknown",
      "name": "Электронные модули",
      "url": "https://www.ozon.ru/category/elektronnye-moduli-31565/"
    },
    {
      "root": "Unknown",
      "name": "Контроллеры интерфейсов",
      "url": "https://www.ozon.ru/category/kontrollery-interfeysov-31899/"
    },
    {
      "root": "Unknown",
      "name": "Микроконтроллеры",
      "url": "https://www.ozon.ru/category/mikrokontrollery-36162/"
    },
    {
      "root": "Unknown",
      "name": "Тестеры для комплектующих",
      "url": "https://www.ozon.ru/category/testery-dlya-kompyuternyh-komplektuyushchih-35299/"
    },
    {
      "root": "Unknown",
      "name": "Компьютеры и периферия",
      "url": "https://www.ozon.ru/category/kompyutery-i-komplektuyushchie-15690/"
    },
    {
      "root": "Unknown",
      "name": "Мониторы",
      "url": "https://www.ozon.ru/category/monitory-15738/"
    },
    {
      "root": "Unknown",
      "name": "Системные блоки",
      "url": "https://www.ozon.ru/category/sistemnye-bloki-15704/"
    },
    {
      "root": "Unknown",
      "name": "Моноблоки",
      "url": "https://www.ozon.ru/category/monobloki-15703/"
    },
    {
      "root": "Unknown",
      "name": "Периферия",
      "url": "https://www.ozon.ru/category/periferiya-dlya-kompyuterov-15736/"
    },
    {
      "root": "Unknown",
      "name": "Сетевое оборудование",
      "url": "https://www.ozon.ru/category/setevoe-oborudovanie-15854/"
    },
    {
      "root": "Unknown",
      "name": "Неттопы и Мини ПК",
      "url": "https://www.ozon.ru/category/mini-pk-15705/"
    },
    {
      "root": "Unknown",
      "name": "Майнеры и криптокошельки",
      "url": "https://www.ozon.ru/category/maynery-i-koshelki-dlya-kriptovalyut-15708/"
    },
    {
      "root": "Unknown",
      "name": "Микрокомпьютеры и комплектующие",
      "url": "https://www.ozon.ru/category/mikrokompyutery-15707/"
    },
    {
      "root": "Unknown",
      "name": "Промышленные компьютеры и серверы",
      "url": "https://www.ozon.ru/category/promyshlennye-kompyutery-i-servery-31361/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти для мониторов",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-monitorov-36076/"
    },
    {
      "root": "Unknown",
      "name": "Программное обеспечение",
      "url": "https://www.ozon.ru/category/programmnoe-obespechenie-12905/"
    },
    {
      "root": "Unknown",
      "name": "Фото и видеокамеры",
      "url": "https://www.ozon.ru/category/foto-i-videokamery-15623/"
    },
    {
      "root": "Unknown",
      "name": "Экшн-камеры",
      "url": "https://www.ozon.ru/category/ekshn-kamery-15630/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для экшн-камер",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-ekshn-kamer-15678/"
    },
    {
      "root": "Unknown",
      "name": "Видеокамеры",
      "url": "https://www.ozon.ru/category/videokamery-15629/"
    },
    {
      "root": "Unknown",
      "name": "Зеркальные фотоаппараты",
      "url": "https://www.ozon.ru/category/zerkalnye-fotokamery-15625/"
    },
    {
      "root": "Unknown",
      "name": "Объективы",
      "url": "https://www.ozon.ru/category/obektivy-15632/"
    },
    {
      "root": "Unknown",
      "name": "Компактные фотоаппараты",
      "url": "https://www.ozon.ru/category/kompaktnye-fotokamery-15626/"
    },
    {
      "root": "Unknown",
      "name": "Фотоаппараты мгновенной печати",
      "url": "https://www.ozon.ru/category/fotoapparaty-mgnovennoy-pechati-15627/"
    },
    {
      "root": "Unknown",
      "name": "Детские фотоаппараты",
      "url": "https://www.ozon.ru/category/detskie-fotoapparaty-i-videokamery-37754/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для фото и видеотехники",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-foto-i-videokamer-15644/"
    },
    {
      "root": "Unknown",
      "name": "Фотофоны",
      "url": "https://www.ozon.ru/category/fotofony-15651/"
    },
    {
      "root": "Unknown",
      "name": "Студийное оборудование",
      "url": "https://www.ozon.ru/category/studiynoe-oborudovanie-15676/"
    },
    {
      "root": "Unknown",
      "name": "Картриджи и фотопленка",
      "url": "https://www.ozon.ru/category/kartridzhi-dlya-foto-30484/"
    },
    {
      "root": "Unknown",
      "name": "Компактные фотопринтеры",
      "url": "https://www.ozon.ru/category/kompaktnye-fotoprintery-35946/"
    },
    {
      "root": "Unknown",
      "name": "Цифровые фоторамки",
      "url": "https://www.ozon.ru/category/tsifrovye-fotoramki-15684/"
    },
    {
      "root": "Unknown",
      "name": "Прочие аксессуары",
      "url": "https://www.ozon.ru/category/pulty-distantsionnogo-upravleniya-dlya-fotokamer-15660/"
    },
    {
      "root": "Unknown",
      "name": "Игровые приставки и ноутбуки",
      "url": "https://www.ozon.ru/category/igrovye-pristavki-i-kompyutery-15800/"
    },
    {
      "root": "Unknown",
      "name": "Игровые приставки",
      "url": "https://www.ozon.ru/category/igrovye-pristavki-30234/"
    },
    {
      "root": "Unknown",
      "name": "Игровые ноутбуки",
      "url": "https://www.ozon.ru/category/igrovye-noutbuki-30601/"
    },
    {
      "root": "Unknown",
      "name": "Офисная техника",
      "url": "https://www.ozon.ru/category/ofisnaya-tehnika-15770/"
    },
    {
      "root": "Unknown",
      "name": "Ноутбуки",
      "url": "https://www.ozon.ru/category/noutbuki-33113/"
    },
    {
      "root": "Unknown",
      "name": "Системные блоки",
      "url": "https://www.ozon.ru/category/sistemnye-bloki-33120/"
    },
    {
      "root": "Unknown",
      "name": "Мониторы",
      "url": "https://www.ozon.ru/category/monitory-37966/"
    },
    {
      "root": "Unknown",
      "name": "МФУ",
      "url": "https://www.ozon.ru/category/mfu-15772/"
    },
    {
      "root": "Unknown",
      "name": "Принтеры",
      "url": "https://www.ozon.ru/category/printery-15771/"
    },
    {
      "root": "Unknown",
      "name": "Картриджи и расходные материалы",
      "url": "https://www.ozon.ru/category/rashodnye-materialy-dlya-ofisnoy-tehniki-15783/"
    },
    {
      "root": "Unknown",
      "name": "Оборудование для торговли",
      "url": "https://www.ozon.ru/category/kassovoe-oborudovanie-15875/"
    },
    {
      "root": "Unknown",
      "name": "3D-оборудование",
      "url": "https://www.ozon.ru/category/3d-pechat-30738/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти и аксессуары",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-3d-printerov-39202/"
    },
    {
      "root": "Unknown",
      "name": "Сканеры",
      "url": "https://www.ozon.ru/category/skanery-15773/"
    },
    {
      "root": "Unknown",
      "name": "Ламинаторы",
      "url": "https://www.ozon.ru/category/laminatory-i-broshyurovshchiki-15777/"
    },
    {
      "root": "Unknown",
      "name": "Шредеры",
      "url": "https://www.ozon.ru/category/shredery-15782/"
    },
    {
      "root": "Unknown",
      "name": "Брошюровщики",
      "url": "https://www.ozon.ru/category/broshyurovshchiki-36266/"
    },
    {
      "root": "Unknown",
      "name": "Проекторы",
      "url": "https://www.ozon.ru/category/proektory-31978/"
    },
    {
      "root": "Unknown",
      "name": "Квадрокоптеры и аксессуары",
      "url": "https://www.ozon.ru/category/kvadrokoptery-i-aksessuary-7159/"
    },
    {
      "root": "Unknown",
      "name": "Квадрокоптеры",
      "url": "https://www.ozon.ru/category/kvadrokoptery-7160/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти и аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-kvadrokopterov-7166/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторы",
      "url": "https://www.ozon.ru/category/akkumulyatory-dlya-kvadrokopterov-7164/"
    },
    {
      "root": "Unknown",
      "name": "Навигаторы",
      "url": "https://www.ozon.ru/category/navigatory-15685/"
    },
    {
      "root": "Unknown",
      "name": "GPS-трекеры и GPS-маяки",
      "url": "https://www.ozon.ru/category/gps-trekery-30784/"
    },
    {
      "root": "Unknown",
      "name": "Туристические навигаторы",
      "url": "https://www.ozon.ru/category/turisticheskie-navigatory-15686/"
    },
    {
      "root": "Unknown",
      "name": "Автомобильные навигаторы",
      "url": "https://www.ozon.ru/category/avtomobilnye-navigatory-15687/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары и запчасти",
      "url": "https://www.ozon.ru/category/chehly-dlya-navigatorov-15903/"
    },
    {
      "root": "Unknown",
      "name": "Умный дом",
      "url": "https://www.ozon.ru/category/umnyy-dom-15849/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-umnogo-doma-15853/"
    },
    {
      "root": "Unknown",
      "name": "Выключатели и реле",
      "url": "https://www.ozon.ru/category/umnye-vyklyuchateli-i-rele-39965/"
    },
    {
      "root": "Unknown",
      "name": "Датчики и регуляторы",
      "url": "https://www.ozon.ru/category/datchiki-dlya-umnogo-doma-39919/"
    },
    {
      "root": "Unknown",
      "name": "Комплекты умного дома",
      "url": "https://www.ozon.ru/category/komplekty-umnogo-doma-15851/"
    },
    {
      "root": "Unknown",
      "name": "Освещение",
      "url": "https://www.ozon.ru/category/umnoe-osveshchenie-39963/"
    },
    {
      "root": "Unknown",
      "name": "Розетки",
      "url": "https://www.ozon.ru/category/umnye-rozetki-15850/"
    },
    {
      "root": "Unknown",
      "name": "Устройства безопасности",
      "url": "https://www.ozon.ru/category/umnye-ustroystva-bezopasnosti-39964/"
    },
    {
      "root": "Unknown",
      "name": "Управление умным домом",
      "url": "https://www.ozon.ru/category/upravlenie-dlya-umnogo-doma-15852/"
    },
    {
      "root": "Unknown",
      "name": "Электрокарнизы",
      "url": "https://www.ozon.ru/category/elektrokarnizy-37724/"
    },
    {
      "root": "Unknown",
      "name": "Телевизоры и видеотехника",
      "url": "https://www.ozon.ru/category/televizory-i-videotehnika-15527/"
    },
    {
      "root": "Unknown",
      "name": "Телевизоры",
      "url": "https://www.ozon.ru/category/televizory-15528/"
    },
    {
      "root": "Unknown",
      "name": "ТВ-приставки и медиаплееры",
      "url": "https://www.ozon.ru/category/mediapleery-15622/"
    },
    {
      "root": "Unknown",
      "name": "Кронштейны и крепления",
      "url": "https://www.ozon.ru/category/kronshteyny-dlya-televizorov-15529/"
    },
    {
      "root": "Unknown",
      "name": "Цифровое и спутниковое ТВ",
      "url": "https://www.ozon.ru/category/tsifrovoe-i-sputnikovoe-tv-15534/"
    },
    {
      "root": "Unknown",
      "name": "Онлайн-кинотеатры",
      "url": "https://www.ozon.ru/category/podpiski-na-onlayn-kinoteatry-32131/"
    },
    {
      "root": "Unknown",
      "name": "Пульты ДУ",
      "url": "https://www.ozon.ru/category/pulty-du-15542/"
    },
    {
      "root": "Unknown",
      "name": "Антенны",
      "url": "https://www.ozon.ru/category/antenny-15531/"
    },
    {
      "root": "Unknown",
      "name": "Запчасти и аксессуары",
      "url": "https://www.ozon.ru/category/zapchasti-dlya-televizorov-35384/"
    },
    {
      "root": "Unknown",
      "name": "DVD-плееры",
      "url": "https://www.ozon.ru/category/dvd-pleery-15620/"
    },
    {
      "root": "Unknown",
      "name": "Проекторы",
      "url": "https://www.ozon.ru/category/proektory-15615/"
    },
    {
      "root": "Unknown",
      "name": "Проекционные экраны",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-proektorov-15616/"
    },
    {
      "root": "Unknown",
      "name": "Интерактивные панели и пиксельные экраны",
      "url": "https://www.ozon.ru/category/interaktivnye-paneli-34684/"
    },
    {
      "root": "Unknown",
      "name": "Охранные системы и видеонаблюдение",
      "url": "https://www.ozon.ru/category/umnyy-dom-i-bezopasnost-15835/"
    },
    {
      "root": "Unknown",
      "name": "Камеры видеонаблюдения",
      "url": "https://www.ozon.ru/category/ulichnye-kamery-videonablyudeniya-31773/"
    },
    {
      "root": "Unknown",
      "name": "Системы видеонаблюдения",
      "url": "https://www.ozon.ru/category/sistemy-videonablyudeniya-15848/"
    },
    {
      "root": "Unknown",
      "name": "Автоматика для ворот и дверей",
      "url": "https://www.ozon.ru/category/avtomatika-dlya-vorot-32466/"
    },
    {
      "root": "Unknown",
      "name": "Домофоны",
      "url": "https://www.ozon.ru/category/domofony-15837/"
    },
    {
      "root": "Unknown",
      "name": "Охранное оборудование для дома и дачи",
      "url": "https://www.ozon.ru/category/ohrannoe-oborudovanie-dlya-doma-i-dachi-15840/"
    },
    {
      "root": "Unknown",
      "name": "Охранные системы для бизнеса",
      "url": "https://www.ozon.ru/category/skud-30686/"
    },
    {
      "root": "Unknown",
      "name": "Персональные видеорегистраторы",
      "url": "https://www.ozon.ru/category/skrytye-kamery-videonablyudeniya-35097/"
    },
    {
      "root": "Unknown",
      "name": "Регистраторы",
      "url": "https://www.ozon.ru/category/registratory-dlya-videonablyudeniya-15847/"
    },
    {
      "root": "Unknown",
      "name": "Муляжи камер видеонаблюдения",
      "url": "https://www.ozon.ru/category/mulyazhi-kamer-videonablyudeniya-15983/"
    },
    {
      "root": "Unknown",
      "name": "Электронные замки",
      "url": "https://www.ozon.ru/category/elektronnye-zamki-15841/"
    },
    {
      "root": "Unknown",
      "name": "Электронные ключи и карты",
      "url": "https://www.ozon.ru/category/elektronnye-klyuchi-30573/"
    },
    {
      "root": "Unknown",
      "name": "Детекторы следящих устройств и антижучки",
      "url": "https://www.ozon.ru/category/podaviteli-signala-gps-31971/"
    },
    {
      "root": "Unknown",
      "name": "Установка видеонаблюдения",
      "url": "https://www.ozon.ru/category/kronshteyny-dlya-kamer-videonablyudeniya-30680/"
    },
    {
      "root": "Unknown",
      "name": "Персональные сигнализации",
      "url": "https://www.ozon.ru/category/personalnye-signalizatsii-31838/"
    },
    {
      "root": "Unknown",
      "name": "Аксессуары для электроники",
      "url": "https://www.ozon.ru/category/aksessuary-dlya-elektroniki-15879/"
    },
    {
      "root": "Unknown",
      "name": "Кабели и переходники",
      "url": "https://www.ozon.ru/category/kabeli-i-perehodniki-15913/"
    },
    {
      "root": "Unknown",
      "name": "Внешние аккумуляторы",
      "url": "https://www.ozon.ru/category/vneshnie-akkumulyatory-15881/"
    },
    {
      "root": "Unknown",
      "name": "Батарейки",
      "url": "https://www.ozon.ru/category/batareyki-15882/"
    },
    {
      "root": "Unknown",
      "name": "Аккумуляторные батарейки",
      "url": "https://www.ozon.ru/category/akkumulyatornye-batareyki-15883/"
    },
    {
      "root": "Unknown",
      "name": "Зарядные устройства для батареек",
      "url": "https://www.ozon.ru/category/zaryadnye-ustroystva-dlya-akkumulyatorov-15886/"
    },
    {
      "root": "Unknown",
      "name": "Сетевые зарядные устройства",
      "url": "https://www.ozon.ru/category/setevye-zaryadnye-ustroystva-15922/"
    },
    {
      "root": "Unknown",
      "name": "Беспроводные зарядные устройства",
      "url": "https://www.ozon.ru/category/besprovodnye-zaryadnye-ustroystva-15923/"
    },
    {
      "root": "Unknown",
      "name": "Автомобильные зарядные устройства",
      "url": "https://www.ozon.ru/category/avtomobilnye-zaryadnye-ustroystva-15921/"
    },
    {
      "root": "Unknown",
      "name": "Робототехника",
      "url": "https://www.ozon.ru/category/roboty-i-drony-15614/"
    },
    {
      "root": "Unknown",
      "name": "Чистящие средства и салфетки",
      "url": "https://www.ozon.ru/category/chistyashchie-sredstva-i-salfetki-dlya-elektroniki-15936/"
    },
    {
      "root": "Unknown",
      "name": "Сетевые блоки питания",
      "url": "https://www.ozon.ru/category/bloki-pitaniya-dlya-setevogo-oborudovaniya-36172/"
    }
  ]
}
```

