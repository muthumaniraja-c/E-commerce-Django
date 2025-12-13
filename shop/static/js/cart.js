// static/js/cart.js
$(document).ready(function() {
    // CSRF Token setup
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Global function to update cart count
    window.updateCartCount = function() {
        $.ajax({
            method: 'GET',
            url: '/get_cart_count/',
            success: function(response) {
                updateBadgeCount('cart-badge', response.cart_count);
                updateBadgeCount('fav-badge', response.fav_count);
            }
        });
    }

    function updateBadgeCount(badgeId, count) {
        const badge = document.getElementById(badgeId);
        if (badge) {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    // Add to cart functionality
    $(document).on('click', '.add-to-cart-btn', function(e) {
        e.preventDefault();
        const productId = $(this).data('product-id');
        const quantity = $('#quantity').val() || 1;

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });

        $.ajax({
            method: 'POST',
            url: '/addtocart',
            data: JSON.stringify({
                'pid': productId,
                'product_qty': parseInt(quantity)
            }),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            success: function(response) {
                // Show a better notification instead of alert
                showNotification(response.status);
                updateCartCount();
            },
            error: function() {
                showNotification('Error adding to cart', 'error');
            }
        });
    });

    // Better notification function
    function showNotification(message, type = 'success') {
        // You can replace this with a toast notification library
        const notification = $(`
            <div class="alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999;">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
});
