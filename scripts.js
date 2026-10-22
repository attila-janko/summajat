const newsSection = document.getElementById("news");
const previousButton = document.getElementById("previous");
const nextButton = document.getElementById("next");
const articlesPerPage = 5;
let currentPage = 0;
let articles = [];

async function fetchArticles() {
  const response = await fetch("articles.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Unable to load articles: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data) ? data.filter((item) => item && item.title && item.summary) : [];
}

function updatePaginationButtons() {
  previousButton.disabled = currentPage === 0;
  nextButton.disabled = currentPage >= Math.max(0, Math.ceil(articles.length / articlesPerPage) - 1);
}

function createArticleElement(article, index) {
  const element = document.createElement("article");
  const heading = document.createElement("h2");
  const summary = document.createElement("p");
  const link = document.createElement("a");

  heading.textContent = String(article.title);
  summary.textContent = String(article.summary);
  link.href = `article.html?index=${encodeURIComponent(index)}`;
  link.className = "read-more";
  link.textContent = "Read More";

  element.append(heading, summary, link);
  return element;
}

function displayArticles() {
  newsSection.textContent = "";
  const start = currentPage * articlesPerPage;
  const end = Math.min(start + articlesPerPage, articles.length);

  for (let index = start; index < end; index += 1) {
    newsSection.appendChild(createArticleElement(articles[index], index));
  }

  updatePaginationButtons();
}

previousButton.addEventListener("click", () => {
  if (currentPage > 0) {
    currentPage -= 1;
    displayArticles();
  }
});

nextButton.addEventListener("click", () => {
  if ((currentPage + 1) * articlesPerPage < articles.length) {
    currentPage += 1;
    displayArticles();
  }
});

(async () => {
  try {
    articles = await fetchArticles();
    displayArticles();
  } catch (error) {
    console.error(error);
    newsSection.textContent = "Unable to load articles.";
    previousButton.disabled = true;
    nextButton.disabled = true;
  }
})();
