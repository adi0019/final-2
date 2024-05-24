import language_tool_python
from spellchecker import SpellChecker
from nltk import word_tokenize, sent_tokenize

def grammar_and_spelling_checker(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]

    # Initialize spellchecker for spelling checking
    spell = SpellChecker()

    # Initialize language_tool_python for grammar checking
    tool = language_tool_python.LanguageTool('en-UK')

    spelling_errors = 0
    grammar_errors = 0
    spelling_error_messages = []
    grammar_error_messages = []
    corrected_sentences = []

    # Check grammar and spelling for each word
    for sentence in words:
        corrected_sentence = []

        for word in sentence:
            # Check for spelling errors
            if word not in spell:
                spelling_errors += 1
                suggestions = list(spell.candidates(word))
                spelling_error_messages.append(f"Spelling error: {word}, Suggestions: {', '.join(suggestions)}")
                
                # Use the first suggestion if available, otherwise keep the original word
                corrected_sentence.append(next(iter(suggestions), word))
            else:
                corrected_sentence.append(word)

        # Join the words back into a sentence for grammar checking
        sentence_text = ' '.join(corrected_sentence)

        # Check for grammar errors
        matches = tool.check(sentence_text)
        grammar_errors += len(matches)

        for match in matches:
            grammar_error_messages.append(f"Grammar error: {match.ruleId} - {match.message}")

        # Append the corrected sentence
        corrected_sentences.append(sentence_text)

    # Calculate accuracy
    accuracy = calculate_accuracy(text, ' '.join(corrected_sentences))

    return spelling_errors, grammar_errors, spelling_error_messages, grammar_error_messages, accuracy

def calculate_accuracy(original_text, corrected_text):
    original_tokens = word_tokenize(original_text)
    corrected_tokens = word_tokenize(corrected_text)
    correct_count = sum(1 for orig, corr in zip(original_tokens, corrected_tokens) if orig == corr)
    accuracy = (correct_count / len(original_tokens)) * 100
    return accuracy

def count_words(text):
    words = word_tokenize(text)
    return len(words)

if __name__ == "__main__":
    while True:
        # Get user input
        user_input = input("Enter the text you want to check (or 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        # Run the grammar and spelling checker
        spelling_errors, grammar_errors, spelling_error_messages, grammar_error_messages, accuracy = grammar_and_spelling_checker(user_input)

        # Print the errors and counts
        if spelling_error_messages or grammar_error_messages:
            print(f"Spelling errors found: {spelling_errors}")
            if spelling_error_messages:
                print("Spelling Error messages:")
                for error in spelling_error_messages:
                    print(error)

            print(f"Grammar errors found: {grammar_errors}")
            if grammar_error_messages:
                print("Grammar Error messages:")
                for error in grammar_error_messages:
                    print(error)
        else:
            print("No errors found.")

        # Print accuracy
        print(f"Accuracy: {accuracy:.2f}%")

        # Print word count
        print(f"Word count: {count_words(user_input)}")

