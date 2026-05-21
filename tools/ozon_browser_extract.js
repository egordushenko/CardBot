(() => {
  const clean = (value) => String(value || "").replace(/\s+/g, " ").trim();
  const lines = document.body.innerText
    .split("\n")
    .map((line) => clean(line))
    .filter(Boolean);

  const stop = new Set([
    "Фото",
    "Отзывы",
    "Описание",
    "Вопросы",
    "Похожие товары",
    "С этим товаром покупают",
    "Фото и видео покупателей",
  ]);
  const stopPrefixes = [
    "Информация о технических характеристиках",
    "Подборки товаров",
    "Зарегистрирован в системе",
    "Отзывы о товаре",
    "Вопросы о товаре",
    "Все отзывы",
    "Этот вариант товара",
    "Рекомендуем",
    "Похожие",
    "Смотрите также",
  ];
  const isStopLine = (line) => stop.has(line) || stopPrefixes.some((prefix) => line.startsWith(prefix));

  const characteristics = {};
  let start = lines.findIndex((line) => line === "Характеристики");
  if (start < 0) {
    start = lines.findIndex((line) => line === "О товаре");
  }
  if (start >= 0) {
    let firstPairIndex = start + 1;
    if (lines[firstPairIndex] === "Перейти к описанию") firstPairIndex += 1;
    for (let i = firstPairIndex; i < lines.length - 1; i += 2) {
      if (isStopLine(lines[i])) break;
      if (lines[i].includes(":")) {
        const [rawKey, ...rawValue] = lines[i].split(":");
        const key = rawKey.trim();
        const value = rawValue.join(":").trim();
        if (key && value && key.length <= 90 && value.length <= 240) {
          characteristics[key] = value;
        }
        i -= 1;
        continue;
      }
      const key = lines[i].replace(/:$/, "");
      const value = lines[i + 1];
      if (isStopLine(value)) break;
      if (key && value && key.length <= 90 && value.length <= 240) {
        characteristics[key] = value;
      }
    }
  }

  const jsonLdItems = [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map((node) => {
      try {
        return JSON.parse(node.textContent);
      } catch (_) {
        return null;
      }
    })
    .flatMap((item) => (Array.isArray(item) ? item : [item]));

  const productLd = jsonLdItems.find((item) => {
    const type = item && item["@type"];
    return type === "Product" || (Array.isArray(type) && type.includes("Product"));
  });

  const rating = productLd?.aggregateRating?.ratingValue
    ? Number(String(productLd.aggregateRating.ratingValue).replace(",", "."))
    : null;
  const reviewCount = productLd?.aggregateRating?.reviewCount
    ? Number(String(productLd.aggregateRating.reviewCount).replace(/\D/g, ""))
    : null;
  const title = clean(productLd?.name || document.querySelector("h1")?.innerText || document.title);
  const description = clean(productLd?.description || "");
  const hashtags = title
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s-]/gu, " ")
    .split(/\s+/)
    .filter((word) => word.length > 3)
    .slice(0, 12)
    .map((word) => `#${word.replace(/-/g, "_")}`);

  const payload = {
    source_url: location.href,
    product_id: (location.pathname.match(/-(\d+)\/?$/) || [])[1] || null,
    category: [...document.querySelectorAll('nav a, [data-widget*="bread"] a')]
      .map((node) => clean(node.innerText))
      .filter(Boolean)
      .join(" / "),
    title,
    description,
    rating,
    review_count: reviewCount,
    characteristics,
    hashtags,
    scraped_at: new Date().toISOString(),
  };

  console.log(JSON.stringify(payload, null, 2));
  navigator.clipboard?.writeText(JSON.stringify(payload, null, 2));
  return payload;
})();
