# Django Tutorial Part 2: Skeleton Website
El challenge nos indica que vayamos a la sección de admin en el navegador y veamos qué pasa. Del fichero `urls.py` deducimos que la URL es `http://localhost:8000/admin`. Al abrirla vemos la página de login. No podemos iniciar sesión porque no tenemos usuario/contraseña aún.

# Django Tutorial Part 3: Models
El challenge consiste en crear un modelo para el idioma (`Language`) de los libros. Lo creamos y lo asociamos directamente a la clase `Book`, mediante un campo `language`, ya que distintas ediciones del mismo libro en distintos idiomas tendrán distintos ISBN, así que no tendría sentido en el `BookInstance`. El idioma lo consideramos un modelo completo porque es algo que se reutiliza habitualmente (usaremos una `ForeignKey`) y el conjunto de idiomas disponible podría cambiar a lo largo del tiempo.

# Django Tutorial Part 4: Admin site
El challenge consiste en las siguientes tareas:
1. Añadir detalles a la tabla de visualización de los `BookInstance`s. Simplemente añadimos un atributo `list_display` a la clase `BookInstanceAdmin` con los campos correspondientes.
2. Añadir un "inline listing" para los `Book`s en la página de edición de `Author`. Probamos con `StackedInline` y `TabularInline`. Aunque con la primera sale un formulario muy largo, nos decantamos por ella ya que la segunda opción hace que la tabla con el estilo por defecto se salga de la pantalla.

# Django Tutorial Part 5: Home page
El challenge consiste en modificar la vista `index` y la plantilla `index.html` para cambiar el título mostrado en la pestaña del navegador, y el recuendo de géneros y libros con una palabra concreta. Seleccionamos las palabras "Fiction" para los géneros y "the" para los libros.

# Django Tutorial Part 6: Generic Views
El challenge consiste en crear vistas de lista y detalle para el modelo `Author` de manera similar al `Book` que nos enseña el tutorial.
- En `catalog/urls.py` añadimos dos nuevos paths a las vistas de lista y detalle.
- En `catalog/views.py` creamos las vistas como clases que heredan de `generic.ListView` y `generic.DetailView`, análogamente a las de `Book`.
- En `catalog/templates/catalog/` creamos las plantillas `author_list.html` y `author_detail.html` con los detalles relevantes.
- En la plantilla `catalog/templates/catalog/book_detail.html` añadimos el enlace a la página del autor correspondiente usando el método `book.author.get_absolute_url`.

# Django Tutorial Part 8: Authentication and Permissions
El challenge consiste en crear una vista de todos los libros en préstamo que solo puedan acceder los usuarios con el rol de bibliotecario, que puedan marcar libros como devueltos.
- En `catalog/views.py` creamos una nueva vista utilizando `PermissionRequiredMixin`. y especificando el permiso `can_mark_returned`.
- En `catalog/urls.py` añadimos un nuevo path a esta vista.
- En `catalog/templates/catalog/` creamos una copia de `bookinstance_list_borrowed_user.html` llamada `bookinstance_list_borrowed.html` y la modificamos.
- En la plantilla básica `base_generic.html` añadimos una sección con un enlace a la nueva vista que solo se muestra si el usuario tiene el permiso `catalog.can_mark_returned`.
- En la página de admin, añadimos el permiso `can_mark_returned` al grupo "Librarians".

# Django Tutorial Part 9: Forms
El challenge consiste en crear formularios y vistas para editar `Book`s, de forma totalmente análoga a lo que hemos hecho para `Author`.
- En `catalog/views.py` creamos las clases `BookCreate`, `BookUpdate` y `BookDelete` con los permisos correspondientes heredando de las clases genéricas `CreateView`, `UpdateView` y `DeleteView`.
- En `catalog/templates/catalog` creamos las plantillas correspondientes: `book_form.html` y `book_confirm_delete.html`.

# Django Tutorial Part 10: Tests
El challenge consiste en programar tests unitarios para la vista `AuthorCreateView`. Para ello, en el fichero `catalog/test/test_views.py` creamos una clase `AuthorCreateViewTest` que hereda de `TestCase` con los siguientes métodos:
- `test_redirect_if_not_logged_in`: Comprueba que se impide el solicita el inicio de sesión si no se ha hecho antes.
- `test_forbidden_if_logged_in_but_not_correct_permission`: Comprueba que se impide el acceso si no se tiene permiso para crear autores.
- `test_form_date_of_death_initially_set_to_expected_date`: Comprueba que la fecha de muerte mostrada inicialmente en el formulario es el 11/11/2023.
- `test_redirects_to_detail_view_on_success`: Comprueba que se redirige a la página de detalles del autor recién creado en caso de que la operación funcione.
- `test_uses_correct_template`: Comprueba que la vista utiliza la plantilla `catalog/author_form.html` como corresponde.
- `test_logged_in_with_permission`: Comprueba que un usuario con permiso para crear autores, puede acceder a la página correspondiente.
- `test_error_if_first_name_missing`: Comprueba que la operación falla si falta el campo del nombre, que es obligatorio.