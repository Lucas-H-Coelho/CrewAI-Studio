import os
import re
import sys
import shutil
from pathlib import Path

def fix_litellm_utils():
    """Corrige o problema de codificação no arquivo utils.py da biblioteca litellm"""
    # Caminho para o arquivo utils.py
    venv_path = Path(os.path.abspath('.venv'))
    utils_path = venv_path / "Lib" / "site-packages" / "litellm" / "utils.py"
    
    if not utils_path.exists():
        print(f"❌ Arquivo não encontrado: {utils_path}")
        return False
    
    try:
        # Criar um backup do arquivo original
        backup_path = utils_path.with_suffix('.py.bak')
        shutil.copy2(utils_path, backup_path)
        print(f"✅ Backup criado em: {backup_path}")
        
        # Ler o conteúdo do arquivo
        with open(utils_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Padrões a serem substituídos
        patterns = [
            (r'\.open\("r"\)', '.open("r", encoding="utf-8")'),
            (r'with resources\.open_text\(([^)]+)\)', r'with resources.open_text(\1, encoding="utf-8")'),
            (r'json\.load\(f\)', 'json.load(f)')
        ]
        
        # Aplicar substituições
        modified = False
        new_content = content
        
        for pattern, replacement in patterns:
            if re.search(pattern, new_content):
                if pattern == r'json\.load\(f\)':
                    # Este padrão não precisa ser substituído diretamente
                    continue
                new_content = re.sub(pattern, replacement, new_content)
                modified = True
        
        # Substituição específica para o problema na linha 188
        anthropic_pattern = r'with resources\.files\([^)]+\)\.joinpath\([^)]+\)\.open\("r"\) as f:'
        if re.search(anthropic_pattern, new_content):
            new_content = re.sub(anthropic_pattern, 
                               'with resources.files("litellm.litellm_core_utils.tokenizers").joinpath("anthropic_tokenizer.json").open("r", encoding="utf-8") as f:', 
                               new_content)
            modified = True
        
        # Substituição para o bloco except
        except_pattern = r'with resources\.open_text\([^)]+, [^)]+\) as f:'
        if re.search(except_pattern, new_content):
            new_content = re.sub(except_pattern, 
                               'with resources.open_text("litellm.litellm_core_utils.tokenizers", "anthropic_tokenizer.json", encoding="utf-8") as f:', 
                               new_content)
            modified = True
        
        # Se houve modificações, escrever o arquivo atualizado
        if modified:
            with open(utils_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Arquivo modificado com sucesso: {utils_path}")
            return True
        else:
            print(f"ℹ️ Nenhuma modificação necessária em: {utils_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {utils_path}: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando correção do arquivo utils.py da biblioteca litellm...")
    success = fix_litellm_utils()
    
    if success:
        print("\n✅ Correção aplicada com sucesso!")
        print("🔄 Tente executar o CrewAI-Studio novamente com o comando:")
        print("   .venv\\Scripts\\activate && streamlit run app/app.py")
    else:
        print("\n⚠️ Não foi possível corrigir o arquivo automaticamente.")
        print("\n📝 Solução alternativa:")
        print("1. Tente executar o CrewAI-Studio com o comando:")
        print("   $env:PYTHONIOENCODING=\"utf-8\"; streamlit run app/app.py")
