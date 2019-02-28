# -*- coding: utf-8 -*-
import sys
from ruamel.yaml import YAML
"""Main module."""


def main():
    '''(re)format yaml'''
    yaml = YAML(typ='rt')
    with open("samples/all-in-one.yml", 'rt') as f_input:
        documents = yaml.load_all(f_input.read())
        for resource in documents:
            # yaml.dump(resource, sys.stdout)
            ns = ''
            if('namespace' in resource['metadata']):
                ns = '{0}/'.format(resource['metadata']['namespace'])
            print(
                '{0}{1}--{2}.yml'
                .format(
                    ns,
                    resource['kind'].lower(),
                    resource['metadata']['name'].lower().replace(":", "-")))


if __name__ == '__main__':
    main()
