
import pytest

from jack_compiler.jack_tokenizer import Tokenizer, TokenType


@pytest.fixture
def create_tokenizer(tmp_path):
    def _create_tokenizer(content):
        test_file = tmp_path / "test.jack"
        test_file.write_text(content)
        tokenizer = Tokenizer(test_file)
        tokenizer.advance()
        return tokenizer
    return _create_tokenizer


def test_skipping_comments_and_empty_chars(create_tokenizer):
    content = """
    // Single line comment

    /* Multi-line
       comment */

    let x = 5;  // Inline comment

    // Another comment
    return;
    """
    tokenizer = create_tokenizer(content)

    # First token should be 'let' (skipping comments and empty lines)
    assert tokenizer.get_current_token().type == TokenType.KEYWORD
    assert tokenizer.get_current_token().value == "let"

    # Verify rest of the tokens
    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.IDENTIFIER
    assert tokenizer.get_current_token().value == "x"

    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.SYMBOL
    assert tokenizer.get_current_token().value == "="

    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.INT_CONST
    assert tokenizer.get_current_token().value == 5

    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.SYMBOL
    assert tokenizer.get_current_token().value == ";"

    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.KEYWORD
    assert tokenizer.get_current_token().value == "return"

    tokenizer.advance()
    assert tokenizer.get_current_token().type == TokenType.SYMBOL
    assert tokenizer.get_current_token().value == ";"


@pytest.mark.parametrize("symbol", [
    '{', '}', '(', ')', '[', ']', '+', '-', '*', '/',
    '&', '|', '<', '>', '=', ';', ',', '.', '~'
])
def test_symbols(create_tokenizer, symbol):
    tokenizer = create_tokenizer(symbol)
    token = tokenizer.get_current_token()
    assert token.type == TokenType.SYMBOL
    assert token.value == symbol


@pytest.mark.parametrize("keyword", [
    "class", "constructor", "function", "method", "field", "static", "var", "int",
    "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
    "else", "while", "return"
])
def test_keywords(create_tokenizer, keyword):
    tokenizer = create_tokenizer(keyword)
    token = tokenizer.get_current_token()
    assert token.type == TokenType.KEYWORD
    assert token.value == keyword


@pytest.mark.parametrize("identifier", [
    "_variable", "_123name"
    "variable", "name123"
])
def test_identifiers(create_tokenizer, identifier):
    tokenizer = create_tokenizer(identifier)
    token = tokenizer.get_current_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == identifier


def test_string_constant(create_tokenizer):
    tokenizer = create_tokenizer('"Hello World"')
    token = tokenizer.get_current_token()
    assert token.type == TokenType.STR_CONST
    assert token.value == "Hello World"

# def test_multiple_lines_with_comment(create_tokenizer):
#     content = "// This is a comment\n\nlet x = 42;"  # Using explicit newlines
#     tokenizer = create_tokenizer(content)
#
#     # Check first token (should be 'let' since comment and empty line should be skipped)
#     assert tokenizer.get_current_token().type == TokenType.KEYWORD
#     assert tokenizer.get_current_token().value == "let"
#
#     tokenizer.advance()
#     assert tokenizer.get_current_token().type == TokenType.IDENTIFIER
#     assert tokenizer.get_current_token().value == "x"
#
#     tokenizer.advance()
#     assert tokenizer.get_current_token().type == TokenType.SYMBOL
#     assert tokenizer.get_current_token().value == "="
#
#     tokenizer.advance()
#     assert tokenizer.get_current_token().type == TokenType.INT_CONST
#     assert tokenizer.get_current_token().value == 42
#
#     tokenizer.advance()
#     assert tokenizer.get_current_token().type == TokenType.SYMBOL
#     assert tokenizer.get_current_token().value == ";"
