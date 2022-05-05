import yaml


def read(config):
    x = yaml.safe_load(open('setting.yml', 'r', encoding='utf-8').read())
    return x[config]
