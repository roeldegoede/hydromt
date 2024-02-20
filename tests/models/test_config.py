from pathlib import Path

from hydromt.io.readers import configread
from hydromt.io.writers import configwrite


def test_config(tmpdir):
    ext = "yml"
    cfdict = {
        "section1": {
            "list": [1, 2, 3],
            # "tuple": (1, "b"), # yaml cannot deal with tuple
            "bool": True,
            "str": "test",
            "int": 1,
            "float": 2.3,
            "None": None,
        },
        "section2": {
            "path": f"config.{ext}",  # path exists -> Path
            "path1": "config1.yml",  # path does not exist -> str
        },
        # evaluation skipped by default for setup_config
        "setup_config": {
            "path": f"config.{ext}",
            "float": 2.3,
        },
    }
    config_fn = tmpdir.join(f"config.{ext}")
    configwrite(config_fn, cfdict)
    cfdict1 = configread(config_fn, abs_path=True)
    assert cfdict["section1"] == cfdict1["section1"]
    assert isinstance(cfdict1["section2"]["path"], Path)
    assert isinstance(cfdict1["section2"]["path1"], str)
    # by default paths in setup_config are not evaluated
    assert isinstance(cfdict1["setup_config"]["path"], str)
    assert isinstance(cfdict1["setup_config"]["float"], float)
