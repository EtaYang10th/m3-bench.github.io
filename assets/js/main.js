// M3-Bench blog — interactive bits (dark theme)
document.addEventListener("DOMContentLoaded", () => {
  // Nav toggle (mobile)
  const toggle = document.querySelector(".nav-toggle");
  const links  = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => links.classList.toggle("open"));
    links.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => links.classList.remove("open"))
    );
  }

  // BibTeX copy
  const copyBtn = document.querySelector(".copy-btn[data-copy]");
  if (copyBtn) {
    copyBtn.addEventListener("click", async () => {
      const target = document.querySelector(copyBtn.getAttribute("data-copy"));
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.innerText.trim());
        const old = copyBtn.innerText;
        copyBtn.innerText = "copied ✓";
        setTimeout(() => (copyBtn.innerText = old), 1400);
      } catch (e) {
        const r = document.createRange();
        r.selectNode(target);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(r);
        document.execCommand("copy");
      }
    });
  }

  // Active nav anchor while scrolling (dark-theme colours)
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
      a.style.color      = active ? "var(--cyan)" : "";
      a.style.background = active ? "rgba(94,241,255,0.08)" : "";
    });
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Animate leaderboard bars on first view
  const bars = document.querySelectorAll(".bar-row .bar > span");
  if ("IntersectionObserver" in window && bars.length) {
    const widths = new Map();
    bars.forEach((b) => {
      widths.set(b, b.style.width);
      b.style.width = "0%";
      b.style.transition = "width .9s cubic-bezier(.2,.7,.2,1)";
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const bar = e.target.querySelector(".bar > span");
          if (bar) bar.style.width = widths.get(bar) || "0%";
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll(".bar-row").forEach((r) => io.observe(r));
  }
});
