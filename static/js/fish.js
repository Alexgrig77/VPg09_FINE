const api = '/api/fish';
const modal = document.getElementById('modal');
const form = document.getElementById('form');
const tbody = document.querySelector('#table tbody');

let isAdmin = false;

async function initRole() {
    const r = await fetch('/api/auth/current', { credentials: 'include' });
    const d = await r.json();
    isAdmin = !!(d.user && d.user.role === 'admin');
}

function load(q) {
    const url = q ? `${api}?q=${encodeURIComponent(q)}` : api;
    fetch(url, {credentials:'include'}).then(r=>r.json()).then(items=>{
        tbody.innerHTML = '';
        items.forEach(r=>{
            const tr = tbody.insertRow();
            tr.innerHTML = `
                <td>${r.Наименование_рыбы||''}</td>
                <td>${r.Наименование_групповое||''}</td>
                <td>${r.Цена!=null?r.Цена:''}</td>
                <td>
                    ${isAdmin ? `
                        <button class="sm" data-edit="${r.id}">Ред</button>
                        <button class="sm" data-del="${r.id}">Удал</button>
                    ` : ``}
                </td>
            `;
        });
        if (isAdmin) {
            tbody.querySelectorAll('[data-edit]').forEach(btn=> btn.onclick = ()=>edit(parseInt(btn.dataset.edit)));
            tbody.querySelectorAll('[data-del]').forEach(btn=> btn.onclick = ()=>del(parseInt(btn.dataset.del)));
        }
    });
}

function showModal(rec){
    form.querySelector('[name="id"]').value = rec?.id || '';
    form.querySelector('[name="Наименование_рыбы"]').value = rec?.Наименование_рыбы || '';
    form.querySelector('[name="Наименование_групповое"]').value = rec?.Наименование_групповое || '';
    form.querySelector('[name="Цена"]').value = rec?.Цена != null ? rec.Цена : '';
    modal.classList.add('show');
}

function edit(id){
    fetch(`${api}/${id}`, {credentials:'include'}).then(r=>r.json()).then(rec=>{
        if(rec.error) alert(rec.error);
        else showModal(rec);
    });
}

function del(id){
    if(!confirm('Удалить?')) return;
    fetch(`${api}/${id}`, {method:'DELETE', credentials:'include'}).then(r=>{ if(r.ok) load(document.getElementById('search').value); });
}

document.getElementById('search').oninput = ()=>load(document.getElementById('search').value);
document.getElementById('btnAdd').onclick = ()=> {
    if (!isAdmin) return;
    showModal(null);
};
document.getElementById('btnCancel').onclick = ()=>modal.classList.remove('show');
form.onsubmit = async (e)=>{
    e.preventDefault();
    if (!isAdmin) return;
    const fd = new FormData(form);
    const id = fd.get('id');
    const data = {
        Наименование_рыбы: fd.get('Наименование_рыбы'),
        Наименование_групповое: fd.get('Наименование_групповое'),
        Цена: parseFloat(fd.get('Цена')) || 0
    };
    const url = id ? `${api}/${id}` : api;
    const method = id ? 'PUT' : 'POST';
    const r = await fetch(url, {method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(data), credentials:'include'});
    const j = await r.json();
    if(r.ok) { modal.classList.remove('show'); load(document.getElementById('search').value); }
    else alert(j.error || 'Ошибка');
};
initRole().then(()=>load());
