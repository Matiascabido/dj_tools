# Sistema de Generación de Música Hardgroove

Este proyecto genera música electrónica del subgénero Hardgroove de manera modular y extensible, siguiendo principios de Clean Code. Inspirado en productores como Ned Bennett, Chlär, D.Dan, Alarico y Bailey Ibbs.

## Características
- **Arquitectura modular**: 8 módulos independientes para estructura, patrones, variación, groove humano, armonía, mezcla, selección de sonidos y renderizado.
- **Fuentes de sonido**: Soporte para samples pregrabados, síntesis por código y modo híbrido.
- **Coherencia**: Mantiene identidad sonora entre tracks para DJ sets reales.
- **Groove humano**: Incluye microtiming, swing, variación de velocity y ghost notes.
- **Evolución**: Variación obligatoria cada 8 compases, energía constante.

## Instalación
1. Instalar dependencias: `pip install -r requirements.txt`
2. Agregar samples WAV en carpetas `samples/kick/`, `samples/hats/`, etc.
3. Configurar parámetros en `config/config.py`

## Uso
Ejecutar `python main.py` para generar un track en `output/`.

## Módulos
1. **Sound Selection Engine**: Selecciona/genera sonidos.
2. **Structure Generator**: Define estructura temporal.
3. **Rhythm Pattern Generator**: Crea patrones rítmicos.
4. **Variation Engine**: Aplica variaciones.
5. **Human Groove Engine**: Añade groove humano.
6. **Harmonic Engine**: Gestiona armonía.
7. **Mixing Engine**: Mezcla niveles.
8. **Audio Renderer**: Exporta WAV.

## Mejoras Futuras
- Groove: Añadir más síncopas basadas en análisis de tracks reales.
- Musicalidad: Integrar IA para detectar patrones repetitivos y variar más.
- Realismo: Usar librerías como pedalboard para síntesis avanzada.
- Calidad sonora: Optimizar renderizado para evitar clipping, añadir reverb sutil.