// ========== THEME TOGGLE (Light/Dark) ==========
function initTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    $('html').attr('data-bs-theme', theme);
    if (theme === 'dark') { $('#lightIcon').hide(); $('#darkIcon').show(); }
    else { $('#lightIcon').show(); $('#darkIcon').hide(); }
}

$('#themeToggle').click(function() {
    const newTheme = $('html').attr('data-bs-theme') === 'light' ? 'dark' : 'light';
    $('html').attr('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    if (newTheme === 'dark') { $('#lightIcon').hide(); $('#darkIcon').show(); }
    else { $('#lightIcon').show(); $('#darkIcon').hide(); }
    showToast(`Switched to ${newTheme} mode`, 'info');
});
initTheme();

// ========== MOBILE SIDEBAR TOGGLE ==========
$(document).ready(function() {
    if ($('.sidebar-toggle').length === 0) {
        $('body').prepend('<div class="sidebar-toggle"><i class="fas fa-bars"></i></div>');
    }
    $('.sidebar-toggle').click(function() {
        $('.sidebar').toggleClass('open');
    });
    // Close sidebar when clicking on a link (mobile)
    $('.sidebar-nav a').click(function() {
        if ($(window).width() <= 768) $('.sidebar').removeClass('open');
    });
});

// ========== GLASSMORPHIC TOAST NOTIFICATIONS ==========
window.showToast = function(message, type = 'success') {
    let borderColor = '#00E5FF';
    let icon = 'fa-check-circle';
    if (type === 'danger') { borderColor = '#FF4D4D'; icon = 'fa-exclamation-circle'; }
    else if (type === 'warning') { borderColor = '#FFB74D'; icon = 'fa-exclamation-triangle'; }
    else if (type === 'info') { borderColor = '#00E5FF'; icon = 'fa-info-circle'; }
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast glassmorphism align-items-center text-white border-0 mb-2" role="alert" style="border-left: 4px solid ${borderColor};">
            <div class="d-flex">
                <div class="toast-body"><i class="fas ${icon} me-2"></i>${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    $('.toast-container').append(toastHtml);
    const toastElement = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElement, { autohide: true, delay: 4000 });
    bsToast.show();
    toastElement.addEventListener('hidden.bs.toast', () => $(toastElement).remove());
};

// ========== NOTIFICATIONS BELL ==========
function loadNotifications() {
    $.get('/api/notifications/', function(data) {
        const list = $('#notificationList');
        list.empty();
        list.append('<li><h6 class="dropdown-header">Notifications</h6></li><li><hr class="dropdown-divider"></li>');
        if (!data.notifications.length) {
            list.append('<li><span class="dropdown-item-text">✨ All caught up!</span></li>');
            $('#notificationBadge').hide();
        } else {
            data.notifications.forEach(n => {
                list.append(`<li><a class="dropdown-item" href="#">${n.message}</a></li>`);
            });
            $('#notificationBadge').text(data.notifications.length).show();
        }
    }).fail(() => console.log('Could not load notifications'));
}
loadNotifications();
setInterval(loadNotifications, 30000);

// ========== ORDER FORM: DYNAMIC ITEMS & CALCULATION ==========
$(document).ready(function() {
    function calculateOrderTotal() {
        let subtotal = 0;
        $('.order-item-row').each(function() {
            const price = parseFloat($(this).find('.item-price').data('price')) || 0;
            const qty = parseInt($(this).find('.item-qty').val()) || 0;
            subtotal += price * qty;
        });
        const tax = subtotal * 0.10;
        const total = subtotal + tax;
        $('#subtotal').text(subtotal.toFixed(2));
        $('#tax').text(tax.toFixed(2));
        $('#total').text(total.toFixed(2));
        $('#id_total_amount').val(total);
    }

    $('#addMenuItem').click(function() {
        const sel = $('#menuItemSelect');
        const id = sel.val();
        if (!id) { showToast('Please select a menu item first', 'warning'); return; }
        const name = sel.find('option:selected').text().split(' - ')[0];
        const price = parseFloat(sel.find('option:selected').data('price'));
        const row = $(`
            <div class="order-item-row row mb-2 p-2 border rounded align-items-center">
                <div class="col-md-5">${name}</div>
                <div class="col-md-2"><input type="number" class="form-control form-control-sm item-qty bg-dark text-white" value="1" min="1"></div>
                <div class="col-md-2 item-price" data-price="${price}">$${price.toFixed(2)}</div>
                <div class="col-md-2 item-subtotal">$${price.toFixed(2)}</div>
                <div class="col-md-1"><button type="button" class="btn btn-sm btn-danger remove-item"><i class="fas fa-trash"></i></button></div>
                <input type="hidden" name="menu_item[]" value="${id}">
                <input type="hidden" name="quantity[]" class="qty-hidden" value="1">
                <input type="hidden" name="price[]" value="${price}">
                <input type="hidden" name="special_instructions[]" value="">
            </div>
        `);
        $('#orderItemsContainer').append(row);
        sel.val('');
        calculateOrderTotal();
    });

    $(document).on('change', '.item-qty', function() {
        const row = $(this).closest('.order-item-row');
        const qty = parseInt($(this).val()) || 0;
        const price = parseFloat(row.find('.item-price').data('price'));
        row.find('.item-subtotal').text(`$${(qty * price).toFixed(2)}`);
        row.find('.qty-hidden').val(qty);
        calculateOrderTotal();
    });

    $(document).on('click', '.remove-item', function() {
        $(this).closest('.order-item-row').remove();
        calculateOrderTotal();
    });

    // ========== PASSWORD MATCH VALIDATION (SIGNUP) ==========
    $('#id_password2').on('keyup', function() {
        const pwd1 = $('#id_password1').val();
        const pwd2 = $(this).val();
        if (pwd1 !== pwd2) {
            $(this).addClass('is-invalid');
            showToast('Passwords do not match', 'danger');
        } else {
            $(this).removeClass('is-invalid');
        }
    });

    // ========== LOGIN VALIDATION ==========
    $('#loginForm').on('submit', function(e) {
        let valid = true;
        if ($('#id_username').val().trim() === '') {
            $('#id_username').addClass('is-invalid');
            valid = false;
        } else $('#id_username').removeClass('is-invalid');
        if ($('#id_password').val() === '') {
            $('#id_password').addClass('is-invalid');
            valid = false;
        } else $('#id_password').removeClass('is-invalid');
        if (!valid) {
            e.preventDefault();
            showToast('Please fill in both email and password', 'danger');
        }
    });

    // ========== FILTERS & RESET (Orders Table) ==========
    $('#searchInput, #statusFilter, #typeFilter, #dateFrom, #dateTo').on('change keyup', function() {
        const search = $('#searchInput').val().toLowerCase();
        const status = $('#statusFilter').val();
        const type = $('#typeFilter').val();
        const dateFrom = $('#dateFrom').val();
        const dateTo = $('#dateTo').val();
        let url = new URL(window.location.href);
        if (search) url.searchParams.set('search', search); else url.searchParams.delete('search');
        if (status) url.searchParams.set('status', status); else url.searchParams.delete('status');
        if (type) url.searchParams.set('order_type', type); else url.searchParams.delete('order_type');
        if (dateFrom) url.searchParams.set('date_from', dateFrom); else url.searchParams.delete('date_from');
        if (dateTo) url.searchParams.set('date_to', dateTo); else url.searchParams.delete('date_to');
        window.location.href = url.toString();
    });

    $('#resetFilters').click(function() {
        window.location.href = window.location.pathname;
        showToast('All filters have been reset', 'success');
    });

    // Low stock filter
    $('#lowStockOnly').change(function() {
        const checked = $(this).is(':checked');
        let url = new URL(window.location.href);
        if (checked) url.searchParams.set('low_stock', 'true');
        else url.searchParams.delete('low_stock');
        window.location.href = url.toString();
    });

    // Stock warning on inventory form
    $('.stock-input').on('input', function() {
        const stock = parseFloat($(this).val()) || 0;
        const thresh = parseFloat($('#id_low_stock_threshold').val()) || 0;
        if (stock <= thresh) $('#stockWarning').show().text('⚠️ Stock is at or below threshold!');
        else $('#stockWarning').hide();
    });
});

// ========== KITCHEN QUEUE REAL‑TIME (every 10 sec) ==========
function loadKitchen() {
    if (!$('#kitchenGrid').length) return;
    $.get('/api/kitchen/queue/', function(data) {
        const container = $('#kitchenGrid');
        container.empty();
        if (!data.length) {
            container.html('<div class="col-12"><div class="alert alert-info">🍽️ No active orders in kitchen.</div></div>');
            return;
        }
        const orders = {};
        data.forEach(item => {
            if (!orders[item.order__slug]) orders[item.order__slug] = { ...item, items: [] };
            orders[item.order__slug].items.push(item);
        });
        for (const slug in orders) {
            const order = orders[slug];
            const card = $(`
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <strong>🍜 Order #${slug.slice(0,8)}</strong>
                            <span class="badge bg-info">${Math.round(order.elapsed_minutes || 0)} min</span>
                        </div>
                        <div class="card-body">
                            <p><i class="fas fa-${order.order__order_type === 'dine_in' ? 'chair' : (order.order__order_type === 'takeaway' ? 'box' : 'truck')}"></i> ${order.order__order_type.replace('_',' ')}</p>
                            ${order.order__table_number ? `<p>📌 Table: ${order.order__table_number}</p>` : ''}
                            <hr>
                            <div class="items-list"></div>
                        </div>
                        <div class="card-footer bg-transparent">
                            <button class="btn btn-sm btn-success w-100 update-order-status" data-slug="${slug}" data-status="completed">✅ Mark Completed</button>
                        </div>
                    </div>
                </div>
            `);
            order.items.forEach(item => {
                card.find('.items-list').append(`
                    <div class="border-bottom pb-2 mb-2">
                        <strong>${item.menu_item__name}</strong> x${item.quantity}
                        ${item.special_instructions ? `<div class="small text-secondary"><i class="fas fa-note-sticky"></i> ${item.special_instructions}</div>` : ''}
                    </div>
                `);
            });
            container.append(card);
        }
        $('.update-order-status').click(function() {
            const slug = $(this).data('slug');
            const status = $(this).data('status');
            $.post(`/api/order/${slug}/status/`, {status: status}, function() {
                loadKitchen();
                showToast('Order status updated', 'success');
            }).fail(() => showToast('Error updating order', 'danger'));
        });
    });
}
if ($('#kitchenGrid').length) { loadKitchen(); setInterval(loadKitchen, 10000); }

// ========== EXCEL EXPORT ==========
$('#exportExcel').click(() => window.location.href = '/export/orders/');