// Main JavaScript functionality

// Navigation
let mobileMenuOpen = false

function toggleMobileMenu() {
  const mobileNav = document.getElementById("mobile-nav")
  const hamburgers = document.querySelectorAll(".hamburger")

  mobileMenuOpen = !mobileMenuOpen

  if (mobileMenuOpen) {
    mobileNav.classList.add("active")
    hamburgers.forEach((hamburger, index) => {
      if (index === 0) hamburger.style.transform = "rotate(45deg) translate(5px, 5px)"
      if (index === 1) hamburger.style.opacity = "0"
      if (index === 2) hamburger.style.transform = "rotate(-45deg) translate(7px, -6px)"
    })
  } else {
    mobileNav.classList.remove("active")
    hamburgers.forEach((hamburger) => {
      hamburger.style.transform = ""
      hamburger.style.opacity = ""
    })
  }
}

function closeMobileMenu() {
  if (mobileMenuOpen) {
    toggleMobileMenu()
  }
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  })
}

// Navbar scroll effect
window.addEventListener("scroll", () => {
  const navbar = document.getElementById("navbar")
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled")
  } else {
    navbar.classList.remove("scrolled")
  }
})

// Smooth scrolling for anchor links
document.addEventListener("DOMContentLoaded", () => {
  // Add smooth scrolling to all anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()

      const targetId = this.getAttribute("href").substring(1)
      if (!targetId) return

      const targetElement = document.getElementById(targetId)
      if (!targetElement) return

      const offset = window.innerWidth < 768 ? 100 : 80

      window.scrollTo({
        top: targetElement.offsetTop - offset,
        behavior: "smooth",
      })

      // Close mobile menu if open
      closeMobileMenu()
    })
  })

  // Initialize animations
  initializeAnimations()

  // Load initial data
  const loadProducts = () => {
    // Placeholder for loadProducts function
    console.log("Loading products...")
  }

  // Remove the old loadGallery call since gallery.js handles its own initialization
  // if (window.loadGallery) {
  //   window.loadGallery()
  // }

  loadProducts()
})

// Animation observer
function initializeAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-fade-in")
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.1 },
  )

  // Observe elements with animation classes
  document
    .querySelectorAll(".animate-on-scroll, .hero-badge, .hero-title, .hero-subtitle, .hero-buttons, .hero-features")
    .forEach((el) => {
      observer.observe(el)
    })
}

// Toast notification system
function showToast(message, type = "success") {
  const toast = document.getElementById("toast")
  const toastMessage = document.getElementById("toast-message")

  toastMessage.textContent = message
  toast.className = `toast ${type}`
  toast.classList.add("show")

  setTimeout(() => {
    toast.classList.remove("show")
  }, 3000)
}

// API helper function
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("API request failed:", error)
    throw error
  }
}

// Loading state helper
function setLoadingState(element, loading) {
  if (loading) {
    element.classList.add("loading")
  } else {
    element.classList.remove("loading")
  }
}
