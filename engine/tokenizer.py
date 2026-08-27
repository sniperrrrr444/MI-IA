class TokenizerAdapter:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def encode(self, text):
        return self.tokenizer.encode(text, add_special_tokens=True)

    def decode(self, tokens):
        return self.tokenizer.decode(tokens, skip_special_tokens=True)
