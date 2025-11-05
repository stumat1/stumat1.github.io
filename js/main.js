document.addEventListener("DOMContentLoaded", function () {
  const el = document.getElementById("lastModified");
  if (el) {
    try {
      const lastModified = new Date(document.lastModified);

      // Check if the date is valid
      if (isNaN(lastModified.getTime()) || document.lastModified === "") {
        // Fallback to current date if document.lastModified is not available
        const currentDate = new Date();
        const options = {
          year: "numeric",
          month: "long",
          day: "numeric",
        };
        const formattedDate = currentDate.toLocaleDateString("en-US", options);
        el.textContent = `Last updated: ${formattedDate}`;
      } else {
        const options = {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        };
        const formattedDate = lastModified.toLocaleDateString("en-US", options);
        el.textContent = `Last updated: ${formattedDate}`;
      }
    } catch (error) {
      // Fallback if there's any error
      console.warn("Error getting last modified date:", error);
      const currentDate = new Date();
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      const formattedDate = currentDate.toLocaleDateString("en-US", options);
      el.textContent = `Last updated: ${formattedDate}`;
    }
  }
});
// This script updates the content of an element with ID 'lastModified'
// to show the last modified date of the document in a human-readable format.
// It waits for the DOM to be fully loaded before executing.
