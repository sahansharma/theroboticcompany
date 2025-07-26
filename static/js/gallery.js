// 3D Gallery functionality

let currentGalleryCategory = "all"

// Declare apiRequest and showToast functions or import them
function apiRequest(url) {
  // Placeholder for actual API request logic
  return fetch(url).then((response) => response.json())
}

function showToast(message, type) {
  // Placeholder for actual toast logic
  console.log(`Toast: ${message} (${type})`)
}

async function loadGallery() {
  try {
    const params = new URLSearchParams({
      category: currentGalleryCategory,
    })
    const response = await apiRequest(`/api/gallery?${params}`)
    document.getElementById("gallery-grid").innerHTML = response.html
  } catch (error) {
    console.error("Failed to load gallery:", error)
    showToast("Failed to load gallery", "error")
  }
}

function setGalleryCategory(category) {
  currentGalleryCategory = category

  // Update active filter button
  document.querySelectorAll(".gallery-filters .filter-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  document.querySelector(`[data-category="${category}"]`).classList.add("active")

  loadGallery()
}

function downloadItem(itemId) {
  showToast("Download started!")
}

function viewDetails(itemId) {
  showToast("Opening 3D viewer...")
}
