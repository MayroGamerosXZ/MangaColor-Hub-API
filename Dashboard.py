import streamlit as st
import requests
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="MangaColor Hub - Panel de Control",
    page_icon="🎨",
    layout="wide"
)

# Dirección de tu API local (Backend)
BACKEND_URL = "http://127.0.0.1:8000"

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("MangaColor Hub")
st.markdown("""
Esta interfaz se conecta en tiempo real a la API de MangaColor Hub y a tu tablero de Trello. 
Utiliza el panel izquierdo para crear y el panel central para gestionar tus capítulos.
""")

st.divider()

# --- FUNCIONES DE AYUDA PARA HABLAR CON LA API ---
def fetch_chapters():
    """Llama a GET /chapters y devuelve una lista"""
    try:
        response = requests.get(f"{BACKEND_URL}/chapters")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error conectando a la API: {e}")
        return []

def get_chapter_ids():
    """Obtiene solo los IDs para los selectboxes"""
    chapters = fetch_chapters()
    return [c["id"] for c in chapters]

# --- BARRA LATERAL (SIDEBAR) - CREAR CAPÍTULO (POST) ---
with st.sidebar:
    st.header("➕ Crear Nuevo Capítulo")
    st.markdown("Completa los datos para registrarlo e enviarlo a Trello.")

    with st.form("create_chapter_form", clear_on_submit=True):
        new_id = st.number_input("ID Único del Capítulo", min_value=1, step=1)
        new_title = st.text_input("Título del Manga o Capítulo")
        new_number = st.number_input("Número de Capítulo", min_value=1.0, step=0.1)

        submit_btn = st.form_submit_button("Registrar en Backlog y Trello")

        if submit_btn:
            # Estructura de datos requerida por Pydantic en tu API
            payload = {
                "id": new_id,
                "title": new_title,
                "chapter_number": new_number,
                "status": "pending" # Empieza por defecto en To Do
            }

            # Petición POST a tu API
            with st.spinner("Creando tarjeta en Trello..."):
                response = requests.post(f"{BACKEND_URL}/chapters", json=payload)

            if response.status_code == 201:
                st.success(f"Capítulo '{new_title}' creado con éxito.")
                # st.balloons() # ¡Una pequeña celebración visual!
            elif response.status_code == 400:
                st.error("Error: El ID del capítulo ya existe.")
            else:
                st.error("Error desconocido al crear el capítulo.")

# --- CUERPO PRINCIPAL ---

# 1. VISUALIZACIÓN GENERAL (GET /chapters)
st.header("📊 Estado Actual del Backlog")
col1, col2 = st.columns([3, 1])

# Botón para refrescar la tabla manualmente
with col2:
    if st.button("🔄 Refrescar Tabla"):
        st.rerun()

# Llamar a la API para obtener los datos
chapters_data = fetch_chapters()

if chapters_data:
    # Convertimos la lista JSON a un DataFrame de Pandas para que se vea bonita
    df = pd.DataFrame(chapters_data)

    # Limpiamos los nombres de las columnas para la vista
    df.columns = ["ID", "Título", "Nro. Capítulo", "Estado Actual", "Trello Card ID"]

    # Mapeo de estados para mejor lectura
    status_map = {"pending": "To Do", "in_progress": "In Progress", "done": "Done"}
    df["Estado Actual"] = df["Estado Actual"].map(status_map)

    # Mostramos la tabla interactiva
    st.dataframe(df.set_index("ID"), use_container_width=True)
else:
    st.info("La API está vacía o el servidor está apagado. Crea un capítulo para empezar.")

st.divider()

# 2. GESTIÓN DE ESTADOS (PATCH /chapters/{id}/status)
st.header("🔄 Actualizar Progreso")
st.markdown("Selecciona un capítulo y cambia su estado. La tarjeta en Trello se moverá automáticamente.")

col_id, col_status, col_btn = st.columns([1, 1, 1])

# Cargar IDs dinámicamente
existing_ids = get_chapter_ids()

with col_id:
    # Si no hay capítulos, mostramos una lista vacía para no romper el selectbox
    selected_id = st.selectbox("ID del Capítulo", existing_ids if existing_ids else ["No hay capítulos"])

with col_status:
    # Mapeo invertido para enviar a la API
    status_options = {"To Do": "pending", "In Progress": "in_progress", "Done": "done"}
    selected_status_view = st.selectbox("Nuevo Estado", list(status_options.keys()))
    selected_status_api = status_options[selected_status_view]

with col_btn:
    # Añadimos espacio vertical para alinear el botón
    st.markdown("<br>", unsafe_allow_html=True)
    update_btn = st.button("Actualizar y Mover Tarjeta")

if update_btn and existing_ids:
    with st.spinner(f"Moviendo tarjeta del Capítulo {selected_id} a {selected_status_view}..."):
        # Petición PATCH a tu API usando Query Parameter
        url = f"{BACKEND_URL}/chapters/{selected_id}/status"
        params = {"new_status": selected_status_api}
        response = requests.patch(url, params=params)

    if response.status_code == 200:
        st.success(f"Capítulo {selected_id} actualizado a '{selected_status_view}' y tarjeta movida.")
        # Refrescamos la página automáticamente para ver la tabla actualizada
        st.rerun()
    else:
        st.error(f"Error al actualizar: {response.json()['detail']}")
elif update_btn and not existing_ids:
    st.warning("Crea un capítulo primero.")