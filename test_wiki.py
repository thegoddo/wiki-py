"""
Test module to test the wki.py file and it's methods
"""
import sys
from unittest.mock import patch
import pytest
from wiki import get_summary, get_full_content, get_results, main


class MockPage:
    def __init__(self, title, content):
        self.title = title
        self.content = content


@pytest.fixture(autouse=True)
def mock_wikipedia():
    with patch("wikipedia.summary") as mock_summary, \
            patch("wikipedia.page") as mock_page, \
            patch("wikipedia.search") as mock_search, \
            patch("wikipedia.set_lang") as mock_set_lang:

        mock_page.return_value = MockPage(
            title="Test Page", content="This is the full content of the test page.")

        yield {
            "summary": mock_summary,
            "page": mock_page,
            "search": mock_search,
            "set_lang": mock_set_lang
        }


def test_get_summary_success(capsys, mock_wikipedia):
    mock_wikipedia["summary"].return_value = "This is a summary of the test page."
    get_summary("Test_Page")
    captured = capsys.readouterr()
    assert "Wikipedia Summary" in captured.out
    assert "This is a summary of the test page." in captured.out


def test_get_summary_page_error(capsys, mock_wikipedia):
    from wikipedia.exceptions import PageError
    mock_wikipedia["summary"].side_effect = PageError("Test_Page")
    get_summary("Non_Existent_Page")
    captured = capsys.readouterr()
    assert "Error: Page 'Non_Existent_Page' not found on Wikipedia." in captured.out


def test_get_summary_disambiguation_error(capsys, mock_wikipedia):
    from wikipedia.exceptions import DisambiguationError
    # DisambiguationError expects the second positional argument (may_refer_to)
    # to be a list of possible options; pass it positionally instead of using
    # the unsupported 'options' keyword.
    mock_wikipedia["summary"].side_effect = DisambiguationError(
        "Test_Page", ["Option A", "Option B"])
    get_summary("Test_Page")
    captured = capsys.readouterr()
    assert "Disambiguation: 'Test_Page' may refer to multiple topics." in captured.out
    assert "Did you mean one of these? Option A, Option B" in captured.out


def test_get_full_content_success(capsys, mock_wikipedia):
    get_full_content("Test_Page")
    captured = capsys.readouterr()
    assert "Full Content for: Test Page" in captured.out
    assert "This is the full content of the test page." in captured.out


def test_get_full_content_page_error(capsys, mock_wikipedia):
    from wikipedia.exceptions import PageError
    mock_wikipedia["page"].side_effect = PageError("Test_Page")
    get_full_content("Non_Existent_Page")
    captured = capsys.readouterr()
    assert "Error: Page 'Non_Existent_Page' not found on Wikipedia." in captured.out


def test_get_results_success(capsys, mock_wikipedia):
    mock_wikipedia["search"].return_value = ["Result 1", "Result 2"]
    get_results("Test Query")
    captured = capsys.readouterr()
    assert "Search results for: Test Query" in captured.out
    assert "--- Result 1" in captured.out
    assert "--- Result 2" in captured.out


def test_get_results_no_results(capsys, mock_wikipedia):
    mock_wikipedia["search"].return_value = []
    get_results("No Results Found")
    captured = capsys.readouterr()
    assert "No results found for 'No Results Found'." in captured.out


def test_main_summary(capsys, mock_wikipedia):
    sys.argv = ["project.py", "-n", "Python"]
    mock_wikipedia["summary"].return_value = "Python is a programming language."
    main()
    captured = capsys.readouterr()
    assert "Wikipedia Summary for: Python" in captured.out
    assert "Python is a programming language." in captured.out
    mock_wikipedia["summary"].assert_called_with("Python", sentences=5)


def test_main_full_content(capsys, mock_wikipedia):
    sys.argv = ["project.py", "-n", "Python", "--full"]
    mock_wikipedia["page"].return_value = MockPage(
        title="Python", content="Python is a popular programming language.")
    main()
    captured = capsys.readouterr()
    assert "Full Content for: Python" in captured.out
    assert "Python is a popular programming language." in captured.out
    mock_wikipedia["page"].assert_called_with("Python")


def test_main_search(capsys, mock_wikipedia):
    sys.argv = ["project.py", "-s", "Science"]
    mock_wikipedia["search"].return_value = ["Biology", "Chemistry"]
    main()
    captured = capsys.readouterr()
    assert "Search results for: Science" in captured.out
    assert "--- Biology" in captured.out
    assert "--- Chemistry" in captured.out
    mock_wikipedia["search"].assert_called_with("Science", results=5)


def test_main_language(capsys, mock_wikipedia):
    sys.argv = ["project.py", "-n", "Chat", "-l", "fr"]
    main()
    mock_wikipedia["set_lang"].assert_called_with("fr")


def test_main_unsupported_language(capsys, mock_wikipedia):
    sys.argv = ["project.py", "-n", "Test", "-l", "xyz"]
    from wikipedia.exceptions import WikipediaException
    mock_wikipedia["set_lang"].side_effect = WikipediaException(
        "Unsupported language")
    main()
    captured = capsys.readouterr()
    assert "Error: The language code 'xyz' is not supported. Using English ('en') instead." in captured.out
    mock_wikipedia["set_lang"].assert_called_with("en")
