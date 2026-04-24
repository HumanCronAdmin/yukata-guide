(async function(){
  const res = await fetch('data/rentals.json');
  const data = await res.json();
  const shops = (data.shops || []).filter(s => s.website && s.verified);
  const grid = document.getElementById('rentalGrid');
  const filters = document.querySelectorAll('.rental-filter button');
  let currentCity = '';

  function render(){
    const list = currentCity ? shops.filter(s => s.city === currentCity) : shops;
    if(list.length === 0){
      grid.innerHTML = '<div class="empty-state">No shops in this city yet. The directory is growing — check back soon.</div>';
      return;
    }
    grid.innerHTML = list.map(s => {
      const priceRange = (s.price_from_jpy && s.price_to_jpy)
        ? `¥${s.price_from_jpy.toLocaleString()} – ¥${s.price_to_jpy.toLocaleString()}`
        : (s.price_from_jpy ? `from ¥${s.price_from_jpy.toLocaleString()}` : 'Price varies');
      const tags = [];
      if(s.verified) tags.push('<span class="tag tag-verified">✓ Verified</span>');
      if(s.english_support) tags.push('<span class="tag">English OK</span>');
      if(s.online_booking) tags.push('<span class="tag">Online Booking</span>');
      return `
        <div class="rental-card">
          <h3>${escapeHtml(s.name)}</h3>
          <div class="rental-meta">${escapeHtml(s.city)} · ${escapeHtml(s.area || '')} · ${priceRange}</div>
          <div class="rental-specialty">${escapeHtml(s.specialty || '')}</div>
          <div class="rental-tags">${tags.join('')}</div>
          <a class="rental-visit" href="${s.website}" target="_blank" rel="noopener" onclick="gtag('event','rental_visit',{shop:'${escapeHtml(s.name)}',city:'${escapeHtml(s.city)}'})">Visit website →</a>
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
    currentCity = b.dataset.city || '';
    render();
  }));

  render();
})();
