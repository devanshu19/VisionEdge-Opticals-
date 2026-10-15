// lens-recommendation.js - Live Lens Recommendation based on real prescriptions

let allPrescriptions = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadPrescriptions();

    const selectEl = document.getElementById('patientRx');
    if (selectEl) {
        selectEl.addEventListener('change', (e) => {
            const rxId = parseInt(e.target.value);
            const rx = allPrescriptions.find(p => p.id === rxId);
            if (rx) {
                renderRxSummary(rx);
            }
        });
    }
});

async function loadPrescriptions() {
    const selectEl = document.getElementById('patientRx');
    if (!selectEl) return;

    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/prescriptions/`);
        if (response.ok) {
            allPrescriptions = await response.json();

            if (allPrescriptions.length === 0) {
                selectEl.innerHTML = '<option value="" disabled selected>No customer prescriptions found</option>';
                const summaryEl = document.getElementById('rxSummary');
                if (summaryEl) {
                    summaryEl.innerHTML = `
                        <div class="text-center py-4 text-muted">
                            <i class="bi bi-file-medical fs-2 mb-2 d-block"></i>
                            <p class="mb-0">No patient prescriptions available.</p>
                            <a href="add-prescription.html" class="btn btn-sm btn-outline-primary mt-2">Add New Prescription</a>
                        </div>
                    `;
                }
                return;
            }

            selectEl.innerHTML = '<option value="" disabled selected>Select Customer Prescription</option>';
            allPrescriptions.forEach((rx, index) => {
                const addText = (rx.od && rx.od.add) ? `(ADD: ${rx.od.add})` : '';
                const opt = document.createElement('option');
                opt.value = rx.id;
                opt.textContent = `${rx.customer_name || 'Customer'} - ${rx.prescription_number || `#${rx.id}`} ${addText}`;
                selectEl.appendChild(opt);
            });

            // Automatically select first real prescription
            selectEl.selectedIndex = 1;
            renderRxSummary(allPrescriptions[0]);
        }
    } catch (err) {
        console.error('Error loading prescriptions for lens guide:', err);
    }
}

function renderRxSummary(rx) {
    const nameEl = document.getElementById('rxSummaryName');
    const odEl = document.getElementById('odSph');
    const osEl = document.getElementById('osSph');
    const addEl = document.getElementById('addPower');
    const noteEl = document.getElementById('rxNote');
    const explanationEl = document.getElementById('recommendationExplanation');

    const customerName = rx.customer_name || 'Customer';
    if (nameEl) nameEl.textContent = `Rx Summary for ${customerName}`;

    const odSph = (rx.od && rx.od.sph) ? `${rx.od.sph} SPH` : '--';
    const osSph = (rx.os && rx.os.sph) ? `${rx.os.sph} SPH` : '--';
    const addPower = (rx.od && rx.od.add) ? rx.od.add : (rx.add_power || '--');

    if (odEl) odEl.textContent = odSph;
    if (osEl) osEl.textContent = osSph;
    if (addEl) addEl.textContent = addPower;

    const hasAdd = addPower && addPower !== '--' && parseFloat(addPower) > 0;
    if (noteEl) {
        noteEl.innerHTML = hasAdd 
            ? `<i class="bi bi-info-circle-fill me-1"></i> Patient requires reading / near-vision assistance.`
            : `<i class="bi bi-info-circle-fill me-1"></i> Patient requires standard distance correction.`;
    }

    if (explanationEl) {
        if (hasAdd) {
            explanationEl.innerHTML = `Based on the prescription's Addition (ADD) value of <strong>${addPower}</strong>, the patient requires multifocal correction. We recommend <strong>Progressive Lenses</strong> for a seamless transition between near, intermediate, and distance vision. Additionally, <strong>Anti Glare (ARC)</strong> and <strong>Blue Cut</strong> coatings are advised for digital device protection.`;
        } else {
            explanationEl.innerHTML = `Based on the single vision distance values (${odSph} / ${osSph}), we recommend high-index <strong>Single Vision Lenses</strong> with <strong>Anti-Reflective Coating (ARC)</strong> for optimal clarity and reduced glare.`;
        }
    }
}
