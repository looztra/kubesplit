from typing import Dict
from ruamel.yaml import YAML


class YamlWriterConfig:
    """
    Config stanza for ruamel.yaml.YAML parser/writer with opinionated defaults
    """

    def __init__(
        self,
        explicit_start: bool = True,
        explicit_end: bool = False,
        default_flow_style: bool = False,
        dash_inwards: bool = True,
        quotes_preserved: bool = True,
        parsing_mode: str = "rt",
    ):
        """
            Args:

            explicit_start: write the start of the yaml doc even when there is\
                only one done in the file
            default_flow_style: if False, block style will be used for nested \
                    arrays/maps
            dash_inwards: push dash inwards if True
            quotes_preserved: preserve quotes if True
            parsing_typ: safe or roundtrip (rt)
        """
        self.explicit_start = explicit_start
        self.explicit_end = explicit_end
        self.default_flow_style = default_flow_style
        self.dash_inwards = dash_inwards
        self.quotes_preserved = quotes_preserved
        self.parsing_mode = parsing_mode


def build_yaml_writer_config_from_args(
    args: Dict[str, any]
) -> YamlWriterConfig:
    return YamlWriterConfig(
        explicit_start=args["explicit_start"],
        explicit_end=args["explicit_end"],
        default_flow_style=args["default_flow_style"],
        dash_inwards=args["dash_inwards"],
        quotes_preserved=args["quotes_preserved"],
        parsing_mode=args["typ"],
    )


def get_opinionated_yaml_writer(
    writer_config: YamlWriterConfig = YamlWriterConfig()
) -> YAML:
    """
    Configure a yaml parser/formatter the yamkix way

    Args:

        writer_config: a YamlWriterConfig instance

    Returns:

        a ruamel.yaml object
    """
    yaml = YAML(typ=writer_config.parsing_mode)
    yaml.explicit_start = writer_config.explicit_start
    yaml.explicit_end = writer_config.explicit_end
    yaml.default_flow_style = writer_config.default_flow_style
    yaml.preserve_quotes = writer_config.quotes_preserved
    if writer_config.dash_inwards:
        yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml
