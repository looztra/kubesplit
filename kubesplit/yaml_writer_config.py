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


class YamlWriterConfigKey:
    @property
    def explicit_start(self) -> str:
        return "explicit_start"

    @property
    def explicit_end(self) -> str:
        return "explicit_end"

    @property
    def default_flow_style(self) -> str:
        return "default_flow_style"

    @property
    def dash_inwards(self) -> str:
        return "dash_inwards"

    @property
    def quotes_preserved(self) -> str:
        return "quotes_preserved"

    @property
    def typ(self) -> str:
        return "typ"


def build_yaml_writer_config_from_args(
    args: Dict[str, any]
) -> YamlWriterConfig:
    return YamlWriterConfig(
        explicit_start=args[YamlWriterConfigKey.explicit_start]
        if YamlWriterConfigKey.explicit_start in args
        else True,
        explicit_end=args[YamlWriterConfigKey.explicit_end]
        if YamlWriterConfigKey.explicit_end in args
        else False,
        default_flow_style=args[YamlWriterConfigKey.default_flow_style]
        if YamlWriterConfigKey.default_flow_style in args
        else False,
        dash_inwards=args[YamlWriterConfigKey.dash_inwards]
        if YamlWriterConfigKey.dash_inwards in args
        else True,
        quotes_preserved=args[YamlWriterConfigKey.quotes_preserved]
        if YamlWriterConfigKey.quotes_preserved in args
        else True,
        parsing_mode=args[YamlWriterConfigKey.typ]
        if YamlWriterConfigKey.typ in args
        else "rt",
    )


def get_opinionated_yaml_writer(
    writer_config: YamlWriterConfig = YamlWriterConfig()
) -> YAML:
    """
    Configure a yaml parser/formatter the yamkix way

    Args:

        writer_config: a YamlWriterConfig instance

    Returns:

        a ruamel.yaml YAML instance
    """
    yaml = YAML(typ=writer_config.parsing_mode)
    yaml.explicit_start = writer_config.explicit_start
    yaml.explicit_end = writer_config.explicit_end
    yaml.default_flow_style = writer_config.default_flow_style
    yaml.preserve_quotes = writer_config.quotes_preserved
    if writer_config.dash_inwards:
        yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml
