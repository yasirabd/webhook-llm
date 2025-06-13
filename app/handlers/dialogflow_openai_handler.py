from fastapi import Request
from fastapi.responses import JSONResponse
from app.services.openai_client import generate_chat_reply
from app.utils.conversation import init_messages

messages = init_messages()

async def handle_dialogflow(request: Request):
    req = await request.json()
    query_result = req.get("queryResult", {})
    action = query_result.get("action")
    query = query_result.get("queryText")

    if action == "input.unknown":
        messages.append({"role": "user", "content": query})
        response = generate_chat_reply(messages)
        reply = response["choices"][0]["message"]["content"].strip()
        messages.append({"role": "assistant", "content": reply})

        print("Percakapan sejauh ini:")
        for m in messages:
            print(f"{m['role']}: {m['content']}")
        
        return JSONResponse({"fulfillmentText": reply, "source": "openai"})

    if action == "input.welcome":
        messages.clear()
        messages.extend(init_messages())
        welcome_msg = "Hai! Saya Robosemar, dokter virtual kamu. Ada keluhan yang ingin disampaikan?"
        messages.append({"role": "assistant", "content": welcome_msg})
        return JSONResponse({"fulfillmentText": welcome_msg, "source": "openai"})

    return JSONResponse({"fulfillmentText": "Tidak bisa memproses permintaan."})