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
        
    db_utils.initialize_db()
    load_data()
    draw_sidebar()
    PageCrewRun.maintain_session_state()
    pages()[ss.page].draw()
    
if __name__ == '__main__':
    main()
