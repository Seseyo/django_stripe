// Get Stripe publishable key
fetch("/catalog/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);


// Event handler
document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    var param = document.location.pathname;
    var items = param.split('/');
    var item_id = items[items.length-1];
    console.log(param);
    fetch("/catalog/buy/" + item_id)
    .then((result) => { return result.json(); })
    .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
        console.log(res);
    });
  });
});