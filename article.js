const titleElement = document.getElementById("article-title");
const textElement = document.getElementById("article-text");
const container = document.getElementById("article-container");

async function fetchArticles() {
  const response = await fetch("articles.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Unable to load articles: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

function showNotFound() {
  if (container) {
    container.textContent = "";
    const heading = document.createElement("h1");
    heading.textContent = "Article not found";
    const message = document.createElement("p");
    message.textContent = "The article you requested could not be found. Please go back to the homepage and try again.";
    container.append(heading, message);
  }
}

(async () => {
  try {
    const rawIndex = new URLSearchParams(window.location.search).get("index");
    const index = Number.parseInt(rawIndex, 10);
    const articles = await fetchArticles();

    if (!Number.isInteger(index) || index < 0 || index >= articles.length) {
      showNotFound();
      return;
    }

    const article = articles[index] || {};
    if (titleElement) titleElement.textContent = String(article.title || "");
    if (textElement) textElement.textContent = String(article.text || "");
  } catch (error) {
    console.error(error);
    showNotFound();
  }
})();
