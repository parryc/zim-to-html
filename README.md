# build manual steps

- after building, go to /boostrap-store/styles.css and change line 914 from `input[type="search"],` to `#searchInput,` to avoid confligt with Algolia
- make sure anything with dynamic js, i.e. the search page, has the "wombat.js" scripts removed from the header, which come from ZIM. they are f'ing with the fetches.

# zimit (used to build full .zim file)

- open docker
- create volume "output"
- then run the command in the command line
	- little snitch will ask for different URLs via the docker process, not the console process

`docker run -v output:/output ghcr.io/openzim/zimit zimit --seeds https://resources.allsetlearning.com/gramwiki/ --name gramwiki --keep --scopeExcludeRx="(oldid|action=|youtube|Special:|printable=yes)" --scopeIncludeRx="(gramwiki/.*|grammar/.*)" --scopeType custom`

`docker run -v output:/output ghcr.io/openzim/zimit zimit --seeds https://resources.allsetlearning.com/chinese/vocabulary --name vocabwiki --keep --scopeExcludeRx="(oldid|action=|youtube|Special:|printable=yes)" --scopeIncludeRx="(vocabwiki/.*|vocabulary/.*)" --scopeType custom`

`docker run -v output:/output ghcr.io/openzim/zimit zimit --seeds https://resources.allsetlearning.com/chinese/pronunciation --name pronwiki --keep --scopeExcludeRx="(oldid|action=|youtube|Special:|printable=yes|mp3)" --scopeIncludeRx="(pronwiki/.*|pronunciation/.*)" --scopeType custom`

- pron wiki might require not downloading the audio via zimit and uploading it separately

- avoids:
	- history
	- log in
	- special pages
	- the print version
- and keeps the crawler from going into the other wikis

## hosting zim file
https://gerowen.substack.com/p/how-i-host-my-own-kiwix-archive

# algolia crawler backup

```
new Crawler({
  appId: "Z9TNH4X62A",
  indexPrefix: "",
  rateLimit: 8,
  maxUrls: 10000,
  schedule: "on the 21 day of the month",
  startUrls: ["https://wikis.allsetlearning.com/chinese/grammar/Main_Page"],
  sitemaps: [],
  saveBackup: false,
  ignoreQueryParams: ["source", "utm_*"],
  actions: [
    {
      indexName: "wiki_test_articles",
      pathsToMatch: ["https://wikis.allsetlearning.com/chinese/grammar/**"],
      recordExtractor: ({ url, $, helpers }) => {
        let defaultHelper = helpers.article({ $, url });
        // some pages can use the default helper, with modifications
        if (defaultHelper.length > 0 && defaultHelper[0].description) {
          defaultHelper[0].description = $(".mw-parser-output > p")
            .eq(0)
            .text()
            .trim();
          defaultHelper[0].name = $("title")
            .text()
            .replace("- Chinese Grammar Wiki", "")
            .trim();
        } else {
          defaultHelper = [
            {
              description: $(".mw-parser-output > p").eq(0).text().trim(),
              content: $(".mw-parser-output").eq(0).attr("content"),
              objectID: url.toString(),
              url: url.toString(),
              name: $("title")
                .text()
                .replace("- Chinese Grammar Wiki", "")
                .trim(),
            },
          ];
        }
        return defaultHelper;
      },
    },
  ],
  initialIndexSettings: {
    wiki_test_articles: {
      distinct: true,
      attributeForDistinct: "url",
      searchableAttributes: [
        "unordered(keywords)",
        "unordered(title)",
        "unordered(description)",
        "url",
      ],
      customRanking: ["asc(depth)"],
      attributesForFaceting: ["category"],
    },
  },
  apiKey: "6158c437d3fdaf6921935f3073a21a2b",
});
```



# wget (DNU)
- [wget option](https://webmasters.stackexchange.com/questions/28702/how-to-dump-a-mediawiki-for-offline-use)
	- `-E` append HTML
	- `-r` recursive
		- may want to specify depth? how to prevent it from getting other wikis at the same time
		- there is also a `-m` command that is useful for mirroring
	- `-p` gets relevant items such as images
	- `-k` convert links for local viewing
`wget -k -p -r -R '*Special*' -R '*Help*' -E https://resources.allsetlearning.com/chinese/grammar`

naively running it doesn't really appear to work – plus it starts going and getting all the other wikis, so may be preferred to write an actual scraper.

ssh-keygen -t ed25519 -b 4096 -C "parry+atlassian@parryc.com" -f ~/.ssh/resources_2025


# zim (DNU)
- [openzim](https://wiki.openzim.org/wiki/OpenZIM) is an offline format that has [python bindings](https://python-libzim.readthedocs.io/en/latest/api_reference/libzim.reader/) and has a [well-maintained](https://github.com/imaybeabitshy/pyzim) library for accessing the ZIM archive
this may be an option: use the standard way of downloading a wiki for offline support and then generate static html files + assets.

- building a zim file: https://wiki.openzim.org/wiki/Build_your_ZIM_file

```
mwoffliner --mwUrl "https://resources.allsetlearning.com/chinese/grammar/" --adminEmail "parry@parryc.com" 
```

```
docker run ghcr.io/openzim/mwoffliner:dev --mwUrl=https://resources.allsetlearning.com/chinese/grammar/ --adminEmail=parry@parryc.com
```
```
--mwWikiPath                MediaWiki article path (by default "/wiki/")
  --mwIndexPhpPath            MediaWiki index.php path (by default "/w/index.php
                              ")
  --mwActionApiPath           MediaWiki API path (by default "/w/api.php")
  --mwRestApiPath             MediaWiki REST API path (by default "/w/rest.php")
  --mwModulePath              MediaWiki module load path (by default "/w/load.ph
                              p")
```

docker run -v .:/output ghcr.io/openzim/mwoffliner:dev --mwUrl=https://resources.allsetlearning.com/gramwiki/ --adminEmail=parry@parryc.com --mwActionApiPath=api.php --mwRestApiPath=rest.php--mwModulePath=load.php --mwWikiPath=/ --mwIndexPhpPath=index.php
