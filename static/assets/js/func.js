console.log("✅ func.js loaded v8.1 - with cart functionality and custom notifications");

// ==========================================
// NOTIFICATION SYSTEM
// ==========================================
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    $('.custom-notification').remove();
    
    const types = {
        'success': { bg: '#10b981', icon: '✓' },
        'error': { bg: '#ef4444', icon: '✕' },
        'warning': { bg: '#f59e0b', icon: '⚠' },
        'info': { bg: '#3b82f6', icon: 'ℹ' }
    };
    
    const config = types[type] || types.info;
    
    const notification = $(`
        <div class="custom-notification" style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${config.bg};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 600;
            font-size: 0.95rem;
            max-width: 400px;
            animation: slideInNotification 0.3s ease;
        ">
            <span style="font-size: 1.2rem;">${config.icon}</span>
            <span>${message}</span>
        </div>
    `);
    
    // Add CSS animation if not already added
    if (!$('#notification-styles').length) {
        $('head').append(`
            <style id="notification-styles">
                @keyframes slideInNotification {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutNotification {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            </style>
        `);
    }
    
    $('body').append(notification);
    
    // Auto remove after 4 seconds
    setTimeout(function() {
        notification.css('animation', 'slideOutNotification 0.3s ease');
        setTimeout(function() {
            notification.remove();
        }, 300);
    }, 4000);
}

