import streamlit as st
from streamlit import session_state as ss
import db_utils
from pg_agents import PageAgents
from pg_tasks import PageTasks
from pg_crews import PageCrews
from pg_tools import PageTools
from pg_crew_run import PageCrewRun
from pg_export_crew import PageExportCrew
from pg_results import PageResults
from pg_knowledge import PageKnowledge
from dotenv import load_dotenv
from llms import load_secrets_fron_env
import os

def pages():
    return {
        'Equipes': PageCrews(),
        'Ferramentas': PageTools(),
        'Agentes': PageAgents(),
        'Tarefas': PageTasks(),
        'Conhecimento': PageKnowledge(),
        'Iniciar!': PageCrewRun(),
        'Resultados': PageResults(),
        'Importar/Exportar': PageExportCrew()
    }

# Mapeamento de nomes de página antigos (inglês) para novos (português)
page_name_translation = {
    'Crews': 'Equipes',
    'Tools': 'Ferramentas',
    'Agents': 'Agentes',
    'Tasks': 'Tarefas',
    'Knowledge': 'Conhecimento',
    'Kickoff!': 'Iniciar!',
    'Results': 'Resultados',
    'Import/export': 'Importar/Exportar'
}

def load_data():
    ss.agents = db_utils.load_agents()
    ss.tasks = db_utils.load_tasks()
    ss.crews = db_utils.load_crews()
    ss.tools = db_utils.load_tools()
    ss.enabled_tools = db_utils.load_tools_state()
    ss.knowledge_sources = db_utils.load_knowledge_sources()

def draw_sidebar():
    with st.sidebar:
        st.image("img/crewai_logo.png")

        if 'page' not in ss:
            ss.page = 'Equipes'  # Página padrão
        else:
            # Verifica se a página na sessão precisa ser traduzida
            if ss.page in page_name_translation:
                ss.page = page_name_translation[ss.page]
            # Se a página atual (possivelmente traduzida) não estiver na lista de páginas válidas,
            # redefina para a página padrão para evitar erros.
            if ss.page not in pages().keys():
                ss.page = 'Equipes'

        current_page_keys = list(pages().keys())
        try:
            current_index = current_page_keys.index(ss.page)
        except ValueError:
            # Se mesmo após a tradução e verificação, a página não for encontrada,
            # defina para a página padrão e pegue seu índice.
            ss.page = 'Equipes'
            current_index = current_page_keys.index(ss.page)
        
        selected_page = st.radio(
            'Página', 
            current_page_keys, 
            index=current_index,
            label_visibility="collapsed"
        )
        
        if selected_page != ss.page:
            ss.page = selected_page
            st.rerun()
            
def main():
    st.set_page_config(page_title="CrewAI Studio", page_icon="img/favicon.ico", layout="wide")
    load_dotenv()
    load_secrets_fron_env()

    # Forçar a desativação do AgentOps
    agentops_enabled = False 
    print("AgentOps foi explicitamente desabilitado no código.")

    # Se AgentOps estiver desabilitado, remove AGENTOPS_API_KEY do ambiente para este processo
    if not agentops_enabled:
        if 'AGENTOPS_API_KEY' in os.environ:
            del os.environ['AGENTOPS_API_KEY']
            print("AGENTOPS_API_KEY foi removida das variáveis de ambiente para este processo.")
        # Também define AGENTOPS_ENABLED como 'false' no ambiente para este processo
        os.environ['AGENTOPS_ENABLED'] = 'false'
        print("AGENTOPS_ENABLED foi definido como 'false' nas variáveis de ambiente para este processo.")

    # A lógica de inicialização original do AgentOps permanece, mas não deve ser acionada
    # se agentops_enabled for False e a chave da API for removida.
    agentops_api_key = os.getenv('AGENTOPS_API_KEY') # Deve ser None agora se foi removida

    if agentops_enabled and not ss.get('agentops_failed', False):
        if not agentops_api_key: # Esta condição será verdadeira se a chave foi removida
            ss.agentops_failed = True
            # Esta mensagem pode não aparecer se agentops_enabled já for False
            print("AgentOps habilitado, mas AGENTOPS_API_KEY não está definida.") 
        else:
            try:
                import agentops
                agentops.init(api_key=agentops_api_key, auto_start_session=False)
                print("AgentOps inicializado com sucesso.")
            except ModuleNotFoundError as e:
                ss.agentops_failed = True
                print(f"Erro ao inicializar AgentOps (Módulo não encontrado): {str(e)}")
            except Exception as e: 
                ss.agentops_failed = True
                print(f"Erro ao inicializar AgentOps: {str(e)}")
    elif agentops_enabled and ss.get('agentops_failed', False):
        print("AgentOps está habilitado, mas falhou na inicialização anteriormente. Não tentará novamente.")
        
    db_utils.initialize_db()
    load_data()
    draw_sidebar()
    PageCrewRun.maintain_session_state()
    pages()[ss.page].draw()
    
if __name__ == '__main__':
    main()
