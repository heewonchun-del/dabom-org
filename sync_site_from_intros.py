# -*- coding: utf-8 -*-
"""Refresh dabom.org product copy from intro_*.txt and add Matheon."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\dev\dabom-org")
DABOM_INTRO = Path(r"d:\dev\installer\dabom\docs")
MATHEON_INTRO = Path(r"d:\dev\comp\matheon_multilingual\docs")

CODES = ["ar", "de", "en", "es", "fr", "ja", "ko", "ru", "zh"]

# User one-liner (ko) / EN equivalent for Matheon lead
MATHEON_LEAD = {
    "ko": "마테온은 시각장애인을 위한 AI 기반의 Windows용 학습·연구 보조 도구입니다.",
    "en": "Matheon is an AI-based Windows learning and research assistant for visually impaired users.",
    "de": "Matheon ist ein KI-basiertes Windows-Lern- und Forschungswerkzeug für sehbehinderte Nutzer.",
    "es": "Matheon es una herramienta de aprendizaje e investigación con IA para Windows, para usuarios con discapacidad visual.",
    "fr": "Matheon est un outil Windows d’apprentissage et de recherche basé sur l’IA pour les personnes malvoyantes.",
    "ja": "マテオンは、視覚障害者のための AI ベースの Windows 学習・研究支援ツールです。",
    "ru": "Matheon — помощник для учёбы и исследований на Windows с ИИ для пользователей с нарушением зрения.",
    "zh": "Matheon 是面向视障用户的 Windows AI 学习与研究辅助工具。",
    "ar": "ماتيون أداة مساعدة للتعلّم والبحث على ويندوز تعتمد على الذكاء الاصطناعي للمستخدمين المكفوفين وضعاف البصر.",
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def strong_name(text: str, *names: str) -> str:
    out = esc(text)
    for n in names:
        out = out.replace(esc(n), f"<strong>{esc(n)}</strong>")
    return out


def bullets(block: str) -> list[str]:
    items = []
    for line in block.splitlines():
        t = line.strip()
        if t.startswith("·") or t.startswith("-") or t.startswith("•"):
            items.append(esc(t.lstrip("·-• ").strip()))
        elif t.startswith("[") and t.endswith("]"):
            continue
        elif t and items and not t.startswith("[") and ":" not in t[:20]:
            # continuation of previous bullet? skip loose lines
            pass
    return items


def section_after(text: str, headers: list[str], stop_headers: list[str]) -> str:
    """Return text after first matching header until next stop header."""
    lines = text.replace("\r\n", "\n").split("\n")
    start = None
    for i, line in enumerate(lines):
        s = line.strip()
        if any(s == h or s.startswith(h) for h in headers):
            start = i + 1
            break
    if start is None:
        return ""
    out = []
    for line in lines[start:]:
        s = line.strip()
        if any(s == h or s.startswith(h) for h in stop_headers):
            break
        out.append(line)
    return "\n".join(out).strip()


def first_paras(text: str, n: int = 2) -> list[str]:
    """Skip title line; return first n non-empty paragraphs."""
    lines = text.replace("\r\n", "\n").split("\n")
    # drop first title line
    body = "\n".join(lines[1:]).strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    # stop at first section header-ish
    clean = []
    for p in paras:
        first = p.split("\n", 1)[0].strip()
        if first in {
            "한 줄로 말하면",
            "In one sentence",
            "스크린리더로 읽을 때",
            "Reading with a screen reader",
            "처음 사용하시는 분",
            "If you are new to Dabom",
            "이미 AI·접근성 도구에 익숙하신 분",
            "If you already use AI or accessibility tools",
            "주요 기능 (요약)",
            "Features at a glance",
            "언어와 도움말",
            "Languages and help",
            "왜 마테온을 만들었나",
            "Why we made Matheon",
            "지금 마테온으로 할 수 있는 일",
            "What you can do with Matheon now",
            "9개 언어로 사용하기",
            "Use it in nine languages",
            "시작하는 방법",
            "Getting started",
            "제작 정보",
            "Credits",
        }:
            break
        clean.append(re.sub(r"\s*\n\s*", " ", p))
        if len(clean) >= n:
            break
    return clean


def dabom_from_intro(lang: str, raw: str) -> dict:
    paras = first_paras(raw, 2)
    lead = MATHEON_LEAD.get(lang, "")  # placeholder wrong - fix below
    # Dabom lead = first sentence of first para or dedicated
    opens = paras[0] if paras else ""
    slogan = ""
    if "Even without sight" in opens or "보이지 않아도" in opens:
        # keep full opens
        pass

    one = section_after(
        raw,
        ["한 줄로 말하면", "In one sentence", "En una frase", "En une phrase",
         "In einem Satz", "一言で言うと", "一句话", "В одном предложении", "بجملة واحدة"],
        ["스크린리더", "Reading with", "처음 사용", "If you are new", "Si es nuevo",
         "Si vous", "Wenn Sie neu", "初めて", "如果您是", "Если вы", "إذا كنت"],
    )
    one_line = re.sub(r"\s*\n\s*", " ", one).strip()

    beginner = section_after(
        raw,
        ["처음 사용하시는 분", "If you are new to Dabom", "Si es nuevo en Dabom",
         "Si vous débutez", "Wenn Sie neu bei Dabom", "ダボムを初めて", "如果您是 Dabom",
         "Если вы новичок", "إذا كنت جديداً"],
        ["이미 AI", "If you already", "Si ya usa", "Si vous utilisez déjà",
         "Wenn Sie KI", "すでに", "如果您已", "Если вы уже", "إذا كنت تستخدم"],
    )
    advanced = section_after(
        raw,
        ["이미 AI·접근성 도구에 익숙하신 분", "If you already use AI or accessibility tools",
         "Si ya usa herramientas", "Si vous utilisez déjà", "Wenn Sie KI",
         "すでに AI", "如果您已熟悉", "Если вы уже", "إذا كنت تستخدم بالفعل"],
        ["주요 기능", "Features at a glance", "Funciones", "Fonctionnalités",
         "Funktionen", "主な機能", "主要功能", "Основные", "الميزات"],
    )
    features = section_after(
        raw,
        ["주요 기능 (요약)", "Features at a glance", "Funciones de un vistazo",
         "Fonctionnalités en bref", "Funktionen im Überblick", "主な機能",
         "功能一览", "Возможности", "الميزات باختصار"],
        ["언어와 도움말", "Languages and help", "Idiomas", "Langues", "Sprachen",
         "言語", "语言", "Языки", "اللغات"],
    )
    langs = section_after(
        raw,
        ["언어와 도움말", "Languages and help", "Idiomas y ayuda", "Langues et aide",
         "Sprachen und Hilfe", "言語とヘルプ", "语言与帮助", "Языки и справка", "اللغات والمساعدة"],
        ["제작", "Made by", "Creado", "Créé", "Erstellt", "制作", "制作", "Создано", "من إعداد"],
    )

    titles = {
        "ko": ("다봄", "한 줄로 말하면", "처음 사용하시는 분", "이미 익숙하신 분", "주요 기능", "언어와 도움말", "시작하기", "다봄 다운로드로 이동"),
        "en": ("Dabom", "In one sentence", "If you are new", "If you already use AI tools", "Features at a glance", "Languages and help", "Getting started", "Go to the Dabom download"),
    }
    t = titles.get(lang, titles["en"])

    how_ko = [
        "아래에서 Dabom_Setup_Full.exe를 받습니다. 로컬 AI를 쓰려면 OllamaSetup.exe도 같은 폴더에 받습니다.",
        "Dabom_Setup_Full.exe를 실행합니다. 옆에 OllamaSetup.exe가 있으면 설치 중 Ollama를 함께 둘 수 있습니다.",
        "설치 후 Alt+Shift+, 로 환경설정 → AI를 연결한 뒤, Alt+Shift+D로 화면 묘사를 시험해 보세요.",
    ]
    how_en = [
        "Download Dabom_Setup_Full.exe below. For optional local AI, also download OllamaSetup.exe into the same folder.",
        "Run Dabom_Setup_Full.exe. If OllamaSetup.exe is beside it, you can install Ollama during setup.",
        "After install, open Preferences (Alt+Shift+Comma), connect an AI service, then try screen description (Alt+Shift+D).",
    ]

    return {
        "nav_dabom": t[0] if lang != "ko" else "다봄",
        "dabom_h2": "다봄" if lang == "ko" else "Dabom",
        "dabom_lead": (
            "다봄은 시각장애인이 AI의 도움으로 일상의 정보에 다가가도록 돕는 Windows 전용 AI 생활 보조 프로그램입니다."
            if lang == "ko"
            else "Dabom is a Windows AI daily-life assistant for visually impaired users."
        ),
        "dabom_intro": strong_name(
            opens
            or (
                "화면을 보지 않아도 스크린리더와 키보드만으로 처음부터 끝까지 사용할 수 있습니다."
                if lang == "ko"
                else "Use it from start to finish with only a screen reader and the keyboard — no need to see the screen."
            ),
            "다봄",
            "Dabom",
        ),
        "dabom_one_h3": "한 줄로 말하면" if lang == "ko" else "In one sentence",
        "dabom_one_p": esc(one_line)
        or (
            "화면·사진·영상·문서·음성을 설명하고, 질문하고, 전사하는 접근성 우선 AI 도우미입니다."
            if lang == "ko"
            else "Dabom describes screens and media, answers questions, transcribes audio, and reads documents — accessibility first."
        ),
        "dabom_new_h3": "처음 사용하시는 분" if lang == "ko" else "If you are new to Dabom",
        "dabom_new_items": bullets(beginner)
        or (
            [
                "NVDA, JAWS, 센스리더 등과 함께 씁니다. 메뉴와 단축키로 이동하고, 마우스는 쓰지 않아도 됩니다.",
                "설치 후 Alt+Shift+, 로 환경설정 → AI 설정에서 서비스와 API 키를 넣습니다.",
                "Alt+Shift+D — 화면 묘사. F2 / F3 — 질문·답변 창. Ctrl+F1 — 키 도움말.",
                "F1 또는 도움말 → 사용자 매뉴얼에서 기능별 설명을 찾습니다.",
            ]
            if lang == "ko"
            else [
                "Works with NVDA, JAWS, SenseReader, and similar tools. Use menus and keyboard shortcuts; a mouse is not required.",
                "After install, open Preferences (Alt+Shift+,). In AI Settings, choose a provider and paste your API key.",
                "Alt+Shift+D — screen description. F2 / F3 — question and answer windows. Ctrl+F1 — key help.",
                "F1 or Help → User Manual for full feature lists.",
            ]
        ),
        "dabom_adv_h3": "이미 익숙하신 분" if lang == "ko" else "If you already use AI or accessibility tools",
        "dabom_adv_p": esc(re.sub(r"\s*\n\s*", " ", advanced).strip())
        or (
            "화면 탐색, 클립보드·카메라, 유튜브·Whisper 전사, PDF·OCR, 프리셋 질문, TTS, Ollama 로컬 AI, 핫키 정의를 한 프로그램에 모았습니다."
            if lang == "ko"
            else "Screen exploration, clipboard and camera, YouTube and Whisper transcription, PDF and OCR, presets, TTS, Ollama local AI, and custom hotkeys — in one place."
        ),
        "dabom_feat_h3": "주요 기능" if lang == "ko" else "Features at a glance",
        "dabom_feat_items": bullets(features)
        or (
            [
                "화면·이미지: 묘사, 탐색, 색·밝기, 카메라, 지폐 등",
                "미디어: 유튜브, 재생, 오디오 설명, Whisper 전사",
                "AI: 질문·번역·PDF·OCR",
                "접근성: 마우스 위치 설명, Ctrl+F1 키 도움말",
            ]
            if lang == "ko"
            else [
                "Screen and images: description, exploration, color, camera, bills",
                "Media: YouTube, playback, audio description, Whisper transcription",
                "AI: Q&A, translation, PDF, OCR",
                "Accessibility: mouse hints, Ctrl+F1 key help",
            ]
        ),
        "dabom_lang_h3": "언어와 도움말" if lang == "ko" else "Languages and help",
        "dabom_lang_p": esc(re.sub(r"\s*\n\s*", " ", langs.split("·")[0] if langs else "").strip())
        or (
            "한국어, English, Español, Français, Deutsch, 日本語, 中文, Русский, العربية — 환경설정에서 전환합니다. intro·매뉴얼·라이선스·AI 가입 안내는 docs 폴더에 있습니다."
            if lang == "ko"
            else "Korean, English, Spanish, French, German, Japanese, Chinese, Russian, Arabic — switch in Preferences. Intro, manuals, licenses, and AI setup guides are in the docs folder."
        ),
        "dabom_how_h3": "시작하기" if lang == "ko" else "Getting started",
        "dabom_how_items": how_ko if lang == "ko" else how_en,
        "goto_dl_dabom": "다봄 다운로드로 이동" if lang == "ko" else "Go to the Dabom download",
        # remove old keys used by previous template
        "dabom_what_h3": "주요 기능" if lang == "ko" else "Features at a glance",
        "dabom_what_lead": "",
        "dabom_what_items": [],
        "dabom_ai_h3": "AI 연결" if lang == "ko" else "AI connection",
        "dabom_ai_p": (
            "클라우드(Claude, GPT, Gemini 등)는 API 키가 필요합니다. PC에서 <strong>Ollama</strong> 로컬 AI도 쓸 수 있습니다. Full 설치 파일 옆에 <code>OllamaSetup.exe</code>가 있으면 설치 마법사에서 Ollama를 함께 둘 수 있습니다."
            if lang == "ko"
            else "Cloud services such as Claude, GPT, and Gemini need an API key. You can also use <strong>Ollama</strong> for local AI on your PC. The full installer can set up Ollama when <code>OllamaSetup.exe</code> is in the same folder."
        ),
    }


def matheon_from_intro(lang: str, raw: str) -> dict:
    paras = first_paras(raw, 2)
    opens = " ".join(paras[:2]) if paras else ""
    # Force version mention to 4.1.5 on site
    opens = re.sub(r"Matheon 4\.0", "Matheon 4.1.5", opens)
    opens = re.sub(r"마테온\(Matheon\) 4\.0", "마테온(Matheon) 4.1.5", opens)
    opens = re.sub(r"마테온 4\.0", "마테온 4.1.5", opens)

    why = section_after(
        raw,
        ["왜 마테온을 만들었나", "Why we made Matheon"],
        ["지금 마테온", "What you can do"],
    )
    can = section_after(
        raw,
        ["지금 마테온으로 할 수 있는 일", "What you can do with Matheon now"],
        ["9개 언어", "Use it in nine languages"],
    )
    langs = section_after(
        raw,
        ["9개 언어로 사용하기", "Use it in nine languages"],
        ["시작하는 방법", "Getting started"],
    )
    start = section_after(
        raw,
        ["시작하는 방법", "Getting started"],
        ["제작 정보", "Credits", "제작:"],
    )

    # Parse [section] groups into feature bullets
    feat_items = []
    cur = None
    for line in can.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            cur = s.strip("[]")
            continue
        if s.startswith("·") or s.startswith("-"):
            item = s.lstrip("·- ").strip()
            if cur:
                feat_items.append(esc(f"{cur}: {item}"))
            else:
                feat_items.append(esc(item))

    how_ko = [
        "아래에서 Matheon_Setup_Full.exe를 받습니다. 로컬 AI를 쓰려면 OllamaSetup.exe도 같은 폴더에 받습니다.",
        "Matheon_Setup_Full.exe를 실행합니다. 옆에 OllamaSetup.exe가 있으면 설치 중 Ollama를 함께 둘 수 있습니다.",
        "실행 후 환경설정에서 AI를 연결하고, 질문창·편집창·도구 메뉴를 차례로 살펴보세요. 자세한 기능은 F1 매뉴얼을 참고하세요.",
    ]
    how_en = [
        "Download Matheon_Setup_Full.exe below. For optional local AI, also download OllamaSetup.exe into the same folder.",
        "Run Matheon_Setup_Full.exe. If OllamaSetup.exe is beside it, you can install Ollama during setup.",
        "After launch, connect your AI in Preferences, then explore the question window, editor, and Tools menu. See F1 for the manual.",
    ]

    return {
        "nav_matheon": "마테온" if lang == "ko" else "Matheon",
        "matheon_h2": "마테온" if lang == "ko" else "Matheon",
        "matheon_lead": MATHEON_LEAD.get(lang, MATHEON_LEAD["en"]),
        "matheon_intro": strong_name(
            opens
            or (
                "마테온은 스크린리더와 키보드만으로 학습·연구를 이어 가도록 만들었습니다."
                if lang == "ko"
                else "Matheon is built so you can study and research with only a screen reader and the keyboard."
            ),
            "마테온",
            "Matheon",
            "마테온(Matheon)",
        ),
        "matheon_why_h3": "왜 마테온을 만들었나" if lang == "ko" else "Why we made Matheon",
        "matheon_why_p": esc(re.sub(r"\s*\n\s*", " ", why).strip())
        or (
            "연구와 학습의 읽기·질문·정리·검색 흐름을 한곳에 모았습니다. 센스리더·NVDA 등과 맞물리며 Ctrl+F1 키 도움말로 익히기 쉽습니다."
            if lang == "ko"
            else "Matheon brings reading, questions, notes, and search into one place. It works with SenseReader, NVDA, and Ctrl+F1 key help."
        ),
        "matheon_feat_h3": "지금 마테온으로 할 수 있는 일" if lang == "ko" else "What you can do with Matheon now",
        "matheon_feat_items": feat_items
        or (
            [
                "AI 대화·연구: 클라우드 AI와 로컬 Ollama, 질문·답변, 학술 검색, 위키피디아",
                "편집·문서: 편집창, PDF 읽기·요약, 사전, 전사",
                "도구: 음성 입력, RSS, 사용자 핫키, 클라우드 동기화",
            ]
            if lang == "ko"
            else [
                "AI dialogue and research: cloud AI and local Ollama, Q&A, academic search, Wikipedia",
                "Editing and documents: editor, PDF reading and summary, dictionary, transcription",
                "Tools: voice input, RSS, custom hotkeys, cloud sync",
            ]
        ),
        "matheon_lang_h3": "9개 언어로 사용하기" if lang == "ko" else "Use it in nine languages",
        "matheon_lang_p": esc(re.sub(r"\s*\n\s*", " ", langs).strip())
        or (
            "한국어, English, Español, Français, Deutsch, 日本語, 中文, Русский, العربية를 지원합니다. 환경설정에서 바꾸면 메뉴가 바로 바뀝니다."
            if lang == "ko"
            else "Matheon supports nine languages. Change the language in Preferences and menus switch immediately."
        ),
        "matheon_how_h3": "시작하는 방법" if lang == "ko" else "Getting started",
        "matheon_how_items": how_ko if lang == "ko" else how_en,
        "matheon_ai_h3": "AI 연결" if lang == "ko" else "AI connection",
        "matheon_ai_p": (
            "클라우드 AI는 API 키가 필요합니다. <strong>Ollama</strong> 로컬 AI도 지원합니다. Full 설치 파일과 같은 폴더에 <code>OllamaSetup.exe</code>를 두면 설치 중 Ollama를 선택할 수 있습니다."
            if lang == "ko"
            else "Cloud AI needs an API key. <strong>Ollama</strong> local AI is also supported. Place <code>OllamaSetup.exe</code> next to the Full installer to offer Ollama during setup."
        ),
        "goto_dl_matheon": "마테온 다운로드로 이동" if lang == "ko" else "Go to the Matheon download",
        "dl_matheon_h3": "마테온 4.1.5 (Windows)" if lang == "ko" else "Matheon 4.1.5 for Windows",
        "dl_matheon_lead": (
            "전체 설치 파일을 받습니다. Ollama 로컬 AI를 쓰려면 <code>OllamaSetup.exe</code>도 <strong>같은 폴더</strong>에 받은 뒤 <code>Matheon_Setup_Full.exe</code>를 실행하십시오."
            if lang == "ko"
            else "Download the full installer. For local AI with Ollama, also download <code>OllamaSetup.exe</code> into the <strong>same folder</strong>, then run <code>Matheon_Setup_Full.exe</code>."
        ),
        "dl_matheon_btn": (
            "마테온 4.1.5 Full 다운로드 — Matheon_Setup_Full.exe"
            if lang == "ko"
            else "Download Matheon 4.1.5 Full — Matheon_Setup_Full.exe"
        ),
        "dl_matheon_file_h3": "마테온 파일 정보" if lang == "ko" else "Matheon file details",
        "dl_matheon_file_items": [
            "Matheon_Setup_Full.exe — full program install (required)."
            if lang != "ko"
            else "Matheon_Setup_Full.exe — 전체 프로그램 설치(필수).",
            "OllamaSetup.exe — optional local AI (same folder)."
            if lang != "ko"
            else "OllamaSetup.exe — 선택 로컬 AI(같은 폴더).",
            "Version 4.1.5. Windows 10 or later, 64-bit."
            if lang != "ko"
            else "버전 4.1.5. Windows 10 이상, 64비트.",
            "Published by The Dabom Project on dabom.org."
            if lang != "ko"
            else "The Dabom Project · dabom.org 공식 배포.",
        ],
        "dl_matheon_need_h3": "마테온에 필요한 것" if lang == "ko" else "What you need for Matheon",
        "dl_matheon_need_items": [
            "A 64-bit Windows 10 or later PC." if lang != "ko" else "64비트 Windows 10 이상 PC.",
            "A screen reader such as NVDA or SenseReader." if lang != "ko" else "NVDA·센스리더 등 스크린리더.",
            "An AI connection: cloud API key and/or Ollama." if lang != "ko" else "AI 연결: 클라우드 API 키 및/또는 Ollama.",
            "Enough free disk space for the installer and optional Ollama." if lang != "ko" else "설치 파일과(선택) Ollama를 둘 충분한 디스크 공간.",
        ],
        "dl_matheon_warn": (
            "새 설치 파일을 처음 실행할 때 Windows가 보안 경고를 띄울 수 있습니다. 이 파일들은 dabom.org에 올린 마테온 공식 패키지입니다."
            if lang == "ko"
            else "Windows may show a security warning the first time you run a new installer. These files are the official Matheon packages published on dabom.org."
        ),
    }


def translate_shell(en: dict, lang: str) -> dict:
    """For non-en/ko: start from EN structure; overlay MATHEON_LEAD and keep EN download labels mostly."""
    d = dict(en)
    d["matheon_lead"] = MATHEON_LEAD.get(lang, en["matheon_lead"])
    # Prefer localized intro file body when present
    return d


def load_intro(folder: Path, lang: str) -> str:
    p = folder / f"intro_{lang}.txt"
    if not p.exists():
        p = folder / "intro_en.txt"
    return p.read_text(encoding="utf-8")


def main() -> None:
    base = json.loads((ROOT / "i18n_base.json").read_text(encoding="utf-8"))
    extra = json.loads((ROOT / "i18n_extra.json").read_text(encoding="utf-8"))

    # Build en/ko carefully from intros
    for lang in ("en", "ko"):
        dab = dabom_from_intro(lang, load_intro(DABOM_INTRO, lang))
        mat = matheon_from_intro(lang, load_intro(MATHEON_INTRO, lang))
        # Fix dabom lead from intro (not matheon)
        if lang == "ko":
            dab["dabom_lead"] = "다봄은 시각장애인이 AI의 도움으로 일상의 정보에 다가가도록 돕는 Windows 전용 AI 생활 보조 프로그램입니다."
            dab["dabom_h2"] = "다봄"
            dab["nav_dabom"] = "다봄"
        else:
            dab["dabom_lead"] = "Dabom is a Windows AI daily-life assistant for visually impaired users."
            dab["dabom_h2"] = "Dabom"
            dab["nav_dabom"] = "Dabom"
        target = base[lang]
        target.update(dab)
        target.update(mat)
        # Site about mentions three products
        if lang == "ko":
            target["about_p1"] = (
                "대표 프로그램은 <strong>다봄</strong> 3.1.4 — AI 기반 Windows 생활 도우미입니다. "
                "학습·연구 보조 <strong>마테온</strong> 4.1.5, 접근성 게임 모음 <strong>다놀</strong> 1.3.3도 받을 수 있습니다."
            )
            target["a11y_lead"] = "다봄·마테온·다놀은 키보드와 음성 안내를 중심에 두고 만들었습니다. 이 웹사이트도 같은 생각입니다."
            target["a11y_end"] = "다봄·마테온·다놀이나 이 페이지에서 스크린리더로 쓰기 어려운 점이 있으면 알려 주세요."
            target["dl_lead"] = "이 사이트에서 공식 설치 파일을 받습니다. 다봄, 마테온, 다놀 순으로 안내합니다."
            target["dl_ollama_btn"] = "OllamaSetup.exe 다운로드 (선택, 약 1.39GB)"
        else:
            target["about_p1"] = (
                "The flagship program here is <strong>Dabom</strong> 3.1.4 — an AI-based Windows daily-life assistant. "
                "You can also download <strong>Matheon</strong> 4.1.5 (learning and research) and <strong>Danol</strong> 1.3.3 (accessible games)."
            )
            target["a11y_lead"] = "Dabom, Matheon, and Danol are built around keyboard use and spoken feedback. This website follows the same idea."
            target["a11y_end"] = "If something on Dabom, Matheon, Danol, or this page is hard to use with a screen reader, write to us."
            target["dl_lead"] = "Download the official packages from this site. Dabom, Matheon, and Danol are listed in that order."
            target["dl_ollama_btn"] = "Download OllamaSetup.exe (optional, about 1.39 GB)"

    # Other languages: copy EN product keys, override leads/nav from intro when possible
    en_dab = {k: v for k, v in base["en"].items() if k.startswith("dabom_") or k in ("nav_dabom", "goto_dl_dabom", "dl_ollama_btn")}
    en_mat = {k: v for k, v in base["en"].items() if k.startswith("matheon_") or k.startswith("dl_matheon") or k in ("nav_matheon", "goto_dl_matheon")}
    for lang in CODES:
        if lang in ("en", "ko"):
            continue
        bucket = extra if lang in extra else base
        if lang not in bucket:
            continue
        t = bucket[lang]
        # Dabom from that language's intro when available
        dab = dabom_from_intro("en", load_intro(DABOM_INTRO, lang))
        # Prefer localized opening from intro
        paras = first_paras(load_intro(DABOM_INTRO, lang), 2)
        if paras:
            dab["dabom_intro"] = strong_name(paras[0], "Dabom", "다봄", "ダボム")
            dab["dabom_lead"] = paras[0].split(".")[0].strip() + ("." if not paras[0].strip().endswith(".") else "")
        # Merge EN how/download-oriented keys for consistency of installer names
        dab["dabom_how_items"] = en_dab.get("dabom_how_items", dab["dabom_how_items"])
        dab["goto_dl_dabom"] = en_dab.get("goto_dl_dabom", "Go to the Dabom download")
        dab["nav_dabom"] = "Dabom"
        dab["dabom_h2"] = "Dabom"
        mat = matheon_from_intro("en", load_intro(MATHEON_INTRO, lang))
        mat["matheon_lead"] = MATHEON_LEAD.get(lang, mat["matheon_lead"])
        paras_m = first_paras(load_intro(MATHEON_INTRO, lang), 2)
        if paras_m:
            body = " ".join(paras_m)
            body = re.sub(r"4\.0", "4.1.5", body)
            mat["matheon_intro"] = strong_name(body, "Matheon", "마테온", "マテオン")
        mat["matheon_how_items"] = en_mat.get("matheon_how_items", mat["matheon_how_items"])
        mat["goto_dl_matheon"] = en_mat.get("goto_dl_matheon", "Go to the Matheon download")
        mat["nav_matheon"] = "Matheon"
        mat["matheon_h2"] = "Matheon"
        # Keep EN download button labels (file names) for clarity; lead from EN with version
        for k, v in en_mat.items():
            if k.startswith("dl_matheon"):
                mat[k] = v
        t.update(dab)
        t.update(mat)
        t["about_p1"] = (
            "The flagship program here is <strong>Dabom</strong> 3.1.4 — an AI-based Windows daily-life assistant. "
            "You can also download <strong>Matheon</strong> 4.1.5 (learning and research) and <strong>Danol</strong> 1.3.3 (accessible games)."
        )
        t["dl_lead"] = "Download the official packages from this site. Dabom, Matheon, and Danol are listed in that order."
        t["a11y_lead"] = "Dabom, Matheon, and Danol are built around keyboard use and spoken feedback. This website follows the same idea."
        t["a11y_end"] = "If something on Dabom, Matheon, Danol, or this page is hard to use with a screen reader, write to us."
        t["dl_ollama_btn"] = base["en"]["dl_ollama_btn"]

    (ROOT / "i18n_base.json").write_text(
        json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "i18n_extra.json").write_text(
        json.dumps(extra, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("i18n updated")


if __name__ == "__main__":
    main()