$(document).ready(function() {
    console.log("✅ Document ready");
    console.log("Initial cart count:", $("#cartCount").text());
    
    // ==========================================
    // ADD TO CART - Works on ALL pages
    // ==========================================
    $(document).on('click', '.add-to-cart-btn, #add-to-cart-btn', function(e){
        e.preventDefault();
        console.log("🛒 Add to cart clicked");
        
        let element = $(this);
        let productId = element.data('product-id') || $(".product-id").val();
        
        // For single product page
        let quantity = parseInt($("#product-quantity").val()) || 1;
        let productPrice = $(".product-price").val() || $(".product-price-" + productId).val();
        let productTitle = $(".product-title").val() || $(".product-title-" + productId).val();
        
        // For all products page (uses data attributes)
        if (!productPrice) {
            productPrice = $(".product-price-" + productId).val();
        }
        if (!productTitle) {
            productTitle = $(".product-title-" + productId).val();
        }
        
        console.log("📦 Adding:", {id: productId, price: productPrice, qty: quantity, title: productTitle});
        
        element.html("Adding...").prop('disabled', true);
        
        $.ajax({
            url: "/ajax_add_to_cart/",
            method: "GET",
            data: {
                id: productId,
                price: productPrice,
                quantity: quantity
            },
            dataType: "json",
            success: function(response){
                console.log("✅ Added to cart!", response);
                
                if(response.success){
                    element.html("✓ Added!");
                    $("#cartCount").text(response.total_items);
                    
                    setTimeout(function(){
                        element.html("Add to cart").prop('disabled', false);
                    }, 2000);
                }
            },
            error: function(xhr, status, error){
                console.error("❌ Error:", error);
                console.error("Response:", xhr.responseText);
                element.html("Error!");
                setTimeout(function(){
                    element.html("Add to cart").prop('disabled', false);
                }, 2000);
            }
        });
    });
    
    // ==========================================
    // REVIEW SUBMISSION
    // ==========================================
    $("#commentForm").submit(function (e) {
        e.preventDefault();
        
        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function (response){
                if (response.boolean == true){
                    $("#review-res").html("Review added successfully");
                    $("#review-section").hide();
                    $("#addr").hide();
                    
                    let html = '<li style="margin-bottom: 15px; border-bottom: 1px solid #e9ecef; padding-bottom: 10px;">';
                    html += '<strong>' + response.new_review.user + '</strong> - ';
                    
                    for (let i = 0; i < response.new_review.rating; i++) {
                        html += '<span style="color: #ffc107;">★</span>';
                    }
                    
                    html += '<p style="margin: 5px 0 0 0;">' + response.new_review.review + '</p>';
                    html += '</li>';
                    
                    $("#review-list").prepend(html);
                }
            }
        });
    });
    
    // ==========================================
    // FILTER PRODUCTS - AJAX VERSION
    // ==========================================
    $(".apply-filter-btn").on('click', function(){
        console.log("🔍 Applying filters...");
        
        let filter_object = {};
        
        // Get selected categories
        let selectedCategories = [];
        $('input[name="category"]:checked').each(function(){
            selectedCategories.push($(this).val());
        });
        
        // Send categories in the format Django expects (categories[])
        if(selectedCategories.length > 0) {
            filter_object['categories[]'] = selectedCategories;
        }
        
        // Get price range
        let minPrice = $("#minPrice").val();
        let maxPrice = $("#maxPrice").val();
        
        if(minPrice) {
            filter_object['min_price'] = minPrice;
        }
        if(maxPrice) {
            filter_object['max_price'] = maxPrice;
        }
        
        console.log("Filter data:", filter_object);
        console.log("AJAX URL:", "/ajax_filter_products/");
        
        // Build proper query string for categories[]
        let queryParams = [];
        if(selectedCategories.length > 0) {
            selectedCategories.forEach(function(catId) {
                queryParams.push('categories[]=' + catId);
            });
        }
        if(minPrice) {
            queryParams.push('min_price=' + minPrice);
        }
        if(maxPrice) {
            queryParams.push('max_price=' + maxPrice);
        }
        
        $.ajax({
            url: "/ajax_filter_products/",
            data: queryParams.join('&'),
            dataType: "json",
            traditional: true,
            beforeSend: function(){
                console.log("⏳ Sending request...");
                $("#products").html('<p class="no-products">Loading products...</p>');
            },
            success: function(response){
                console.log("✅ SUCCESS!");
                console.log("Response:", response);
                console.log("Count:", response.count);
                console.log("Data length:", response.data ? response.data.length : 0);
                $("#products").html(response.data);
            },
            error: function(xhr, status, error){
                console.error("❌ AJAX ERROR!");
                console.error("Status:", status);
                console.error("Error:", error);
                console.error("Status Code:", xhr.status);
                console.error("Response Text:", xhr.responseText);
                
                // Show detailed error
                let errorMsg = "Error loading products.";
                if (xhr.responseText) {
                    errorMsg += " Details: " + xhr.responseText.substring(0, 200);
                }
                $("#products").html('<p class="no-products">' + errorMsg + '</p>');
            },
            complete: function(){
                console.log("🏁 Request completed");
            }
        });
    });
    
    // Clear filters
    window.clearFilters = function() {
        console.log("🧹 Clearing filters...");
        
        $('input[name="category"]').prop('checked', false);
        $("#minPrice").val(0);
        $("#maxPrice").val(1000);
        $("#priceRange").val(1000);
        
        $.ajax({
            url: "/ajax_filter_products/",
            data: "",
            dataType: "json",
            traditional: true,
            success: function(response){
                console.log("✅ Filters cleared");
                $("#products").html(response.data);
            },
            error: function(xhr, status, error){
                console.error("❌ Clear error:", error);
                $("#products").html('<p class="no-products">Error loading products.</p>');
            }
        });
    };
    
    // Update max price when slider changes
    window.updateMaxPrice = function(value) {
        $("#maxPrice").val(value);
    };
    
    // Update slider when max price input changes
    $("#maxPrice").on('input', function(){
        $("#priceRange").val($(this).val());
    });
    
    // Update slider when range changes
    $("#priceRange").on('input', function(){
        $("#maxPrice").val($(this).val());
    });
    
    // ==========================================
    // CART MANAGEMENT - Quantity and Delete
    // ==========================================
    console.log("🛒 Cart handlers setup");
    
    // Decrease quantity button
    $(document).on('click', '.decrease-btn', function(e) {
        e.preventDefault();
        const $btn = $(this);
        if ($btn.prop('disabled')) return;
        
        const productId = $btn.data('product-id');
        const $quantityInput = $(`#quantity-${productId}`);
        const currentQuantity = parseInt($quantityInput.val()) || 1;
        const newQuantity = Math.max(1, currentQuantity - 1);
        
        console.log(`📉 Decreasing quantity for product ${productId}: ${currentQuantity} → ${newQuantity}`);
        updateCartQuantity(productId, newQuantity);
    });
    
    // Increase quantity button
    $(document).on('click', '.increase-btn', function(e) {
        e.preventDefault();
        const $btn = $(this);
        const productId = $btn.data('product-id');
        const $quantityInput = $(`#quantity-${productId}`);
        const currentQuantity = parseInt($quantityInput.val()) || 1;
        const newQuantity = currentQuantity + 1;
        
        console.log(`📈 Increasing quantity for product ${productId}: ${currentQuantity} → ${newQuantity}`);
        updateCartQuantity(productId, newQuantity);
    });
    
    // Quantity input change
    $(document).on('change', '.quantity-input', function() {
        const $input = $(this);
        const productId = $input.data('product-id');
        let newQuantity = parseInt($input.val()) || 1;
        
        // Ensure minimum of 1
        if (newQuantity < 1) {
            newQuantity = 1;
            $input.val(1);
        }
        
        console.log(`✏️ Manual quantity change for product ${productId}: ${newQuantity}`);
        updateCartQuantity(productId, newQuantity);
    });
    
    // Delete button
    $(document).on('click', '.delete-btn', function(e) {
        e.preventDefault();
        const $btn = $(this);
        const productId = $btn.data('product-id');
        
        console.log(`🗑️ Delete button clicked for product ${productId}`);
        deleteCartItem(productId);
    });
    
    console.log("✅ Cart event handlers registered");
});

