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
    # Corrected escape logic
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
    
    # Ensure formatted_result is a string before passing to normalize_list_indentation
    safe_formatted_result = str(formatted_result) if formatted_result is not None else ""
    fixed_md = normalize_list_indentation(safe_formatted_result)

    # Converte Markdown -> HTML
    markdown_html = md.markdown(
        fixed_md,
        extensions=['markdown.extensions.extra']  # opcional: extra para tabelas, código, sane_lists
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
                    background-color: #f4f4f4; /* Cor de fundo suave */
                    color: #333; /* Cor do texto principal */
                }}
                h1 {{
                    color: #007bff; /* Azul vibrante para o título principal */
                    text-align: center;
                }}
                .section {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #fff; /* Fundo branco para seções */
                    border-radius: 8px; /* Bordas arredondadas */
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Sombra suave */
                }}
                .input-item {{
                    margin: 5px 0;
                    padding: 5px;
                    border-bottom: 1px solid #eee; /* Linha sutil entre itens */
                }}
                .input-item:last-child {{
                    border-bottom: none; /* Remove a borda do último item */
                }}
                h2, h3, h4, h5, h6 {{
                    color: #0056b3; /* Azul mais escuro para subtítulos */
                    margin-top: 1em;
                }}
                code {{
                    background-color: #e9ecef; /* Fundo mais claro para código */
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Consolas', 'Courier New', monospace;
                    color: #c7254e; /* Cor para o texto do código */
                }}
                pre code {{
                    background-color: #e9ecef;
                    display: block;
                    padding: 10px;
                    white-space: pre-wrap;
                    font-family: 'Consolas', 'Courier New', monospace;
                    border: 1px solid #ddd; /* Borda sutil para blocos de código */
                }}
                button#printButton {{
                    background-color: #007bff; /* Azul para o botão */
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                button#printButton:hover {{
                    background-color: #0056b3; /* Azul mais escuro no hover */
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
                        box-shadow: none; /* Remove sombra na impressão */
                        border: 1px solid #ddd; /* Adiciona borda para clareza na impressão */
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
    """ # Ensure this f-string is properly closed
    return html_content

def format_result(result):
    """
    Retorna o resultado em formato de string, extraindo dados relevantes de estruturas aninhadas, se necessário.
    """
    if isinstance(result, dict):
        if 'result' in result:
            if isinstance(result['result'], dict):
                if 'final_output' in result['result']:
                    return str(result['result']['final_output']) # Ensure string conversion
                elif 'raw' in result['result']:
                    return str(result['result']['raw']) # Ensure string conversion
                else:
                    return str(result['result'])
            elif hasattr(result['result'], 'raw'):
                 # Ensure result.raw is converted to string if it's not already
                return str(result['result'].raw) if result['result'].raw is not None else ""
            else:
                return str(result['result']) # Ensure string conversion if it's some other object
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
        # Return empty string or md_text if it's not a string to prevent errors.
        # Depending on expected behavior, an error might be more appropriate.
        return "" 

    for line in md_text.splitlines():
        # encontra linhas com espaços no início, seguidas por marcadores '*' ou '-' 
        m = re.match(r'^(?P<spaces> +)(?P<bullet>[-*])\s+(.*)$', line)
        if m:
            spaces_count = len(m.group('spaces'))
            level = spaces_count // 2  # Níveis de indentação da IA (2 espaços cada)
            new_indent = ' ' * (level * 4)
            bullet = m.group('bullet')
            content_match = m.group(3) # Content part after bullet and space
            content = str(content_match) if content_match is not None else ""
            normalized_lines.append(f"{new_indent}{bullet} {content}")
        else:
            normalized_lines.append(line)
    # This is line 188 (approximately, depending on exact preceding lines)
    # Ensure the string literal "
" is correctly formed.
    return "
".join(normalized_lines)

# Ensure there's a newline at the very end of the file.
