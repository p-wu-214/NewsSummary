import argparse

from config import hyper_params

import news_crawler
import torch
from summarizer import Summarizer
from postgres import PostGres

import subprocess as sp

db = PostGres()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-m', '--mode', help='Two modes [crawl] or [summarize]', action='store',
                        dest='mode', required=True, type=str)
    args = parser.parse_args()
    if args.mode == 'crawl':
        crawl()
        return
    if args.mode == 'summarize':
        summarize()
        return
    else:
        parser.print_help()

def crawl():
    articles = news_crawler.get_google_news()
    db.articles_to_db(articles)

def summarize():
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    summarized_dict = {}
    summarizer_list = []
    for model in hyper_params['pegasus_models']:
        print('creating model:', model)
        summarizer_list.append(Summarizer(model, device=torch_device))
    # some kind of system where to manage transferring in and out between cuda and cpu
    for summarizer in summarizer_list:
        count = 0
        summarizer.to_device()
        print('summarizing for:', summarizer.model_name)
        for article_id, content in db.get_articles_to_summarize():
            if article_id not in summarized_dict:
                summarized_dict[article_id] = {}
            summarized_dict[article_id][summarizer.model_name] = summarizer.generate_summary_on_device(content)
        summarizer.remove()
        del summarizer
        torch.cuda.empty_cache()
    db.summaries_to_db(summarized_dict)

def get_gpu_memory():
  _output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]

  COMMAND = "nvidia-smi --query-gpu=memory.free --format=csv"
  memory_free_info = _output_to_list(sp.check_output(COMMAND.split()))[1:]
  memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
  return memory_free_values

get_gpu_memory()

if __name__ == "__main__":
    main()
