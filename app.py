import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import re

# Configuración de la página
st.set_page_config(page_title="Test de Dones - Remanente Vencedor", layout="centered", page_icon="⛪")

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stRadio p {font-size: 16px !important;}
    div[data-testid="stForm"] {padding: 20px; border-radius: 10px; border: 1px solid #ddd;}
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
col1, col2 = st.columns([1, 4]) 

with col1:
    try:
        logo = Image.open("image_0.png")
        st.image(logo, use_column_width='always')
    except FileNotFoundError:
        st.warning("⚠️ Falta el logo (image_0.png)")

with col2:
    st.markdown("""
        <h2 style='text-align: left; color: #2E86C1; margin-bottom: 0px; padding-top: 10px;'>
            Iglesia Cristiana <br> "Remanente Vencedor"
        </h2>
        """, unsafe_allow_html=True)

st.markdown("---") 

# --- INTRODUCCIÓN Y CITA ---
st.title("🧩 Test de Dones Vocacionales")

st.markdown("""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #2E86C1;">
    <p style="font-style: italic; margin-bottom: 0;">
    "De manera que, teniendo diferentes dones, según la gracia que nos es dada, 
    si el de <b>profecía</b>, úsese conforme a la medida de la fe; 
    o si de <b>servicio</b>, en servir; 
    o el que <b>enseña</b>, en la enseñanza; 
    el que <b>exhorta</b>, en la exhortación; 
    el que <b>reparte</b>, con liberalidad; 
    el que <b>preside</b>, con solicitud; 
    el que hace <b>misericordia</b>, con alegría."
    </p>
    <p style="text-align: right; font-weight: bold; margin-top: 5px;">— Romanos 12: 6-8</p>
</div>
""", unsafe_allow_html=True)

st.write("""
**Instrucciones:**
Lee cada afirmación y evalúala con sinceridad según la frecuencia con la que ocurre en tu vida.
* **5** = Casi Siempre (¡Es muy yo!)
* **3** = Algunas Veces
* **1** = Rara Vez
* **0** = Nunca
""")
st.markdown("---")

# --- BASE DE DATOS DE PREGUNTAS ---
# Nota: Los números al inicio del texto se ignorarán al mostrarse, 
# se usan solo para referencia interna.
preguntas_db = {
    "El que Preside (Liderazgo)": [
        "1. ¿Te entregas con mucha pasión y sacrificio para lograr que una meta se cumpla?",
        "2. ¿Te sientes más realizado y feliz cuando trabajas por objetivos claros?",
        "3. ¿Te gusta ceder tu lugar a otros para que ellos brillen o crezcan en su potencial?",
        "4. ¿Eres una persona visionaria? (Ves el 'panorama completo' antes que los pequeños detalles).",
        "5. ¿Prefieres no tomar el liderazgo a menos que te lo deleguen oficialmente?",
        "6. ¿Eres capaz de expresar tus ideas y organizar cosas de manera que todos entiendan claramente?",
        "7. ¿Asumes el mando automáticamente si ves que no hay nadie liderando?",
        "8. ¿Soportarías críticas difíciles con tal de terminar la tarea encomendada?",
        "9. ¿Disfrutas más los proyectos grandes a largo plazo que las tareas pequeñas e inmediatas?",
        "10. ¿Prefieres estar bajo autoridad (tener mentor/jefe) para aprender a tener autoridad tú mismo?",
        "11. ¿Te gusta delegar tareas a otros y supervisarlos para ver su progreso?",
        "12. ¿Te sientes muy motivado a organizar todo lo que cae bajo tu responsabilidad?"
    ],
    "El que Reparte (Generosidad)": [
        "13. ¿Te gusta dar o donar anónimamente (sin que nadie se entere)?",
        "14. ¿Das libremente tu dinero, tiempo o energía sin que te pese hacerlo?",
        "15. ¿Sientes satisfacción al apoyar financieramente a personas o ministerios?",
        "16. ¿Te esfuerzas porque tu ofrenda o regalo sea siempre de la mejor calidad posible?",
        "17. ¿Te ofreces rápido como voluntario para ayudar donde haga falta?",
        "18. ¿Manejas tu dinero con sabiduría y ahorras? (Eres frugal en tus gastos).",
        "19. ¿Te da mucha alegría saber que tu ayuda fue la respuesta exacta a la oración de alguien?",
        "20. ¿Buscas confirmación interna sobre *cuánto* debes dar en una situación específica?",
        "21. ¿Ves la hospitalidad (recibir gente en casa) como una oportunidad para dar?",
        "22. ¿Intercedes (oras) frecuentemente por las necesidades y salvación de otros?",
        "23. ¿Crees firmemente en el principio bíblico de diezmar y ofrendar generosamente?",
        "24. ¿Das o apoyas solo cuando sientes una guía espiritual clara, no por impulso?"
    ],
    "El que Exhorta (Exhortación)": [
        "25. ¿Te encanta motivar a otros para que vivan vidas victoriosas?",
        "26. ¿Tienes facilidad de palabra y eres elocuente al comunicarte?",
        "27. ¿Validas la verdad a través de la experiencia práctica y luego la confirmas con la Escritura?",
        "28. ¿Animas a otros a que desarrollen su propio ministerio o potencial al máximo?",
        "29. ¿Aceptas a la gente tal como es, sin juzgarla de entrada?",
        "30. ¿Prefieres aplicar la verdad a la vida diaria en lugar de solo investigarla teóricamente?",
        "31. ¿Te enfocas mucho en trabajar directamente con la gente y sus problemas?",
        "32. ¿Te gusta dar consejo personal (uno a uno) a quien lo necesita?",
        "33. ¿Ves las pruebas y problemas como oportunidades necesarias para crecer?",
        "34. ¿Te gusta dar 'pasos de acción' precisos para ayudar a alguien a salir de un problema?",
        "35. ¿Te gusta ver una respuesta visible (cambios reales) cuando enseñas o aconsejas?",
        "36. ¿Prefieres usar ejemplos de la vida real antes que ilustraciones teóricas o abstractas?"
    ],
    "El que Enseña (Enseñanza)": [
        "37. ¿Verificas los hechos y fuentes antes de aceptar algo como verdad?",
        "38. ¿Disfrutas mucho estudiar e investigar un tema a fondo?",
        "39. ¿Haces hincapié en los hechos exactos y en el uso preciso de las palabras?",
        "40. ¿Tienes un vocabulario extenso y lo usas con facilidad al explicar?",
        "41. ¿Eres objetivo y analítico (eres bueno investigando datos y detalles)?",
        "42. ¿Prefieres enseñar a los creyentes en un estudio bíblico antes que hacer evangelismo en la calle?",
        "43. ¿Sueles verificar las fuentes de lo que dicen otros maestros o predicadores?",
        "44. ¿Presentas la verdad de una manera lógica, sistemática y ordenada?",
        "45. ¿Prefieres los estudios que tienen una aplicación práctica clara?",
        "46. ¿Te molesta mucho cuando alguien saca textos bíblicos fuera de su contexto?",
        "47. ¿Disfrutas el estudio del origen y significado profundo de las palabras?",
        "48. ¿Te interesa sobre todo que la verdad bíblica quede establecida en cualquier situación?"
    ],
    "El que hace Misericordia (Compasión)": [
        "49. ¿Sientes una atracción natural hacia la gente que está herida, triste o en problemas?",
        "50. ¿Te gusta hacer cosas especiales y detallistas para que otros se sientan bien?",
        "51. ¿Captas fácil el ambiente emocional o el lenguaje corporal de las personas sin que te digan nada?",
        "52. ¿Buscas siempre lo bueno en la gente y evitas criticar sus fallas?",
        "53. ¿Tienes mucho cuidado con tus palabras para no herir los sentimientos de nadie?",
        "54. ¿Te afecta más el dolor emocional de alguien que su dolor físico?",
        "55. ¿Te sientes atraído a hacer amistad con personas que también son sensibles y compasivas?",
        "56. ¿Tienes una capacidad inmensa para mostrar amor y afecto físico o verbal?",
        "57. ¿Detectas fácilmente cuando alguien es falso o tiene malas intenciones, aunque no lo digas?",
        "58. ¿Tomas acción rápida para consolar y sanar las heridas emocionales en otros?",
        "59. ¿Confías en la gente y tiendes a ser una persona confiada?",
        "60. ¿Evitas los conflictos, peleas y las confrontaciones a toda costa?"
    ],
    "Profecía (Percepción Espiritual)": [
        "61. ¿Dices las cosas francamente y sin rodeos, 'al pan, pan y al vino, vino'?",
        "62. ¿Animas y retas a las personas a arrepentirse para que den buen fruto en sus vidas?",
        "63. ¿Actúas con valentía basándote en tus principios espirituales, aunque no sea popular?",
        "64. ¿Identificas rápidamente la diferencia entre el bien y el mal (y odias lo malo)?",
        "65. ¿Ves la Biblia como la base absoluta y final para toda verdad y autoridad?",
        "66. ¿Tiendes a ver las cosas en 'blanco o negro', sin muchos términos medios?",
        "67. ¿Sientes un dolor profundo y una carga por el pecado de otros o de la sociedad?",
        "68. ¿Eres muy persuasivo y convincente cuando hablas de lo que crees?",
        "69. ¿Te impacientas cuando ves que alguien no ve sus propios errores ('puntos ciegos')?",
        "70. ¿Percibes fácilmente el carácter real o la verdadera intención de las personas?",
        "71. ¿Crees que aceptar y pasar por dificultades produce un quebrantamiento positivo en la persona?",
        "72. ¿Prefieres tener pocos amigos íntimos y leales en lugar de muchos conocidos superficiales?"
    ],
    "Servicio (Servicio Práctico)": [
        "73. ¿Necesitas sentirte apreciado y valorado por las tareas que haces?",
        "74. ¿Te das cuenta rápido de las necesidades prácticas (cosas que faltan, que hay que arreglar o limpiar)?",
        "75. ¿Disfrutas los trabajos manuales y funcionales que tienen un resultado visible?",
        "76. ¿Te interesa más cubrir las necesidades de otros que las tuyas propias en un momento dado?",
        "77. ¿Te cuesta mucho decir 'no' cuando alguien te pide ayuda práctica?",
        "78. ¿Asumes responsabilidades operativas si ves que no hay nadie encargado?",
        "79. ¿Eres meticuloso, leal y te gusta tener las cosas ordenadas y en su lugar?",
        "80. ¿Siempre terminas lo que has comenzado, no te gusta dejar cosas a medias?",
        "81. ¿Disfrutas mostrando hospitalidad práctica (servir comida, arreglar el lugar, acomodar sillas)?",
        "82. ¿Sientes gran gozo y satisfacción al haber hecho algo útil que se necesitaba?",
        "83. ¿Tiendes a hacer más de lo que te piden originalmente?",
        "84. ¿Tienes un nivel de energía física alto para trabajar y mantenerte activo?"
    ]
}

# --- LÓGICA DE MEZCLA (INTERLEAVING) ---
# En lugar de mostrarlas por bloque, las vamos a intercalar:
# Una de liderazgo, una de generosidad, una de exhortación... y repetimos.
# Así el usuario no sabe qué categoría está respondiendo.

# 1. Preparar listas
categorias = list(preguntas_db.keys())
num_preguntas_por_cat = 12
lista_mezclada = []

# 2. Intercalar (Zip manual)
for i in range(num_preguntas_por_cat):
    for cat in categorias:
        if i < len(preguntas_db[cat]):
            # Tomamos la pregunta cruda
            pregunta_cruda = preguntas_db[cat][i]
            # Limpiamos el número hardcodeado ("1. Texto" -> "Texto") usando RegEx
            texto_limpio = re.sub(r'^\d+\.\s*', '', pregunta_cruda)
            
            lista_mezclada.append({
                "categoria": cat,
                "texto": texto_limpio,
                "id_original": f"{cat}_{i}" # ID único para Streamlit
            })

# Diccionario para guardar puntuaciones (se inicializa en 0)
scores = {cat: 0 for cat in categorias}

# --- FORMULARIO ÚNICO ---
with st.form("test_dones"):
    st.markdown("### 📝 Cuestionario")
    
    # Iteramos por la lista mezclada y re-numeramos del 1 al 84 visualmente
    for idx, item in enumerate(lista_mezclada, 1):
        # Mostramos pregunta con número nuevo dinámico (idx)
        label_pregunta = f"**{idx}.** {item['texto']}"
        
        # Opciones de respuesta
        val = st.radio(
            label_pregunta,
            options=[0, 1, 3, 5],
            format_func=lambda x: {0: "0 (Nunca)", 1: "1 (Rara vez)", 3: "3 (A veces)", 5: "5 (Casi siempre)"}.get(x),
            horizontal=True,
            index=0,
            key=item['id_original'] # Clave interna única
        )
        
        # Sumamos el valor a la categoría correcta (invisible para el usuario)
        scores[item['categoria']] += val
        
        # Pequeño separador visual cada 7 preguntas para descansar la vista
        if idx % 7 == 0 and idx != 84:
            st.markdown("---")

    st.markdown("### 🎉 ¡Has terminado!")
    st.write("Haz clic en el botón para revelar tu perfil.")
    submitted = st.form_submit_button("👉 Calcular mis Resultados 📊", type="primary")

# --- RESULTADOS ---
if submitted:
    st.success("¡Resultados Calculados con Éxito!")
    st.balloons()
    
    # Preparar datos para el gráfico
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Visualización con Radar Chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Cerrar el círculo
        theta=categories + [categories[0]], # Cerrar el círculo
        fill='toself',
        fillcolor='rgba(46, 134, 193, 0.4)', 
        line=dict(color='#2E86C1'),
        name='Mis Dones'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 60], 
                tickfont=dict(size=10),
                gridcolor='lightgrey'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='black', weight='bold'),
                rotation=90,
                direction='clockwise'
            ),
             bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title={
            'text': "Tu Radar de Dones",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, color='#2E86C1')
        },
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interpretación
    max_score = max(scores.values())
    top_dones = [k for k, v in scores.items() if v == max_score]
    
    st.markdown("---")
    st.header("📋 Interpretación Rápida")
    st.markdown(f"Tus dones principales parecen ser: **{', '.join(top_dones)}** ({max_score} puntos).")
    st.write("Estos son los lentes a través de los cuales ves la vida y el ministerio.")
    
    with st.expander("Ver tabla detallada de puntajes"):
        df_scores = pd.DataFrame(list(scores.items()), columns=['Don', 'Puntaje Total (Máx 60)'])
        df_scores = df_scores.sort_values(by='Puntaje Total (Máx 60)', ascending=False)
        st.table(df_scores.reset_index(drop=True))

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: grey;'>Iglesia Cristiana 'Remanente Vencedor' | Herramienta de Edificación</p>", unsafe_allow_html=True)

```
