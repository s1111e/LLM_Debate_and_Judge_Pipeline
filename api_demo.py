from openai import OpenAI

client = OpenAI(
    base_url="http://10.100.1.212:8888/v1",
    api_key="utsa-08GdYYyq2lzmWc02fhfMSKzv3ACPwYgq6U02BozaaupZym1wGQzJBNC59dV4wFTi"
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "Do not output reasoning. Provide only the final answer."},
        {"role": "user", "content": "If 5 machines make 5 buttons in 5 minutes, how many minutes will 100 machines need to make 100 buttons?"},
           ],
    temperature=0.2,
    top_p=0.2,
    max_tokens=2048,
    frequency_penalty=0,
    presence_penalty=0,
)

print(response.choices[0].message.content)
