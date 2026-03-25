const responsiblesApi = '/api/admin/responsibles';
const usersApi = '/api/admin/users';

const fullNameSelect = document.getElementById('fullNameSelect');
const createForm = document.getElementById('createForm');
const usersTable = document.getElementById('usersTable');
const tbody = usersTable.querySelector('tbody');

async function loadResponsibles() {
    const r = await fetch(responsiblesApi, { credentials: 'include' });
    const list = await r.json();
    fullNameSelect.innerHTML = list.map(v => `<option value="${v}">${v}</option>`).join('');
}

async function loadUsers() {
    const r = await fetch(usersApi, { credentials: 'include' });
    const users = await r.json();
    tbody.innerHTML = '';

    users.forEach(u => {
        const tr = tbody.insertRow();
        tr.dataset.userId = u.id;
        const activeLabel = u.is_active ? 'Активен' : 'Неактивен';
        tr.innerHTML = `
            <td>${u.id}</td>
            <td>${u.username}</td>
            <td>${u.full_name}</td>
            <td>${u.role || 'user'}</td>
            <td>${activeLabel}</td>
            <td style="text-align:right; white-space:nowrap;">
                <button class="sm" data-action="toggle-status" data-is-active="${u.is_active ? 0 : 1}"> ${u.is_active ? 'Отключить' : 'Включить'} </button>
                <button class="sm" data-action="change-password">Пароль</button>
            </td>
        `;
    });
}

createForm.onsubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(createForm);
    const username = (fd.get('username') || '').toString().trim();
    const full_name = (fd.get('full_name') || '').toString().trim();
    const password = fd.get('password') || '';

    const r = await fetch(usersApi, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, full_name, password })
    });
    const d = await r.json();
    if(!r.ok) {
        alert(d.error || 'Ошибка');
        return;
    }

    createForm.reset();
    await loadResponsibles();
    await loadUsers();
};

document.getElementById('btnReload').onclick = async () => {
    await loadResponsibles();
    await loadUsers();
};

usersTable.onclick = async (e) => {
    const btn = e.target.closest('button');
    if(!btn) return;

    const tr = btn.closest('tr');
    const userId = tr ? tr.dataset.userId : null;
    if(!userId) return;

    const action = btn.dataset.action;
    if(action === 'toggle-status') {
        const nextIsActive = btn.dataset.isActive === '1';
        const r = await fetch(`${usersApi}/${userId}/status`, {
            method: 'PUT',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_active: nextIsActive })
        });
        const d = await r.json();
        if(!r.ok) alert(d.error || 'Ошибка');
        await loadUsers();
    }

    if(action === 'change-password') {
        const newPassword = prompt('Введите новый пароль:');
        if(!newPassword) return;
        const r = await fetch(`${usersApi}/${userId}/password`, {
            method: 'PUT',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: newPassword })
        });
        const d = await r.json();
        if(!r.ok) alert(d.error || 'Ошибка');
        else alert('Пароль обновлен');
    }
};

// Initial load
loadResponsibles().then(loadUsers);

