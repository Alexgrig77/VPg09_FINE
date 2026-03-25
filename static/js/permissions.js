const api = '/api/permissions';
const modal = document.getElementById('modal');
const form = document.getElementById('form');
const tbody = document.querySelector('#table tbody');

let isAdmin = false;

async function initRole() {
    const r = await fetch('/api/auth/current', { credentials: 'include' });
    const d = await r.json();
    isAdmin = !!(d.user && d.user.role === 'admin');
    const btnAdd = document.getElementById('btnAdd');
    if (btnAdd) btnAdd.style.display = isAdmin ? '' : 'none';
}

function load(q) {
    const url = q ? `${api}?q=${encodeURIComponent(q)}` : api;
    fetch(url, {credentials:'include'}).then(r=>r.json()).then(items=>{
        tbody.innerHTML = '';
        items.forEach(r=>{
            const tr = tbody.insertRow();
            tr.innerHTML = `
                <td>${r.Номер_разрешения||''}</td>
                <td>${r.Год||''}</td>
                <td>${r.Район_промысла||''}</td>
                <td>${r.Ответственный||''}</td>
                <td>${r.Наименование_групповое||''}</td>
                <td>${r.Лимит_кг||''}</td>
                <td>
                    ${isAdmin ? `
                        <button class="sm" data-edit="${r.id}">Ред</button>
                        <button class="sm" data-del="${r.id}">Удал</button>
                    ` : ``}
                </td>
            `;
        });
        if (isAdmin) {
            tbody.querySelectorAll('[data-edit]').forEach(btn=>{
                btn.onclick = ()=>edit(parseInt(btn.dataset.edit));
            });
            tbody.querySelectorAll('[data-del]').forEach(btn=>{
                btn.onclick = ()=>del(parseInt(btn.dataset.del));
            });
        }
    });
}

function showModal(rec){
    if (!isAdmin) return; // Подстраховка: на сервере тоже есть проверка доступа
    form.querySelector('[name="id"]').value = rec?.id || '';
    form.querySelector('[name="Номер_разрешения"]').value = rec?.Номер_разрешения || '';
    form.querySelector('[name="Год"]').value = rec?.Год || '';
    form.querySelector('[name="Район_промысла"]').value = rec?.Район_промысла || '';
    form.querySelector('[name="Ответственный"]').value = rec?.Ответственный || '';
    form.querySelector('[name="Наименование_групповое"]').value = rec?.Наименование_групповое || '';
    form.querySelector('[name="Лимит_кг"]').value = rec?.Лимит_кг || '';
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
    fetch(`${api}/${id}`, {method:'DELETE', credentials:'include'}).then(r=>{
        if(r.ok) load(document.getElementById('search').value);
    });
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
        Номер_разрешения: fd.get('Номер_разрешения'),
        Год: fd.get('Год'),
        Район_промысла: fd.get('Район_промысла'),
        Ответственный: fd.get('Ответственный'),
        Наименование_групповое: fd.get('Наименование_групповое'),
        Лимит_кг: fd.get('Лимит_кг') ? parseInt(fd.get('Лимит_кг')) : null
    };
    const url = id ? `${api}/${id}` : api;
    const method = id ? 'PUT' : 'POST';
    const r = await fetch(url, {method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(data), credentials:'include'});
    const j = await r.json();
    if(r.ok) { modal.classList.remove('show'); load(document.getElementById('search').value); }
    else alert(j.error || 'Ошибка');
};

initRole().then(()=>load());
