import streamlit as st
from openai import OpenAI

# 1. Configuración de la página con diseño ancho y moderno
st.set_page_config(
    page_title="Astra AI | Next-Gen Global",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS personalizados para una interfaz ultra moderna
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .pricing-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Lista completa de países del mundo para el selector
LISTA_PAISES = [
    "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda", "Arabia Saudita", 
    "Argelia", "Argentina", "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Bangladés", 
    "Barbados", "Baréin", "Bélgica", "Belice", "Benín", "Bielorrusia", "Birmania", "Bolivia", 
    "Bosnia y Herzegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", 
    "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar", "Chad", "Chile", "China", 
    "Chipre", "Colombia", "Comoras", "Congo", "Corea del Norte", "Corea del Sur", "Costa de Marfil", 
    "Costa Rica", "Croacia", "Cuba", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", 
    "Emiratos Árabes Unidos", "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", 
    "Estonia", "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", 
    "Ghana", "Granada", "Grecia", "Guatemala", "Guinea", "Guinea Ecuatorial", "Guinea-Bisáu", 
    "Guyana", "Haití", "Honduras", "Hungría", "India", "Indonesia", "Irak", "Irán", "Irlanda", 
    "Islandia", "Islas Marshall", "Islas Salomón", "Israel", "Italia", "Jamaica", "Japón", 
    "Jordania", "Kazajistán", "Kenia", "Kirguistán", "Kiribati", "Kuwait", "Laos", "Lesoto", 
    "Letonia", "Líbano", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", 
    "Macedonia del Norte", "Madagascar", "Malasia", "Malaui", "Maldivas", "Malí", "Malta", 
    "Marruecos", "Mauricio", "Mauritania", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", 
    "Montenegro", "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger", "Nigeria", 
    "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", "Palaos", "Panamá", 
    "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido", "República Centroafricana", 
    "República Checa", "República Democrática del Congo", "República Dominicana", "Ruanda", "Rumanía", 
    "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino", "San Vicente y las Granadinas", 
    "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles", "Sierra Leona", 
    "Singapur", "Siria", "Somalia", "Sri Lanka", "Suazilandia", "Sudáfrica", "Sudán", "Sudán del Sur", 
    "Suecia", "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán", "Timor Oriental", "Togo", 
    "Tonga", "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", 
    "Uganda", "Uruguay", "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue"
]

# 3. Inicializar Estados de Sesión
if "usuario_logueado" not in st.session_state:
    st.session_state.usuario_logueado = False
if "email_usuario" not in st.session_state:
    st.session_state.email_usuario = ""
if "pais_usuario" not in st.session_state:
    st.session_state.pais_usuario = "Venezuela"
if "plan_actual" not in st.session_state:
    st.session_state.plan_actual = "Normal (Gratis)"
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "paso_auth" not in st.session_state:
    st.session_state.paso_auth = "formulario" # "formulario", "verificar_codigo", "elegir_pais"

# --- SECCIÓN DE AUTENTICACIÓN AVANZADA ---
if not st.session_state.usuario_logueado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>✨ Astra AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af;'>Ecosistema global de Inteligencia Artificial.</p>", unsafe_allow_html=True)
        
        # Paso 1: Ingresar credenciales o registro
        if st.session_state.paso_auth == "formulario":
            tab_login, tab_registro = st.tabs(["🔑 Iniciar Sesión", "📝 Crear Cuenta"])
            
            with tab_login:
                st.subheader("Accede a tu cuenta")
                email_ingreso = st.text_input("Correo electrónico", key="login_email")
                pass_ingreso = st.text_input("Contraseña", type="password", key="login_pass")
                
                if st.button("Continuar con verificación", use_container_width=True):
                    if email_ingreso:
                        st.session_state.email_usuario = email_ingreso
                        st.session_state.paso_auth = "verificar_codigo"
                        st.success("📩 ¡Código de acceso enviado a tu Gmail!")
                        st.rerun()
                    else:
                        st.error("Por favor ingresa un correo válido.")
                        
            with tab_registro:
                st.subheader("Únete a Astra AI")
                nuevo_email = st.text_input("Correo electrónico", key="reg_email")
                nueva_pass = st.text_input("Crea una contraseña", type="password", key="reg_pass")
                
                if st.button("Registrarse y verificar", use_container_width=True):
                    if nuevo_email:
                        st.session_state.email_usuario = nuevo_email
                        st.session_state.paso_auth = "verificar_codigo"
                        st.success("📩 ¡Código de registro enviado a tu Gmail!")
                        st.rerun()
                    else:
                        st.error("Por favor completa los campos.")

        # Paso 2: Validación de código enviado por Gmail
        elif st.session_state.paso_auth == "verificar_codigo":
            st.info(f"Hemos enviado un código de verificación de 4 dígitos a: **{st.session_state.email_usuario}**")
            st.caption("(Código de prueba simulado: usa **1234**)")
            
            codigo_ingresado = st.text_input("Ingresa el código recibido por Gmail:", type="password")
            
            if st.button("Verificar Código", use_container_width=True):
                if codigo_ingresado == "1234":
                    st.success("✅ ¡Código verificado con éxito!")
                    st.session_state.paso_auth = "elegir_pais"
                    st.rerun()
                else:
                    st.error("❌ Código incorrecto. Intenta con 1234.")

        # Paso 3: Selección de región / país (con buscador de lista completa)
        elif st.session_state.paso_auth == "elegir_pais":
            st.subheader("🌍 Selecciona tu Región o País")
            st.write("Selecciona tu país de origen para personalizar tu experiencia global sin restricciones:")
            
            pais_seleccionado = st.selectbox("Busca o selecciona tu país:", LISTA_PAISES, index=LISTA_PAISES.index("Venezuela") if "Venezuela" in LISTA_PAISES else 0)
            
            if st.button("Comenzar a usar Astra AI", use_container_width=True):
                st.session_state.pais_usuario = pais_seleccionado
                st.session_state.usuario_logueado = True
                st.success("¡Configuración completada con éxito!")
                st.rerun()