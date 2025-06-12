self.addEventListener("install", e =>
  e.waitUntil(
    caches.open("omega-cache").then(c => c.addAll(["/js/omega-agent.js"]))
  )
);
