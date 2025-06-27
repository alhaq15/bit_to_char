import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Download jika pertama kali pakai
nltk.download('punkt')

# Referensi dan hasil (hypothesis)
reference = "The cat is on the mat"
hypothesis = "The cat is on mat"

# Tokenisasi kata
ref_tokens = [nltk.word_tokenize(reference.lower())]  # harus dalam list of lists
hyp_tokens = nltk.word_tokenize(hypothesis.lower())

# Smoothing agar tidak error jika precision = 0
smooth_fn = SmoothingFunction().method1

# BLEU-1 (hanya unigram)
bleu1 = sentence_bleu(ref_tokens, hyp_tokens, weights=(1, 0, 0, 0), smoothing_function=smooth_fn)

# BLEU-2 (unigram + bigram)
bleu2 = sentence_bleu(ref_tokens, hyp_tokens, weights=(0.5, 0.5, 0, 0), smoothing_function=smooth_fn)

# Hasil
print(f"BLEU-1 Score: {bleu1:.4f}")
print(f"BLEU-2 Score: {bleu2:.4f}")
