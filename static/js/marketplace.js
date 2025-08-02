// Marketplace functionality

let currentCategory = "all"
let currentSearch = ""
let currentPage = 1
let pageSize = 12
let totalProducts = 0
let loadingProducts = false

// Declare apiRequest and showToast functions or import them
async function apiRequest(url) {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error("Network response was not ok")
  }
  return response.json()
}

function showToast(message, type = "success") {
  console.log(`Toast: ${message} (${type})`)
}

async function loadProducts(reset = false) {
  if (loadingProducts) return;
  loadingProducts = true;
  try {
    if (reset) {
      currentPage = 1;
      totalProducts = 0;
      document.getElementById("products-grid").innerHTML = '';
    }
    const params = new URLSearchParams({
      category: currentCategory,
      search: currentSearch,
      page: currentPage,
      page_size: pageSize
    })
    const data = await apiRequest(`/api/products?${params}`)
    totalProducts = data.total
    renderProducts(data.products, reset)
    updateLoadMoreButton()
  } catch (error) {
    console.error("Failed to load products:", error)
    showToast("Failed to load products", "error")
  } finally {
    loadingProducts = false;
  }
}

function renderProducts(products, reset = false) {
  const grid = document.getElementById("products-grid")
  if (reset && products.length === 0) {
    grid.innerHTML = `
      <div class="no-results">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 6H3v11a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-2"></path>
          <path d="M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2"></path>
          <line x1="12" x2="12" y1="11" y2="15"></line>
          <line x1="10" x2="14" y1="13" y2="13"></line>
        </svg>
        <h3>No products found</h3>
        <p>Try adjusting your search or filter criteria.</p>
      </div>
    `
    return
  }
  const html = products.map(
    (product) => `
      <div class="product-card">
        <div class="product-image">
          ${product.featured ? '<div class="product-badge">Featured</div>' : ""}
          <img src="${product.image}" alt="${product.name}" style="width: 100%; height: 180px; object-fit: contain; background: #e0e7ef; border-radius: 1rem;" />
        </div>
        <div class="product-info">
          <h3 class="product-title">${product.name}</h3>
          <p class="product-description">${product.description}</p>
          <div class="product-rating">
            <span class="rating-stars">★</span>
            <span>${product.rating}</span>
            <span>(${product.reviews} reviews)</span>
          </div>
          <div class="product-footer">
            <span class="product-price">$${product.price}</span>
            <button class="add-to-cart-btn" ${!product.in_stock ? "disabled" : ""} onclick="addToCart('${product.id}')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13v6a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2v-6m-9 0h9"></path>
              </svg>
              ${product.in_stock ? "Add to Cart" : "Out of Stock"}
            </button>
          </div>
        </div>
      </div>
    `
  ).join("")
  if (reset) {
    grid.innerHTML = html
  } else {
    grid.innerHTML += html
  }
}

function updateLoadMoreButton() {
  let btn = document.getElementById('load-more-products')
  if (!btn) {
    btn = document.createElement('button')
    btn.id = 'load-more-products'
    btn.className = 'btn btn-primary'
    btn.textContent = 'Load More'
    btn.onclick = () => {
      currentPage++
      loadProducts(false)
    }
    document.querySelector('.section-footer').appendChild(btn)
  }
  // Show or hide button
  if ((currentPage * pageSize) >= totalProducts) {
    btn.style.display = 'none'
  } else {
    btn.style.display = 'inline-block'
  }
}

function setProductCategory(category) {
  currentCategory = category
  // Update active filter button
  document.querySelectorAll(".category-filters .filter-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  document.querySelector(`[data-category="${category}"]`).classList.add("active")
  loadProducts(true)
}

function filterProducts() {
  currentSearch = document.getElementById("product-search").value
  loadProducts(true)
}

function addToCart(productId) {
  // Simulate adding to cart
  showToast("Product added to cart!")
}

// Initialize marketplace
document.addEventListener("DOMContentLoaded", () => {
  // Add event listeners for search input
  const searchInput = document.getElementById("product-search")
  if (searchInput) {
    let searchTimeout
    searchInput.addEventListener("input", () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(filterProducts, 300)
    })
  }
  loadProducts(true)
})
