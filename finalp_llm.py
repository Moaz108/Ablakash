# -*- coding: utf-8 -*-
import google.generativeai as genai
token="AIzaSyDoODWms5gtz32k1gH5wr2Ti1f9z7w_0xc"
genai.configure(api_key=token)
model = genai.GenerativeModel("gemini-1.5-flash")

def prompt_template(query, retrieved_context, features):
    prompt = f"""
You are an expert in furniture recommendations.
Use the following retrieved context and user features to answer the question concisely (maximum three sentences).
Retrieved furniture options:
{retrieved_context}
User features: {features}
If the user's query is to receive a recommendation, please recommend one option from the retrieved items, and ask if the user needs further help.
Also, in your final sentence, include: "if you don't like this furniture just tell me to get furniture from ikea store."
Always end with "thanks for asking!".
Question: {query}
Helpful Answer:
"""
    return prompt

def get_llm_response(conversation_history):
    prompt = "\n".join(conversation_history) + "\nAssistant:"
    response = model.generate_content(prompt)
    return response.text.strip()

def process_furniture():

  conversation_history = []

  initial_message = "Hello! Please list the furniture features you are looking for. When you are finished, type 'done' ."
  conversation_history.append("Assistant: " + initial_message)
  print("Assistant:", initial_message)

  while True:
    user_input = input("You: ").strip()
    conversation_history.append("User: " + user_input)

    if user_input.lower() == "done":
        features_list = [line.replace("User: ", "") for line in conversation_history if line.startswith("User:") and line.lower() != "done"]
        features = " ".join(features_list)

        retrieved = ['balck circle expensive sofa ','red wood sofa','blak square sofa']
        print(f"the best fit ones for are {retrieved}")
        rec_question = "Based on the features you provided, would you like me to recommend one furniture option for you? Please answer yes or no."
        conversation_history.append("Assistant: " + rec_question)
        print("\nAssistant:", rec_question)

        rec_reply = input("You: ").strip()
        conversation_history.append("User: " + rec_reply)

        if rec_reply.lower() in ["yes", "y"]:

            rec_prompt = prompt_template("Please recommend one furniture option based on my features.", retrieved, features)
            conversation_history.append("Assistant: " + rec_prompt)
            rec_response = model.generate_content(rec_prompt)
            recommendation = rec_response.text.strip()
            conversation_history.append("Assistant: " + recommendation)
            print("\nAssistant:", recommendation)
            break
        elif rec_reply.lower() in ["no", "n"]:
            fallback_msg = "Alright, if you don't like these options, just tell me to get furniture from ikea store. Thanks for asking!"
            conversation_history.append("Assistant: " + fallback_msg)
            print("\nAssistant:", fallback_msg)
            break
        else:
            print("\nAssistant: Please answer with yes or no.")
            continue
    else:
        reply = get_llm_response(conversation_history)
        conversation_history.append("Assistant: " + reply)
        print("Assistant:", reply)

  print("\n Thank you ")

def main():
    while True:
        process_furniture()
        another = input("\nWould you like to enter details for another furniture item? (yes/no): ").strip().lower()
        if another not in ["yes", "y"]:
            print("\nThank you for using the furniture recommendation system!")
            break

if __name__ == "__main__":
    main()

