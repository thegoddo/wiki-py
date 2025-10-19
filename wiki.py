import wikipedia
import argparse
from colorama import Fore, Style, init

init(autoreset=True)


def get_summary(name):
    try:
        text = wikipedia.summary(name, sentences=5)
        print(f"\n{Fore.CYAN}{'='*50}")
        print(
            f"{Fore.CYAN}  ✨ Wikipedia Summary for: {Fore.YELLOW}{name.capitalize()}{Fore.CYAN} ✨")
        print(f"{Fore.CYAN}{'='*50}\n")
        print(f"{Fore.WHITE}{text}")
        print(Style.RESET_ALL)
    except wikipedia.exceptions.PageError:
        print(
            f"\n{Fore.RED}Error: Page '{name}' not found on Wikipedia.{Style.RESET_ALL}")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"\n{Fore.YELLOW}Disambiguation: '{name}' may refer to multiple topics. Please be more specific.{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Did you mean one of these? {', '.join(e.options[:5])}{Style.RESET_ALL}")


def get_full_content(name):
    try:
        page = wikipedia.page(name)
        print(f"\n{Fore.MAGENTA}{'='*50}")
        print(
            f"{Fore.MAGENTA}  📚 Full Content for: {Fore.WHITE}{page.title}{Fore.MAGENTA} 📚")
        print(f"{Fore.MAGENTA}{'='*50}\n")
        print(f"{Fore.WHITE}{page.content}")
        print(Style.RESET_ALL)
    except wikipedia.exceptions.PageError:
        print(
            f"\n{Fore.RED}Error: Page '{name}' not found on Wikipedia.{Style.RESET_ALL}")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"\n{Fore.YELLOW}Disambiguation: '{name}' may refer to multiple topics. Please be more specific.{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Did you mean one of these? {', '.join(e.options[:5])}{Style.RESET_ALL}")


def get_results(query):
    try:
        results = wikipedia.search(query, results=5)
        if results:
            print(f"\n{Fore.BLUE}{'='*50}")
            print(
                f"{Fore.BLUE}  🔍 Search results for: {Fore.WHITE}{query.capitalize()}{Fore.BLUE} 🔍")
            print(f"{Fore.BLUE}{'='*50}\n")
            for result in results:
                print(f"{Fore.GREEN}--- {result}{Style.RESET_ALL}")
        else:
            print(
                f"\n{Fore.YELLOW}No results found for '{query}'.{Style.RESET_ALL}")
    except wikipedia.exceptions.WikipediaException as e:
        print(f"\n{Fore.RED}An error occurred during search: {e}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="A Wikipedia search and summary tool with colorful output and language support.",
        epilog="Examples: \n  python wiki_tool.py -n 'Python' -l 'en'\n  python wiki_tool.py -n 'Python' --full\n  python wiki_tool.py -s 'science' -l 'es'"
    )

    parser.add_argument("-l", "--lang", type=str, default="en",
                        help="Specify the language code (e.g., 'en', 'es', 'de'). Defaults to 'en'.")
    parser.add_argument("-f", "--full", action="store_true",
                        help="Get the full content of the article instead of just a summary. Must be used with -n/--name.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--search", type=str,
                       help="Search for a subject on Wikipedia.")
    group.add_argument("-n", "--name", type=str,
                       help="Get a summary for a specific topic.")

    args = parser.parse_args()

    try:
        wikipedia.set_lang(args.lang)
    except Exception:
        print(f"\n{Fore.RED}Error: The language code '{args.lang}' is not supported. Using English ('en') instead.{Style.RESET_ALL}")
        wikipedia.set_lang("en")

    if args.name:
        if args.full:
            get_full_content(args.name)
        else:
            get_summary(args.name)
    elif args.search:
        get_results(args.search)
    elif args.full:
        print(
            f"\n{Fore.RED}Error: The '--full' flag must be used with a topic name using '-n'.{Style.RESET_ALL}")
        parser.print_help()


if __name__ == "__main__":
    main()
