const api = '/api/catches';
const modal = document.getElementById('modal');
const form = document.getElementById('form');
const tbody = document.querySelector('#table tbody');
const permSelect = form.querySelector('[name="Разрешение"]');
const fishSelect = form.querySelector('[name="Наименование_рыбы"]');

let isAdmin = false;

async function initRole() {
    const r = await fetch('/api/auth/current', { credentials: 'include' });
    const d = await r.json();
    isAdmin = !!(d.user && d.user.role === 'admin');
}

async function loadOptions() {
    const [pRes, fRes] = await Promise.all([
        fetch('/api/permission-numbers', {credentials:'include'}),
        fetch('/api/fish-names', {credentials:'include'})
    ]);
    const perms = await pRes.json();
    const fish = await fRes.json();
    permSelect.innerHTML = '<option value="">—</option>' + perms.map(p=>`<option value="${p}">${p}</option>`).join('');
    fishSelect.innerHTML = '<option value="">—</option>' + fish.map(f=>`<option value="${f}">${f}</option>`).join('');
}

function load() {
    fetch(api, {credentials:'include'}).then(r=>r.json()).then(items=>{
        tbody.innerHTML = '';
        items.forEach(r=>{
            const tr = tbody.insertRow();
            tr.innerHTML = `
                <td>${r.Разрешение||''}</td>
                <td>${r.Дата_вылова||''}</td>
                <td>${r.Наименование_рыбы||''}</td>
                <td>${r.Количество||''}</td>
                <td>${r.Сумма!=null?r.Сумма:''}</td>
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

async function showModal(rec){
    await loadOptions();
    form.querySelector('[name="id"]').value = rec?.id || '';
    form.querySelector('[name="Разрешение"]').value = rec?.Разрешение || '';
    form.querySelector('[name="Дата_вылова"]').value = rec?.Дата_вылова || '';
    form.querySelector('[name="Наименование_рыбы"]').value = rec?.Наименование_рыбы || '';
    form.querySelector('[name="Количество"]').value = rec?.Количество || '';
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
    fetch(`${api}/${id}`, {method:'DELETE', credentials:'include'}).then(r=>{ if(r.ok) load(); });
}

document.getElementById('btnAdd').onclick = ()=>showModal(null);
document.getElementById('btnCancel').onclick = ()=>modal.classList.remove('show');
form.onsubmit = async (e)=>{
    e.preventDefault();
    const fd = new FormData(form);
    const id = fd.get('id');
    const data = {
        Разрешение: fd.get('Разрешение'),
        Дата_вылова: fd.get('Дата_вылова'),
        Наименование_рыбы: fd.get('Наименование_рыбы'),
        Количество: parseInt(fd.get('Количество')) || 0
    };
    const url = id ? `${api}/${id}` : api;
    const method = id ? 'PUT' : 'POST';
    const r = await fetch(url, {method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(data), credentials:'include'});
    const j = await r.json();
    if(r.ok) { modal.classList.remove('show'); load(); }
    else alert(j.error || 'Ошибка');
};
initRole().then(()=>load());
