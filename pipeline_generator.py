import yaml
import os

BLUEPRINT_PATH = 'blueprint.yaml'
OUTPUT_PATH = os.path.join('.github', 'workflows', 'generated.yml')

def load_blueprint():
    with open(BLUEPRINT_PATH, 'r') as f:
        return yaml.safe_load(f)

def generate_workflow(bp):
    stages = bp['project']['stages']
    lang = bp['project']['language']
    deploy = bp['project']['deployment']

    jobs = {}
    for stage in stages:
        if stage == 'deploy':
            jobs[stage] = {
                'uses': f'./.github/workflows/deploy-{deploy}.yml@main'
            }
        else:
            jobs[stage] = {
                'uses': f'./.github/workflows/{lang}.yml@main',
                'with': {
                    'job': stage
                }
            }

    return {
        'name': 'Generated CI/CD Pipeline',
        'on': {
            'push': {
                'branches': ['main']
            }
        },
        'jobs': jobs
    }

def save_workflow(data):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"✅ Workflow created at {OUTPUT_PATH}")

if __name__ == "__main__":
    blueprint = load_blueprint()
    workflow = generate_workflow(blueprint)
    save_workflow(workflow)
