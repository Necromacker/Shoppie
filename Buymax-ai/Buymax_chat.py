from flask import Flask, jsonify, render_template, request, session
import google.generativeai as genai
from api import Gemini_API_KEY as api
import logging
import sys
import textwrap
import re

# Configure logging to show in console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def format_text_types(text):
    """Format different types of text with appropriate styling"""
    # Handle headings
    text = re.sub(r'^# (.*?)$', r'<h1 class="heading-1">\1</h1>', text, flags=re.MULTILINE)
    
    # Handle code blocks with language specification
    text = re.sub(r'```(python|javascript|html|css|java|cpp|csharp|php|ruby|swift|go|rust|typescript|sql|bash|shell|yaml|json|markdown|xml|kotlin|scala|r|matlab|perl|haskell|lua|dart|elixir|clojure|groovy|powershell|batch|ini|toml|properties|dockerfile|nginx|apache|gitignore|editorconfig|eslintrc|prettierrc|babelrc|webpack|rollup|vite|jest|mocha|chai|cypress|selenium|pytest|unittest|nose|robot|cucumber|gherkin|protractor|karma|jasmine|mocha|chai|sinon|ava|tape|tap)?\n(.*?)```', 
        r'<div class="code-block"><div class="code-header"><span class="code-language">\1</span><button class="copy-button" onclick="copyCode(this)">Copy</button></div><pre><code class="code-text">\2</code></pre></div>', 
        text, flags=re.DOTALL)
    
    # Handle inline code
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    
    # Handle bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Handle italic text
    text = re.sub(r'(.*?)\*$', r'<em class="italic-text">\1</em>', text)
    
    # Handle highlighted text
    text = re.sub(r'(Important Note:)', r'<span class="highlight-text">\1</span>', text)
    
    # Handle strikethrough text
    text = re.sub(r'~~(.*?)~~', r'<del class="strikethrough-text">\1</del>', text)
    
    # Handle underlined text
    text = re.sub(r'__(.*?)__', r'<u class="underlined-text">\1</u>', text)
    
    # Handle ordered lists
    text = re.sub(r'(\d+\.\s.*?)(?=\d+\.\s|$)', r'<div class="numbered-point">\1</div>', text, flags=re.DOTALL)
    
    # Handle unordered lists
    text = re.sub(r'(\*\s.*?)(?=\*\s|$)', r'<div class="bullet-point">\1</div>', text, flags=re.DOTALL)
    
    # Handle blockquotes
    text = re.sub(r'^> (.*?)$', r'<blockquote class="blockquote">\1</blockquote>', text, flags=re.MULTILINE)
    
    # Handle links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="link-text" target="_blank">\1</a>', text)
    
    # Handle image links
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="image-link">', text)
    
    return text

def format_nested_points(text):
    """Format text with nested bullet points and numbered lists"""
    lines = text.split('\n')
    formatted_lines = []
    current_indent = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('')
            continue
            
        # Count leading asterisks for nesting level
        indent = 0
        while line.startswith('*'):
            indent += 1
            line = line[1:].strip()
            
        # Handle numbered points
        if re.match(r'^\d+\.', line):
            formatted_lines.append(f'<div class="numbered-point" style="margin-left: {indent * 2}rem">{line}</div>')
        # Handle bullet points
        elif line.startswith('*') or line.startswith('-'):
            formatted_lines.append(f'<div class="bullet-point" style="margin-left: {indent * 2}rem">{line}</div>')
        # Handle regular text
        else:
            formatted_lines.append(f'<div class="text-line" style="margin-left: {indent * 2}rem">{line}</div>')
    
    return '\n'.join(formatted_lines)

def format_response(text):
    # First, detect and format code blocks
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    current_code_block = []
    current_language = 'python'  # default language
    
    for i, line in enumerate(lines):
        # Check if line looks like code (starts with common code patterns)
        if (line.strip().startswith(('def ', 'class ', 'import ', 'from ', 'print(', 'if ', 'for ', 'while ', 'return ', 'try:', 'except:', 'with ', 'async def ')) or
            line.strip().endswith((':', ';', '{', '}', ']', ')'))) and not in_code_block:
            # Check if next few lines also look like code
            next_lines = lines[i:i+3]
            if any(next_line.strip().startswith(('    ', '\t', 'def ', 'class ', 'if ', 'for ', 'while ')) for next_line in next_lines if next_line.strip()):
                in_code_block = True
                current_code_block = [line]
                # Try to detect language based on first line
                if line.strip().startswith(('function ', 'const ', 'let ', 'var ', 'console.')):
                    current_language = 'javascript'
                elif line.strip().startswith(('public ', 'private ', 'class ', 'void ', 'int ', 'String ')):
                    current_language = 'java'
                elif line.strip().startswith(('<?php', '$', 'function ')):
                    current_language = 'php'
                continue
        
        if in_code_block:
            if line.strip() == '' and not any(l.strip() for l in current_code_block):
                # Empty line in code block, keep it
                current_code_block.append(line)
            elif line.strip() == '' and all(l.strip() == '' for l in lines[i+1:i+3]):
                # End of code block (2 or more empty lines)
                code_text = '\n'.join(current_code_block)
                formatted_lines.append(f'```{current_language}\n{code_text}\n```')
                in_code_block = False
                current_code_block = []
            else:
                current_code_block.append(line)
        else:
            # Only add non-code lines to formatted_lines
            if not line.strip().startswith(('def ', 'class ', 'import ', 'from ', 'print(', 'if ', 'for ', 'while ', 'return ', 'try:', 'except:', 'with ', 'async def ')):
                formatted_lines.append(line)
    
    # Handle any remaining code block
    if in_code_block:
        code_text = '\n'.join(current_code_block)
        formatted_lines.append(f'```{current_language}\n{code_text}\n```')
    
    # Join the lines back together
    text = '\n'.join(formatted_lines)
    
    # Apply other formatting
    text = format_text_types(text)
    
    return text

# Log the API key (first few characters only for security)
logger.info(f"Initializing with API key starting with: {api[:5]}...")

try:
    genai.configure(api_key=api)
    model = genai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat(history=[])
    logger.info("Successfully initialized Buymax AI")
except Exception as e:
    logger.error(f"Failed to initialize Buymax AI: {str(e)}")
    raise

app = Flask(__name__)
chat_history = []

@app.route('/')
def index():
    return render_template('chat.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')
        logger.info(f"Received chat request with input: {user_input}")

        if not user_input:
            logger.warning("No user input provided")
            return jsonify({"error": "No user input provided."}), 400

        try:
            logger.info("Sending message to Buymax AI...")
            response = chat.send_message(user_input)
            formatted_response = format_response(response.text)
            logger.info(f"Received response from Buymax AI: {formatted_response[:100]}...")
            chat_history.append({"user": user_input, "bot": formatted_response})
            return jsonify({"response": formatted_response})
        except Exception as e:
            logger.error(f"Error in Buymax AI call: {str(e)}")
            return jsonify({"error": f"Error in AI response: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

