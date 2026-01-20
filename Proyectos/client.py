import flet as ft
import requests

# TU URL DE RENDER
API_URL = "https://nexus-api-ngen.onrender.com"

def main(page: ft.Page):
    print("⏳ Iniciando App Modo Seguro...")
    page.title = "Nexus App (Modo Seguro)"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    # --- VARIABLES DE ESTADO ---
    token_actual = None
    
    # --- CONTENEDOR PRINCIPAL (Aquí cambiaremos las pantallas) ---
    cuerpo_principal = ft.Container()

    # --- DEFINICIÓN DE PANTALLAS ---
    
    # 1. PANTALLA MURO
    def obtener_vista_muro():
        columna_posts = ft.Column()
        
        # Función interna para cargar
        def cargar_datos(e=None):
            print("🔄 Descargando datos...")
            columna_posts.controls.clear()
            columna_posts.controls.append(ft.Text("Cargando...", color="yellow"))
            page.update()
            
            try:
                res = requests.get(f"{API_URL}/publicaciones/", timeout=60)
                columna_posts.controls.clear() # Limpiar el "Cargando"
                
                if res.status_code == 200:
                    posts = res.json()
                    if not posts:
                        columna_posts.controls.append(ft.Text("📭 No hay novedades."))
                    for post in posts:
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
                    print("✅ Datos cargados.")
                else:
                    columna_posts.controls.append(ft.Text("Error del servidor", color="red"))
            except Exception as err:
                columna_posts.controls.append(ft.Text(f"Error de conexión: {err}", color="red"))
            page.update()

        # Botón de actualizar dentro del muro
        boton_refresh = ft.ElevatedButton("🔄 Refrescar Muro", on_click=cargar_datos)
        
        # Cargamos datos al crear la vista
        cargar_datos() 
        
        return ft.Column([boton_refresh, columna_posts])

    # 2. PANTALLA PUBLICAR
    def obtener_vista_publicar():
        txt_titulo = ft.TextField(label="Título", border_color="blue")
        txt_contenido = ft.TextField(label="Contenido", multiline=True, min_lines=3)
        lbl_estado = ft.Text()

        def enviar(e):
            if not token_actual:
                lbl_estado.value = "🔒 Inicia sesión primero"
                lbl_estado.color = "red"
                page.update()
                return

            headers = {"Authorization": f"Bearer {token_actual}"}
            datos = {"titulo": txt_titulo.value, "contenido": txt_contenido.value, "usuario_id": 0}
            
            try:
                res = requests.post(f"{API_URL}/publicar/", json=datos, headers=headers)
                if res.status_code == 200:
                    lbl_estado.value = "✅ ¡Publicado!"
                    lbl_estado.color = "green"
                    txt_titulo.value = ""
                    txt_contenido.value = ""
                else:
                    lbl_estado.value = f"❌ Error: {res.text}"
            except Exception as err:
                lbl_estado.value = f"Error: {err}"
            page.update()

        return ft.Column([
            ft.Text("Nueva Publicación", size=20, weight="bold"),
            txt_titulo, 
            txt_contenido, 
            ft.ElevatedButton("🚀 Enviar", on_click=enviar),
            lbl_estado
        ], spacing=20)

    # 3. PANTALLA CUENTA
    def obtener_vista_cuenta():
        txt_user = ft.TextField(label="Usuario")
        txt_pass = ft.TextField(label="Contraseña", password=True)
        lbl_login = ft.Text()

        def entrar(e):
            nonlocal token_actual
            try:
                datos = {"username": txt_user.value, "password": txt_pass.value}
                res = requests.post(f"{API_URL}/token", data=datos)
                if res.status_code == 200:
                    token_actual = res.json()['access_token']
                    lbl_login.value = f"🔓 Bienvenido {txt_user.value}"
                    lbl_login.color = "green"
                else:
                    lbl_login.value = "❌ Datos incorrectos"
                    lbl_login.color = "red"
            except Exception as err:
                lbl_login.value = f"Error: {err}"
            page.update()

        return ft.Column([
            ft.Text("Iniciar Sesión", size=20),
            txt_user, 
            txt_pass, 
            ft.ElevatedButton("🔑 Entrar", on_click=entrar),
            lbl_login
        ], spacing=20)

    # --- NAVEGACIÓN MANUAL (BOTONES) ---
    def ir_a_muro(e):
        cuerpo_principal.content = obtener_vista_muro()
        page.update()

    def ir_a_publicar(e):
        cuerpo_principal.content = obtener_vista_publicar()
        page.update()

    def ir_a_cuenta(e):
        cuerpo_principal.content = obtener_vista_cuenta()
        page.update()

    # Barra de botones (Menú)
    menu = ft.Row([
        ft.ElevatedButton("🏠 Muro", on_click=ir_a_muro),
        ft.ElevatedButton("✍️ Publicar", on_click=ir_a_publicar),
        ft.ElevatedButton("👤 Cuenta", on_click=ir_a_cuenta),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Agregamos todo a la página
    page.add(
        ft.Text("Nexus App", size=30, weight="bold", color="blue"),
        menu,
        ft.Divider(),
        cuerpo_principal
    )
    
    # Cargamos el muro al inicio
    ir_a_muro(None)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)