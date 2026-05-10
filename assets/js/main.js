// SPARK blog — interactive bits
document.addEventListener("DOMContentLoaded", () => {
  // Nav toggle (mobile)
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
    links.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => links.classList.remove("open"))
    );
  }

  // Tabs (case studies + evidence)
  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const buttons = group.querySelectorAll(".tabs button");
    const panels = group.querySelectorAll(".tab-panel");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.getAttribute("data-target");
        buttons.forEach((b) => b.classList.toggle("active", b === btn));
        panels.forEach((p) =>
          p.classList.toggle("active", p.getAttribute("data-panel") === target)
        );
      });
    });
  });

  // BibTeX copy
  const copyBtn = document.querySelector(".copy-btn[data-copy]");
  if (copyBtn) {
    copyBtn.addEventListener("click", async () => {
      const target = document.querySelector(copyBtn.getAttribute("data-copy"));
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.innerText.trim());
        const old = copyBtn.innerText;
        copyBtn.innerText = "Copied ✓";
        setTimeout(() => (copyBtn.innerText = old), 1500);
      } catch (e) {
        // Fallback
        const r = document.createRange();
        r.selectNode(target);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(r);
        document.execCommand("copy");
      }
    });
  }

  // Active section in nav on scroll
  const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
  const sections = Array.from(navAnchors)
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);
  const onScroll = () => {
    const y = window.scrollY + 120;
    let current = null;
    for (const s of sections) {
      if (s.offsetTop <= y) current = s;
    }
    navAnchors.forEach((a) => {
      const active = current && a.getAttribute("href") === "#" + current.id;
      a.style.color = active ? "var(--c-text)" : "";
      a.style.background = active ? "var(--c-bg-soft)" : "";
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
});
