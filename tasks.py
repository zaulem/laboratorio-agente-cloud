def agregar_tarea(tareas, titulo, categoria="general"):
    titulo = titulo.strip()
    if not titulo:
        raise ValueError("El título es obligatorio")
    if not isinstance(categoria, str) or not categoria.strip():
        raise ValueError("La categoría es obligatoria")
    categoria = categoria.strip()
    tarea = {
        "id": len(tareas) + 1,
        "titulo": titulo,
        "categoria": categoria,
        "completada": False,
    }
    tareas.append(tarea)
    return tarea


def completar_tarea(tareas, tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = True
            return tarea
    raise ValueError("Tarea no encontrada")


def pendientes(tareas, categoria=None):
    tareas_pendientes = [t for t in tareas if not t["completada"]]
    if categoria is None:
        return tareas_pendientes
    cat_lower = categoria.strip().lower()
    return [t for t in tareas_pendientes if t.get("categoria", "").lower() == cat_lower]
