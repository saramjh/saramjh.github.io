(() => {
  // Theme switch
  const body = document.body;
  const lamp = document.getElementById("mode");

  const toggleTheme = (state) => {
    if (state === "dark") {
      localStorage.setItem("theme", "light");
      body.removeAttribute("data-theme");
    } else if (state === "light") {
      localStorage.setItem("theme", "dark");
      body.setAttribute("data-theme", "dark");
    } else {
      initTheme(state);
    }
  };

  lamp.addEventListener("click", () =>
    toggleTheme(localStorage.getItem("theme"))
  );

  // Blur the content when the menu is open
  const cbox = document.getElementById("menu-trigger");

  if (cbox) {
    cbox.addEventListener("change", function () {
      const area = document.querySelector(".wrapper");
      this.checked
        ? area.classList.add("blurry")
        : area.classList.remove("blurry");
    });
  }

  // Dynamic Image Contract: Prioritize first image (LCP), lazy-load subsequent images
  const postImages = document.querySelectorAll("main img:not(.author-avatar)");
  postImages.forEach((img, index) => {
    if (index === 0) {
      if (!img.hasAttribute("fetchpriority")) {
        img.setAttribute("fetchpriority", "high");
      }
      img.setAttribute("loading", "eager");
    } else {
      if (!img.hasAttribute("loading")) {
        img.setAttribute("loading", "lazy");
      }
    }
    if (!img.hasAttribute("decoding")) {
      img.setAttribute("decoding", "async");
    }
  });
})();