// ==========================================
// CART FUNCTIONS
// ==========================================

function updateCartQuantity(productId, newQuantity) {
    newQuantity = parseInt(newQuantity);
    
    if (isNaN(newQuantity) || newQuantity < 1) {
        console.warn(`⚠️ Invalid quantity: ${newQuantity}`);
        return;
    }
    
    const itemElement = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
    if (!itemElement) {
        console.error(`❌ Item element not found for product ${productId}`);
        return;
    }
    
    // Add loading state
    itemElement.classList.add('loading');
    const $item = $(itemElement);
    $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', true);
    
    console.log(`🔄 Updating quantity for product ${productId} to ${newQuantity}`);
    
    // Ensure productId is a string
    productId = String(productId);
    
    $.ajax({
        url: "/ajax_update_cart_item/",
        method: "GET",
        data: {
            id: productId,
            quantity: newQuantity
        },
        dataType: "json",
        beforeSend: function(xhr) {
            console.log("📤 Sending request:", {id: productId, quantity: newQuantity});
        },
        success: function(response) {
            console.log("✅ Update response:", response);
            
            if (response.success) {
                // Update quantity input
                const $quantityInput = $(`#quantity-${productId}`);
                $quantityInput.val(response.item_quantity);
                
                // Get price from the price element (unit price)
                const $priceElement = $item.find('.cart-item-price');
                const priceText = $priceElement.text().replace('$', '').trim();
                const unitPrice = parseFloat(priceText);
                
                if (!isNaN(unitPrice)) {
                    // Calculate and update subtotal
                    const newSubtotal = unitPrice * response.item_quantity;
                    $(`#subtotal-${productId}`).text('$' + newSubtotal.toFixed(2));
                }
                
                // Update totals in summary
                if (response.total_amount !== undefined) {
                    $('#cart-subtotal').text('$' + response.total_amount.toFixed(2));
                    $('#cart-total').text('$' + response.total_amount.toFixed(2));
                }
                
                // Update cart count in header
                if (response.total_items !== undefined) {
                    $("#cartCount").text(response.total_items);
                    const itemText = response.total_items === 1 ? 'item' : 'items';
                    $('#cart-items-count').text(response.total_items + ' ' + itemText + ' in your cart');
                }
                
                // Update decrease button state
                const $decreaseBtn = $item.find('.decrease-btn');
                if (response.item_quantity <= 1) {
                    $decreaseBtn.prop('disabled', true);
                } else {
                    $decreaseBtn.prop('disabled', false);
                }
                
                // Enable all buttons
                $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', false);
                
                // If quantity is 0, item was removed
                if (response.item_quantity === 0) {
                    $item.css({
                        'transition': 'opacity 0.3s, transform 0.3s',
                        'opacity': '0',
                        'transform': 'translateX(-20px)'
                    });
                    
                    setTimeout(function() {
                        $item.remove();
                        // Reload if cart is empty
                        if (response.total_items === 0) {
                            location.reload();
                        }
                    }, 300);
                }
            } else {
                // Log error but don't show notification
                console.error("Failed to update quantity:", response.message || "Unknown error");
                $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', false);
            }
        },
        error: function(xhr, status, error) {
            console.error("❌ Error updating quantity:", error);
            console.error("Status:", status);
            console.error("Status Code:", xhr.status);
            console.error("Response:", xhr.responseText);
            
            console.error("Error updating quantity:", xhr.responseText);
            // Re-enable buttons on error
            $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', false);
        },
        complete: function() {
            itemElement.classList.remove('loading');
        }
    });
}

