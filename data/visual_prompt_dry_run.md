# Visual Prompt Dry Run

- Cases: 12
- Concepts: 58
- Cases with issues: 0

## Case 1: clothing / wb

Input: Рашгард Therapy черный размер M, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине

Issues: none

Photo analysis:
- photo 0: tags=['back', 'on_model']; usable_for=['back_on_model', 'print_reference']; defects=[]
- photo 1: tags=['closeup', 'label']; usable_for=['closeup', 'label_reference']; defects=[]
- photo 2: tags=['front', 'on_model']; usable_for=['front_on_model']; defects=[]
- photo 3: tags=['flatlay', 'front']; usable_for=['hero', 'flatlay']; defects=[]
- photo 4: tags=['back', 'flatlay']; usable_for=['back_flatlay', 'print_reference']; defects=[]

### Image 1: hero / photo 3

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Рашгард Therapy черный, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 3; do not merge details from other photos.
COMPOSITION: clean hero flatlay, product fully visible and neatly shaped.
BACKGROUND: light warm studio surface with soft shadows, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Товарный вид; Без лишнего фона. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Рашгард Therapy черный, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of fabric, seams or print detail; do not crop away the meaningful detail.
BACKGROUND: soft neutral studio macro background with fabric texture visible; Do NOT use a pure white empty background.
TEXT OVERLAY: Ткань и детали; Аккуратная печать. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: lifestyle_back / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Рашгард Therapy черный, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине
SLIDE ROLE: lifestyle_back
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, back view, natural confident pose.
BACKGROUND: marketplace sports or streetwear studio background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Принт на спине. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Рашгард Therapy черный, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, front view, natural pose, good fit visible.
BACKGROUND: bright marketplace studio or gym background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Свобода движений. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: lifestyle_three_quarter / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Рашгард Therapy черный, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине
SLIDE ROLE: lifestyle_three_quarter
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, three-quarter 30-60 degree angle, natural pose.
BACKGROUND: premium marketplace lifestyle background with soft directional light; Do NOT use a pure white empty background.
TEXT OVERLAY: Подчеркивает посадку. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 2: clothing / wb

Input: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки

Issues: none

Photo analysis:
- photo 0: tags=['back', 'on_model']; usable_for=['back_on_model', 'print_reference']; defects=[]
- photo 1: tags=['closeup', 'label']; usable_for=['closeup', 'label_reference']; defects=[]
- photo 2: tags=['front', 'on_model']; usable_for=['front_on_model']; defects=[]
- photo 3: tags=['flatlay', 'front']; usable_for=['hero', 'flatlay']; defects=[]
- photo 4: tags=['back', 'flatlay']; usable_for=['back_flatlay', 'print_reference']; defects=[]

### Image 1: hero / photo 3

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 3; do not merge details from other photos.
COMPOSITION: clean hero flatlay, product fully visible and neatly shaped.
BACKGROUND: light warm studio surface with soft shadows, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Товарный вид; Без лишнего фона. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of fabric, seams or print detail; do not crop away the meaningful detail.
BACKGROUND: soft neutral studio macro background with fabric texture visible; Do NOT use a pure white empty background.
TEXT OVERLAY: Ткань и детали; Аккуратная печать. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: lifestyle_back / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки
SLIDE ROLE: lifestyle_back
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, back view, natural confident pose.
BACKGROUND: marketplace sports or streetwear studio background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Принт на спине. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, front view, natural pose, good fit visible.
BACKGROUND: bright marketplace studio or gym background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Свобода движений. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: lifestyle_three_quarter / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки
SLIDE ROLE: lifestyle_three_quarter
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: adult model wearing the clothing, three-quarter 30-60 degree angle, natural pose.
BACKGROUND: premium marketplace lifestyle background with soft directional light; Do NOT use a pure white empty background.
TEXT OVERLAY: Подчеркивает посадку. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 3: home_decor / ozon

Input: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot on a desk or tabletop, full product visible.
BACKGROUND: light interior desk scene with soft shadows, blurred contextual elements, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Наглядный таймер. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with the product on the left and 3 concise icon facts on the right.
BACKGROUND: warm studio tabletop with subtle interior depth and soft shadows; Do NOT use a pure white empty background.
TEXT OVERLAY: 5 минут; Деревянная основа. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: closeup sand/glass or material detail, texture and construction visible.
BACKGROUND: macro interior background with warm blur and directional light; Do NOT use a pure white empty background.
TEXT OVERLAY: Белый песок; Защита колбы. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: interior / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе
SLIDE ROLE: interior
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: product placed on an interior shelf or table as decor.
BACKGROUND: cozy shelf interior with books, plant or decor softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Декор для стола. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: scenario desk/kitchen use case, product in realistic context.
BACKGROUND: desk or kitchen counter with contextual props softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Для кухни и работы. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 4: home_decor / ozon

