from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

class Summarizer:
    def __init__(self, model_name, device):
        self.model_name = model_name
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
        self.device = device

    def generate_summary_on_device(self, src_text):
        batch = self.tokenizer.prepare_seq2seq_batch([src_text], truncation=True, padding='longest').to(
            self.device)
        generated_summary = self.tokenizer.batch_decode(self.model.generate(**batch), skip_special_tokens=True)
        del batch
        torch.cuda.empty_cache()
        return generated_summary

    def to_device(self):
        self.model.to(self.device)

    def remove(self):
        del self.model
        del self.tokenizer
