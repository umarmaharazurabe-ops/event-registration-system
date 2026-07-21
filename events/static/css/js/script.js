// =========================
// Event Registration System
// =========================

document.addEventListener("DOMContentLoaded", () => {

    console.log("Event Registration System Loaded");

    // Smooth button effect
    const btn = document.querySelector(".btn");

    if (btn) {
        btn.addEventListener("click", () => {
            btn.innerHTML = "Loading...";
            
            setTimeout(() => {
                btn.innerHTML = "Explore Events";
            }, 1000);
        });
    }

});