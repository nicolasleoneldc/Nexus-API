import flet as ft
import requests

# TU URL DE RENDER (Asegúrate de que sea la correcta)
API_URL = "https://nexus-api-ngen.onrender.com"

def main(page: ft.Page):
    page.title = "Nexus App"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    # --- VARIABLES DE ESTADO (MEMORIA DE LA APP) ---
    token_actual = None  # Aquí guardaremos el "Pase VIP" cuando te loguees
    
    # --- PESTAÑA 1: EL MURO (FEED) ---
    columna_posts = ft.Column()
    
    def cargar_datos(e):
        columna_posts.controls.clear()
        try:
            res = requests.get(f"{API_URL}/publicaciones/")
            if res.status_code == 200:
                posts = res.json()
                if not posts:
                    columna_posts.controls.append(ft.Text("📭 No hay novedades."))
                for post in posts:
                    # Tarjeta de diseño para cada post
                    columna_posts.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(post['titulo'], size=20, weight="bold", color="cyan"),
                                    ft.Divider(),
                                    ft.Text(post['contenido'], size=16),
                                ]),
                                padding=15
                            )
                        )
                    )
            else:
                columna_posts.controls.append(ft.Text("Error al cargar posts", color="red"))
        except Exception as err:
            columna_posts.controls.append(ft.Text(f"Error de conexión: {err}", color="red"))
        page.update()

    vista_muro = ft.Container(
        content=ft.Column([
            ft.ElevatedButton("🔄 Actualizar", on_click=cargar_datos),
            columna_posts
        ]), padding=20
    )

    # --- PESTAÑA 2: PUBLICAR (NUEVO) ---
    txt_titulo = ft.TextField(label="Título", border_color="blue")
    txt_contenido = ft.TextField(label="¿Qué estás pensando?", multiline=True, min_lines=3)
    lbl_resultado_publicar = ft.Text()

    def enviar_publicacion(e):
        nonlocal token_actual
        if not token_actual:
            lbl_resultado_publicar.value = "🔒 ¡Necesitas iniciar sesión primero!"
            lbl_resultado_publicar.color = "red"
            page.update()
            return

        headers = {"Authorization": f"Bearer {token_actual}"}
        datos = {
            "titulo": txt_titulo.value,
            "contenido": txt_contenido.value,
            "usuario_id": 0 # El servidor lo ignora y pone el real, pero hay que enviarlo
        }
        
        try:
            res = requests.post(f"{API_URL}/publicar/", json=datos, headers=headers)
            if res.status_code == 200:
                lbl_resultado_publicar.value = "✅ ¡Publicado con éxito!"
                lbl_resultado_publicar.color = "green"
                txt_titulo.value = ""
                txt_contenido.value = ""
            else:
                lbl_resultado_publicar.value = f"❌ Error: {res.text}"
        except Exception as err:
            lbl_resultado_publicar.value = f"Error: {err}"
        page.update()

    vista_publicar = ft.Container(
        content=ft.Column([
            ft.Text("Crear Nueva Publicación", size=25, weight="bold"),
            txt_titulo,
            txt_contenido,
            ft.ElevatedButton("🚀 Publicar", on_click=enviar_publicacion),
            lbl_resultado_publicar
        ], spacing=20), padding=20
    )

    # --- PESTAÑA 3: CUENTA (LOGIN) ---
    txt_user = ft.TextField(label="Usuario (ej: AdminSupremo)")
    txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    lbl_login = ft.Text()

    def iniciar_sesion(e):
        nonlocal token_actual
        try:
            # Fíjate que el login pide FORM DATA, no JSON normal
            datos = {
                "username": txt_user.value,
                "password": txt_pass.value
            }
            res = requests.post(f"{API_URL}/token", data=datos)
            
            if res.status_code == 200:
                info = res.json()
                token_actual = info['access_token']
                lbl_login.value = f"🔓 ¡Hola {txt_user.value}! Ya tienes permiso."
                lbl_login.color = "green"
            else:
                lbl_login.value = "❌ Usuario o contraseña incorrectos"
                lbl_login.color = "red"
        except Exception as err:
            lbl_login.value = f"Error: {err}"
        page.update()

    vista_cuenta = ft.Container(
        content=ft.Column([
            ft.Text("Iniciar Sesión", size=25),
            txt_user,
            txt_pass,
            ft.ElevatedButton("🔑 Entrar", on_click=iniciar_sesion),
            lbl_login
        ], spacing=20), padding=20
    )

    # --- NAVEGACIÓN (TABS) ---
    taps = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Muro", icon="home", content=vista_muro),
            ft.Tab(text="Publicar", iicon="add_circle", content=vista_publicar),
            ft.Tab(text="Cuenta", icon="person", content=vista_cuenta),
        ],
        expand=1,
    )

    page.add(taps)
    cargar_datos(None) # Cargar datos al inicio

ft.app(target=main)

#hubo cambio? prueba001
#Prueba 002 - hay cambios?