function deleteCartItem(productId) {
    if (!confirm("Are you sure you want to remove this item from your cart?")) {
        return;
    }
    
    const itemElement = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
    if (!itemElement) {
        console.error(`❌ Item element not found for product ${productId}`);
        return;
    }
    
    const $item = $(itemElement);
    $item.addClass('loading');
    $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', true);
    
    console.log(`🗑️ Deleting product ${productId}`);
    
    // Ensure productId is a string
    productId = String(productId);
    
    $.ajax({
        url: "/ajax_delete_cart_item/",
        method: "GET",
        data: {
            id: productId
        },
        dataType: "json",
        beforeSend: function(xhr) {
            console.log("📤 Sending delete request:", {id: productId});
        },
        success: function(response) {
            console.log("✅ Delete response:", response);
            
            if (response.success) {
                // Animate removal silently (no alert)
                $item.css({
                    'transition': 'opacity 0.3s, transform 0.3s',
                    'opacity': '0',
                    'transform': 'translateX(-20px)'
                });
                
                setTimeout(function() {
                    $item.remove();
                    
                    // Update totals
                    if (response.total_amount !== undefined) {
                        $('#cart-subtotal').text('$' + response.total_amount.toFixed(2));
                        $('#cart-total').text('$' + response.total_amount.toFixed(2));
                    }
                    
                    // Update cart count in header
                    if (response.total_items !== undefined) {
                        $("#cartCount").text(response.total_items);
                        const itemText = response.total_items === 1 ? 'item' : 'items';
                        $('#cart-items-count').text(response.total_items + ' ' + itemText + ' in your cart');
                    }
                    
                    // Reload if cart is empty
                    if (response.total_items === 0) {
                        location.reload();
                    }
                }, 300);
            } else {
                // Log error but don't show notification
                console.error("Failed to remove item:", response.message || "Unknown error");
                $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', false);
            }
        },
        error: function(xhr, status, error) {
            console.error("❌ Error deleting item:", error);
            console.error("Status:", status);
            console.error("Status Code:", xhr.status);
            console.error("Response:", xhr.responseText);
            
            console.error("Error removing item:", xhr.responseText);
            $item.removeClass('loading');
            $item.find('.quantity-btn, .quantity-input, .delete-btn').prop('disabled', false);
        }
    });
}

// ==========================================
// ADDRESS MANAGEMENT FUNCTIONS
// ==========================================

// Edit address function
window.editAddress = function(addressId) {
    // Redirect to edit page
    window.location.href = '/edit-address/' + addressId + '/';
};

// Set default address function
window.setDefaultAddress = function(addressId) {
    if (!confirm('Set this address as default?')) {
        return;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajax({
        url: '/set-default-address/' + addressId + '/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(response) {
            if (response.success) {
                showNotification('Default address updated successfully', 'success');
                setTimeout(function() {
                    location.reload();
                }, 1000);
            } else {
                showNotification(response.message || 'Error updating default address', 'error');
            }
        },
        error: function() {
            showNotification('An error occurred', 'error');
        }
    });
};

// Remove address function
window.removeAddress = function(addressId) {
    if (!confirm('Are you sure you want to remove this address?')) {
        return;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajax({
        url: '/delete-address/' + addressId + '/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(response) {
            if (response.success) {
                $('#address-card-' + addressId).fadeOut(300, function() {
                    $(this).remove();
                });
                showNotification('Address deleted successfully', 'success');
            } else {
                showNotification(response.message || 'Error deleting address', 'error');
            }
        },
        error: function() {
            showNotification('An error occurred', 'error');
        }
    });
};

// Helper function to get CSRF token
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

// ==========================================
// WISHLIST FUNCTIONS
// ==========================================

