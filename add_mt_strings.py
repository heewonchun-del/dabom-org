# -*- coding: utf-8 -*-
"""Add accessible Google-Translate section strings and rebuild index.html."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"d:\dev\dabom-org")

# Extra target languages for machine translation (beyond the site's 9).
# value = Google Translate `tl` code; label = English name for stable SR sorting,
# with native name where helpful.
MT_TARGETS = [
    ("pt", "Portuguese — Português"),
    ("it", "Italian — Italiano"),
    ("nl", "Dutch — Nederlands"),
    ("pl", "Polish — Polski"),
    ("tr", "Turkish — Türkçe"),
    ("vi", "Vietnamese — Tiếng Việt"),
    ("th", "Thai — ไทย"),
    ("id", "Indonesian — Bahasa Indonesia"),
    ("hi", "Hindi — हिन्दी"),
    ("bn", "Bengali — বাংলা"),
    ("uk", "Ukrainian — Українська"),
    ("cs", "Czech — Čeština"),
    ("ro", "Romanian — Română"),
    ("hu", "Hungarian — Magyar"),
    ("sv", "Swedish — Svenska"),
    ("da", "Danish — Dansk"),
    ("fi", "Finnish — Suomi"),
    ("no", "Norwegian — Norsk"),
    ("el", "Greek — Ελληνικά"),
    ("he", "Hebrew — עברית"),
    ("ms", "Malay — Bahasa Melayu"),
    ("tl", "Filipino — Tagalog"),
    ("sw", "Swahili — Kiswahili"),
    ("fa", "Persian — فارسی"),
]

MT_STRINGS = {
    "en": {
        "nav_translate": "Other languages",
        "mt_h2": "Other languages (machine translation)",
        "mt_lead": "This website is written by hand in nine languages. If you need another language, use the list below. Choose a language, then activate the button. Google Translate will open in the same window and show an automatic translation of the English page. That translation is not checked by a person and may contain mistakes.",
        "mt_label": "Translate this page into",
        "mt_submit": "Open Google Translate",
        "mt_note": "The button leaves Dabom.org and opens Google Translate. You can go back with your browser’s Back key. For the nine languages named at the top of this page, use that language list instead — those texts are not machine translated.",
    },
    "ko": {
        "nav_translate": "다른 언어",
        "mt_h2": "다른 언어 (자동 번역)",
        "mt_lead": "이 웹사이트는 아홉 개 언어로 직접 작성되어 있습니다. 그 밖의 언어가 필요하면 아래 목록을 쓰십시오. 언어를 고른 뒤 단추를 누르십시오. 같은 창에서 Google 번역이 열리고, 영어 페이지를 자동으로 번역해 보여 줍니다. 사람이 검수한 글이 아니므로 오류가 있을 수 있습니다.",
        "mt_label": "이 페이지를 다음 언어로 번역",
        "mt_submit": "Google 번역 열기",
        "mt_note": "단추를 누르면 Dabom.org를 떠나 Google 번역으로 갑니다. 브라우저의 뒤로 가기로 돌아올 수 있습니다. 이 페이지 위쪽에 있는 아홉 개 언어는 자동 번역이 아니니, 그 언어들은 위쪽 목록을 쓰십시오.",
    },
    "de": {
        "nav_translate": "Andere Sprachen",
        "mt_h2": "Andere Sprachen (maschinelle Übersetzung)",
        "mt_lead": "Diese Website ist in neun Sprachen von Hand geschrieben. Für eine andere Sprache nutzen Sie die Liste unten. Wählen Sie eine Sprache und betätigen Sie die Schaltfläche. Google Übersetzer öffnet sich im selben Fenster und zeigt eine automatische Übersetzung der englischen Seite. Die Übersetzung wurde nicht von Menschen geprüft und kann Fehler enthalten.",
        "mt_label": "Diese Seite übersetzen nach",
        "mt_submit": "Google Übersetzer öffnen",
        "mt_note": "Die Schaltfläche verlässt Dabom.org und öffnet Google Übersetzer. Mit der Zurück-Taste des Browsers kommen Sie zurück. Für die neun Sprachen oben auf der Seite nutzen Sie bitte jene Liste — das sind keine Maschinenübersetzungen.",
    },
    "es": {
        "nav_translate": "Otros idiomas",
        "mt_h2": "Otros idiomas (traducción automática)",
        "mt_lead": "Este sitio está escrito a mano en nueve idiomas. Si necesita otro, use la lista de abajo. Elija un idioma y active el botón. Google Traductor se abrirá en la misma ventana y mostrará una traducción automática de la página en inglés. Esa traducción no la ha revisado una persona y puede tener errores.",
        "mt_label": "Traducir esta página a",
        "mt_submit": "Abrir Google Traductor",
        "mt_note": "El botón sale de Dabom.org y abre Google Traductor. Puede volver con Atrás del navegador. Para los nueve idiomas de arriba, use esa lista: esos textos no son traducción automática.",
    },
    "fr": {
        "nav_translate": "Autres langues",
        "mt_h2": "Autres langues (traduction automatique)",
        "mt_lead": "Ce site est rédigé à la main en neuf langues. Pour une autre langue, utilisez la liste ci-dessous. Choisissez une langue, puis activez le bouton. Google Traduction s’ouvre dans la même fenêtre et affiche une traduction automatique de la page en anglais. Cette traduction n’a pas été relue par une personne et peut contenir des erreurs.",
        "mt_label": "Traduire cette page en",
        "mt_submit": "Ouvrir Google Traduction",
        "mt_note": "Le bouton quitte Dabom.org et ouvre Google Traduction. Revenez avec le bouton Précédent du navigateur. Pour les neuf langues en haut de page, utilisez cette liste — ce ne sont pas des traductions automatiques.",
    },
    "ja": {
        "nav_translate": "ほかの言語",
        "mt_h2": "ほかの言語（機械翻訳）",
        "mt_lead": "このサイトは9つの言語で人手により書かれています。それ以外の言語が必要なときは、下の一覧を使ってください。言語を選び、ボタンを実行します。同じウィンドウで Google 翻訳が開き、英語ページの自動翻訳が表示されます。人が確認した文章ではないため、誤りが含まれることがあります。",
        "mt_label": "このページの翻訳先の言語",
        "mt_submit": "Google 翻訳を開く",
        "mt_note": "ボタンを押すと Dabom.org を離れ、Google 翻訳に移動します。ブラウザの戻るで戻れます。ページ上部の9言語は機械翻訳ではありません。それらの言語は上部の一覧を使ってください。",
    },
    "ru": {
        "nav_translate": "Другие языки",
        "mt_h2": "Другие языки (машинный перевод)",
        "mt_lead": "Этот сайт написан вручную на девяти языках. Если нужен другой язык, воспользуйтесь списком ниже. Выберите язык и нажмите кнопку. В том же окне откроется Google Переводчик с автоматическим переводом английской страницы. Текст не проверялся человеком и может содержать ошибки.",
        "mt_label": "Перевести эту страницу на",
        "mt_submit": "Открыть Google Переводчик",
        "mt_note": "Кнопка уводит с Dabom.org на Google Переводчик. Вернуться можно кнопкой «Назад» в браузере. Для девяти языков вверху страницы используйте тот список — это не машинный перевод.",
    },
    "zh": {
        "nav_translate": "其他语言",
        "mt_h2": "其他语言（机器翻译）",
        "mt_lead": "本网站以九种语言人工编写。若需要其他语言，请使用下方列表。先选择语言，再激活按钮。将在同一窗口打开 Google 翻译，并显示英文页面的自动译文。该译文未经人工校对，可能有错误。",
        "mt_label": "将本页翻译为",
        "mt_submit": "打开 Google 翻译",
        "mt_note": "按钮会离开 Dabom.org 并打开 Google 翻译。可用浏览器的“后退”返回。页面顶部的九种语言请用顶部列表——那些不是机器翻译。",
    },
    "ar": {
        "nav_translate": "لغات أخرى",
        "mt_h2": "لغات أخرى (ترجمة آلية)",
        "mt_lead": "هذا الموقع مكتوب يدويًا بتسع لغات. إذا احتجت لغة أخرى، استخدم القائمة أدناه. اختر لغة ثم فعّل الزر. سيفتح Google Translate في النافذة نفسها ويعرض ترجمة آلية للصفحة الإنجليزية. هذه الترجمة لم يراجعها إنسان وقد تحتوي على أخطاء.",
        "mt_label": "ترجمة هذه الصفحة إلى",
        "mt_submit": "فتح Google Translate",
        "mt_note": "الزر يغادر Dabom.org ويفتح Google Translate. يمكنك الرجوع بزر الرجوع في المتصفح. للغات التسع في أعلى الصفحة استخدم تلك القائمة — تلك النصوص ليست ترجمة آلية.",
    },
}


def patch_json(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for lang, blob in data.items():
        extra = MT_STRINGS.get(lang)
        if not extra:
            raise SystemExit(f"no MT strings for {lang} in {path.name}")
        blob.update(extra)
        # Mention translate section in a11y list if not already
        marker = "Google"
        items = blob.get("a11y_items") or []
        if not any("Google" in x or "번역" in x or "Übersetz" in x or "Traduc" in x or "翻訳" in x or "Перевод" in x or "翻译" in x or "ترجم" in x for x in items):
            tip = {
                "en": "A section called Other languages offers Google Translate through a labeled list and a button, without needing a mouse.",
                "ko": "‘다른 언어’ 구역에서 목록과 단추만으로 Google 번역을 열 수 있으며, 마우스는 필요 없습니다.",
                "de": "Der Abschnitt „Andere Sprachen“ öffnet Google Übersetzer über eine beschriftete Liste und eine Schaltfläche — ohne Maus.",
                "es": "La sección Otros idiomas abre Google Traductor con una lista etiquetada y un botón, sin necesidad de ratón.",
                "fr": "La section Autres langues ouvre Google Traduction via une liste libellée et un bouton, sans souris.",
                "ja": "「ほかの言語」の節では、ラベル付きの一覧とボタンだけで Google 翻訳を開けます。マウスは不要です。",
                "ru": "Раздел «Другие языки» открывает Google Переводчик через подписанный список и кнопку, без мыши.",
                "zh": "“其他语言”一节可通过带标签的列表和按钮打开 Google 翻译，无需鼠标。",
                "ar": "قسم «لغات أخرى» يفتح Google Translate عبر قائمة مع تسمية وزر، دون الحاجة إلى فأرة.",
            }[lang]
            items = list(items) + [tip]
            blob["a11y_items"] = items
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched", path.name)


def main() -> None:
    patch_json(ROOT / "i18n_base.json")
    patch_json(ROOT / "i18n_extra.json")
    # Persist MT_TARGETS for build_index
    (ROOT / "mt_targets.json").write_text(
        json.dumps(MT_TARGETS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote mt_targets.json")


if __name__ == "__main__":
    main()
