document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("predict-form");
    const priceValue = document.getElementById("price-value");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const productName = document.getElementById("product-name").value;
        const itemCondition = document.getElementById("item-condition").value;
        const category = document.getElementById("category").value;
        const shipping = document.getElementById("shipping").value;
        const itemDescription = document.getElementById("item-description").value;

        const predictedPrice = calculatePrice(itemCondition, shipping);
        
        priceValue.textContent = `$${predictedPrice.toFixed(2)}`;
    });

    function calculatePrice(itemCondition, shipping) {
        // Your price calculation logic here
        // For example, a simple calculation based on condition and shipping
        return 100 + (itemCondition * 10) + (shipping * 20);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("predict-form");
    const priceValue = document.getElementById("price-value");
    const categoryInput = document.getElementById("category");
    const categoryErrorMessage = document.getElementById("category-error");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const productName = document.getElementById("product-name").value;
        const itemCondition = document.getElementById("item-condition").value;
        const category = categoryInput.value;
        const shipping = document.getElementById("shipping").value;
        const itemDescription = document.getElementById("item-description").value;

        // Check if the category matches the pattern
        if (!isValidCategory(category)) {
            categoryErrorMessage.textContent = "Category must match the pattern 'main_cat/sub_cat1/sub_cat2'";
            return;
        } else {
            categoryErrorMessage.textContent = ""; // Clear any previous error message
        }

        const predictedPrice = calculatePrice(itemCondition, shipping);
        
        priceValue.textContent = `$${predictedPrice.toFixed(2)}`;
    });

    function calculatePrice(itemCondition, shipping) {
        // Your price calculation logic here
        // For example, a simple calculation based on condition and shipping
        return 100 + (itemCondition * 10) + (shipping * 20);
    }

    function isValidCategory(category) {
        const pattern = /^[\w\s]+\/[\w\s]+\/[\w\s]+$/;
        return pattern.test(category);
    }
});