// Add to wishlist function (global)
window.addToWishlist = function(element) {
    const productId = $(element).data('product-id') || $(element).closest('.card, .wishlist-item').find('[class*="product-id"]').val();
    
    if (!productId) {
        console.error('Product ID not found');
        showNotification('Error: Product ID not found', 'error');
        return;
    }
    
    console.log('❤️ Adding to wishlist:', productId);
    
    // Check if user is authenticated
    if (!isUserAuthenticated()) {
        showNotification('Please login to add items to wishlist', 'warning');
        window.location.href = '/login/';
        return;
    }
    
    const $btn = $(element);
    const originalText = $btn.html();
    $btn.prop('disabled', true).html('...');
    
    $.ajax({
        url: '/ajax_add_to_wishlist/',
        method: 'GET',
        data: {
            id: productId
        },
        dataType: 'json',
        success: function(response) {
            console.log('✅ Wishlist response:', response);
            
            if (response.success) {
                showNotification('Added to wishlist! ❤️', 'success');
                $btn.html('❤️').css('color', '#ef4444');
                
                // Update wishlist count if element exists
                updateWishlistCount();
            } else {
                if (response.in_wishlist) {
                    showNotification('Already in wishlist', 'info');
                    $btn.html('❤️').css('color', '#ef4444');
                } else {
                    showNotification(response.message || 'Error adding to wishlist', 'error');
                    $btn.html(originalText);
                }
            }
        },
        error: function(xhr, status, error) {
            console.error('❌ Wishlist error:', error);
            showNotification('Error adding to wishlist', 'error');
            $btn.html(originalText).prop('disabled', false);
        },
        complete: function() {
            $btn.prop('disabled', false);
        }
    });
};

// Remove from wishlist function
window.removeFromWishlist = function(productId) {
    if (!confirm('Remove this item from your wishlist?')) {
        return;
    }
    
    console.log('🗑️ Removing from wishlist:', productId);
    
    const $item = $(`.wishlist-item[data-product-id="${productId}"]`);
    $item.css('opacity', '0.5');
    
    $.ajax({
        url: '/ajax_remove_from_wishlist/',
        method: 'GET',
        data: {
            id: productId
        },
        dataType: 'json',
        success: function(response) {
            console.log('✅ Remove wishlist response:', response);
            
            if (response.success) {
                showNotification('Removed from wishlist', 'success');
                
                // Animate removal
                $item.fadeOut(300, function() {
                    $(this).remove();
                    
                    // Check if wishlist is empty
                    if ($('.wishlist-item').length === 0) {
                        location.reload();
                    }
                });
                
                // Update wishlist count
                updateWishlistCount();
            } else {
                showNotification(response.message || 'Error removing from wishlist', 'error');
                $item.css('opacity', '1');
            }
        },
        error: function(xhr, status, error) {
            console.error('❌ Remove wishlist error:', error);
            showNotification('Error removing from wishlist', 'error');
            $item.css('opacity', '1');
        }
    });
};

// Update wishlist count in header
function updateWishlistCount() {
    // If on wishlist page, count items directly
    if ($('.wishlist-item').length > 0) {
        const count = $('.wishlist-item').length;
        if ($('#wishCount').length) {
            $('#wishCount').text(count);
        }
        return;
    }
    
    // Otherwise, make AJAX call to get count
    $.ajax({
        url: '/ajax_wishlist_count/',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response.success && $('#wishCount').length) {
                $('#wishCount').text(response.count || 0);
            }
        },
        error: function() {
            // Silently fail - count will update on next page load
        }
    });
}

// Check if user is authenticated
function isUserAuthenticated() {
    // Check if there's a user session (you can improve this)
    return document.cookie.indexOf('sessionid') !== -1 || 
           document.cookie.indexOf('csrftoken') !== -1;
}

// Wishlist button handlers
$(document).ready(function() {
    // Handle remove wishlist button clicks
    $(document).on('click', '.remove-wishlist-btn', function(e) {
        e.preventDefault();
        const productId = $(this).data('product-id');
        if (productId) {
            removeFromWishlist(productId);
        }
    });
    
    // Handle add to wishlist button clicks (for buttons with class)
    $(document).on('click', '.add-to-wishlist', function(e) {
        e.preventDefault();
        addToWishlist(this);
    });
    
    // Update wishlist count on page load if user is authenticated
    if (isUserAuthenticated()) {
        updateWishlistCount();
    }
});