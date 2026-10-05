"""Reject duplicate YAML keys instead of accepting last-value-wins configuration."""
import yaml
class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader,node,deep=False):
    loader.flatten_mapping(node)
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        try:
            if key in result:
                raise yaml.constructor.ConstructorError('mapping',node.start_mark,'duplicate key: '+str(key),key_node.start_mark)
            result[key]=loader.construct_object(value_node,deep=deep)
        except TypeError as exc:
            raise yaml.constructor.ConstructorError('mapping',node.start_mark,'unhashable key',key_node.start_mark) from exc
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)

def parse(text):
    return yaml.load(text,Loader=UniqueLoader)
