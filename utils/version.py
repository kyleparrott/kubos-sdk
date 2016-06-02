from pip.utils import ensure_dir, get_installed_version
import container

def get_kubos_sdk_version():
    return get_installed_version('kubos-sdk')

def get_container_tag():
    cli = container.get_cli()
    kubos_images = cli.images(name='kubostech/kubos-sdk')
    if len(kubos_images) > 0 and 'RepoTags' in kubos_images[0]:
        tag_name = kubos_images[0]['RepoTags'][0]
        return tag_name.replace("kubostech/kubos-sdk:", "")
    return "None Found"
