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

  /* ---- screenshot lightbox ---- */
  /* A thumbnail is only 270px wide, so tapping one opens the same file in a
     modal <dialog> sized to the viewport, with the arrow keys and the on-screen
     arrows walking the strip without closing it. */
  function lightbox(gallery) {
    var dialog = gallery.querySelector("[data-gallery-lightbox]");
    var openers = gallery.querySelectorAll("[data-gallery-open]");
    /* no <dialog> support: the thumbnails stay plain, scrollable pictures */
    if (!dialog || !openers.length || typeof dialog.showModal !== "function") {
      if (dialog) dialog.remove();
      openers.forEach(function (button) { button.style.cursor = "default"; });
      return;
    }

    var figure = dialog.querySelector("[data-lightbox-figure]");
    var counter = dialog.querySelector("[data-lightbox-count]");
    var steps = dialog.querySelectorAll("[data-lightbox-step]");
    var closer = dialog.querySelector("[data-lightbox-close]");
    var thumbs = [];
    openers.forEach(function (button) { thumbs.push(button.querySelector("img")); });
    var index = 0;
    var opener = null;

    function show(wanted) {
      index = (wanted + thumbs.length) % thumbs.length;
      var thumb = thumbs[index];
      var big = document.createElement("img");
      big.className = "lightbox__image";
      /* the attributes, not the layout size: these are the file's real pixels */
      big.width = Number(thumb.getAttribute("width"));
      big.height = Number(thumb.getAttribute("height"));
      big.alt = thumb.alt;
      big.decoding = "async";
      big.src = thumb.currentSrc || thumb.src;
      figure.textContent = "";
      figure.appendChild(big);
      counter.textContent = index + 1 + " of " + thumbs.length;
      steps.forEach(function (button) { button.hidden = thumbs.length < 2; });
      /* keep the strip behind the dialog on the screenshot being looked at */
      openers[index].scrollIntoView({ block: "nearest", inline: "nearest" });
    }

    openers.forEach(function (button) {
      button.addEventListener("click", function () {
        opener = button;
        show(Number(button.getAttribute("data-gallery-open")));
        document.documentElement.classList.add("is-lightbox-open");
        dialog.showModal();
        /* the dialog, not the close button: focusing a control would ring it */
        dialog.focus();
      });
    });

    steps.forEach(function (button) {
      button.addEventListener("click", function () {
        show(index + Number(button.getAttribute("data-lightbox-step")));
      });
    });

    if (closer) {
      closer.addEventListener("click", function () { dialog.close(); });
    }

    /* the figure is centred in a full-viewport dialog, so anything outside it
       is backdrop as far as the visitor is concerned */
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog || event.target === figure) dialog.close();
    });

    dialog.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight") { event.preventDefault(); show(index + 1); }
      else if (event.key === "ArrowLeft") { event.preventDefault(); show(index - 1); }
    });

    /* Escape closes natively, so undo the scroll lock on the event, not the button */
    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("is-lightbox-open");
      figure.textContent = "";
      if (opener) opener.focus();
    });
  }

  /* ---- screenshot galleries ---- */
  document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
    var viewport = gallery.querySelector(".gallery__viewport");
    var buttons = gallery.querySelectorAll("[data-gallery-step]");
    if (!viewport || !buttons.length) return;

    function go(direction) {
      /* each arrow runs the strip all the way to its end */
      var target = direction > 0 ? viewport.scrollWidth - viewport.clientWidth : 0;
      if (typeof viewport.scrollTo === "function") {
        viewport.scrollTo({ left: target, behavior: "smooth" });
      } else {
        viewport.scrollLeft = target;
      }
      /* Safari fires no scroll event when the position is already at an end */
      setTimeout(sync, 400);
    }

    function sync() {
      var max = viewport.scrollWidth - viewport.clientWidth;
      var left = viewport.scrollLeft;
      buttons.forEach(function (button) {
        /* nothing to scroll at all: no arrows */
        button.hidden = max <= 2;
        /* parked at that end: keep the arrow in place but dim and inert */
        var forward = button.getAttribute("data-gallery-step") === "1";
        button.disabled = forward ? left >= max - 2 : left <= 2;
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        go(Number(button.getAttribute("data-gallery-step")));
      });
    });

    var pending = false;
    viewport.addEventListener("scroll", function () {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () { pending = false; sync(); });
    }, { passive: true });

    window.addEventListener("resize", sync);
    lightbox(gallery);
    /* images are lazy, so scrollWidth only settles once they have loaded */
    viewport.querySelectorAll("img").forEach(function (image) {
      if (!image.complete) image.addEventListener("load", sync, { once: true });
    });
    sync();
  });

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
