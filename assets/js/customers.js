document.addEventListener("DOMContentLoaded", () => {
    // Populate Customers Table if exists
    const tableBody = document.getElementById('customersTableBody');
    if (tableBody) {
        populateCustomersTable();
        
        // Search functionality
        const searchInput = document.getElementById('searchCustomer');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                const rows = tableBody.querySelectorAll('tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(term) ? '' : 'none';
                });
            });
        }
    }

    // Handle Add Customer Form
    const addCustomerForm = document.getElementById('addCustomerForm');
    if (addCustomerForm) {
        addCustomerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (addCustomerForm.checkValidity()) {
                const btn = addCustomerForm.querySelector('button[type="submit"]');
                const originalText = btn.innerHTML;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
                btn.disabled = true;
                
                setTimeout(() => {
                    if(typeof showToast === 'function') {
                        showToast('Success', 'Customer added successfully!');
                    }
                    setTimeout(() => {
                        window.location.href = 'customers.html';
                    }, 1500);
                }, 1000);
            } else {
                addCustomerForm.classList.add('was-validated');
            }
        });
    }
});

const dummyCustomers = [
    { id: 'CUST-001', name: 'Alexander Pierce', email: 'alex@example.com', phone: '+1 555-0100', lastVisit: '2023-10-25', spent: '$450.00', status: 'Active' },
    { id: 'CUST-002', name: 'Sarah Connor', email: 'sarah.c@example.com', phone: '+1 555-0101', lastVisit: '2023-10-20', spent: '$120.00', status: 'Active' },
    { id: 'CUST-003', name: 'James Smith', email: 'jsmith@example.com', phone: '+1 555-0102', lastVisit: '2023-09-15', spent: '$850.00', status: 'Inactive' },
    { id: 'CUST-004', name: 'Emma Watson', email: 'emma@example.com', phone: '+1 555-0103', lastVisit: '2023-10-26', spent: '$320.00', status: 'Active' },
    { id: 'CUST-005', name: 'Michael Brown', email: 'mbrown@example.com', phone: '+1 555-0104', lastVisit: '2023-08-01', spent: '$1,200.00', status: 'Active' },
    { id: 'CUST-006', name: 'Lisa Ray', email: 'lisa.ray@example.com', phone: '+1 555-0105', lastVisit: '2022-12-10', spent: '$150.00', status: 'Inactive' }
];

function populateCustomersTable() {
    const tbody = document.getElementById('customersTableBody');
    let html = '';
    
    dummyCustomers.forEach((cust, index) => {
        const badgeClass = cust.status === 'Active' ? 'bg-success text-success' : 'bg-secondary text-secondary';
        const delay = index * 50; // Staggered animation
        
        html += `
            <tr data-aos="fade-up" data-aos-delay="${delay}">
                <td class="fw-medium text-secondary ps-4">${cust.id}</td>
                <td>
                    <div class="d-flex align-items-center">
                        <div class="bg-primary bg-opacity-10 text-primary rounded-circle me-3 d-flex align-items-center justify-content-center fw-bold" style="width: 40px; height: 40px;">
                            ${cust.name.charAt(0)}
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold">${cust.name}</h6>
                            <small class="text-muted">${cust.email}</small>
                        </div>
                    </div>
                </td>
                <td class="text-muted"><i class="bi bi-telephone me-2"></i>${cust.phone}</td>
                <td class="text-muted">${cust.lastVisit}</td>
                <td class="fw-bold">${cust.spent}</td>
                <td><span class="badge ${badgeClass} bg-opacity-10 px-3 py-2 rounded-pill border border-${cust.status === 'Active'?'success':'secondary'}">${cust.status}</span></td>
                <td class="text-end pe-4">
                    <div class="dropdown">
                        <button class="btn btn-sm btn-light border-0 shadow-none" type="button" data-bs-toggle="dropdown">
                            <i class="bi bi-three-dots-vertical"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end shadow border-0">
                            <li><a class="dropdown-item" href="#"><i class="bi bi-eye text-primary me-2"></i> View Profile</a></li>
                            <li><a class="dropdown-item" href="add-prescription.html"><i class="bi bi-file-medical text-info me-2"></i> Add Prescription</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="#" onclick="openDeleteModal('${cust.name}')"><i class="bi bi-trash me-2"></i> Delete</a></li>
                        </ul>
                    </div>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

let customerToDelete = null;

function openDeleteModal(name) {
    customerToDelete = name;
    const modal = new bootstrap.Modal(document.getElementById('deleteCustomerModal'));
    modal.show();
}

function confirmDelete() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteCustomerModal'));
    modal.hide();
    
    if(typeof showToast === 'function') {
        showToast('Deleted', `${customerToDelete} has been deleted.`, 'danger');
    }
}
