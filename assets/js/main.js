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

  // Keep keyboard focus inside the full-screen mobile menu.
  const cbox = document.getElementById("menu-trigger");

  if (cbox) {
    const area = document.querySelector(".wrapper");
    const mobile = window.matchMedia("(max-width: 768px)");
    const syncMenu = () => {
      const open = cbox.checked && mobile.matches;
      area.classList.toggle("blurry", open);
      area.inert = open;
      cbox.setAttribute("aria-expanded", String(open));
    };

    cbox.addEventListener("change", syncMenu);
    window.addEventListener("keydown", (event) => {
      if (event.key !== "Escape" || !cbox.checked || !mobile.matches) return;
      cbox.checked = false;
      syncMenu();
      cbox.focus();
      event.preventDefault();
    });
    mobile.addEventListener("change", () => {
      if (!mobile.matches) cbox.checked = false;
      syncMenu();
    });
    syncMenu();
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
