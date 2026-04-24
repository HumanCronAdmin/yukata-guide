"""
polish_voice.py — Targeted natural-flow polish on already-voice-fixed yukata articles

入力: projects/yukata-guide/data/guides.js (voice-rewrite済のPASS状態)
処理: 破綻した文・過剰受動態・残留禁止語変化形を Gemini で polish
出力: projects/yukata-guide/data/guides.js (in-place)

基本方針: 声は既に直ってる。残ってるのは grammar/flow/naturalness。
"""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from ai_router import ai_call

TARGET = ROOT / "projects" / "yukata-guide" / "data" / "guides.js"

POLISH_PROMPT = """You are polishing an English SEO guide article for a Japan information site.

The article is already in third-person and passes voice checks. Focus now on NATURAL FLOW and GRAMMAR.

CONSTRAINTS (must keep):
1. Stay in third person. No "I", "we", "my", "our", "let me", "you should", "you must".
2. No AI-banned words: quintessential, elevate(d/ing/s), facilitate(d/ing/s), comprehensive, significantly, honestly, certainly, essentially, absolutely, incredibly, genuinely, crucial, vital, seamless, sophisticated, iconic, emblematic
3. Preserve every fact, step number, Japanese term (kanji+romaji), product name, measurement, and rule.
4. "you" / "your" addressing the reader for second-person instructional voice IS allowed and preferred over heavy passive stacks. ("Your waist" is fine; "I'll show you" is not.)

WHAT TO FIX:
1. Broken grammar — subject/verb missing, nonsensical phrasing
2. Over-stacked passive voice (4+ consecutive "is X-ed" sentences) — alternate with imperative-free active voice using "you/your" reader-addressed form
3. Awkward rewrites where meaning got lost (e.g., "aims to help wonderful summer memories" is broken)
4. Remove any remaining banned-word variants (facilitating, elevated, etc.)

Return ONLY the polished text. No preamble. Same length ±15%. Preserve markdown formatting (** for bold, * for lists, \\n for linebreaks).

===ORIGINAL===
{text}
===END ORIGINAL==="""

BANNED_VARIANTS = re.compile(
    r"\b(facilitat\w*|elevat\w*|quintessential\w*|comprehens\w*|significantl\w*|honestl\w*|certainl\w*|"
    r"essentially|absolutely|incredibly|genuinely|seamless\w*|sophisticated|iconic|emblematic)\b",
    re.IGNORECASE,
)

BROKEN_PATTERNS = [
    re.compile(r"aims to help wonderful"),  # Known broken phrase
    re.compile(r"is held\b.*?\bis wrapped\b.*?\bis tied\b.*?\bis"),  # 4+ consecutive passive
]


def needs_polish(text):
    if not text or not isinstance(text, str) or len(text) < 30:
        return False
    if BANNED_VARIANTS.search(text):
        return True
    if any(p.search(text) for p in BROKEN_PATTERNS):
        return True
    # Over-passive: 4+ "is <past-participle>" within 300 chars
    passive_hits = re.findall(r"\b(?:is|are|was|were)\s+\w+ed\b", text)
    if len(passive_hits) >= 4 and len(text) < 800:
        return True
    return False


def polish_text(text, label=""):
    if not needs_polish(text):
        return text
    prompt = POLISH_PROMPT.format(text=text)
    try:
        result = ai_call(prompt, task_type="quality", require_api="gemini",
                         max_tokens=max(len(text) // 2 + 500, 1500))
        if not result or not result.get("text"):
            print(f"  [SKIP] {label}: no result", flush=True)
            return text
        out = result["text"].strip()
        out = re.sub(r"^```[a-z]*\n?", "", out)
        out = re.sub(r"\n?```$", "", out)
        # Sanity: result shouldn't be drastically shorter
        if len(out) < len(text) * 0.5:
            print(f"  [WARN] {label}: too short ({len(out)} vs {len(text)}), keeping original", flush=True)
            return text
        # Sanity: still banned?
        if BANNED_VARIANTS.search(out):
            print(f"  [WARN] {label}: still has banned variant, keeping original", flush=True)
            return text
        print(f"  [OK] {label}: polished ({len(text)} -> {len(out)})", flush=True)
        return out
    except Exception as e:
        print(f"  [ERR] {label}: {e}", flush=True)
        return text


def polish_article(article):
    aid = article.get("id", "?")
    print(f"[{aid}] scanning for polish targets...", flush=True)
    if article.get("intro"):
        article["intro"] = polish_text(article["intro"], f"{aid}/intro")
    for i, sec in enumerate(article.get("sections", [])):
        head = sec.get("heading", f"sec{i}")
        if sec.get("content"):
            sec["content"] = polish_text(sec["content"], f"{aid}/{head}/content")
        if sec.get("steps"):
            sec["steps"] = [polish_text(s, f"{aid}/{head}/step{j}") for j, s in enumerate(sec["steps"])]
    for i, faq in enumerate(article.get("faq", [])):
        if faq.get("a"):
            faq["a"] = polish_text(faq["a"], f"{aid}/faq{i}")
    return article


def main():
    raw = TARGET.read_text(encoding="utf-8")
    m = re.search(r"const\s+guides\s*=\s*(\[.*\])\s*;?\s*$", raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"Could not parse {TARGET}")
    articles = json.loads(m.group(1))
    print(f"Loaded {len(articles)} articles", flush=True)
    polished = [polish_article(a) for a in articles]
    out_js = "const guides = " + json.dumps(polished, indent=1, ensure_ascii=False) + ";\n"
    TARGET.write_text(out_js, encoding="utf-8")
    print(f"Wrote {TARGET} ({len(out_js)} chars)", flush=True)


if __name__ == "__main__":
    main()
