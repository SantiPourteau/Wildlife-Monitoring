import cv2




# Cargar el frame con OpenCV
imagen = cv2.imread("primer_frame.jpg")

# Crear una ventana para dibujar la bounding box manualmente
bounding_box = []

def dibujar_rectangulo(event, x, y, flags, param):
    global bounding_box, imagen
    if event == cv2.EVENT_LBUTTONDOWN:
        bounding_box = [(x, y)]  # Punto inicial
    elif event == cv2.EVENT_LBUTTONUP:
        bounding_box.append((x, y))  # Punto final
        # Dibujar el rectángulo en la imagen
        cv2.rectangle(imagen, bounding_box[0], bounding_box[1], (0, 255, 0), 2)
        cv2.imshow("Frame con Bounding Box", imagen)

# Mostrar el frame y permitir al usuario dibujar la bounding box
cv2.imshow("Frame con Bounding Box", imagen)
cv2.setMouseCallback("Frame con Bounding Box", dibujar_rectangulo)

print("Dibuja la bounding box sobre Messi y presiona 'q' para salir.")
while True:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

# Guardar las coordenadas de la bounding box
if bounding_box:
    print(f"Bounding Box: {bounding_box}")
    with open("bounding_box.txt", "w") as f:
        f.write(f"Bounding Box: {bounding_box}")
else:
    print("No se generó una bounding box.")