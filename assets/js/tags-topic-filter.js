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

  input.addEventListener("input", update);
  panel.hidden = false;
  update();
})();
