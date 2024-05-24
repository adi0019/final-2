from flask import Flask, request, jsonify
import language_tool_python
from spellchecker import SpellChecker
from nltk import word_tokenize, sent_tokenize

app = Flask(__name__)

def grammar_and_spelling_checker(text):
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]

    spell = SpellChecker()
    tool = language_tool_python.LanguageTool('en-UK')

    spelling_errors = 0
    grammar_errors = 0
    spelling_error_messages = []
    grammar_error_messages = []
    corrected_sentences = []

    for sentence in words:
        corrected_sentence = []

        for word in sentence:
            if word not in spell:
                spelling_errors += 1
                suggestions = list(spell.candidates(word))
                spelling_error_messages.append(f"Spelling error: {word}, Suggestions: {', '.join(suggestions)}")
                corrected_sentence.append(next(iter(suggestions), word))
            else:
                corrected_sentence.append(word)

        sentence_text = ' '.join(corrected_sentence)

        matches = tool.check(sentence_text)
        grammar_errors += len(matches)

        for match in matches:
            grammar_error_messages.append(f"Grammar error: {match.ruleId} - {match.message}")

        corrected_sentences.append(sentence_text)

    accuracy = calculate_accuracy(text, ' '.join(corrected_sentences))

    return {
        "spelling_errors_count": spelling_errors,
        "grammar_errors_count": grammar_errors,
        "spelling_error_messages": spelling_error_messages,
        "grammar_error_messages": grammar_error_messages,
        "accuracy": accuracy
    }

def calculate_accuracy(original_text, corrected_text):
    original_tokens = word_tokenize(original_text)
    corrected_tokens = word_tokenize(corrected_text)
    correct_count = sum(1 for orig, corr in zip(original_tokens, corrected_tokens) if orig == corr)
    accuracy = (correct_count / len(original_tokens)) * 100
    return accuracy

def count_words(text):
    words = word_tokenize(text)
    return len(words)

@app.route('/', methods=['POST'])
def check_text():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = grammar_and_spelling_checker(text)
    return jsonify(result)

@app.route('/wordcount', methods=['POST'])
def word_count():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    word_count = count_words(text)
    return jsonify({"word_count": word_count})

if __name__ == "__main__":
    app.run(debug=True)




