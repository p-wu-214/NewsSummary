# NewsSummary

This repository contains code for crawling out daily news article from Google News and generating a summary of the news article. The system will generate a summary for each pretrained model defined inside of config.py. Pretrained models retrieved from huggingface/transformers. News metadata, article and summary are stored inside a database.

# Basic Usage

```
main.py --mode crawl to crawl for article content from Google News and store into database
main.py --mode summarze to generate article summary using pretrained pegasus models defined in config.py
```
# License
License
See the LICENSE file for license rights and limitations (MIT).
