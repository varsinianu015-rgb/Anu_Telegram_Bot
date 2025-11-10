import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings

import asyncio
import nest_asyncio

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# 1. LLM setup
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)

# 2. Prompt + chain
prompt = PromptTemplate.from_template("Answer Clearly: {question}")
qa_chain = LLMChain(llm=llm, prompt=prompt)

# 3. Load sample document
loader = TextLoader("sample.txt")
documents = loader.load()

# 4. Embeddings + FAISS
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = FAISS.from_documents(documents, embedding)
retriever = vectordb.as_retriever()

# 5. RAG chain
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 6. Tools
search_tool = Tool(
    name="Web Search",
    func=lambda x: "Web search disabled in this demo.",
    description="Search the internet for additional information"
)

tools = [
    Tool(name="Simple QA", func=qa_chain.run, description="Answer with basic LLMChain"),
    Tool(name="RAG Search", func=rag_chain.run, description="Answer using document retrieval"),
    search_tool
]

# 7. Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 8. Agent setup
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# === Telegram Bot Logic ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your AI Assistant 🤖. Ask me anything!")
# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Help Menu*\n\n"
        "• `/ask <query>` — Ask anything using AI or your document.\n"
        "• `/image` — Send an image next, I’ll describe it for you.\n"
        "• `/help` — Show this help message.",
        parse_mode="Markdown"
    )

# /ask
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("⚠️ Please provide a question.\nExample: `/ask What is in sample.txt?`", parse_mode="Markdown")
        return
    await update.message.reply_text("🤔 Thinking...")
    try:
        response = agent.run(query)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("❌ Sorry, something went wrong. Try again later.")

# /image command
image_mode = {}

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    image_mode[user_id] = True
    await update.message.reply_text("📷 Please send me an image to describe it.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"\nUser: {user_text}")

    try:
        response = agent.run(user_text)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

# Main entry
def main():
    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("image", image_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
