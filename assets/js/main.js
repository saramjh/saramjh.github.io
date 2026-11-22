(() => {
  // Theme switch
  const body = document.body;
  const lamp = document.getElementById("mode");

  const syncThemeState = () => {
    if (lamp) {
      lamp.setAttribute("aria-pressed", String(body.getAttribute("data-theme") === "dark"));
    }
  };

  const toggleTheme = () => {
    const wasDark = body.getAttribute("data-theme") === "dark";
    if (wasDark) body.removeAttribute("data-theme");
    else body.setAttribute("data-theme", "dark");
    try {
      localStorage.setItem("theme", wasDark ? "light" : "dark");
    } catch (_) {
      // The on-page switch still works when browser storage is restricted.
    }
    syncThemeState();
  };

  if (lamp) {
    syncThemeState();
    lamp.addEventListener("click", toggleTheme);
  }

  // Keep keyboard focus inside the full-screen mobile menu.
  const cbox = document.getElementById("menu-trigger");

  if (cbox) {
    const backgrounds = document.querySelectorAll(
      "body > .wrapper, body > .folio, body > .folio-footer, body > .folio-skip-link, body > .site-skip-link"
    );
    const mobile = window.matchMedia("(max-width: 768px)");
    const syncMenu = () => {
      const open = cbox.checked && mobile.matches;
      backgrounds.forEach((area) => {
        if (area.classList.contains("wrapper")) {
          area.classList.toggle("blurry", open);
        }
        area.inert = open;
      });
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
