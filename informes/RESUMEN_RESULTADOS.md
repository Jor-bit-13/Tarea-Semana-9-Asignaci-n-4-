# Resumen de resultados reales — capturas de consola
**Fuente:** sesiones observadas de `auditoria_cis.py` antes/después y `aplicar_cis.py` sobre tres equipos del laboratorio.

| Equipo | Inicial: cumple / no cumple / no verificado | Final: cumple / no cumple / no verificado |
|---|---:|---:|
| R1 (10.7.63.1) | 3 / 1 / 0 | 4 / 0 / 0 |
| SW1 (10.7.63.2) | 3 / 1 / 0 | 4 / 0 / 0 |
| FG1 (10.7.63.3) | 3 / 2 / 1 | 5 / 0 / 1 |
| **Total** | **9 / 4 / 1** | **13 / 0 / 1** |

## Valores verificados después del cambio
- R1: `show ip ssh` → SSH 2.0, `Authentication timeout: 60 secs`, `Authentication retries: 3`.
- SW1: mismo resultado SSH 2.0, timeout 60 s, tres intentos.
- FG1: `set admin-lockout-duration 300` y `set admin-telnet disable`. Además se observó `set admintimeout 5`, `set admin-lockout-threshold 3`, `set admin-ssh-v1 disable`.
- `strong-crypto`: **NO VERIFICADO**.

## Pruebas de comunicación
- Ubuntu (10.7.63.50) → R1/SW1/FG1: 4/4 respuestas por destino.
- PC1 → R1/SW1/FG1: 5/5 respuestas por destino.
- PC2 ↔ interfaz FG1 `10.7.66.1`: respuestas ICMP satisfactorias.
- Ubuntu → PC2 `10.7.66.10`: 4 enviados, 0 recibidos incluso con ruta vía `10.7.63.3`.

**Limitación:** licencia FG1 `Invalid`, política ICMP configurada pero filtrado no verificado. No presentar los pings fallidos como «prueba de firewall que bloquea» ni el script como CIS-CAT oficial.

> Los archivos nativos `informe_antes.md`, `informe_inicial.md`, `informe_posterior.md` e `informe_auditoria_posterior.md` existen en el Ubuntu del laboratorio. Se deben copiar y añadir a las carpetas de este repositorio sin alterar su contenido y conservando la cronología. Este resumen es documentación, **no una sustitución de los archivos originales**.
