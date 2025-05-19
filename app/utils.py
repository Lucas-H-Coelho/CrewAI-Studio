import random
import string
from streamlit import markdown
import markdown as md
from datetime import datetime

def rnd_id(length=8):
    characters = string.ascii_letters + string.digits
    random_text = ''.join(random.choice(characters) for _ in range(length))
    return random_text

def escape_quotes(s):
<<<<<<< HEAD
    # Corrected escape logic for use in generated code/strings
=======
>>>>>>> 6fd1bb3 (asas)
    return s.replace('"', '"').replace("'", "'")

def fix_columns_width():
    markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

def generate_printable_view(crew_name, result, inputs, formatted_result, created_at=None):
    """
    Gera uma visualização HTML simples para impressão.
    """
    if created_at is None:
        created_at = datetime.now().isoformat()
    created_at_str = datetime.fromisoformat(created_at).strftime('%Y-%m-%d %H:%M:%S')
    
    safe_formatted_result = str(formatted_result) if formatted_result is not None else ""
    fixed_md = normalize_list_indentation(safe_formatted_result)

    markdown_html = md.markdown(
        fixed_md,
        extensions=['markdown.extensions.extra']
    )

    html_content = f"""
    <html>
        <head>
            <title>Resultado do CrewAI Studio - {crew_name}</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                    max-width: 800px;
                    margin: auto;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                h1 {{
                    color: #007bff;
                    text-align: center;
                }}
                .section {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .input-item {{
                    margin: 5px 0;
                    padding: 5px;
                    border-bottom: 1px solid #eee;
                }}
                .input-item:last-child {{
                    border-bottom: none;
                }}
                h2, h3, h4, h5, h6 {{
                    color: #0056b3;
                    margin-top: 1em;
                }}
                code {{
                    background-color: #e9ecef;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Consolas', 'Courier New', monospace;
                    color: #c7254e;
                }}
                pre code {{
                    background-color: #e9ecef;
                    display: block;
                    padding: 10px;
                    white-space: pre-wrap;
                    font-family: 'Consolas', 'Courier New', monospace;
                    border: 1px solid #ddd;
                }}
                button#printButton {{
                    background-color: #007bff;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                button#printButton:hover {{
                    background-color: #0056b3;
                }}
                @media print {{
                    #printButton {{
                        display: none;
                    }}
                    .page-break {{
                        page-break-before: always;
                    }}
                    body {{
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }}
                    .section {{
                        box-shadow: none;
                        border: 1px solid #ddd;
                    }}
                }}
            </style>
        </head>
        <body>
            <button id="printButton" onclick="window.print();" style="margin-bottom: 20px;">
                Imprimir
            </button>

            <h1>Resultado do CrewAI Studio</h1>
            <div class="section">
                <h2>Informações da Equipe</h2>
                <p><strong>Nome da Equipe:</strong> {crew_name}</p>
                <p><strong>Criado em:</strong> {created_at_str}</p>
            </div>
            <div class="section">
                <h2>Entradas</h2>
                {''.join(f'<div class="input-item"><strong>{k}:</strong> {v}</div>' for k, v in inputs.items())}
            </div>
            <div class="page-break"></div>
            <div class="section">
                {markdown_html}
            </div>
        </body>
    </html>
    """
    return html_content

def format_result(result):
    """
    Retorna o resultado em formato de string, extraindo dados relevantes de estruturas aninhadas, se necessário.
    """
    if isinstance(result, dict):
        if 'result' in result:
            if isinstance(result['result'], dict):
                if 'final_output' in result['result']:
                    return str(result['result']['final_output'])
                elif 'raw' in result['result']:
                    return str(result['result']['raw'])
                else:
                    return str(result['result'])
            elif hasattr(result['result'], 'raw'):
                return str(result['result'].raw) if result['result'].raw is not None else ""
            else:
                return str(result['result'])
        return str(result)
    return str(result)

def normalize_list_indentation(md_text: str) -> str:
    """
    Converte linhas começando com múltiplos de 2 espaços (gerado por IA) para
    múltiplos de 4 espaços para que Python-Markdown interprete listas aninhadas corretamente.
    Preserva marcadores '-' e '*'.
    """
    import re
    normalized_lines = [] 
    if not isinstance(md_text, str):
<<<<<<< HEAD
        return "" 
=======
        return ""
>>>>>>> 6fd1bb3 (asas)

    for line in md_text.splitlines():
        m = re.match(r'^(?P<spaces> +)(?P<bullet>[-*])\s+(.*)$', line)
        if m:
            spaces_count = len(m.group('spaces'))
            level = spaces_count // 2
            new_indent = ' ' * (level * 4)
            bullet = m.group('bullet')
            content_match = m.group(3)
            content = str(content_match) if content_match is not None else ""
            normalized_lines.append(f"{new_indent}{bullet} {content}")
        else:
            normalized_lines.append(line)
    return "
".join(normalized_lines)