Input: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot of the lamp on a desk or bedside table, full silhouette visible.
BACKGROUND: warm desk or bedroom interior with soft glow and blurred decor, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Мягкий свет. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with lamp and 3 concise lighting benefits.
BACKGROUND: modern desk scene with books or laptop softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Для работы и отдыха. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: closeup of switch, base, light form or texture.
BACKGROUND: macro desk background with warm directional light; Do NOT use a pure white empty background.
TEXT OVERLAY: Удобное управление. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: lamp used as bedside, desk or room decor lighting.
BACKGROUND: cozy room interior with soft evening light; Do NOT use a pure white empty background.
TEXT OVERLAY: Создает уют. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: interior / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см
SLIDE ROLE: interior
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: lamp integrated into a modern interior, visible on desk, shelf or bedside table.
BACKGROUND: room interior with books, decor and soft ambient light, background gently blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Декор и свет. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 5: electronics / wb

Input: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot, full product visible, premium marketplace framing.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Чистый звук. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with product and 3 concise benefits.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Подключение без лишних проводов. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of material, texture, connector, label or functional detail.
BACKGROUND: macro version of the contextual scene with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Разъемы крупно. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: realistic use-case lifestyle image, product naturally used in context.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Для работы и прогулок. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: scenario image showing where and how the customer uses the product.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Всегда под рукой. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 6: cosmetics / ozon

Input: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot, full product visible, premium marketplace framing.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Уход каждый день. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with product and 3 concise benefits.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Увлажнение и ровный тон. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of material, texture, connector, label or functional detail.
BACKGROUND: macro version of the contextual scene with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Текстура и флакон. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: realistic use-case lifestyle image, product naturally used in context.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Легко в рутине. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: scenario image showing where and how the customer uses the product.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Для утреннего ухода. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 7: home_decor / wb

Input: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot on a bathroom shelf or vanity surface, full organizer visible, clean product arrangement.
BACKGROUND: light bathroom interior with sink, mirror or towels softly blurred, warm studio light, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Порядок в ванной. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with organizer on one side and 3 concise storage benefits on the other.
BACKGROUND: clean bathroom countertop scene with subtle depth and soft shadows; Do NOT use a pure white empty background.
TEXT OVERLAY: 3 секции; Все под рукой. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: closeup of compartments, edges and material finish; show practical storage details.
BACKGROUND: macro bathroom background with soft towel or tile blur; Do NOT use a pure white empty background.
TEXT OVERLAY: Для косметики и щеток. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: organizer in use with cosmetics, toothbrushes or small accessories neatly placed.
BACKGROUND: realistic vanity or bathroom shelf scene with contextual props softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Аккуратное хранение. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: interior / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток
SLIDE ROLE: interior
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: organizer placed in a clean bathroom storage zone, showing how it fits the interior.
BACKGROUND: bathroom shelf or countertop with mirror, towels and light decor softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Вписывается в интерьер. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 8: electronics / ozon

Input: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]
- photo 4: tags=['flatlay']; usable_for=['hero']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot, full product visible, premium marketplace framing.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Чистый звук. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with product and 3 concise benefits.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Подключение без лишних проводов. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of material, texture, connector, label or functional detail.
BACKGROUND: macro version of the contextual scene with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Разъемы крупно. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: realistic use-case lifestyle image, product naturally used in context.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Для работы и прогулок. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: scenario image showing where and how the customer uses the product.
BACKGROUND: modern desk setup with soft screen glow and blurred accessories; Do NOT use a pure white empty background.
TEXT OVERLAY: Всегда под рукой. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 9: food / wb

Input: Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot, full product visible, premium marketplace framing.
BACKGROUND: warm kitchen tabletop or cafe counter with appetizing natural light; Do NOT use a pure white empty background.
TEXT OVERLAY: Вкусный перекус. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with product and 3 concise benefits.
BACKGROUND: warm kitchen tabletop or cafe counter with appetizing natural light; Do NOT use a pure white empty background.
TEXT OVERLAY: Состав и польза. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of material, texture, connector, label or functional detail.
BACKGROUND: macro version of the contextual scene with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Аппетитная текстура. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: realistic use-case lifestyle image, product naturally used in context.
BACKGROUND: warm kitchen tabletop or cafe counter with appetizing natural light; Do NOT use a pure white empty background.
TEXT OVERLAY: С собой каждый день. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 10: kids / ozon

