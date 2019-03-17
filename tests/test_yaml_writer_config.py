from kubesplit.yaml_writer_config import YamlWriterConfig
from kubesplit.yaml_writer_config import get_opinionated_yaml_writer
from ruamel.yaml import YAML


def test_default_values():
    sut: YamlWriterConfig = YamlWriterConfig()
    assert sut.parsing_mode == "rt"
    assert sut.explicit_start
    assert not sut.explicit_end
    assert not sut.default_flow_style
    assert sut.dash_inwards
    assert sut.quotes_preserved


def test_get_opinionated_yaml_writer_with_defaults():
    sut: YAML = get_opinionated_yaml_writer()
    assert sut.typ == "rt"
    assert sut.explicit_start
    assert not sut.explicit_end
    assert not sut.default_flow_style
    assert sut.preserve_quotes
    assert sut.map_indent == 2
    assert sut.sequence_dash_offset == 2
    assert sut.sequence_indent == 4
