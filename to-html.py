import pyzim
import os
import shutil
from helpers import to_css
from urllib.parse import unquote, quote

build = True

roots_to_ignore = [
    "fonts.gstatic.com",
    "i.ytimg.com",
    "jnn-pa.googleapis.com",
    "www.google.com",
    "www.gstatic.com",
    "www.youtube-nocookie.com",
    "youtube.fuzzy.replayweb.page",
    "yt3.ggpht.com",
]
too_long = [
    "load.php?debug=false&lang=en&modules=ext.ASLExtension|jquery,site|jquery.accessKeyLabel,checkboxShiftClick,client,cookie,getAttrs,highlightText,suggestions,tabIndex|mediawiki.RegExp,String,Title,api,base,searchSuggest,util|mediawiki.page.ready,startup|skins.allset|user.defaults&skin=allset&version=0lnfta7",
    "load.php?lang=en&modules=mediawiki.htmlform.styles|mediawiki.legacy.commonPrint,shared|mediawiki.special.userlogin.common.styles|mediawiki.special.userlogin.login.styles|mediawiki.ui|mediawiki.ui.button,checkbox,input,radio&only=styles&printable=1&skin=allset",
    "load.php?debug=false&lang=en&modules=jquery,oojs,oojs-ui-core,oojs-ui-widgets|mediawiki.special.search|mediawiki.widgets|mediawiki.widgets.SearchInputWidget|oojs-ui.styles.icons-editing-advanced,icons-moderation,icons-movement|skins.allset&skin=allset&version=1ngvlmj"
    "load.php?lang=en&modules=mediawiki.helplink,special,ui|mediawiki.legacy.commonPrint,shared|mediawiki.special.search.styles|mediawiki.ui.button,input|mediawiki.widgets.SearchInputWidget.styles|mediawiki.widgets.styles|oojs-ui-core.styles|oojs-ui.styles.icons-alerts,icons-content,icons-interactions,indicators,textures&only=styles&skin=allset",
    "load.php?debug=false&lang=en&modules=jquery,oojs,oojs-ui-core,oojs-ui-widgets|mediawiki.special.search|mediawiki.widgets|mediawiki.widgets.SearchInputWidget|oojs-ui.styles.icons-editing-advanced,icons-moderation,icons-movement|skins.allset&skin=allset&version=1ngvlmj",
    "load.php?lang=en&modules=mediawiki.helplink,special,ui|mediawiki.legacy.commonPrint,shared|mediawiki.special.search.styles|mediawiki.ui.button,input|mediawiki.widgets.SearchInputWidget.styles|mediawiki.widgets.styles|oojs-ui-core.styles|oojs-ui.styles.icons-alerts,icons-content,icons-interactions,indicators,textures&only=styles&skin=allset",
]

css_files = [
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.cite.styles|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.cite.styles|mediawiki.legacy.commonPrint,shared|mediawiki.toc.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.cite.styles|mediawiki.legacy.commonPrint,shared|mediawiki.toc.styles|onoi.dataTables.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.pygments|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.smw.page.styles|ext.smw.style|ext.smw.tooltip.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.smw.special.styles|ext.smw.style|ext.smw.tooltip.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.smw.style|ext.smw.tooltip.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=ext.smw.style|ext.smw.tooltip.styles|smw.tableprinter.datatable.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.action.view.categoryPage.styles|mediawiki.action.view.redirectPage|mediawiki.helplink|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.action.view.categoryPage.styles|mediawiki.helplink|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.action.view.filepage,redirectPage|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.action.view.filepage|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.action.view.redirectPage|mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.helplink,special,ui|mediawiki.legacy.commonPrint,shared|mediawiki.special.search.styles|mediawiki.ui.button,input|mediawiki.widgets.SearchInputWidget.styles|mediawiki.widgets.styles|oojs-ui-core.styles|oojs-ui.styles.icons-alerts,icons-content,icons-interactions,indicators,textures&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.toc.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|mediawiki.toc.styles|onoi.dataTables.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=mediawiki.legacy.commonPrint,shared|onoi.dataTables.styles&only=styles&skin=allset",
    "resources.allsetlearning.com/gramwiki/load.php?lang=en&modules=site.styles&only=styles&skin=allset",

]

# jsdeliver is "select2@4.0.13
resources_to_ignore = ["cdn.jsdeliver.net", "fulltext", "listing", "title", "www.fluentu.com"]

