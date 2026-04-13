(() => {
  let products = [];
  const CATEGORY_LABEL = {
    yukata: "Yukata", obi: "Obi", geta: "Geta", accessories: "Accessories", set: "Set"
  };
  const GENDER_LABEL = {
    women: "Women", men: "Men", unisex: "Unisex", kids: "Kids"
  };
  const MATERIAL_LABEL = {
    cotton: "Cotton", polyester: "Polyester", linen: "Linen", "cotton-blend": "Cotton Blend",
    wood: "Wood", fabric: "Fabric", metal: "Metal", bamboo: "Bamboo", plastic: "Plastic", paulownia: "Paulownia Wood"
  };

  const $ = id => document.getElementById(id);

  function populateFilters() {
    const cats = [...new Set(products.map(p => p.category))].sort();
    const genders = [...new Set(products.map(p => p.gender))].sort();
    const mats = [...new Set(products.map(p => p.material))].sort();

    cats.forEach(c => $("category").innerHTML += `<option value="${c}">${CATEGORY_LABEL[c] || c}</option>`);
    genders.forEach(g => $("gender").innerHTML += `<option value="${g}">${GENDER_LABEL[g] || g}</option>`);
    mats.forEach(m => $("material").innerHTML += `<option value="${m}">${MATERIAL_LABEL[m] || m}</option>`);
  }

  function getFiltered() {
    const q = $("search").value.toLowerCase();
    const cat = $("category").value;
    const gen = $("gender").value;
    const mat = $("material").value;
    const sort = $("sort").value;

    let list = products.filter(p => {
      if (cat && p.category !== cat) return false;
      if (gen && p.gender !== gen) return false;
      if (mat && p.material !== mat) return false;
      if (q && !p.name.toLowerCase().includes(q) && !p.brand.toLowerCase().includes(q)) return false;
      return true;
    });

    if (sort === "price-asc") list.sort((a, b) => a.price_usd - b.price_usd);
    else if (sort === "price-desc") list.sort((a, b) => b.price_usd - a.price_usd);
    else if (sort === "name-asc") list.sort((a, b) => a.name.localeCompare(b.name));

    return list;
  }

  function renderCard(p) {
    const sizesHtml = (p.sizes_available || []).map(s => `<span class="size-tag">${s}</span>`).join("");
    const prosHtml = (p.pros || []).map(pr => `<li>${pr}</li>`).join("");
    const expertHtml = p.expert_note ? `<div class="expert-note">${p.expert_note}</div>` : "";
    const styleHtml = p.style_tip ? `<div class="style-tip">${p.style_tip}</div>` : "";
    const setBadge = p.includes_obi ? `<span class="badge badge-set">Includes Obi</span>` : "";
    const nameJa = p.name_ja ? `<div class="name-ja">${p.name_ja}</div>` : "";
    const patternMeta = p.pattern ? `<span>${p.pattern}</span>` : "";
    const amazonHtml = p.amazon_url ? `<a href="${p.amazon_url}" class="amazon-link" target="_blank" rel="noopener">Search on Amazon</a>` : "";

    return `<div class="product-card">
      <div class="brand">${p.brand}</div>
      <h3>${p.name}</h3>
      ${nameJa}
      <div class="badges">
        <span class="badge badge-cat">${CATEGORY_LABEL[p.category] || p.category}</span>
        <span class="badge badge-mat">${MATERIAL_LABEL[p.material] || p.material}</span>
        <span class="badge badge-gender">${GENDER_LABEL[p.gender] || p.gender}</span>
        ${setBadge}
      </div>
      <div class="product-meta">
        ${patternMeta}
      </div>
      <div class="sizes">${sizesHtml}</div>
      <div class="product-price">$${p.price_usd.toFixed(2)}</div>
      <ul class="product-pros">${prosHtml}</ul>
      <div class="product-best"><strong>Best for:</strong> ${p.best_for}</div>
      ${expertHtml}
      ${styleHtml}
      ${amazonHtml}
    </div>`;
  }

  function render() {
    const list = getFiltered();
    $("resultCount").textContent = `${list.length} product${list.length !== 1 ? "s" : ""} found`;
    $("grid").innerHTML = list.map(renderCard).join("");
  }

  function init() {
    fetch("data/products.json")
      .then(r => r.json())
      .then(data => {
        products = data;
        populateFilters();
        render();
      })
      .catch(err => {
        $("grid").innerHTML = `<p style="padding:24px;color:#6B6B8D">Could not load products. ${err.message}</p>`;
      });

    ["search", "category", "gender", "material", "sort"].forEach(id => {
      $(id).addEventListener(id === "search" ? "input" : "change", render);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
