import flet as ft
import requests

# 1. Configuración: La dirección de tu API en la nube
API_URL = "https://nexus-api-ngen.onrender.com" 

def main(page: ft.Page):
    page.title = "Nexus App"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    # Título de la app
    titulo = ft.Text("Novedades de Nexus", size=30, weight="bold", color="blue")
    
    # Contenedor donde pondremos las publicaciones
    columna_posts = ft.Column()

    # Función para traer datos del servidor
    def cargar_datos(e):
        columna_posts.controls.clear() # Limpiar lista anterior
        
        try:
            # Petición GET al endpoint /publicaciones/ que vimos en tu Swagger
            respuesta = requests.get(f"{API_URL}/publicaciones/")
            publicaciones = respuesta.json()
            
            # Si no hay nada, mostramos aviso
            if not publicaciones:
                 columna_posts.controls.append(ft.Text("No hay publicaciones aún."))
            
            # Creamos una tarjeta por cada publicación
            for post in publicaciones:
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON),
                                title=ft.Text(post['titulo'], weight="bold"),
                                subtitle=ft.Text(post['contenido']),
                            ),
                        ]),
                        padding=10,
                    )
                )
                columna_posts.controls.append(card)
                
        except Exception as error:
            columna_posts.controls.append(ft.Text(f"Error de conexión: {error}", color="red"))
        
        page.update()

    # Botón para recargar
    boton_cargar = ft.ElevatedButton("Actualizar Muro", on_click=cargar_datos)

    # Agregamos todo a la pantalla
    page.add(
        titulo,
        boton_cargar,
        columna_posts
    )
    
    # Cargamos los datos al iniciar
    cargar_datos(None)

# Ejecutar la app
ft.app(target=main)