#!/usr/bin/env python3
"""
Auditoria inicial de controles de seguridad CIS
Router Cisco, Switch Cisco y FortiGate
Modo: solo lectura
"""

import re
import pexpect
from getpass import getpass
from datetime import datetime
from pathlib import Path

EQUIPOS = {
    "R1": {"ip": "10.7.63.1", "usuario": "adminlab", "tipo": "cisco"},
    "SW1": {"ip": "10.7.63.2", "usuario": "adminlab", "tipo": "cisco"},
    "FG1": {"ip": "10.7.63.3", "usuario": "admin", "tipo": "fortigate"},
}

PROMPT = r"(?m)^[\w.()/-]+\s*[>#]\s*$"

CISCO = [
    "show ip ssh",
    "show running-config | section line vty",
    "show running-config | include tcp-keepalives",
    "show running-config | include ip source-route",
    "show running-config | include logging buffered",
    "show running-config | include ip http",
]

FORTIGATE = [
    "get system status",
    "show full-configuration system global | grep admintimeout",
    "show full-configuration system global | grep admin-lockout",
    "show full-configuration system global | grep strong-crypto",
    "show full-configuration system global | grep admin-ssh-v1",
    "show full-configuration system global | grep admin-telnet",
    "show system interface port1",
    "show system interface port2",
]


def evaluar(tipo, datos):
    resultados = {}

    def revisar(nombre, condicion):
        if condicion is None:
            estado = "NO VERIFICADO"
        elif condicion:
            estado = "CUMPLE"
        else:
            estado = "NO CUMPLE"
        resultados[nombre] = estado

    if tipo == "cisco":
        ssh = datos.get("show ip ssh", "")
        vty = datos.get("show running-config | section line vty", "")

        revisar(
            "SSH version 2",
            bool(re.search(r"SSH Enabled\s*-\s*version 2", ssh, re.I))
        )

        tiempo = re.search(r"Authentication timeout:\s*(\d+)", ssh, re.I)
        revisar("Timeout SSH <= 60 segundos",
                int(tiempo.group(1)) <= 60 if tiempo else None)

        intentos = re.search(r"Authentication retries:\s*(\d+)", ssh, re.I)
        revisar("Intentos SSH <= 3",
                int(intentos.group(1)) <= 3 if intentos else None)

        revisar("VTY exclusivamente SSH",
                "transport input ssh" in vty if "line vty" in vty else None)

    elif tipo == "fortigate":
        global_cfg = "\n".join(
            datos.get(c, "") for c in FORTIGATE if "global" in c
        )

        def opcion(nombre):
            resultado = re.search(
                rf"(?m)^\s*set {re.escape(nombre)}\s+(\S+)",
                global_cfg
            )
            return resultado.group(1) if resultado else None

        timeout = opcion("admintimeout")
        limite = opcion("admin-lockout-threshold")
        duracion = opcion("admin-lockout-duration")
        revisar("Inactividad administrativa <= 5 minutos",
                int(timeout) <= 5 if timeout and timeout.isdigit() else None)
        revisar("Bloqueo tras <= 3 intentos",
                int(limite) <= 3 if limite and limite.isdigit() else None)
        revisar("Bloqueo >= 300 segundos",
                int(duracion) >= 300 if duracion and duracion.isdigit() else None)

        crypto = opcion("strong-crypto")
        revisar("Cifrado fuerte",
                crypto == "enable" if crypto is not None else None)

        sshv1 = opcion("admin-ssh-v1")
        revisar("SSH version 1 desactivado",
                sshv1 == "disable" if sshv1 is not None else None)

        telnet = opcion("admin-telnet")
        revisar("Telnet administrativo desactivado",
                telnet == "disable" if telnet is not None else None)

    return resultados


def auditar(nombre, equipo):
    ip = equipo["ip"]
    usuario = equipo["usuario"]
    tipo = equipo["tipo"]
    print(f"\nAuditoria de {nombre} ({ip})")
    password = getpass("Contrasena SSH: ")

    argumentos = ["-tt", "-oStrictHostKeyChecking=yes", "-oConnectTimeout=12"]
    if tipo == "cisco":
        argumentos += [
            "-oKexAlgorithms=+diffie-hellman-group1-sha1",
            "-oHostKeyAlgorithms=+ssh-rsa",
            "-oCiphers=+aes128-cbc",
        ]
    argumentos.append(f"{usuario}@{ip}")

    sesion = pexpect.spawn("ssh", argumentos, encoding="utf-8", timeout=45)

    try:
        respuesta = sesion.expect([
            r"(?i)password:\s*$",
            PROMPT,
            pexpect.EOF,
            pexpect.TIMEOUT
        ])
        if respuesta == 0:
            sesion.sendline(password)
            sesion.expect(PROMPT)
        elif respuesta != 1:
            raise RuntimeError("No se pudo establecer la conexion SSH")

        print("Conexion SSH establecida")

        if tipo == "cisco":
            sesion.sendline("terminal length 0")
            sesion.expect(PROMPT)

        comandos = CISCO if tipo == "cisco" else FORTIGATE
        datos = {}
        for cmd in comandos:
            sesion.sendline(cmd)
            sesion.expect(PROMPT)
            datos[cmd] = sesion.before
            print(f"Revisado: {cmd}")

        resultados = evaluar(tipo, datos)
        destino = Path("informes_cis") / nombre
        destino.mkdir(parents=True, exist_ok=True)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lineas = [
            f"# Auditoria CIS - {nombre}", "",
            f"Fecha: {fecha}", f"Direccion IP: {ip}",
            f"Tipo: {tipo}", "", "## Resultados de seguridad", ""
        ]

        print("\nRESULTADOS DE AUDITORIA")
        for control, estado in resultados.items():
            print(f"{estado}: {control}")
            lineas.append(f"- **{control}:** {estado}")

        archivo = destino / "informe_inicial.md"
        archivo.write_text(
            "\n".join(lineas) + "\n",
            encoding="utf-8"
        )
        print(f"\nInforme guardado en: {archivo}")
    finally:
        sesion.close(force=True)


def main():
    print("=" * 55)
    print("AUDITORIA INICIAL CIS - LABORATORIO GNS3")
    print("=" * 55)
    for nombre, equipo in EQUIPOS.items():
        try:
            auditar(nombre, equipo)
        except Exception as error:
            print(f"\nERROR auditando {nombre}: {error}")
    print("\nAuditoria inicial terminada.")


if __name__ == "__main__":
    main()
