// theme.js

// Function to toggle dark mode and save preference
function toggleDarkMode() {
    // Toggles the 'dark-mode' class on the body.
    // It returns true if the class was added (now dark mode), false if removed (now light mode).
    const isDark = document.body.classList.toggle("dark-mode");

    // Save the preference to localStorage.
    // We store "true" or "false" as strings.
    localStorage.setItem("darkMode", isDark ? "true" : "false");

    // Get the checkbox element (assuming its ID is 'darkToggle')
    const checkbox = document.getElementById("darkToggle");
    // If the checkbox exists, ensure its checked state matches the current dark mode state.
    if (checkbox) {
        checkbox.checked = isDark;
    }
}

// Initialize theme when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("darkMode"); // Get saved preference from localStorage
    const darkToggleCheckbox = document.getElementById("darkToggle"); // Get the checkbox element

    // Apply dark mode immediately based on saved preference
    if (savedTheme === "true") {
        document.body.classList.add("dark-mode");
        // If the checkbox exists, ensure it reflects the dark mode state
        if (darkToggleCheckbox) {
            darkToggleCheckbox.checked = true;
        }
    } else {
        // If no preference, or explicitly "false", ensure light mode.
        // This also handles the first load when 'darkMode' isn't in localStorage yet.
        document.body.classList.remove("dark-mode");
        if (darkToggleCheckbox) {
            darkToggleCheckbox.checked = false;
        }
    }

    // Attach event listener to the dark mode toggle checkbox/button
    // Assuming your toggle is a checkbox with ID 'darkToggle'.
    // If it's a different element, adjust the ID and event type (e.g., 'click' for a button).
    if (darkToggleCheckbox) {
        darkToggleCheckbox.addEventListener("change", toggleDarkMode);
    }
    // If your toggle is a simple button, it would be:
    // const darkModeButton = document.getElementById("darkModeButton");
    // if (darkModeButton) {
    //     darkModeButton.addEventListener("click", toggleDarkMode);
    // }
});