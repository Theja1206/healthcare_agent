from agents.main_agent import MultiFunctionAgent
from rich import print

def main():
    agent = MultiFunctionAgent()
    print("[bold green] Multi -Function AI Agent started..![/bold green]")
    print("Type 'Exit' to Stop \n")

    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == 'Exit':
    #         print("Agent stopped")
    #         break
    #     response = agent.process_query(user_input)
    #     print(f"[bold blue] Agent :[/bold blue] {response} \n")
    while True:
        user_input = input("You: ")

    # Proper exit condition
        if user_input.strip().lower() == "exit":
            print("[bold red]Agent stopped[/bold red]")
            break

        response = agent.process_query(user_input)
        print(f"[bold blue]Agent:[/bold blue] {response}\n")

        
if __name__ == "__main__":
    main()
