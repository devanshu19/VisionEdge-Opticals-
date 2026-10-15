let searchTimeout;

document.addEventListener('DOMContentLoaded', async () => {
    await loadUsers();

    const searchInput = document.getElementById('searchUser');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(loadUsers, 300);
        });
    }

    const filterRole = document.getElementById('filterRole');
    if (filterRole) {
        filterRole.addEventListener('change', loadUsers);
    }

    const addForm = document.getElementById('addUserForm');
    if (addForm) {
        addForm.addEventListener('submit', handleAddUserSubmit);
    }

    const editForm = document.getElementById('editUserForm');
    if (editForm) {
        editForm.addEventListener('submit', handleEditUserSubmit);
    }
});

async function loadUsers() {
    try {
        const search = document.getElementById('searchUser')?.value.trim() || '';
        const role = document.getElementById('filterRole')?.value || 'all';

        let url = `${API_BASE_URL}/auth/users?role=${encodeURIComponent(role)}`;
        if (search) url += `&search=${encodeURIComponent(search)}`;

        const response = await fetchWithAuth(url);
        if (!response.ok) throw new Error('Failed to fetch users');

        const users = await response.json();
        const tbody = document.getElementById('usersTableBody');
        tbody.innerHTML = '';

        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted"><i class="bi bi-people fs-2 d-block mb-2"></i>No users found.</td></tr>';
            return;
        }

        users.forEach(u => {
            let roleBadge = 'bg-secondary';
            if (u.role === 'admin') roleBadge = 'bg-danger text-white';
            else if (u.role === 'staff') roleBadge = 'bg-info text-white';
            else if (u.role === 'customer') roleBadge = 'bg-success text-white';

            const fullName = u.name || `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.username;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="ps-4 fw-medium text-primary">#USR-${u.id}</td>
                <td>
                    <div class="fw-bold">${fullName}</div>
                    <small class="text-muted">@${u.username}</small>
                </td>
                <td>${u.email || '-'}</td>
                <td>${u.phone || '-'}</td>
                <td><span class="badge ${roleBadge} px-3 py-1 rounded-pill text-uppercase">${u.role}</span></td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary rounded-circle me-1" title="Edit User" onclick="openEditUserModal(${u.id}, '${(u.first_name || '').replace(/'/g, "\\'")}', '${(u.last_name || '').replace(/'/g, "\\'")}', '${u.email}', '${u.phone || ''}', '${u.role}')">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger rounded-circle" title="Delete User" onclick="deleteUser(${u.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error('Error loading users:', e);
        document.getElementById('usersTableBody').innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function handleAddUserSubmit(e) {
    e.preventDefault();

    const data = {
        first_name: document.getElementById('userFirstName').value.trim(),
        last_name: document.getElementById('userLastName').value.trim(),
        username: document.getElementById('userUsername').value.trim(),
        email: document.getElementById('userEmail').value.trim(),
        phone: document.getElementById('userPhone').value.trim(),
        role: document.getElementById('userRole').value,
        password: document.getElementById('userPassword').value
    };

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/auth/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const modalEl = document.getElementById('addUserModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            document.getElementById('addUserForm').reset();
            if (window.showToast) window.showToast('Created', 'User created successfully');
            loadUsers();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to create user');
        }
    } catch (err) {
        alert('Network Error');
    }
}

function openEditUserModal(id, firstName, lastName, email, phone, role) {
    document.getElementById('editUserId').value = id;
    document.getElementById('editFirstName').value = firstName || '';
    document.getElementById('editLastName').value = lastName || '';
    document.getElementById('editEmail').value = email || '';
    document.getElementById('editPhone').value = phone || '';
    document.getElementById('editRole').value = role || 'staff';
    document.getElementById('editPassword').value = '';

    const modal = new bootstrap.Modal(document.getElementById('editUserModal'));
    modal.show();
}

async function handleEditUserSubmit(e) {
    e.preventDefault();

    const id = document.getElementById('editUserId').value;
    const data = {
        first_name: document.getElementById('editFirstName').value.trim(),
        last_name: document.getElementById('editLastName').value.trim(),
        email: document.getElementById('editEmail').value.trim(),
        phone: document.getElementById('editPhone').value.trim(),
        role: document.getElementById('editRole').value
    };

    const password = document.getElementById('editPassword').value;
    if (password) data.password = password;

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/auth/users/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const modalEl = document.getElementById('editUserModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            if (window.showToast) window.showToast('Updated', 'User updated successfully');
            loadUsers();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to update user');
        }
    } catch (err) {
        alert('Network Error');
    }
}

async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/auth/users/${id}`, { method: 'DELETE' });
        if (response.ok) {
            if (window.showToast) window.showToast('Deleted', 'User deleted successfully');
            loadUsers();
        } else {
            const err = await response.json();
            alert(err.message || 'Failed to delete user');
        }
    } catch (e) {
        alert('Network error');
    }
}
