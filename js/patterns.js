(async function(){
  const res = await fetch('data/patterns.json');
  const data = await res.json();
  const patterns = data.patterns || [];
  const grid = document.getElementById('patternGrid');
  const filters = document.querySelectorAll('#seasonFilter button');
  let currentSeason = '';

  function render(){
    const list = currentSeason
      ? patterns.filter(p => (p.season || '').toLowerCase().includes(currentSeason))
      : patterns;
    grid.innerHTML = list.map(p => {
      const tags = [];
      if(p.season) tags.push(`<span class="pattern-tag season">${escapeHtml(p.season)}</span>`);
      if(p.best_for) tags.push(`<span class="pattern-tag">${escapeHtml(p.best_for)}</span>`);
      return `
        <div class="pattern-card" onclick="gtag('event','pattern_view',{pattern:'${escapeHtml(p.slug)}'})">
          <div class="pattern-name-en">${escapeHtml(p.name_en || p.name_romaji)}</div>
          <div class="pattern-name-jp"><span class="kanji">${escapeHtml(p.name_kanji || '')}</span><span>${escapeHtml(p.name_romaji || '')}</span></div>
          <div class="pattern-meaning">${escapeHtml(p.meaning || '')}</div>
          <div class="pattern-tags">${tags.join('')}</div>
          ${p.pair_with ? `<div class="pattern-meaning" style="margin-top:8px;font-size:.82rem;color:#777"><strong>Obi pairing:</strong> ${escapeHtml(p.pair_with)}</div>` : ''}
        </div>`;
    }).join('');
  }

  function escapeHtml(t){
    if(!t) return '';
    return String(t).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  filters.forEach(b => b.addEventListener('click', () => {
    filters.forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    currentSeason = b.dataset.season || '';
    render();
  }));

  render();
})();
