# dabom.org (GitHub Pages)

Public site for The Dabom Project / Danol downloads.

## Language support

`index.html` ships **9 languages**: `ar`, `de`, `en`, `es`, `fr`, `ja`, `ko`, `ru`, `zh`.

Detection order:

1. `?lang=` query parameter  
2. `localStorage` key `dabom-lang`  
3. Browser `navigator.languages` / `navigator.language`  
4. Otherwise **English**, and a chooser banner asks the visitor to pick a supported language  

### Other languages (screen-reader friendly)

Section **Other languages** (`#translate`): choose a target language from a labeled list, then activate **Open Google Translate**.  
Same-window navigation to Google Translate of the English page (`?lang=en`). No mouse-only widget.

Rebuild after editing strings:

```bat
python add_mt_strings.py
python build_index.py
```

Sources: `i18n_base.json` (en, ko, de), `i18n_extra.json` (es, fr, ja, ru, zh, ar), `mt_targets.json`.
