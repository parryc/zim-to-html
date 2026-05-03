manual steps

- after building, go to /boostrap-store/styles.css and change line 914 from `input[type="search"],` to `#searchInput,` to avoid confligt with Algolia
- make sure anything with dynamic js, i.e. the search page, has the "wombat.js" scripts removed from the header, which come from ZIM. they are f'ing with the fetches.