# Sombra independiente de protagonista 97/F1

Reutilización del maestro de sombra aprobado por Miguel, SHA-256 `97b994a6dec9db1aba06ced1ab9f5359d354fe24279564b0586ce7ccab4c83c0` y recorte `[373,540,916,751]`. No se ha generado otra familia ni alterado el original. Tamaño nativo 16×4; pintura dentro del bbox nativo PC/Amiga, dos densidades 8×/12× y exportación determinista existente.

El tipo 22 conserva propietario y generación, orden First, altura propia cero y coordenadas nativas: X=ownerX+(ownerHeight>>2)+5; Y=ownerY+(ownerHeight>>2)-3. F0 con altura del propietario >8; F1 en otro caso. No se fusiona con el cuerpo ni se añade sombra de suelo. Se conserva su desaparición nativa con propietario oculto, recorte/agua o destrucción.

PASS 64 casos Window/SDL por sistema para ambos frames/formatos: dos sombras con propietarios distintos, dos alturas válidas por frame, recorte, oclusión cero, 8×/12×, paleta, vínculo/generación/fuente inválidos y recuperación SDL. ASan/UBSan Windows y Linux; LSan Linux. La cobertura gráfica completa no implica aceptación global visual/jugable ni cierra R4/R5.

## Cierre de ciclo de vida

La fórmula de posición y selección de F0/F1 corresponde al instante del manejador nativo. El propietario puede cambiar después en el mismo tick. La publicación conserva el frame/ancla ya elegidos, comprueba la preparación nativa y el vínculo de origen; no exige que coincidan con una posición/altura posterior ni reclasifica la sombra por una destrucción posterior del dueño. La creación 8D/F2 se cubre por separado.
