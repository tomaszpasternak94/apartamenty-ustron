// Daty w stopce
(function setMetaDates(){
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
  const u = document.getElementById('last-update');
  if (u) u.textContent = new Date().toISOString().slice(0,10);
})();

// Kolor badge wg statusu (dokładne dopasowanie)
function statusClass(status){
  const s = (status || '').toLowerCase().trim();
  if (s === 'dostępny')      return 'badge-green';
  if (s === 'zarezerwowany') return 'badge-orange';
  if (s === 'niedostępny')   return 'badge-gray';
  return '';
}

// Formatowanie kwot
function formatPLN(n){
  if (Number.isNaN(n) || n == null) return '—';
  return `${Math.round(n).toLocaleString('pl-PL')} zł`;
}
function formatPLNperM2(n){
  if (Number.isNaN(n) || n == null) return '—';
  return `${Math.round(n).toLocaleString('pl-PL')} zł/m²`;
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
      const pow = Number(x.powierzchnia_m2) || 0;

      // Wejście: cena_brutto albo cena_m2 (lub oba / żadne)
      let cenaBrutto = (x.cena_brutto != null) ? Number(x.cena_brutto) : null;
      let cenaM2     = (x.cena_m2     != null) ? Number(x.cena_m2)     : null;

      // Uzupełnij brakujące
      if ((cenaBrutto == null || Number.isNaN(cenaBrutto)) && pow > 0 && cenaM2 != null){
        cenaBrutto = Math.round(cenaM2 * pow);
      }
      if ((cenaM2 == null || Number.isNaN(cenaM2)) && pow > 0 && cenaBrutto != null){
        cenaM2 = Math.round(cenaBrutto / pow);
      }

      const card = document.createElement('article');
      card.className = 'lokal';

      const kosztyHTML = (x.koszty_dodatkowe || [])
        .map(k => `<li>${k.nazwa}: <span class="kwota">${Number(k.kwota).toLocaleString('pl-PL')} zł</span>${k.opcjonalnie ? ' (opcjonalnie)' : ''}</li>`)
        .join('') || '<li>Brak</li>';

      const historiaHTML = (x.historia_ceny || [])
        .map(h => {
          const data = h.data || '';
          let total = (h.kwota != null) ? Number(h.kwota) : null;
          let per   = (h.cena_m2 != null) ? Number(h.cena_m2) : null;

          if ((total == null || Number.isNaN(total)) && per != null && pow > 0){
            total = Math.round(per * pow);
          }
          // Domyślnie pokaz cenę całkowitą brutto. Jeśli jej brak, pokaż cenę za m2.
          const display = (total != null && !Number.isNaN(total))
            ? formatPLN(total)
            : (per != null && !Number.isNaN(per)) ? formatPLNperM2(per) : '—';

          return `<tr><td>${data}</td><td>${display}</td></tr>`;
        })
        .join('');

      const plikiHTML = (x.pliki || [])
        .map(p => `<a href="${p.href}" target="_blank" rel="noopener">📄 ${p.etykieta}</a>`)
        .join(' · ');

      card.innerHTML = `
        <h3>${x.nazwa || (x.id ? `Lokal ${x.id}` : 'Lokal')}</h3>
        <span class="badge ${statusClass(x.status)}">${x.status || '—'}</span>

        <div class="kv">
          <p><strong>Powierzchnia:</strong> ${pow ? pow.toFixed(2) : '—'} m²</p>
          ${x.pietro ? `<p><strong>Piętro:</strong> ${x.pietro}</p>` : ''}
          ${x.pokoje ? `<p><strong>Pokoje:</strong> ${x.pokoje}</p>` : ''}
          ${x.adres  ? `<p><strong>Adres:</strong> ${x.adres}</p>`   : ''}
        </div>

        <div class="cena">
          ${cenaBrutto != null ? `<div><strong>Cena brutto:</strong> ${formatPLN(cenaBrutto)}</div>` : ''}
          ${cenaM2     != null ? `<div><strong>Cena za m²:</strong> ${formatPLNperM2(cenaM2)}</div>` : ''}
          ${(cenaBrutto == null && cenaM2 == null) ? `<div><em>Brak danych cenowych</em></div>` : ''}
        </div>

        ${(x.koszty_dodatkowe && x.koszty_dodatkowe.length)
          ? `<details class="details">
               <summary>Koszty dodatkowe</summary>
               <ul style="margin:.4rem 0 0 .9rem">${kosztyHTML}</ul>
             </details>`
          : ''}

        ${plikiHTML ? `<p style="margin-top:.4rem">${plikiHTML}</p>` : ''}

        ${(x.historia_ceny && x.historia_ceny.length)
          ? `<table class="historia" aria-label="Historia ceny – ${x.id || ''}" style="margin-top:.6rem">
               <caption style="text-align:left;margin:.4rem 0 .2rem;">Historia cen</caption>
               <thead><tr><th>Data</th><th>Cena</th></tr></thead>
               <tbody>${historiaHTML}</tbody>
             </table>`
          : ''}
      `;

      root.appendChild(card);
    });
  } catch(err){
    console.error(err);
    root.innerHTML = `<div class="panel">Nie udało się wczytać danych ofert. Spróbuj odświeżyć stronę.</div>`;
  }
}

document.addEventListener('DOMContentLoaded', renderLokale);
