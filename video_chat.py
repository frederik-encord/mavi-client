from mavi_client import MaviClient, ChatHistoryItem
from dotenv import load_dotenv
import typer
from typing import List, Optional
import json
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from utils import select_videos

console = Console()


def format_chat_history(history: List[ChatHistoryItem]) -> str:
    """Format chat history for display"""
    output = ""
    for item in history:
        output += f"User: {item.user}\n"
        output += f"Assistant: {item.robot}\n\n"
    return output


def save_history(history: List[dict], filename: str):
    """Save chat history to a file"""
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)


def load_history(filename: str) -> List[dict]:
    """Load chat history from a file"""
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)


def main(
    history_file: Optional[str] = typer.Option(
        None, help="File to save/load chat history"
    ),
    stream: bool = typer.Option(False, help="Stream the response"),
):
    """
    Chat with an AI assistant about specific videos.

    Example:
    python video_chat.py video123 video456
    """
    client = MaviClient()

    # Load history if file is provided
    history = []
    if history_file and os.path.exists(history_file):
        try:
            raw_history = load_history(history_file)
            history = [ChatHistoryItem(**item) for item in raw_history]
            console.print(f"Loaded chat history from {history_file}")
            console.print(Markdown(format_chat_history(history)))
        except Exception as e:
            console.print(f"Error loading history: {e}", style="bold red")

    video_nos = select_videos(client)
    console.print(f"Chatting about videos: {', '.join(video_nos)}", style="bold green")
    console.print("Type 'exit' or 'quit' to end the conversation.", style="bold yellow")

    chat_history: List[ChatHistoryItem] = []

    while True:
        # Get user input
        user_message = Prompt.ask("\n[bold blue]You[/bold blue]")

        # Check if user wants to exit
        if user_message.lower() in ["exit", "quit"]:
            if history_file and chat_history:
                save_history([h.model_dump() for h in chat_history], history_file)
                console.print(
                    f"Chat history saved to {history_file}", style="bold green"
                )
            break

        raw_response = client.video_chat(
            video_nos=video_nos,
            message=user_message,
            history=chat_history,
            stream=False,
        )

        ai_message = raw_response.data.msg
        console.print(f"\n[bold green]Assistant[/bold green]: {ai_message}")
        chat_history.append(ChatHistoryItem(user=user_message, robot=ai_message))


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
