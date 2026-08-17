/* Replaces jQuery + scrolly + scrollex + breakpoints (124 KB) with the one
   behaviour that actually needed JavaScript: highlighting the nav link for the
   section currently in view.

   Smooth scrolling is CSS (`scroll-behavior`), and the mobile nav is CSS (the
   sidebar stacks), so neither needs code. Degrades to a plain, working page if
   this file fails to load or IntersectionObserver is unavailable. */
(function () {
	"use strict";

	var links = Array.prototype.slice.call(
		document.querySelectorAll("#nav a[href^='#']")
	);
	if (!links.length || !("IntersectionObserver" in window)) return;

	var byId = {};
	var sections = [];
	links.forEach(function (link) {
		var section = document.getElementById(link.hash.slice(1));
		if (!section) return;
		byId[section.id] = link;
		sections.push(section);
	});
	if (!sections.length) return;

	var visible = new Set();

	function activate() {
		// Choose the visible section nearest the top of the viewport, so that
		// short sections at the end of the page still win when scrolled to.
		var best = null;
		var bestTop = Infinity;
		visible.forEach(function (id) {
			var top = Math.abs(document.getElementById(id).getBoundingClientRect().top);
			if (top < bestTop) {
				bestTop = top;
				best = id;
			}
		});
		if (!best) return;
		links.forEach(function (link) {
			link.classList.remove("active");
		});
		byId[best].classList.add("active");
	}

	var observer = new IntersectionObserver(
		function (entries) {
			entries.forEach(function (entry) {
				if (entry.isIntersecting) visible.add(entry.target.id);
				else visible.delete(entry.target.id);
			});
			activate();
		},
		// A band across the middle of the viewport: a section counts as "current"
		// once it reaches the upper third and stops when it leaves the lower third.
		{ rootMargin: "-25% 0px -60% 0px", threshold: 0 }
	);

	sections.forEach(function (section) {
		observer.observe(section);
	});
})();
