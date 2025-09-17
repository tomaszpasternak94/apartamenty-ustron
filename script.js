async function renderLokale(){
  const root=document.getElementById('lista-lokali');
  try{
    const res=await fetch('data.json');
    const data=await res.json();
    data.forEach(x=>{
      const div=document.createElement('div');
      div.className='lokal';
      div.innerHTML=`<h3>${x.nazwa}</h3>
        <p>Status: ${x.status}</p>
        <p>Powierzchnia: ${x.powierzchnia_m2} m²</p>
        <p>Cena: ${x.cena_brutto.toLocaleString('pl-PL')} zł</p>`;
      root.appendChild(div);
    });
  }catch(e){root.innerHTML='Błąd wczytywania danych';}
}
document.addEventListener('DOMContentLoaded',renderLokale);
