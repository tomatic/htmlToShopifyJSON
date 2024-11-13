# htmlToShopifyJSON

This script converts HTML to JSON for Shopify rich text metafields.

The file `test.html` contains example HTML code with all tags currently supported by the RTE in the theme editor:

- h1 - h6
- p
- ul, ol and li
- a
- strong
- em

The script works for the test.html file but hasn't been tested for all possible combinations, syntax variations, tag attributes, etc. But since BeautifulSoup is doing the parsing, it should handle most tags.
