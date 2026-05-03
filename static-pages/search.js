/*
  Initialize the search client
*/
const { liteClient: algoliasearch } = window["algoliasearch/lite"];
const searchClient = algoliasearch(
  "Z9TNH4X62A",
  "35f2fef62508643a32dd31c385e6347f",
);

let searchParams = new URLSearchParams(window.location.search)

if(searchParams.has("search")) {
  const searchDiv = document.createElement("div")
  const content = document.getElementById('mw-content-text')
  searchDiv.innerHTML = "<div class=\"ais-InstantSearch\">\n" +
      "                <div class=\"right-panel\">\n" +
      "                    <div id=\"searchbox\"></div>\n" +
      "                    <div id=\"hits\"></div>\n" +
      "                    <div id=\"pagination\"></div>\n" +
      "                </div>\n" +
      "            </div>"
  content.replaceWith(searchDiv)
  document.getElementsByTagName("h1")[0].innerText = "Search Results"

  // remove unnecessary category links html
  const catLinks = document.getElementById('catlinks')
  if(catLinks) {
      catLinks.innerHTML = ''
  }
}

// Render the InstantSearch.js wrapper
// Replace INDEX_NAME with the name of your index.
const search = instantsearch({
  indexName: "wiki_test_articles",

    initialUiState: {"wiki_test_articles": {query: searchParams.get('search') ?? ''}},
    searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: "#searchbox",
  }),

  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: (hit, { html, components }) => html`
        <div>
          <div class="hit-name">
            <a href="${hit.url}">${hit.name}</a>
          </div>
          <div class="hit-description">
            ${components.Highlight({ hit, attribute: "description" })}
          </div>
        </div>
      `,
    },
  }),
]);

search.start();