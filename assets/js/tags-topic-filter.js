(() => {
  const panel = document.getElementById("tag-topic-filter");
  const input = document.getElementById("tag-topic-query");
  const status = document.getElementById("tag-topic-status");
  if (!panel || !input || !status) return;

  const links = [...document.querySelectorAll("#tag-topic-links .tag-item")];
  const all = links.find((link) => link.getAttribute("href") === "#");
  const topics = links.filter((link) => link !== all);
  if (!topics.length) return;

  const normalize = (value) => String(value).normalize("NFKC").toLocaleLowerCase().trim();
  const names = topics.map((link) => normalize(link.textContent));

  // Keep this local filter in the current history entry, not the URL,
  // cookies, sessionStorage, or analytics. Respect unrelated page state.
  const stateKey = "__devTagTopicSearch";
  const maxQueryLength = 120;
  const historyObject = () => {
    try {
      const state = window.history.state;
      return state === null || (
        typeof state === "object" && !Array.isArray(state)
      ) ? state : undefined;
    } catch (_) {
      return undefined;
    }
  };
  const restoreQuery = () => {
    const state = historyObject();
    const query = state && state[stateKey] && state[stateKey].query;
    return typeof query === "string" &&
      query.length <= maxQueryLength &&
      !query.includes("\ufffd") ? query : "";
  };
  const rememberQuery = () => {
    const state = historyObject();
    if (state === undefined) return; // Never replace a peer's primitive state.
    const next = { ...(state || {}) };
    const query = input.value;
    if (typeof query === "string" && query.length > 0 &&
        query.length <= maxQueryLength && !query.includes("\ufffd")) {
      next[stateKey] = { query };
    } else if (state && Object.prototype.hasOwnProperty.call(state, stateKey)) {
      delete next[stateKey]; // Clearing the search also clears saved text.
    } else {
      return;
    }
    try {
      window.history.replaceState(next, ""); // Original URL and hash unchanged.
    } catch (_) {
      // Filtering must still work in restricted history environments.
    }
  };

  const update = () => {
    const query = normalize(input.value);
    let count = 0;
    topics.forEach((link, i) => {
      const matches = !query || names[i].includes(query);
      link.hidden = !matches;
      if (matches) count++;
    });
    if (all) all.hidden = Boolean(query);
    status.textContent = query ? count + " of " + topics.length + " topics" : topics.length + " topics";
  };

  input.value = restoreQuery();
  input.addEventListener("input", () => {
    update();
    rememberQuery();
  });
  if (typeof window !== "undefined" && window.addEventListener) {
    // Chrome emits popstate with a null state BEFORE hashchange for a new
    // native #tag link. Distinguish that click from Back/Forward history.
    const topicLinks = document.getElementById("tag-topic-links");
    let followingTagClick = false;
    if (topicLinks) {
      topicLinks.addEventListener("click", (event) => {
        const target = event.target;
        const anchor = target && typeof target.closest === "function" ?
          target.closest("a.tag-item[href^='#']") : null;
        followingTagClick = Boolean(anchor && topicLinks.contains(anchor) &&
          !event.defaultPrevented && !event.ctrlKey && !event.metaKey &&
          !event.shiftKey && !event.altKey &&
          anchor.getAttribute("href") !== window.location.hash);
      });
    }
    window.addEventListener("popstate", () => {
      if (followingTagClick) {
        followingTagClick = false;
        rememberQuery(); // Attach query to the newly-created #tag entry.
      } else {
        input.value = restoreQuery(); // Existing Back/Forward state owns this entry.
        update();
      }
    });
    window.addEventListener("hashchange", () => {
      if (!followingTagClick) return;
      followingTagClick = false;
      rememberQuery(); // Fallback when a browser only fires hashchange.
    });
  }
  panel.hidden = false;
  update();
})();
