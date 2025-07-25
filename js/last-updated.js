document.addEventListener("DOMContentLoaded", function () {
  const lastModified = new Date(document.lastModified);
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  const formattedDate = lastModified.toLocaleDateString("en-US", options);
  const el = document.getElementById("lastModified");
  if (el) {
    el.textContent = `Last updated: ${formattedDate}`;
  }
});
// This script updates the content of an element with ID 'lastModified'
// to show the last modified date of the document in a human-readable format.
