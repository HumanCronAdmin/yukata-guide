"""
rewrite_voice.py — Surgical voice rewrite for yukata-guide articles

入力: /tmp/yukata_failed_articles_20260424.js.bak (FAIL記事3本のJSON)
処理: 各intro/section.content/section.steps を Gemini に渡し、
      一人称/命令文/AI禁止語だけを書き換える(事実・手順・商品リストは保持)
出力: projects/yukata-guide/data/guides.js

使い方:
  py projects/yukata-guide/scripts/rewrite_voice.py

事実骨格は保持するので Layer 1 PASSは維持、voice/liability/AI語のみ修正対象。
"""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from ai_router import ai_call

import os
_TEMP = Path(os.environ.get("TEMP", r"C:\Users\user\AppData\Local\Temp"))
BACKUP_CANDIDATES = [
    _TEMP / "yukata_failed_articles_20260424.js.bak",
    Path("/tmp/yukata_failed_articles_20260424.js.bak"),
    ROOT / "projects" / "yukata-guide" / "data" / "guides.js.FAIL_backup_20260424",
]
BACKUP = next((p for p in BACKUP_CANDIDATES if p.exists()), BACKUP_CANDIDATES[0])
OUTPUT = ROOT / "projects" / "yukata-guide" / "data" / "guides.js"

REWRITE_PROMPT = """You are editing an English SEO article for a Japan information guide site.

CRITICAL CONSTRAINTS — the site's voice_profile_japan_expat REQUIRES:
1. Third person only. REMOVE all first-person: "I", "we", "my", "our", "let me", "let's", "we'll", "you'll find", "from someone who", "as someone living here"
2. No imperative/command phrasing toward the reader. REWRITE as factual description:
   - "you should wrap" -> "the right panel wraps"
   - "you need to tie" -> "the koshihimo is tied"
   - "you must double-check" -> "this step is double-checked"
   - "make sure you" -> "it is"  (or restructure)
3. No AI-banned words anywhere: quintessential, elevate, elevated, honestly, certainly, essentially, ultimately, importantly, absolutely, incredibly, genuinely, truly, definitely, significantly, beautifully, meticulously, exquisite, invaluable, crucial, vital, seamless, sophisticated, iconic, emblematic
4. No first-person experience claims ("from someone who's navigated festivals", "in my experience")
5. PRESERVE: all facts, Japanese terms (romaji+kanji), step numbers, product lists, FAQ answers

Return ONLY the rewritten text. No preamble, no explanation, no JSON — just the plain rewritten text that goes back into the same field.

===ORIGINAL TEXT===
{text}
===END ORIGINAL==="""


def rewrite_text(text, label=""):
    if not text or not isinstance(text, str):
        return text
    # Quick skip: if text has no violations, don't round-trip
    lowered = text.lower()
    triggers = ["i ", " i'", "we ", "we'", "our ", "my ", "let me", "let's", "you should",
                "you need to", "you must", "you'll ", "make sure you", "from someone",
                "quintessential", "elevate", "elevated", "honestly", "certainly", "essentially",
                "ultimately", "importantly", "absolutely", "incredibly", "genuinely", "truly",
                "definitely", "significantly", "beautifully", "exquisite", "invaluable", "crucial",
                "vital", "seamless", "sophisticated", "iconic", "emblematic"]
    has_issue = any(t in lowered for t in triggers) or re.search(r"\bI\b", text)
    if not has_issue:
        return text

    prompt = REWRITE_PROMPT.format(text=text)
    try:
        result = ai_call(prompt, task_type="quality", require_api="gemini",
                         max_tokens=len(text) // 2 + 2000)
        out = result.get("text", "").strip() if isinstance(result, dict) else str(result).strip()
        # Strip any leading/trailing markdown or code fences
        out = re.sub(r"^```[a-z]*\n?", "", out)
        out = re.sub(r"\n?```$", "", out)
        if len(out) < len(text) * 0.3:
            print(f"  [WARN] {label}: rewrite too short ({len(out)} vs {len(text)}), keeping original")
            return text
        return out
    except Exception as e:
        print(f"  [ERR] {label}: {e}", flush=True)
        return text


def rewrite_article(article):
    aid = article.get("id", "?")
    print(f"[{aid}] rewriting...", flush=True)
    if article.get("intro"):
        article["intro"] = rewrite_text(article["intro"], f"{aid}/intro")
    for i, sec in enumerate(article.get("sections", [])):
        head = sec.get("heading", f"sec{i}")
        if sec.get("content"):
            sec["content"] = rewrite_text(sec["content"], f"{aid}/{head}/content")
        if sec.get("steps"):
            sec["steps"] = [rewrite_text(s, f"{aid}/{head}/step{j}") for j, s in enumerate(sec["steps"])]
    # FAQs: rewrite answers if needed
    for i, faq in enumerate(article.get("faq", [])):
        if faq.get("a"):
            faq["a"] = rewrite_text(faq["a"], f"{aid}/faq{i}")
    return article


def load_backup():
    raw = BACKUP.read_text(encoding="utf-8")
    # Strip "const guides = " prefix and trailing ";"
    m = re.search(r"const\s+guides\s*=\s*(\[.*\])\s*;?\s*$", raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"Could not parse backup: {BACKUP}")
    return json.loads(m.group(1))


def main():
    articles = load_backup()
    print(f"Loaded {len(articles)} articles from {BACKUP}")
    rewritten = [rewrite_article(a) for a in articles]
    out_js = "const guides = " + json.dumps(rewritten, indent=1, ensure_ascii=False) + ";\n"
    OUTPUT.write_text(out_js, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(out_js)} chars)")


if __name__ == "__main__":
    main()
