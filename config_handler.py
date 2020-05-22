import yaml

config = yaml.safe_load(open("config.yml"))

# Default values
config['Bird']['color'] += 'bird'

config['Pipe']['color'] = 'pipe-' + config['Pipe']['color']

