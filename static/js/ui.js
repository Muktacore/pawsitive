document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.querySelector(".create-post-btn");
  const postForm = document.querySelector(".create-post-form");
  const hamburger = document.querySelector(".hamburger");
  const dropdown = document.querySelector(".dropdown");

  // Toggle post form
  if (toggleBtn && postForm) {
    toggleBtn.addEventListener("click", () => {
      postForm.classList.toggle("hidden");
    });

    // Optional: Close form on outside click
    document.addEventListener("click", (e) => {
      if (!postForm.contains(e.target) && !toggleBtn.contains(e.target)) {
        postForm.classList.add("hidden");
      }
    });
  }

  // Toggle hamburger menu
  if (hamburger && dropdown) {
    hamburger.addEventListener("click", () => {
      dropdown.classList.toggle("hidden");
    });

    // Optional: Close dropdown on outside click
    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target) && !hamburger.contains(e.target)) {
        dropdown.classList.add("hidden");
      }
    });
  }
});
  