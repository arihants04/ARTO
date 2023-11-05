import replicate

output = replicate.run(
  "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
  input={
    "top_k": 50,
    "top_p": 1,
    "prompt": "Will Meta value go up or down? The current consumer sentiment is positive, a regression model is predicting an increase, and it closed at 435 today",
    "temperature": 0.75,
    "system_prompt": "You answer the prompt without any greetings.You answer in short replies of 2 to 3 sentences",
    "max_new_tokens": 800,
    "min_new_tokens": -1,
    "repetition_penalty": 1
  }
)
bruh = ""

for i in output:
    bruh += (i)

print(bruh)
