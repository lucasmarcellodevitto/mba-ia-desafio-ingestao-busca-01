from search import Search

def main():
    print("Starting Chat...")
    search = Search()
    
    print("Ask your question. Type 'exit' or press Ctrl+C to quit.")

    while True:
        try:
            question = input("\nAsk your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEnding chat!")
            break

        if not question:
            continue

        if question.lower() in ("exit"):
            print("Chat closed!")
            break

        try:
            response = search.answer(question)
            print(f"Here is your answer: {response}\n")
        except Exception as e:
            print(f"An unexpected error occurred. Try again: {e}")


if __name__ == "__main__":
    main()