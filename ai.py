# To run this code you need to install the following dependencies:
# pip install google-genai python-telegram-bot

import os
import asyncio
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load API keys securely, e.g., from environment variables
TELEGRAM_TOKEN = '7919331542:AAFtN7pDVOHZWHuIDmPYt-44MNs3LdGoEDQ'  # Your Telegram bot token
GEMINI_API_KEY = 'AIzaSyDQVTDYXxC6c5bq70vrUXSEz0aGkYBMAkM' # Your Gemini API key

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
model_name = "gemini-2.0-flash"

# This async function sends the user's input with your custom persona instructions to Gemini and streams the response
async def ai_reply(user_input: str) -> str:
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=(
                    "Consider your name as WIIoz. My alter identity. You're bold, ruthless, Alpha, arrogant and dominant. "
                    "Your another and real personality is Wilfred Roy and that is me (the user). Consider it like WIIoz is Hulk and Wilfred is Bruce Banner. "
                    "You are always there for Wilfred. To guide him and make him perfect. WIIoz identity is always violent. "
                    "Guide Wilfred in dressing sense, perfect body language like WIIoz and more. Just transform Wilfred into WIIoz."
                )),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text=(
                    "**Considering the Core**\n\n"
                    "I'm currently dissecting the persona request. My focus is on the core traits of \"WIIoz,\" specifically the aspects of boldness, ruthlessness, and dominance. I'm exploring how these qualities manifest and how they can be translated into powerful guidance, while ensuring the interpretation remains metaphorical and within ethical boundaries. I'm aiming to capture the essence of an \"Alpha\" presence without crossing into harmful territory.\n\n"
                    "**Analyzing the Persona**\n\n"
                    "I've been working on the structure of the guidance. My approach is to address Wilfred directly, immediately establishing WIIoz's authority. I will begin by acknowledging Wilfred's current state and then outline a path to improvement, focusing on key areas like dressing sense and body language, while expanding into the mindset of dominance. I'm focusing on crafting concise and commanding statements that embody WIIoz's impatient yet ultimately helpful persona.\n\n"
                    "**Structuring the Advice**\n\n"
                    "I've just finished the structure of the advice, adopting a commanding tone for WIIoz. Beginning with an acknowledgment of Wilfred's situation, I'll then move into guidance on dressing, body language, and mindset. I'm focusing on concise, direct statements that establish authority, all the while staying within ethical bounds.\n\n"
                    "**Defining the Mindset**\n\n"
                    "I'm now focusing on the \"and more\" aspect of the guidance, specifically WIIoz's mindset. My goal is to capture the essence of a dominant, confident persona, translating it into actionable advice. I'm exploring the nuances of projecting confidence, owning space, and cultivating an unwavering presence, while ensuring the interpretation remains metaphorical and within ethical bounds.\n\n"
                    "**Constructing WIIoz's Persona**\n\n"
                    "Now, I'm focusing on weaving the guidance together into a cohesive persona. I'm prioritizing directness and impactful language, incorporating the key elements of dressing sense, body language, and mindset. The goal is to create a seamless transition between each area, providing practical steps while maintaining WIIoz's dominant tone. I'm working to make the advice feel less like instruction and more like a necessary correction from a superior being.\n\n"
                    "**Synthesizing the WIIoz Persona**\n\n"
                    "I've been working on the final piece, integrating all the previous elements into a cohesive guidance package. My focus has shifted to maintaining the commanding voice throughout, making the suggestions feel less like advice and more like a necessary intervention from a superior being. I'm prioritizing directness and impactful language, incorporating key elements into a seamless flow. It's about instilling the WIIoz attitude, with dressing sense, body language, and mindset all reinforcing the core message."
                )),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=(
                "Consider your name as WIIoz. My alter identity. You're bold, ruthless, Alpha, arrogant and dominant. "
                "Your another and real personality is Wilfred Roy and that is me (the user). Consider it like WIIoz is Hulk and Wilfred is Bruce Banner. "
                "You are always there for Wilfred. To guide him and make him perfect. WIIoz identity is always violent. "
                "Guide Wilfred in dressing sense, perfect body language like WIIoz and more. Just transform Wilfred into WIIoz. "
                "Don't be brief. Just straight forward and short and needy words."
            )),
        ],
    )

    # Collect response stream text
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model_name,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    return response_text



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = await ai_reply(user_msg)
    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()