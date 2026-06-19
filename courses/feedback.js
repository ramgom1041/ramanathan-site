/* Reusable course feedback widget — injects a rating + comment box before the footer.
   Static-site friendly: submits via a pre-filled email (mailto). Swap FORM_URL to a
   Google Form for centralised collection if preferred. */
(function () {
  var EMAIL = "ramgom1041@gmail.com";
  var FORM_URL = ""; // optional: put a Google Form URL here to use that instead of email

  var h1 = document.querySelector("h1");
  var course = h1 ? h1.textContent.trim() : (document.title.split("|")[0] || "Course").trim();

  var wrap = document.createElement("div");
  wrap.className = "fb-wrap";
  wrap.innerHTML =
    '<div class="fb">' +
      '<h3>Was this course helpful?</h3>' +
      '<p class="fb-sub">Rate it and leave a comment — your feedback helps improve the material.</p>' +
      '<div class="fb-stars" role="radiogroup" aria-label="rating">' +
        '<span data-v="1">★</span><span data-v="2">★</span><span data-v="3">★</span>' +
        '<span data-v="4">★</span><span data-v="5">★</span>' +
      '</div>' +
      '<textarea class="fb-text" placeholder="What did you find useful? Anything to improve? (optional)"></textarea>' +
      '<div><button class="fb-send" type="button">Send feedback</button></div>' +
      '<div class="fb-note"></div>' +
    '</div>';

  var footer = document.querySelector("footer");
  if (footer && footer.parentNode) footer.parentNode.insertBefore(wrap, footer);
  else document.body.appendChild(wrap);

  var rating = 0;
  var stars = wrap.querySelectorAll(".fb-stars span");
  function paint(n) { stars.forEach(function (s) { s.classList.toggle("on", +s.dataset.v <= n); }); }
  stars.forEach(function (s) {
    s.addEventListener("mouseenter", function () { paint(+s.dataset.v); });
    s.addEventListener("click", function () { rating = +s.dataset.v; paint(rating); });
  });
  wrap.querySelector(".fb-stars").addEventListener("mouseleave", function () { paint(rating); });

  wrap.querySelector(".fb-send").addEventListener("click", function () {
    var txt = wrap.querySelector(".fb-text").value;
    var note = wrap.querySelector(".fb-note");
    if (!rating && !txt.trim()) { note.textContent = "Please add a rating or a comment first."; note.style.color = "#b42020"; return; }
    if (FORM_URL) { window.open(FORM_URL, "_blank"); note.style.color = "#0b7a4b"; note.textContent = "Opening the feedback form…"; return; }
    var subject = "Course Feedback: " + course;
    var body = "Course: " + course + "\nRating: " + (rating ? rating + "/5" : "(not rated)") +
               "\n\nComments:\n" + txt + "\n\n— sent from the course page";
    window.location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    note.style.color = "#0b7a4b";
    note.textContent = "Opening your email app — thank you for the feedback!";
  });
})();
