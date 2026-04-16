# Yukata Guide — 仕様書

## 現状（2026-04-16時点）
- **公開済み:** index.html (トップ) + database.html (商品DB 30件) + products.json
- **デプロイ済み:** https://humancronadmin.github.io/yukata-guide/
- **GA4 + Clarity:** 設定済み
- **足りないもの:** SEO記事ページ（検索流入の本丸）

## Problem
英語で浴衣を包括的にカバーするサイトがゼロ。japan-guide.comやブログ記事が散在するだけ。
特に「外国人体型向けサイズガイド」「浴衣の着方ステップバイステップ」は競合ゼロ。

## Solution
既存データベースに加え、SEO記事を段階的に追加。検索流入→DB→アフィリエイトの導線を作る。

## Tech Stack
- GitHub Pages, Vanilla JS + Tailwind CSS (CDN)
- GA4 (G-MXKH7PSKC2) + Clarity
- Amazon JPアフィリエイト (japantool-20)

## 今回のスコープ: SEO記事3本追加（Week 1: 4/16〜4/20）

### 追加ファイル
- `guide.html` — 記事表示ページ（URLパラメータ `?id=xxx` で記事切替）
- `data/guides.js` — 記事データ（3本分）
- index.htmlに「Guides」セクション追加（カード3枚→guide.htmlへ導線）

### 記事1: How to Wear a Yukata: Step-by-Step for Beginners
- **Target keyword:** "how to wear yukata"
- **Search volume:** High / Competition: 4
- **Intent:** Informational
- **構成:**
  1. イントロ — 浴衣は誰でも着られる（怖くない）
  2. What You'll Need — 必要な小物一覧（腰ひも・伊達締め・帯・下駄）→ 各Amazon商品リンク
  3. Step-by-Step (8ステップ) — 右前を先に / 腰ひもの位置 / おはしょり / 伊達締め / 帯の結び方
  4. Common Mistakes — 左前にしてしまう（=死装束）/ 襟が開きすぎ / 帯が高すぎ
  5. Men vs Women — 男性の着方の違い（おはしょりなし・帯の位置低め）
  6. Quick Tips for Festivals — 動きやすい帯結び / 暑さ対策 / 持ち物
- **Schema:** HowTo markup
- **アフィリエイト:** 腰ひも・伊達締め・帯・下駄・浴衣セット

### 記事2: Yukata vs Kimono: Key Differences Foreigners Need to Know
- **Target keyword:** "yukata vs kimono difference"
- **Search volume:** Medium / Competition: 3
- **Intent:** Informational
- **構成:**
  1. 一言で言うと — 浴衣=夏のカジュアル着物。着物=フォーマル〜普段着
  2. 比較表 — 素材・季節・値段・着付け時間・小物の数・TPO
  3. When to Wear Yukata — 花火・祭り・旅館・夏のお出かけ
  4. When to Wear Kimono — 成人式・結婚式・お茶会・正月
  5. Can Foreigners Wear Yukata? — 文化盗用の議論に対する現実的な回答
  6. Where to Start — 初心者は浴衣から→DBへ導線
- **Schema:** Article + FAQPage
- **アフィリエイト:** 浴衣セット（入門用）

### 記事3: Yukata Size Guide for Non-Japanese Body Types
- **Target keyword:** "yukata size guide for foreigners"
- **Search volume:** Medium / Competition: 2（競合ほぼゼロ）
- **Intent:** Informational → Transactional
- **構成:**
  1. Why Standard Sizing Doesn't Work — 日本のS/M/Lは身長ベース、体型考慮なし
  2. How Japanese Sizing Works — 身丈・裄丈・袖丈の意味と測り方
  3. Size Chart — 身長×ヒップの2軸マッピング表（S〜3L + TL）
  4. Tall Foreigners (170cm+) — TL/トールサイズの選び方・おはしょりで調整
  5. Plus Size (ヒップ100cm+) — BL/3Lサイズ・仕立て直し
  6. How to Measure Yourself — 3箇所（身長・ヒップ・裄丈）の測り方図解
  7. Recommended Products by Size — サイズ別おすすめ浴衣→DB/Amazonリンク
- **Schema:** Article + HowTo (測り方)
- **アフィリエイト:** サイズ別浴衣・メジャー

## 季節タイムライン（最重要）
- **4月末〜5月:** 検索上昇開始 ← 今。5月前半に3記事公開必須
- **7月〜8月:** ピーク（花火・祭り・お盆）
- **通年:** 旅館需要あり（低いがゼロではない）

## Week 2以降のロードマップ
1. アクセサリーチェックリスト記事
2. メンズ浴衣ガイド
3. Where to Buy Yukata in Tokyo（実店舗レビュー）
4. How to Buy Secondhand Yukata on Mercari
5. ケア・保管ガイド
6. 祭り別スタイリングガイド

## Revenue Model
- **初期:** Amazon JP affiliate (japantool-20)
- **中期 (月5,000PV〜):** 楽天追加 + ブランド営業
- **長期 (月10,000PV〜):** スポンサード記事

## publish向け情報
- **URL:** https://humancronadmin.github.io/yukata-guide/
- **ターゲット:** 日本に住む/旅行する英語圏の外国人で浴衣を着たい人
- **訴求:** "The only English guide covering yukata sizing for non-Japanese body types"
- **投稿先:** r/japanlife, r/JapanTravel, r/movingtojapan
- **note切り口:** 「外国人向け浴衣ガイドを作った理由」
