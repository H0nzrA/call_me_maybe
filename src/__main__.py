from llm_sdk import Small_LLM_Model

def main() -> None:
    print("Call Me Maybe")
    model = Small_LLM_Model()
    prompt = "Hello world"
    input_ids = model.encode(prompt).tolist()[0]
    for _ in range(40):
        logit = model.get_logits_from_input_ids(input_ids)
        next_token = logit.index(max(logit))

        input_ids.append(next_token)

    val = model.decode(input_ids)
    print(val)

if __name__ == "__main__":
    main()
