import pandas as pd
from sumatra.projects import load_project
import yaml

def parameters2columns(parameters):
    """Convert sumatra yaml parameters to Pandas columns
    """
    if hasattr(yaml, "FullLoader"):
        # PyYAML 5.1 deprecated the plain yaml.load(input) function
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        d_orig = yaml.load(parameters['content'], Loader=yaml.FullLoader)
    else:
        d_orig = yaml.load(parameters['content'])
    d = dict()
    for k, v in d_orig.iteritems():
        d["--" + k] = v
    return pd.Series(d)

def smt2df(path=None):
    """Load sumatra project and convert to Pandas DataFrame

    Read project from directory passed as the argument and return Project
    object and project records converted to Pandas DataFrame. 
    If no argument is given, the project is read from the current
    directory.
    """
    project = load_project('.')
    df = pd.read_json(project.record_store.export('benchmark8'),
                      convert_dates=["timestamp"])

    df = df.merge(df.parameters.apply(parameters2columns), left_index=True, right_index=True)

    df['nproc'] = df.launch_mode.apply(lambda x: x['parameters']['n'])

    return project, df

def delete_smt_record(label, project):
    project.delete_record(label, delete_data=True)
    shutil.rmtree(os.path.join("Data", label))
