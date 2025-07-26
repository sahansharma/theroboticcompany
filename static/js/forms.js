// Form handling functionality

// Declare variables before using them
function showToast(message, type = "success") {
  console.log(`Toast: ${message} (${type})`)
}

function setLoadingState(button, isLoading) {
  if (isLoading) {
    button.disabled = true
    button.textContent = "Loading..."
  } else {
    button.disabled = false
    button.textContent = "Submit"
  }
}

async function apiRequest(url, options) {
  const response = await fetch(url, options)
  if (!response.ok) {
    throw new Error("Network response was not ok")
  }
  return response.json()
}

// Newsletter form
document.addEventListener("DOMContentLoaded", () => {
  const newsletterForm = document.getElementById("newsletter-form")
  if (newsletterForm) {
    newsletterForm.addEventListener("submit", handleNewsletterSubmit)
  }

  const demoForm = document.getElementById("demo-form")
  if (demoForm) {
    demoForm.addEventListener("submit", handleDemoSubmit)
  }
})

async function handleNewsletterSubmit(event) {
  event.preventDefault()

  const form = event.target
  const email = form.querySelector("#newsletter-email").value
  const submitBtn = form.querySelector('button[type="submit"]')

  if (!email) {
    showToast("Please enter your email address", "error")
    return
  }

  setLoadingState(submitBtn, true)

  try {
    await apiRequest("/api/newsletter", {
      method: "POST",
      body: JSON.stringify({ email }),
    })

    showToast("Thank you for subscribing!")
    form.reset()
  } catch (error) {
    console.error("Newsletter subscription error:", error)
    showToast("Failed to subscribe. Please try again.", "error")
  } finally {
    setLoadingState(submitBtn, false)
  }
}

async function handleDemoSubmit(event) {
  event.preventDefault()

  const form = event.target
  const formData = new FormData(form)
  const data = Object.fromEntries(formData.entries())
  const submitBtn = form.querySelector('button[type="submit"]')

  if (!data.fullName || !data.email) {
    showToast("Please fill in all required fields", "error")
    return
  }

  setLoadingState(submitBtn, true)

  try {
    await apiRequest("/api/demo-request", {
      method: "POST",
      body: JSON.stringify(data),
    })

    showToast("Demo request submitted successfully!")
    form.reset()
  } catch (error) {
    console.error("Demo request error:", error)
    showToast("Failed to submit request. Please try again.", "error")
  } finally {
    setLoadingState(submitBtn, false)
  }
}
