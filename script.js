(function setMetaDates(){
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
  const u = document.getElementById('last-update');
  if (u) u.textContent = new Date().toISOString().slice(0,10);
})();

// dynamic status badge color
function statusClass(status) {
  if (!status) return '';
  const s = status.toLowerCase();
  if (s.includes('dostępny'))   return 'badge-green';
  if (s.includes('zarezerw'))   return 'badge-orange';
  if (s.includes('niedostęp'))  return 'badge-gray';
  return '';
}

// Render listy lokali z data.json
async function renderLokale(){
  const root = document.getElementById('lista-lokali');
  if (!root) return;

  try{
    const res = await fetch('data.json', { cache: 'no-store' });
    if(!res.ok) throw new Error('HTTP '+res.status);
    const data = await res.json();

    // siatka kart
    root.style.display = 'grid';
    root.style.gridTemplateColumns = 'repeat(3,1fr)';
    root.style.gap = '1rem';

    if (window.innerWidth < 1000) root.style.gridTemplateColumns = 'repeat(2,1fr)';
    if (window.innerWidth < 640)  root.style.gridTemplateColumns = '1fr';

    data.forEach(x => {
      const cenaM2 = (x.cena_brutto && x.powierzchnia_m2) ? Math.round(x.cena_brutto / x.powierzchnia_m2) : null;

      const card = document.createElement('article');
      card.className = 'lokal';

      const kosztyHTML = (x.koszty_dodatkowe || [])
        .map(k => `<li>${k.nazwa}: ${Number(k.kwota).toLocaleString('pl-PL')} zł${k.opcjonalnie ? ' (opcjonalnie)' : ''}</li>`)
        .join('') || '<li>Brak</li>';

      const plikiHTML = (x.pliki || [])
        .map(p => `<a href="${p.href}" target="_blank" rel="noopener">📄 ${p.etykieta}</a>`)
        .join(' · ');

      const historiaHTML = (x.historia_ceny || [])
        .map(h => `<tr><td>${h.data}</td><td>${Number(h.kwota).toLocaleString('pl-PL')} zł</td><td>${h.uwagi || ''}</td></tr>`)
        .join('');

      card.innerHTML = `
        <h3>${x.nazwa}</h3>
        <span class="badge ${statusClass(x.status)}">${x.status || '—'}</span>

        <div class="kv">
          <p><strong>Powierzchnia:</strong> ${Number(x.powierzchnia_m2).toFixed(2)} m²</p>
          ${x.pietro ? `<p><strong>Piętro:</strong> ${x.pietro}</p>` : ''}
          ${x.pokoje ? `<p><strong>Pokoje:</strong> ${x.pokoje}</p>` : ''}
          ${x.adres ? `<p><strong>Adres:</strong> ${x.adres}</p>` : ''}
        </div>

        <div class="cena">
          <div><strong>Cena brutto:</strong> ${Number(x.cena_brutto).toLocaleString('pl-PL')} zł</div>
          ${cenaM2 ? `<div><strong>Cena za m²:</strong> ${cenaM2.toLocaleString('pl-PL')} zł/m²</div>` : ''}
        </div>

        <details class="details">
          <summary>Koszty dodatkowe</summary>
          <ul style="margin:.4rem 0 0 .9rem">${kosztyHTML}</ul>
        </details>

        ${plikiHTML ? `<p style="margin-top:.4rem">${plikiHTML}</p>` : ''}

        <table class="historia" aria-label="Historia ceny – ${x.id || ''}" style="margin-top:.6rem">
          <caption style="text-align:left;margin:.4rem 0 .2rem;">Historia ceny — ${x.id || ''}</caption>
          <thead><tr><th>Data</th><th>Cena brutto</th><th>Uwagi</th></tr></thead>
          <tbody>${historiaHTML}</tbody>
        </table>
      `;

      root.appendChild(card);
    });
  } catch(err){
    console.error(err);
    root.innerHTML = `<div class="panel">Nie udało się wczytać danych ofert. Spróbuj odświeżyć stronę.</div>`;
  }
}

document.addEventListener('DOMContentLoaded', renderLokale);