mapped_filenames = {
    "select2.min.css?ver=6.7.1": "select2.min.css",
    "responsive.css?10b44": "responsive.css",
    "styles.css?83b94": "styles.css",
    "font-awesome.css?3e78a": "font-awesome.css",
    "skin-style.css?ea523": "skin-style.css",
    "fluentu-ccw-public.css?ver=1.0.0": "fluentu-ccw-public.css",
    "style.css?v=1756517142&ver=6.7.1": "style.css",
    "style.css?ver=6.7.1": "style.css",
    "style.css?ver=2.7.3": "style.css",
    "style.css?ver=1729492450": "style.css",
    "style.css?ver=1696844687": "style.css",
    "lite-yt-embed.css?ver=6.7.1": "lite-yt-embed.css",
    "default.css?ver=3.1.3": "default.css",
    "animate.css?ver=3.6.0": "animate.css",
    "wp-quiz.css?ver=2.1.11": "wp-quiz.css",
    "font-awesome.min.css?ver=4.7.0-modified": "font-awesome.min.css",
    "wp-review.css?ver=3.4.11": "wp-review.css",
    "related.css?ver=5.30.11": "related.css",
    "style.css?ver=1748332982": "style.css",
    "style.css?ver=1": "style.css",
    "load.php?debug=false&lang=en&modules=ext.cite.ux-enhancements|jquery|skins.allset&skin=allset&version=1aatwqe": "1aatwqe.js",
    "load.php?debug=false&lang=en&modules=ext.jquery.async|ext.libs.tippy|ext.smw|ext.smw.tooltips|smw.tippy&skin=allset&version=0h7taxi": "0h7taxi.js",
    "load.php?debug=false&lang=en&modules=ext.smw.tooltip|smw.property.page&skin=allset&version=0eiflws": "0eiflws.js",
    "load.php?debug=false&lang=en&modules=jquery,oojs-ui-core,oojs-ui-widgets|oojs-ui.styles.icons-editing-advanced|skins.allset&skin=allset&version=0qdij45": "0qdij45.js",
    "load.php?debug=false&lang=en&modules=jquery|jquery.tablesorter|jquery.tablesorter.styles|mediawiki.cldr,language|mediawiki.language.months|mediawiki.libs.pluralruleparser|skins.allset&skin=allset&version=1xevhq4": "1xevhq4.js",
    "load.php?debug=false&lang=en&modules=jquery|mediawiki.action.view.metadata|skins.allset&skin=allset&version=0mi5kaf": "0mi5kaf.js",
    "load.php?debug=false&lang=en&modules=jquery|mediawiki.action.view.redirect|skins.allset&skin=allset&version=1xjsun3": "1xjsun3.js",
    "load.php?debug=false&lang=en&modules=jquery|mediawiki.api.parse|skins.allset&skin=allset&version=1nzgxcl": "1nzgxcl.js",
    "load.php?debug=false&lang=en&modules=jquery|mediawiki.cookie,toc|skins.allset&skin=allset&version=1n4l3qz": "1n4l3qz.js",
    "load.php?debug=false&lang=en&modules=jquery|skins.allset&skin=allset&version=1pkqjj2": "1pkqjj2.js",
    "load.php?lang=en&modules=startup&only=scripts&skin=allset": "startup.js"
}

with pyzim.Zim.open("./gramwiki_2025-08-full.zim") as zim:
    for e in zim.iter_entries():
        if e.url.split("/")[0] in roots_to_ignore:
            continue
        # skip printing metadata
        if e.namespace == "M":
            continue
        # skip outputting templates
        if "Template:" in e.url:
            continue
        # skip outputting "?title="Special:Search" pages, since we can't do anything with them
        if '?title=Special:Search' in e.url:
            continue
        # skip property search pages
        if '?title=Property:' in e.url:
            continue
        if e.is_redirect:
            e = e.resolve()

        # TODO: This isn't precise enough, as some titles have slashes in them, unfortunately
        path = e.url.split("/")
        folder_path = os.path.join("site", "/".join(path[:-1]))
        if path[0] in resources_to_ignore:
            continue
        if path[0] == "resources.allsetlearning.com":
            folder_path = os.path.join("site", "/".join(path[1:-1]))
        orig_filename = path[-1]
        filename = unquote(path[-1])

        # it doesn't look like cloudflare will serve files with ? in the name
        if "css" in filename and "?" in filename:
            filename = filename.split("?")[0]
            mapped_filenames[orig_filename] = filename

        # CloudFlare automatically strips '.html', but we need
        # the file to contain it so the mimetype is correct.
        if build and e.mimetype == "text/html":
            filename = f"{filename}.html"
        os.makedirs(folder_path, exist_ok=True)
        # print(e.url, os.path.join(folder_path, filename), e.mimetype)
        if e.url.endswith("/"):
            filename = "index.html"
        if filename in too_long:
            print("!!! filename is too long, skipping", filename)
            continue
        try:
            if e.url in css_files:
                filename = to_css(e.url)
                print("@ renamed: ", filename)
            if e.mimetype.startswith("text"):
                with open(os.path.join(folder_path, filename), "w") as f:
                    content = e.read().decode("utf-8")
                    for og_fn in mapped_filenames:
                        content = content.replace(quote(og_fn), mapped_filenames[og_fn])
                    for css_file in css_files:
                        _corrected_fn = to_css(css_file)
                        _fn_in_file = quote(css_file.split('/')[2])
                        content = content.replace(_fn_in_file, _corrected_fn)
                    print(content, file=f)
            # write images as direct binary files
            else:
                with open(os.path.join(folder_path, filename), "bw") as f:
                    f.write(e.read())
        except:
            print("too long probably!", e.url)


# copy in static files
## resources index page
shutil.copy2('./static-pages/index.html', './site/chinese')
## gramwiki index page (with search & yt video added to it)
shutil.copy2('./static-pages/gramwiki-index.html', './site/gramwiki/index.html')
shutil.copy2('./static-pages/search.js', './site/gramwiki/')
## update Main_Page with yt video added to it
shutil.copy2('./static-pages/Main_Page.html', './site/chinese/grammar/Main_Page.html')
## cloudflare files
shutil.copy2('./static-pages/_redirects', './site/')
## style update (searchbox fix)
shutil.copy2('./static-pages/style.css', './site/gramwiki/skins/allset/bootstrap-store/styles.css')

# print(mapped_filenames)
# if e.url == "resources.allsetlearning.com/gramwiki/":
#     print(e.full_url)
#     e.resolve()
#     with open('main.html', 'w') as f:
#         print(e.read().decode('utf-8'), file=f)
# else:
#     print(e.full_url)
