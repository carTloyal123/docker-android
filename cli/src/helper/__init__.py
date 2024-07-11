import logging
import os
import requests

logger = logging.getLogger("helper")


def convert_str_to_bool(given_str: str) -> bool:
    """
    Convert String to Boolean value

    :param given_str: given string
    :return: converted string in Boolean
    """
    if given_str:
        if type(given_str) is str:
            return given_str.lower() in ("yes", "true", "t", "1")
        else:
            raise AttributeError
    else:
        logger.info(f"'{given_str}' is empty!")
        return False


def get_env_value_or_raise(env_key: str) -> str:
    """
    Get value of necessary environment variable.

    :param env_key: given environment variable
    :return: env_value in String
    """
    try:
        env_value = os.getenv(env_key)
        if not env_value:
            raise RuntimeError(f"'{env_key}' is missing.")
        elif env_value.isspace():
            raise RuntimeError(f"'{env_key}' contains only white space.")
        return env_value
    except TypeError as t_err:
        logger.error(t_err)


def symlink_force(source: str, target: str) -> None:
    """
    Create Symbolic link

    :param source: source file
    :param target: target file
    :return: None
    """
    try:
        os.symlink(source, target)
    except FileNotFoundError as ffe_err:
        logger.error(ffe_err)
    except FileExistsError:
        os.remove(target)
        os.symlink(source, target)

def get_latest_artifact(owner, repo, save_path) -> str:
    """
    Download the latest release artifact from a GitHub repository to a specific path

    :param owner: GitHub repository owner
    :param repo: GitHub repository name
    :param save_path: Path to save the downloaded file
    :return: Name of the downloaded file
    """

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get the latest release
    latest_release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(latest_release_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the latest release: {response.status_code}, {response.text}")
    
    latest_release = response.json()
    logger.info(f"Latest release: {latest_release['tag_name']}")
    
    # Find the asset
    assets = latest_release['assets']
    if not assets:
        raise Exception("No assets found in the latest release")
    
    # Download the first asset (you can modify this to download a specific asset if needed)
    asset = assets[0]
    download_url = asset['browser_download_url']
    file_name = asset['name']
    
    logger.info(f"Downloading {file_name} from {download_url}")
    download_response = requests.get(download_url, headers=headers)
    
    if download_response.status_code != 200:
        raise Exception(f"Failed to download the asset: {download_response.status_code}, {download_response.text}")
    
    # Save the file
    full_file_path = os.path.join(save_path, file_name)
    with open(full_file_path, 'wb') as file:
        file.write(download_response.content)
    
    logger.info(f"Downloaded {file_name} successfully")
    return file_name
