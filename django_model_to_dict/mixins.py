from .plugins import FilebrowserFieldSerializationPlugin


class ToDictMixin:
    
    _serialization_plugins = (FilebrowserFieldSerializationPlugin, )

    def to_dict(self):
        opts = self._meta
        data = {}

        # initializing manually specified field grouping
        if self.TO_DICT_GROUPING:
            for prefix in self.TO_DICT_GROUPING:
                data[prefix] = {}

        # initializing prefixed field grouping
        if self.TO_DICT_GROUPING_PREFIXES:
            for prefix in self.TO_DICT_GROUPING_PREFIXES:
                data[self._clean_grouping_prefix(prefix)] = {}

        for f in opts.concrete_fields:
            # skipping explicitly specified fields
            if self.TO_DICT_SKIP_FIELDS:
                if f.name in self.TO_DICT_SKIP_FIELDS:
                    continue
            # handling prefixed fields grouping
            if self.TO_DICT_GROUPING_PREFIXES:
                prefix = self._get_grouping_prefix(f.name)
                if prefix:
                    prefix_key = self._clean_grouping_prefix(prefix)
                    data[prefix_key][f.name.replace(prefix, '')] = f.value_from_object(self)
                    continue
            # handling manually specified field grouping
            if self.TO_DICT_GROUPING:
                if f.name in self.TO_DICT_GROUPING.keys():
                    data[f.name] = f.value_from_object(self)
                    continue
            # handling images and other non-trivial files
            if self._handle_nontrivial_field(f, data):
                continue
            # handling default case
            data[f.name] = f.value_from_object(self)

        # cleanup for unused grouping
        for k in [k for k in data.keys() if data[k] == {}]:
            del data[k]

        # the mixin allows to redifine the related fields strategy
        if hasattr(self, '_to_dict_related_fields_strategy'):
            self._to_dict_related_fields_strategy(opts, data)
        else:
            self._default_related_fields_strategy(opts, data)

        # calling pre_finish_hook if exists
        if hasattr(self, '_to_dict_pre_finish_hook'):
            self._to_dict_pre_finish_hook(data)

        return data

    def _handle_nontrivial_field(self, field, data):
        for plugin in self._serialization_plugins:
            if plugin.check_field(field):
                data[field.name] = plugin.serialize_field(field, self)
                return True
        return False

    def _default_related_fields_strategy(self, opts, data):
        related_fields = [f for f in opts.get_all_related_objects() if f.is_relation and f.multiple]
        for rf in related_fields:
            data[rf.name] = [i.to_dict() for i in getattr(self, rf.name).all()]

    def _get_grouping_prefix(self, field_name):
        if not self.TO_DICT_GROUPING_PREFIXES:
            return None
        for group_prefix in self.TO_DICT_GROUPING_PREFIXES:
            if field_name.startswith(group_prefix):
                return group_prefix
            
    def _clean_grouping_prefix(self, prefix):
        return prefix.replace('_', '')