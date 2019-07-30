import subprocess


def main():
    subprocess.run([
        "gunicorn", "barrier.wsgi:app"
    ])


if __name__ == '__main__':
    main()