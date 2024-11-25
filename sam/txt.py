# Bounding box en formato (x1, y1), (x2, y2)
bounding_box = [(567, 249), (627, 347)]

# Convertir al formato xywh
x1, y1 = bounding_box[0]  # Esquina superior izquierda
x2, y2 = bounding_box[1]  # Esquina inferior derecha
x = x1
y = y1
w = x2 - x1  # Ancho
h = y2 - y1  # Alto

# Crear el contenido del archivo en formato xywh
bounding_box_xywh = f"{x} {y} {w} {h}"

# Escribir al archivo txt
with open("path_to_first_frame_bbox.txt", "w") as f:
    f.write(bounding_box_xywh)

print("Archivo 'path_to_first_frame_bbox.txt' generado con éxito!")
