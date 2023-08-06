from flask import Flask, render_template, request,jsonify
from transformers import MarianMTModel, MarianTokenizer
import pickle
import re
import torch
from fairseq.models.transformer import TransformerModel
from fairseq.data.encoders import register_bpe


app = Flask(__name__)


class SentencePieceBPE(object):
    def __init__(self, args):
        import sentencepiece as spm
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(args.spm_model_path)

    def encode(self, x: str) -> str:
        return self.sp.EncodeAsPieces(x)

    def decode(self, x: str) -> str:
        return self.sp.DecodePieces(x)


    # Register SentencePieceBPE as BPE for Fairseq
register_bpe("sentencepiece", SentencePieceBPE)

@app.route('/')
def index():
    return render_template('translation.html')


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    # Get the text to be translated from the request
    text = request.args.get('text')


    with open('model.pckl', 'rb') as f:
        langdetect_Model = pickle.load(f)

    # Clean Function
    def clean_text(text):
       
        # Separate camel case words
        text = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)
    
        # Converting the text to lower case
        text = text.lower()
        
        # Removing the symbols and numbers
        text = re.sub(r'[\([{})\]!@#$,’&-_/،"%^*?؟:;~`0-9\.\\\u064B-\u065F\u0670]', ' ', text)
                
        # Removing URLs
        text = re.sub('http\S+\s*', ' ', text)
    
        # Removing RT and cc
        text = re.sub(r'\bRT\b|\bcc\b', ' ', text)
    
        # Removing hashtags
        text = re.sub('#\S+', '', text)
    
        # Removing mentions
        text = re.sub('@\S+', '  ', text)
    
        # Removing extra whitespace
        text = re.sub('\s+', ' ', text)
    
        return text

    source_language = ""
    target_language = ""
    input_text_clean = clean_text(text)     
    # Check if the cleaned input is valid
    if not re.match('^[A-Za-z\s]+$', input_text_clean) and not re.match('^[\u0621-\u064A\s]+$', input_text_clean):
        source_language = "The input must be a text in English or Arabic."
        translated_text = ""
    elif re.search(r'(.)\1{3,}', input_text_clean):
        source_language = "Wrong input."
        translated_text = ""
    else:
        predictions = langdetect_Model.predict([input_text_clean])
        predictions_plain = [p[:] for p in predictions]
        if "Arabic" in predictions_plain or "English" in predictions_plain:
            source_language = (", ".join(predictions_plain)) # Display the predicted languages as a comma-separated string
            if source_language == "English" :
                target_language = "Arabic"
                # Load the Fairseq trained model
                model_path = "en-ar-model"
                model = TransformerModel.from_pretrained(
                    model_path,
                    checkpoint_file="checkpoint_best.pt",
                    data_name_or_path="en-ar-model",
                    source_lang="en",  # Specify the source language code
                    target_lang="ar",  # Specify the target language code
                    bpe="sentencepiece",  # Use SentencePiece BPE
                    sentencepiece_vocab="ar-en.32kspm.vocab",  # Path to SentencePiece vocabulary
                    spm_model_path="ar-en.32kspm.model",  # Path to SentencePiece model
                    sentencepiece_model="ar-en.32kspm.model",  # Path to SentencePiece model
                )

                model.eval()
                # Tokenize the input sentence
                tokens = model.encode(text)

                # Convert the tokens to PyTorch tensor
                input_tensor = torch.LongTensor(tokens).unsqueeze(0)  # Add batch dimension

                # Generate translation using the model
                with torch.no_grad():
                    translation = model.generate(input_tensor, beam=5)

                # Get the translated sentence without special tokens
                translated_text = model.decode(translation[0][0]["tokens"])

            else :
                target_language = "English"
                # Perform translation logic here
                src_text = [text]
                model_name = 'huggingface' #model path
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
                translatedtext = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
                translated_text = translatedtext[0].replace('"', '')                           
            
        else:
            source_language = ("The input must be a text in English or Arabic.")
            translated_text = "Please enter a valid input"
         

        # Return the translated text as a response
    return {'source_language': source_language, 'target_language': target_language, 'translated_text': translated_text}


   




if __name__ == '__main__':
    app.run(debug=True)

