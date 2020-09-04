from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch


class Summarizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print('training on', self.torch_device)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name).to(self.torch_device)
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)

    def generate_summary(self, src_text):
        batch = self.tokenizer.prepare_seq2seq_batch([src_text], truncation=True, padding='longest').to(
            self.torch_device)
        generated_summary = self.tokenizer.batch_decode(self.model.generate(**batch), skip_special_tokens=True)
        return generated_summary


# src_text = [
#     """
#      (CNN)White House Coronavirus Task Force member Dr. Anthony Fauci said he was undergoing surgery and not part of the discussion during the August 20 task force meeting when updated US Centers for Disease Control and Prevention guidelines were discussed.
# "I was under general anesthesia in the operating room and was not part of any discussion or deliberation regarding the new testing recommendations," Fauci, director of the National Institute of Allergy and Infectious Diseases, told CNN Chief Medical Correspondent Dr. Sanjay Gupta.
# "I am concerned about the interpretation of these recommendations and worried it will give people the incorrect assumption that asymptomatic spread is not of great concern. In fact it is," he added.
# CDC was pressured &#39;from the top down&#39; to change coronavirus testing guidance, official says
# CDC was pressured 'from the top down' to change coronavirus testing guidance, official says
# Fauci had surgery on Thursday morning to remove a polyp on his vocal cord. He had general anesthesia and doctors advised him to curtail his talking for a while to allow his vocal cords to recover.
#
# The updated guidelines were released on Monday. Previous CDC testing guidance said anyone who had close contact with someone with coronavirus should get tested, whether they have symptoms or not.
# The site was changed to say: "If you have been in close contact (within 6 feet) of a person with a COVID-19 infection for at least 15 minutes but do not have symptoms, you do not necessarily need a test unless you are a vulnerable individual or your health care provider or State or local public health officials recommend you take one."
# Covid-19 child cases in the US have increased by 21% since early August, new data shows
# Covid-19 child cases in the US have increased by 21% since early August, new data shows
# A senior federal health official close to the process told CNN on Wednesday the changes came as a result of pressure from the Trump administration. "It's coming from the top down," the source said.
# US Health and Human Services Assistant Secretary Dr. Brett Giroir said during a phone call with reporters on Wednesday that the updated CDC guidance on Covid-19 testing was last discussed and approved by task force members last Thursday.
# Giroir said in the call that the updated testing guidelines originated from within the CDC and were written by multiple authors, adding that he, Fauci, Dr. Deborah Birx and Dr. Stephen Hahn worked on them.
#
# "The new guidelines are a CDC action. As always, guidelines received appropriate attention, consultation and input from task force experts, and I mean the medical and scientific experts," Giroir said, also mentioning CDC Director Dr. Robert Redfield. "All the task force experts advise on coronavirus-related matters."
#     """
# ]
#
# if __name__ == "__main__":
#     summarizer = Summarizer()
#     generated_summaries = summarizer.generate_summary(src_text)
#     print(generated_summaries)
