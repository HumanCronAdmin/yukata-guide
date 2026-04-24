# Yukata-Guide Voice Template (お手本・承認版)

**Reference commit**: `b4cdafc` (2026-04-24)
**Approved article**: `data/guides.js` 3本 (how-to-wear / yukata-vs-kimono / sizing-guide)
**Quality gate**: 4層全PASS (Liability / Layer1 事実 / Layer2 温度感 / Layer3 独自性)

このテンプレートは浴衣系SEO記事・info_guide系記事 (japan-life-guide / stationery-atlas 等) の voice_profile_japan_expat 準拠の書き方を示す。新規記事生成時は必ずこのテンプレを参照プロンプトに入れる。

---

## 絶対ルール (違反=FAIL)

### 1. 三人称・一人称禁止
- NG: `I often see`, `Let me`, `We'll`, `let's`, `in my experience`, `from someone who's navigated`
- OK: `Visitors often express`, `This guide covers`, `Japanese people are almost always`

### 2. 命令文禁止 (info_guideはゼロ許容)
- NG: `you should`, `you need to`, `you must`, `make sure you`
- OK: 受動記述 `is tied`, `is wrapped`, `is recommended` または読者二人称のassertive `your waist`, `your obi`

### 3. AI禁止語 (regex検出対象・変化形含む)
- quintessential(ly), elevate(d/s/ing), facilitate(d/s/ing), comprehensive(ly), significantly, honestly, certainly, essentially, absolutely, incredibly, genuinely, seamless, sophisticated, iconic, emblematic
- 代替: `raise(d)`, `help`, `complete/thorough`, `noticeably/clearly`, 副詞を削除

### 4. 命令文回避で受動態重なり過ぎ注意
- 4文連続 `is X-ed` になったら `your` 読者二人称で1-2文差し込む
- 例: `The koshihimo is tied at the waist. Your hands smooth the front.` のように交互に

---

## 承認版のトーン特徴 (コピー元)

### Intro の型 (3段落構成)
1. **状況描写段**: `Welcome to Japan! One of the most enchanting experiences during the warmer months...` — 季節/場面から入る
2. **ハードル解消段**: `Visitors often express hesitation... Japanese people are almost always thrilled...` — 初心者の心理的壁を崩す
3. **ガイド宣言段**: `This guide covers everything needed... This preparation aims to help create wonderful summer memories.` — 記事の網羅範囲を一行で

### Section content の型
- 1-2文で目的説明 → 箇条書きで要素 → 各要素 `**名前(kanji)**: 説明 + 役割` の形式
- 例: `**Koshihimo (腰紐)**: These are thin fabric waist ties, typically made of cotton or gauze. At least two, possibly three, are needed to secure the yukata.`

### Steps の型
- `**Step N: <Action Noun Phrase>**\n<受動態または three-person 記述>`
- 例: `**Step 4: Wrap the Right Panel**\nThe right panel of the yukata is wrapped firmly across the body, ensuring it goes against the body first.`

### 日本語用語は必ず kanji + romaji セット
- `yukata (浴衣)`, `obi (帯)`, `koshihimo (腰紐)`, `ohashori (おはしょり)`, `migi-mae (右前)`, `hidari-mae (左前)`, `shinishozoku (死装束)`, `bunko musubi (文庫結び)`

### FAQ の型
- Q: 読者目線の疑問 (1文)
- A: 2-4文の三人称解説。`Yes/No` → `Yes. Japanese people are generally happy to see...` のように断定+理由

---

## 新規記事生成時のプロンプト雛形

```
Write an English SEO article in JSON format for: "<TITLE>"

Target keyword: "<KEYWORD>"
Audience: English-speaking foreigners in Japan or planning to visit Japan
Voice profile: voice_profile_japan_expat — **third person ONLY**. No "I", "we", "my", "our", "let me", "let's", "we'll".
Tone: Informative, guide-like, tatami calm. NOT enthusiastic, NOT reassuring-over-reader.

BANNED (will FAIL auto-gate):
- Imperatives: "you should", "you need to", "you must", "make sure you"
- AI words: quintessential, elevate(d/s), facilitate(d/s), comprehensive, significantly, honestly, certainly, essentially, absolutely, incredibly, genuinely, seamless, sophisticated, iconic
- First-person experience claims: "from someone who's navigated", "in my experience"

REQUIRED:
- All Japanese terms with kanji + romaji: e.g., "yukata (浴衣)", "obi (帯)"
- Intro = 3 paragraphs (situation / concern-resolution / guide-scope)
- Each section: 1-2 intro sentences + structured bullets/steps
- FAQ answers in 2-4 sentences, third person, definite

See projects/yukata-guide/data/guides.js (commit b4cdafc) for the approved example.

Return ONLY valid JSON matching the structure in the example. No preamble.
```

---

## 品質ゲート通過までの手順 (コンテンツ追加時)

1. Gemini で生成 (上記プロンプト使用)
2. `py scripts/article_quality_gate.py --file <path> --project yukata-guide` で4層チェック
3. FAIL したら:
   - Liability FAIL → 命令文/一人称をgrep → 手動書換 or `projects/yukata-guide/scripts/rewrite_voice.py` を生成結果に適用
   - Layer 2 FAIL → voice違反箇所を `polish_voice.py` で修正
4. 全PASS → hookが二重検証しながらcommit+push

---

## 既存お手本コンテンツ (参照)

- `data/guides.js` how-to-wear のintro → 3段落構成の見本
- `data/guides.js` how-to-wear Step-by-Step: Women's Yukata → 受動態+`your`ミックスの見本
- `data/guides.js` yukata-vs-kimono の比較セクション → 情報羅列型の見本
- `data/guides.js` sizing-guide の FAQ → Q/A型の見本

将来の浴衣記事は上記を読んで同じ硬さ/情報密度で書く。
