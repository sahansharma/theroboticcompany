// 3D Gallery functionality with dropdown selector

let galleryItems = []
let currentModel = null

// Declare apiRequest and showToast functions or import them
function apiRequest(url) {
  return fetch(url).then((response) => response.json())
}

function showToast(message, type = "success") {
  console.log(`Toast: ${message} (${type})`)
}

// Load gallery items and populate dropdown
async function loadGalleryItems() {
  try {
    const response = await apiRequest('/api/gallery')
    galleryItems = response.items || []
    populateModelSelector()
  } catch (error) {
    console.error("Failed to load gallery items:", error)
    showToast("Failed to load 3D models", "error")
  }
}

// Populate the model selector dropdown
function populateModelSelector() {
  const selector = document.getElementById('model-selector')
  if (!selector) return
  
  // Clear existing options except the first one
  selector.innerHTML = '<option value="">Select a 3D Model...</option>'
  
  // Add options for each model
  galleryItems.forEach((item, index) => {
    const option = document.createElement('option')
    option.value = index
    option.textContent = item.title
    selector.appendChild(option)
  })
}

// Load the selected model
async function loadSelectedModel() {
  const selector = document.getElementById('model-selector')
  const selectedIndex = selector.value
  
  if (!selectedIndex || selectedIndex === '') {
    hideModelViewer()
    return
  }
  
  const selectedItem = galleryItems[selectedIndex]
  if (!selectedItem) {
    showToast("Model not found", "error")
    return
  }
  
  showLoadingState()
  
  try {
    await displayModel(selectedItem)
    currentModel = selectedItem
  } catch (error) {
    console.error("Failed to load model:", error)
    showToast("Failed to load 3D model", "error")
    hideModelViewer()
  } finally {
    hideLoadingState()
  }
}

// Display the selected model
async function displayModel(item) {
  const container = document.getElementById('model-viewer-container')
  const viewer = document.getElementById('model-viewer')
  const title = document.getElementById('model-title')
  const description = document.getElementById('model-description')
  const category = document.getElementById('model-category')
  const artist = document.getElementById('model-artist')
  const size = document.getElementById('model-size')
  
  // Update model info
  title.textContent = item.title
  description.textContent = item.description
  category.textContent = item.category
  artist.textContent = item.artist
  size.textContent = getFileSize(item.model_url)
  
  // Create model-viewer element
  viewer.innerHTML = ''
  const modelViewer = document.createElement('model-viewer')
  modelViewer.src = item.model_url
  modelViewer.alt = item.title
  modelViewer.cameraControls = true
  modelViewer.autoRotate = true
  modelViewer.shadowIntensity = 1
  modelViewer.environmentImage = 'neutral'
  modelViewer.exposure = 1
  modelViewer.style.width = '100%'
  modelViewer.style.height = '100%'
  
  viewer.appendChild(modelViewer)
  
  // Show the container
  container.style.display = 'block'
  
  // Scroll to the viewer
  container.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// Reset the model view
function resetModelView() {
  const modelViewer = document.querySelector('#model-viewer model-viewer')
  if (modelViewer) {
    modelViewer.cameraOrbit = '0deg 75deg 105%'
    modelViewer.cameraTarget = '0m 0m 0m'
  }
}

// Download the current model
function downloadCurrentModel() {
  if (!currentModel) {
    showToast("No model selected", "error")
    return
  }
  
  const link = document.createElement('a')
  link.href = currentModel.model_url
  link.download = currentModel.title.replace(/\s+/g, '_') + '.glb'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  showToast("Download started!", "success")
}

// Show loading state
function showLoadingState() {
  const loading = document.getElementById('model-loading')
  const container = document.getElementById('model-viewer-container')
  
  if (loading) loading.style.display = 'flex'
  if (container) container.style.display = 'none'
}

// Hide loading state
function hideLoadingState() {
  const loading = document.getElementById('model-loading')
  if (loading) loading.style.display = 'none'
}

// Hide model viewer
function hideModelViewer() {
  const container = document.getElementById('model-viewer-container')
  if (container) container.style.display = 'none'
}

// Get file size (placeholder - would need server-side implementation)
function getFileSize(url) {
  // This is a placeholder - in a real implementation, you'd get this from the server
  const sizes = {
    'Cable.glb': '126 MB',
    'controller.glb': '130 MB',
    'camera.glb': '45 MB',
    'Microchip.glb': '104 KB',
    'sensor.glb': '33 KB',
    'Cable Long.glb': '16 KB',
    'Rover.glb': '324 KB',
    'Battery.glb': '42 KB'
  }
  
  const filename = url.split('/').pop()
  return sizes[filename] || 'Unknown'
}

// Initialize gallery when page loads
document.addEventListener('DOMContentLoaded', () => {
  loadGalleryItems()
})

// Make functions globally accessible
window.loadSelectedModel = loadSelectedModel
window.resetModelView = resetModelView
window.downloadCurrentModel = downloadCurrentModel
