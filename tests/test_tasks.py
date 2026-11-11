import unittest

from tasks import agregar_tarea, completar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_agregar_tarea_categoria_por_defecto(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Tarea sin categoría explícita")
        self.assertEqual(tarea["categoria"], "general")

    def test_agregar_tarea_categoria_valida(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Estudiar examen", categoria="estudio")
        self.assertEqual(tarea["categoria"], "estudio")

    def test_agregar_tarea_categoria_vacia_o_espacios(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Tarea inválida", categoria="")
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Tarea inválida", categoria="   ")

    def test_pendientes_filtrado_categoria(self):
        tareas = []
        agregar_tarea(tareas, "Tarea 1", categoria="trabajo")
        agregar_tarea(tareas, "Tarea 2", categoria="personal")
        agregar_tarea(tareas, "Tarea 3", categoria="trabajo")
        completar_tarea(tareas, 1)

        # Sin categoría devuelve todas las pendientes
        todas_pendientes = pendientes(tareas)
        self.assertEqual(len(todas_pendientes), 2)
        self.assertEqual([t["id"] for t in todas_pendientes], [2, 3])

        # Con categoría devuelve solo las de esa categoría
        pendientes_trabajo = pendientes(tareas, categoria="trabajo")
        self.assertEqual(len(pendientes_trabajo), 1)
        self.assertEqual(pendientes_trabajo[0]["id"], 3)

        # Filtrado insensible a mayúsculas y minúsculas
        pendientes_personal = pendientes(tareas, categoria="PERSONAL")
        self.assertEqual(len(pendientes_personal), 1)
        self.assertEqual(pendientes_personal[0]["id"], 2)

        # Categoría sin coincidencias
        pendientes_vacio = pendientes(tareas, categoria="inexistente")
        self.assertEqual(pendientes_vacio, [])

    def test_pendientes_tarea_sin_clave_categoria(self):
        tareas = [
            {"id": 1, "titulo": "Tarea sin clave categoria", "completada": False},
            {"id": 2, "titulo": "Tarea con categoria", "categoria": "trabajo", "completada": False},
        ]
        # Sin filtro: debe incluirla
        resultado_sin_filtro = pendientes(tareas)
        self.assertEqual(len(resultado_sin_filtro), 2)
        self.assertIn(tareas[0], resultado_sin_filtro)

        # Con filtro por categoría específica: debe excluirla sin lanzar ningún error
        resultado_con_filtro = pendientes(tareas, categoria="trabajo")
        self.assertEqual(len(resultado_con_filtro), 1)
        self.assertEqual(resultado_con_filtro[0]["id"], 2)
        self.assertNotIn(tareas[0], resultado_con_filtro)


if __name__ == "__main__":
    unittest.main()
