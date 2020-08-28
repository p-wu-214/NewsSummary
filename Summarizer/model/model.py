from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
src_text = [
    """
     (CNN)White House Coronavirus Task Force member Dr. Anthony Fauci said he was undergoing surgery and not part of the discussion during the August 20 task force meeting when updated US Centers for Disease Control and Prevention guidelines were discussed.
"I was under general anesthesia in the operating room and was not part of any discussion or deliberation regarding the new testing recommendations," Fauci, director of the National Institute of Allergy and Infectious Diseases, told CNN Chief Medical Correspondent Dr. Sanjay Gupta.
"I am concerned about the interpretation of these recommendations and worried it will give people the incorrect assumption that asymptomatic spread is not of great concern. In fact it is," he added.
CDC was pressured &#39;from the top down&#39; to change coronavirus testing guidance, official says
CDC was pressured 'from the top down' to change coronavirus testing guidance, official says
Fauci had surgery on Thursday morning to remove a polyp on his vocal cord. He had general anesthesia and doctors advised him to curtail his talking for a while to allow his vocal cords to recover.

The updated guidelines were released on Monday. Previous CDC testing guidance said anyone who had close contact with someone with coronavirus should get tested, whether they have symptoms or not.
The site was changed to say: "If you have been in close contact (within 6 feet) of a person with a COVID-19 infection for at least 15 minutes but do not have symptoms, you do not necessarily need a test unless you are a vulnerable individual or your health care provider or State or local public health officials recommend you take one."
Covid-19 child cases in the US have increased by 21% since early August, new data shows
Covid-19 child cases in the US have increased by 21% since early August, new data shows
A senior federal health official close to the process told CNN on Wednesday the changes came as a result of pressure from the Trump administration. "It's coming from the top down," the source said.
US Health and Human Services Assistant Secretary Dr. Brett Giroir said during a phone call with reporters on Wednesday that the updated CDC guidance on Covid-19 testing was last discussed and approved by task force members last Thursday.
Giroir said in the call that the updated testing guidelines originated from within the CDC and were written by multiple authors, adding that he, Fauci, Dr. Deborah Birx and Dr. Stephen Hahn worked on them.

"The new guidelines are a CDC action. As always, guidelines received appropriate attention, consultation and input from task force experts, and I mean the medical and scientific experts," Giroir said, also mentioning CDC Director Dr. Robert Redfield. "All the task force experts advise on coronavirus-related matters."
    """
]

result = {}

model_name = 'google/pegasus-gigaword'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
translated = model.generate(**batch)
tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
result['gigaword'] = tgt_text[0]

# model_name = 'google/pegasus-xsum'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# result['xsum'] = tgt_text[0]
#
# model_name = 'google/pegasus-multi_news'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# result['multi_news'] = tgt_text[0]
#
# model_name = 'google/pegasus-newsroom'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# result['newsroom'] = tgt_text[0]
#
# model_name = 'google/pegasus-cnn_dailymail'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# result['cnn_dailymail'] = tgt_text[0]
#
# model_name = 'google/pegasus-large'
# torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
# batch = tokenizer.prepare_seq2seq_batch(src_text, truncation=True, padding='longest').to(torch_device)
# translated = model.generate(**batch)
# tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
# result['large'] = tgt_text[0]

print(result)