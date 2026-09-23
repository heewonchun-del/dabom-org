# dabom.org (GitHub Pages)

Public site for **The Dabom Project**: **Dabom** (AI daily-life assistant) first, then **Danol** (accessible games).

## Downloads (GitHub Releases)

Large installers are **not** stored in this git tree. Links on the page point to Releases:

| Product | Release tag | Assets |
|--------|-------------|--------|
| Dabom 3.1 | `dabom-v3.1` | `Dabom_Setup_Full.exe`, `OllamaSetup.exe` (optional; same folder) |
| Danol 1.3 | `danol-v1.3` | `danol_setup_full.zip` (exe + Ollama) |

Dabom Full + Ollama cannot be one zip (over GitHub’s ~2 GB per-file limit), so they are separate downloads.

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

Sources: `i18n_base.json` (en, ko, de — hand-written), `i18n_extra.json` (es, fr, ja, ru, zh, ar), `mt_targets.json`.
