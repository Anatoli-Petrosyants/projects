(function () {
  "use strict";

  /* ---- theme toggle ---- */
  var root = document.documentElement;
  var toggle = document.querySelector(".theme-toggle");

  function systemPrefersLight() {
    return window.matchMedia("(prefers-color-scheme: light)").matches;
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var effective = current || (systemPrefersLight() ? "light" : "dark");
      var next = effective === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
      toggle.setAttribute("aria-label", next === "dark" ? "Switch to light theme" : "Switch to dark theme");
    });
  }

  /* ---- reveal on scroll ---- */
  var revealables = document.querySelectorAll(".reveal");
  if (revealables.length) {
    if (!("IntersectionObserver" in window)) {
      revealables.forEach(function (el) { el.classList.add("is-visible"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
      revealables.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---- contact form -> mailto ---- */
  var form = document.querySelector("[data-mailto-form]");
  if (!form) return;

  var mailTo = form.getAttribute("data-mailto-form");

  function setError(input, message) {
    var slot = input.parentElement.querySelector(".error");
    if (slot) slot.textContent = message || "";
    input.setAttribute("aria-invalid", message ? "true" : "false");
  }

  function validate() {
    var ok = true;
    var name = form.elements.name;
    var email = form.elements.email;
    var message = form.elements.message;

    if (!name.value.trim()) { setError(name, "Please enter your name."); ok = false; }
    else setError(name, "");

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) {
      setError(email, "Please enter a valid email address."); ok = false;
    } else setError(email, "");

    if (message.value.trim().length < 10) {
      setError(message, "Please write at least 10 characters."); ok = false;
    } else setError(message, "");

    return ok;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!validate()) {
      var firstBad = form.querySelector('[aria-invalid="true"]');
      if (firstBad) firstBad.focus();
      return;
    }

    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    var topic = form.elements.topic ? form.elements.topic.value : "";
    var message = form.elements.message.value.trim();

    var subject = topic ? topic + ": " + name : "Portfolio enquiry from " + name;
    var body = message + "\n\n" + name + "\n" + email;

    window.location.href =
      "mailto:" + mailTo +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);

    var status = form.querySelector("[data-form-status]");
    if (status) {
      status.textContent = "Opening your email app… if nothing happens, email " + mailTo + " directly.";
    }
  });
})();
