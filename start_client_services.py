import argparse
import os
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceSpec:
    name: str
    module: str
    port: int


# Stack minimale pour le front client React actuel
CLIENT_SERVICES: list[ServiceSpec] = [
    ServiceSpec("AUTHENTIFICATION", "MICROSERVICES.AUTHENTIFICATION.main:app", 8001),
    ServiceSpec("CATALOGUE", "MICROSERVICES.CATALOGUE.main:app", 8002),
    ServiceSpec("COMMANDE", "MICROSERVICES.COMMANDE.main:app", 8003),
    ServiceSpec("FAVORIS", "MICROSERVICES.FAVORIS.main:app", 8005),
    ServiceSpec("FACTURE", "MICROSERVICES.FACTURE.main:app", 8006),
    ServiceSpec("PAIEMENT_CLIENTS", "MICROSERVICES.PAIEMENT_CLIENTS.main:app", 8007),
]


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def stop_process(proc: subprocess.Popen, name: str):
    if proc.poll() is not None:
        return

    print(f"Arrêt de {name}...")

    try:
        if os.name == "nt":
            proc.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            proc.terminate()
    except Exception:
        proc.terminate()

    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    parser = argparse.ArgumentParser(
        description="Lancer uniquement les microservices nécessaires au front client"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Activer --reload pour uvicorn (mode dev)",
    )
    parser.add_argument(
        "--same-terminal",
        action="store_true",
        help="Force le lancement dans ce terminal (sans nouvelles fenêtres)",
    )
    args = parser.parse_args()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    ports_occupes = [svc for svc in CLIENT_SERVICES if is_port_in_use(svc.port)]
    if ports_occupes:
        print("Ports déjà occupés. Libère-les avant de lancer la stack client :")
        for svc in ports_occupes:
            print(f"- {svc.name}: {svc.port}")
        sys.exit(1)

    print("Démarrage de la stack client...")
    processes: list[tuple[ServiceSpec, subprocess.Popen]] = []

    mode_multi_fenetres = os.name == "nt" and not args.same_terminal
    if mode_multi_fenetres:
        print("Mode Windows: un terminal séparé par service.")
    else:
        print("Mode terminal unique.")

    try:
        for spec in CLIENT_SERVICES:
            cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                spec.module,
                "--host",
                "0.0.0.0",
                "--port",
                str(spec.port),
            ]
            if args.reload:
                cmd.append("--reload")

            if mode_multi_fenetres:
                creationflags = subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
                proc = subprocess.Popen(
                    cmd,
                    cwd=root_dir,
                    creationflags=creationflags,
                )
            else:
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
                proc = subprocess.Popen(
                    cmd,
                    cwd=root_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=creationflags,
                )

                if proc.stdout is not None:
                    from threading import Thread

                    def _stream(name: str, pipe):
                        try:
                            for line in iter(pipe.readline, ""):
                                if not line:
                                    break
                                print(f"[{name}] {line.rstrip()}")
                        finally:
                            pipe.close()

                    Thread(target=_stream, args=(spec.name, proc.stdout), daemon=True).start()

            processes.append((spec, proc))
            print(f"- {spec.name} lancé sur http://localhost:{spec.port}")
            time.sleep(0.2)

        print("\nStack client démarrée.")
        print("Appuie sur Ctrl+C ici pour arrêter tous ces services.\n")

        while True:
            for spec, proc in processes:
                exit_code = proc.poll()
                if exit_code is not None:
                    print(f"\n⚠️ Le service {spec.name} s'est arrêté (code {exit_code}).")
                    raise KeyboardInterrupt
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nArrêt global en cours...")
    finally:
        for spec, proc in processes:
            stop_process(proc, spec.name)
        print("Tous les services client sont arrêtés.")


if __name__ == "__main__":
    main()
