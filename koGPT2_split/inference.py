from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from util import perplexity

# inference
def generate_text(sequence, max_length, top_k=50, top_p=0.95, temperature=0.85):
    model_path = "C:/Users/USER/final-project-level3-nlp-06-main/models" # "./models"
    model = GPT2LMHeadModel.from_pretrained(model_path)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
    ids = tokenizer.encode(f'{sequence},', return_tensors='pt')
    outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        bos_token_id=model.config.bos_token_id,
        eos_token_id=model.config.eos_token_id,
        pad_token_id=model.config.pad_token_id,
        top_k=top_k, # Top-K 샘플링
        top_p=top_p, # Top-P 샘플링
        temperature=temperature, # 높을수록 다양한 결과를 내도록 함
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    ppl = perplexity(model=model, generated_sentence=outputs[0], stride=32)
    print('Perplexity : ', ppl)
    return result


def main():
    input_text = "옛날 옛적에 나무" # keyword_key[0]
    outputs = []
    
    max_len = 60
    k = 50
    p = 0.95
    temperature = 0.85
    
    # 5번 반복 -> 5개 결과 추출
    header = '=' * 15 + f'k: {k}, p:{p}, len:{max_len}, temp:{temperature}' + '=' * 15
    print(header)
        
    output = generate_text(input_text, max_len, k, p, temperature)
    outputs.append(header + '\n' + output + '\n')
    print(output)

    # Append 모드로 저장합니다. 결과 확인용!
    # 경로 설정 다시 # ./RESULT/result_{input_text}.txt'
    
    with open(f'C:/Users/USER/final-project-level3-nlp-06-main/KoGPT2/RESULT/result_{input_text}_2.txt', 'a') as f:
        for output in outputs:
            f.write(output)



    
if __name__ == "__main__":
    main()
    