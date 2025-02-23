import subprocess
import os
import sys

from helper import logger

def check_git_updates():
    repo_path = os.getcwd()
    try:
        subprocess.run(['git', '-C', repo_path, 'fetch'], check=True)

        current_branch = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', '--abbrev-ref', 'HEAD'],
            text=True
        ).strip()

        local_commit = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', current_branch],
            text=True
        ).strip()

        remote_commit = subprocess.check_output(
            ['git', '-C', repo_path, 'rev-parse', f'origin/{current_branch}'],
            text=True
        ).strip()

        # Сравниваем локальный и удаленный коммиты
        if local_commit != remote_commit:
            logger.info(f"Обновления доступны для ветки '{current_branch}'")
            logger.info(f"Локальный коммит: {local_commit}\n"
                        f"Удаленный коммит: {remote_commit}")

            update = input("обновить код? (y/n): ").strip().lower()
            if update == 'y':
                subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
                logger.success("Код успешно обновлён.")
            else:
                logger.warning("Обновление кода отменено.")
        else:
            logger.success(f"Ваша ветка '{current_branch}' актуальна.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка выполнения команды: {e}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    check_git_updates()
    subprocess.run([sys.executable, 'main.py'])
