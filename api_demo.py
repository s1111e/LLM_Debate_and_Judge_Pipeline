from api_basics import query_llm


def main():
    prompt = (
        "If 5 machines make 5 buttons in 5 minutes, "
        "how many minutes will 100 machines need to make 100 buttons? "
        "Provide only the final answer."
    )

    response, tokens = query_llm(
        prompt,
        temperature=0.2,
        max_tokens=128,
        max_retries=1
    )

    print(response)
    print(f"tokens={tokens}")


if __name__ == "__main__":
    main()
