from ape.installtools import cleanup, get_ape_venv, create_project_venv, fetch_pool, add_to_path

cleanup()

venv = create_project_venv()

venv.pip_install_requirements('requirements.txt')


add_to_path(
    venv.get_paths(),
)