Input: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]
- photo 4: tags=['flatlay']; usable_for=['hero']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: clean product hero flatlay, full item visible.
BACKGROUND: soft pastel studio surface with gentle shadows, not empty white; Do NOT use a pure white empty background.
TEXT OVERLAY: Комфорт каждый день. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
- Do NOT use adult models for children's clothing.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: child model of appropriate age wearing the item, neutral safe pose.
BACKGROUND: bright child-safe room or studio background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Удобно ребенку. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
- Do NOT use adult models for children's clothing.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of fabric, seam or functional detail.
BACKGROUND: soft studio macro background; Do NOT use a pure white empty background.
TEXT OVERLAY: Мягкая ткань. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
- Do NOT use adult models for children's clothing.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: clean product hero flatlay, full item visible.
BACKGROUND: soft pastel studio surface with gentle shadows, not empty white; Do NOT use a pure white empty background.
TEXT OVERLAY: Комфорт каждый день. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
- Do NOT use adult models for children's clothing.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: child model of appropriate age wearing the item, neutral safe pose.
BACKGROUND: bright child-safe room or studio background, softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Удобно ребенку. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
- Do NOT put clothing size on overlay text.
- Preserve printed logos and text exactly; do not invent or move print elements.
- Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.
- Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.
- Do NOT use adult models for children's clothing.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 11: cosmetics / wb

Input: Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot, full product visible, premium marketplace framing.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Уход каждый день. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with product and 3 concise benefits.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Увлажнение и ровный тон. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: close-up of material, texture, connector, label or functional detail.
BACKGROUND: macro version of the contextual scene with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Текстура и флакон. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: lifestyle_front / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Wildberries.
PRODUCT: Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи
SLIDE ROLE: lifestyle_front
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: realistic use-case lifestyle image, product naturally used in context.
BACKGROUND: clean bathroom or vanity scene with soft reflections and product-safe lighting; Do NOT use a pure white empty background.
TEXT OVERLAY: Легко в рутине. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

## Case 12: home_decor / ozon

Input: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу

Issues: none

Photo analysis:
- photo 0: tags=['flatlay']; usable_for=['hero']; defects=[]
- photo 1: tags=['closeup']; usable_for=['closeup']; defects=[]
- photo 2: tags=['front']; usable_for=['facts']; defects=[]
- photo 3: tags=['closeup']; usable_for=['detail']; defects=[]

### Image 1: hero / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу
SLIDE ROLE: hero
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: hero product shot of bath mat laid flat, full shape visible, neat edges and soft pile visible.
BACKGROUND: light bathroom floor scene near shower or bathtub, soft shadows and blurred interior elements, not a pure white empty background; Do NOT use a pure white empty background.
TEXT OVERLAY: Мягкий ворс. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 2: facts / photo 2

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу
SLIDE ROLE: facts
REFERENCE PHOTO: use only photo 2; do not merge details from other photos.
COMPOSITION: facts card with bath mat and 3 concise comfort or safety benefits.
BACKGROUND: clean bathroom floor with subtle tile texture and soft daylight; Do NOT use a pure white empty background.
TEXT OVERLAY: Не скользит; Быстро впитывает. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 3: closeup / photo 1

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу
SLIDE ROLE: closeup
REFERENCE PHOTO: use only photo 1; do not merge details from other photos.
COMPOSITION: closeup of pile texture and edge finish, show softness without changing material.
BACKGROUND: macro bathroom textile background with shallow depth of field; Do NOT use a pure white empty background.
TEXT OVERLAY: Приятен для ног. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 4: scenario / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу
SLIDE ROLE: scenario
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: bath mat placed near bathtub, shower or sink in a realistic bathroom use case.
BACKGROUND: cozy bathroom interior with towels and neutral decor softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Комфорт после душа. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```

### Image 5: interior / photo 0

Issues: none

```text
Create a 3:4 marketplace image for Ozon.
PRODUCT: Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу
SLIDE ROLE: interior
REFERENCE PHOTO: use only photo 0; do not merge details from other photos.
COMPOSITION: bath mat shown as part of a finished bathroom interior, full placement visible.
BACKGROUND: bright bathroom scene with bathtub, sink or shower elements softly blurred; Do NOT use a pure white empty background.
TEXT OVERLAY: Для ванной и душа. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.
No trusted visible text detected.
No specific source photo defects detected.
NEGATIVE CONSTRAINTS:
- Do NOT use a pure white empty background; use contextual light studio or interior background.
- Use large readable modern sans-serif typography only.
- Use 1-2 text blocks, not random corner labels.
- Do NOT use meaningless headings like "Детали".
- Preserve exact product shape, color, texture and proportions.
- Use only the selected reference photo; do not mix details from other photos.
QA TARGETS: pure_white_background, small_text, bad_typography, deformation, print_mismatch.
Make the image polished, commercial and ready for a marketplace gallery.
```
