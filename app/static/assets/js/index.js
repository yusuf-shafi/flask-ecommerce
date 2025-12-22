function addToBasket(productId) {
  const qtyEl = document.getElementById(`qty-${productId}`);
  const sizeEl = document.getElementById(`size-${productId}`);

  const quantity = qtyEl ? qtyEl.value : "1";
  const size = sizeEl ? sizeEl.value.trim() : "";

  if (!size) {
    alert("Please enter/select a size.");
    return;
  }

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/basket", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        alert("Added to basket!");
      } else {
        try {
          const res = JSON.parse(xhr.responseText);
          alert(res.error || "Failed to add product to basket.");
        } catch {
          alert("Failed to add product to basket.");
        }
      }
    }
  };

  const data = JSON.stringify({
    product_id: productId,
    quantity: quantity,
    size: size
  });

  xhr.send(data);
}
