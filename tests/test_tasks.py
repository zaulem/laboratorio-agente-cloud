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


if __name__ == "__main__":
    unittest.main()
