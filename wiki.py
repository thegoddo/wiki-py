"""
This script let's you access wikipedia from your terminal with the help of wikipedia api library.
"""

import argparse
import wikipedia
from colorama import Fore, Style, init

init(autoreset=True)


def get_summary(name):
    """
    Fetch and print a formatted, colored Wikipedia summary for a given topic.

    Parameters
    ----------
    name : str
        The search term or page title to look up on Wikipedia.

    Returns
    -------
    None
        This function prints output to standard output and does not return a value.

    Behavior
    --------
    - Uses wikipedia.summary(name, sentences=5) to retrieve up to five sentences of summary text.
    - Prints a colored header, the topic name (capitalized),
        and the retrieved summary using colorama Fore and Style constants.
    - On successful fetch, prints the summary;
        on failure, prints a user-friendly error or disambiguation message.

    Error handling
    --------------
    - wikipedia.exceptions.PageError:
        If no page is found for the given name,
        the function prints an error message indicating the page was not found.
    - wikipedia.exceptions.DisambiguationError:
        If the query is ambiguous,
        the function prints a disambiguation notice and suggests a few possible options
        (uses e.options[:5]).

    Side effects
    ------------
    - Produces console output with colored formatting
        (relies on colorama constants like Fore and Style).
    - Does not raise the handled wikipedia exceptions to the caller;
        they are caught and reported via printed messages.

    Notes
    -----
    - The function assumes the wikipedia and colorama modules are
        available and that colorama has been initialized if needed.
    - Example usage: get_summary("Python (programming language)")
    """

    try:
        text = wikipedia.summary(name, sentences=5)
        print(f"\n{Fore.CYAN}{'='*50}")
        print(
            f"{Fore.CYAN}  ✨ Wikipedia Summary for: {Fore.YELLOW}{name.capitalize()}{Fore.CYAN} ✨"
        )
        print(f"{Fore.CYAN}{'='*50}\n")
        print(f"{Fore.WHITE}{text}")
        print(Style.RESET_ALL)
    except wikipedia.exceptions.PageError:
        print(
            f"\n{Fore.RED}Error: Page '{name}' not found on Wikipedia.{Style.RESET_ALL}"
        )
    except wikipedia.exceptions.DisambiguationError as e:
        print(
            f"\n{Fore.YELLOW}Disambiguation: '{name}' may refer to multiple topics. Please be more specific.{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}Did you mean one of these? {', '.join(e.options[:5])}{Style.RESET_ALL}"
        )


def get_full_content(name):
    """
    Fetches and displays the full content of a Wikipedia page for the given name.

    Args:
        name (str): The title of the Wikipedia page to retrieve.

    Behavior:
        - Prints the full content of the specified Wikipedia page with formatted output.
        - Handles cases where the page does not exist or is ambiguous:
            - If the page is not found, prints an error message.
            - If the page title is ambiguous, prints a disambiguation message and suggests possible options.

    Exceptions:
        wikipedia.exceptions.PageError: Raised if the page does not exist.
        wikipedia.exceptions.DisambiguationError: Raised if the page title is ambiguous.
    """

    try:
        page = wikipedia.page(name)
        print(f"\n{Fore.MAGENTA}{'='*50}")
        print(
            f"{Fore.MAGENTA}  📚 Full Content for: {Fore.WHITE}{page.title}{Fore.MAGENTA} 📚"
        )
        print(f"{Fore.MAGENTA}{'='*50}\n")
        print(f"{Fore.WHITE}{page.content}")
        print(Style.RESET_ALL)
    except wikipedia.exceptions.PageError:
        print(
            f"\n{Fore.RED}Error: Page '{name}' not found on Wikipedia.{Style.RESET_ALL}"
        )
    except wikipedia.exceptions.DisambiguationError as e:
        print(
            f"\n{Fore.YELLOW}Disambiguation: '{name}' may refer to multiple topics. Please be more specific.{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}Did you mean one of these? {', '.join(e.options[:5])}{Style.RESET_ALL}"
        )


def get_results(query):
    """
    Searches Wikipedia for the given query and prints the top 5 results.

    Args:
        query (str): The search term to query Wikipedia.

    Behavior:
        - Prints a formatted list of up to 5 search results if found.
        - If no results are found, prints a message indicating so.
        - Handles Wikipedia-related exceptions and prints an error message if an exception occurs.

    Note:
        Requires the `wikipedia` library and color formatting via `colorama` (Fore, Style).
    """
    try:
        results = wikipedia.search(query, results=5)
        if results:
            print(f"\n{Fore.BLUE}{'='*50}")
            print(
                f"{Fore.BLUE}  🔍 Search results for: {Fore.WHITE}{query.capitalize()}{Fore.BLUE} 🔍"
            )
            print(f"{Fore.BLUE}{'='*50}\n")
            for result in results:
                print(f"{Fore.GREEN}--- {result}{Style.RESET_ALL}")
        else:
            print(
                f"\n{Fore.YELLOW}No results found for '{query}'.{Style.RESET_ALL}")
    except wikipedia.exceptions.WikipediaException as e:
        print(f"\n{Fore.RED}An error occurred during search: {e}{Style.RESET_ALL}")


def main():
    """
    Parses command-line arguments and executes Wikipedia search or summary retrieval.

    This function sets up an argument parser for a Wikipedia tool that allows users to:
    - Search for Wikipedia articles by subject.
    - Retrieve a summary or the full content of a specific Wikipedia article.
    - Specify the language of the Wikipedia content.

    Arguments:
        -l, --lang: Language code for Wikipedia (default: 'en').
        -f, --full: Flag to retrieve the full article content (must be used with -n/--name).
        -s, --search: Subject to search for on Wikipedia (mutually exclusive with -n).
        -n, --name: Name of the Wikipedia article to retrieve (mutually exclusive with -s).

    Handles invalid language codes by defaulting to English and provides user-friendly error messages.
    """
    parser = argparse.ArgumentParser(
        description="A Wikipedia search and summary tool with colorful output and language support.",
        epilog="Examples: \n  python wiki_tool.py -n 'Python' -l 'en'\n  python wiki_tool.py -n 'Python' --full\n  python wiki_tool.py -s 'science' -l 'es'",
    )

    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="en",
        help="Specify the language code (e.g., 'en', 'es', 'de'). Defaults to 'en'.",
    )
    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="Get the full content of the article instead of just a summary. Must be used with -n/--name.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s", "--search", type=str, help="Search for a subject on Wikipedia."
    )
    group.add_argument(
        "-n", "--name", type=str, help="Get a summary for a specific topic."
    )

    args = parser.parse_args()

    try:
        wikipedia.set_lang(args.lang)
    except ValueError:
        print(
            f"\n{Fore.RED}Error: The language code '{args.lang}' is not supported. Using English ('en') instead.{Style.RESET_ALL}"
        )
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
            f"\n{Fore.RED}Error: The '--full' flag must be used with a topic name using '-n'.{Style.RESET_ALL}"
        )
        parser.print_help()


if __name__ == "__main__":
    main()
