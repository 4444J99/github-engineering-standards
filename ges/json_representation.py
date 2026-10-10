"""Locate an exact JSON string token without confusing equal-valued occurrences."""
import hashlib
import json
import re

from .published_assurance import _require


def decoded_json_expression(raw: bytes, representation: dict, span: dict) -> bytes:
    fields = {'mode', 'json_pointer', 'token_start_byte', 'token_end_byte',
              'decoded_expression_sha256'}
    _require(isinstance(representation, dict) and set(representation) == fields and
             representation['mode'] == 'JSON_STRING', 'Malformed JSON representation')
    pointer = representation['json_pointer']
    _require(isinstance(pointer, str) and (pointer == '' or pointer.startswith('/')) and
             re.search(r'~(?![01])', pointer) is None, 'Invalid JSON pointer')
    start, end = representation['token_start_byte'], representation['token_end_byte']
    _require(type(start) is int and type(end) is int and 0 <= start < end <= len(raw),
             'Invalid JSON token byte bounds')
    _require(isinstance(span, dict) and set(span) == {'start_byte', 'end_byte', 'sha256'} and
             type(span['start_byte']) is int and type(span['end_byte']) is int and
             span['start_byte'] == start + 1 and span['end_byte'] == end - 1 and
             hashlib.sha256(raw[start+1:end-1]).hexdigest() == span['sha256'],
             'JSON expression must bind the complete raw token interior')
    _require(len(raw) <= 50_000_000, 'JSON output exceeds bounded parsing size')

    def reject_constant(value):
        raise ValueError('Non-JSON constant: ' + value)

    decoder = json.JSONDecoder(parse_constant=reject_constant)
    selected = None
    try:
        text = raw.decode('utf-8')

        def whitespace(position):
            while position < len(text) and text[position] in ' \t\r\n':
                position += 1
            return position

        def string(position):
            _require(position < len(text) and text[position] == '"', 'Expected JSON string')
            value, after = decoder.raw_decode(text, position)
            value.encode('utf-8')  # Reject unpaired surrogates, including object keys.
            return value, after

        def value(position, location, depth):
            nonlocal selected
            _require(depth <= 200, 'JSON nesting exceeds bound')
            position = whitespace(position)
            _require(position < len(text), 'Incomplete JSON value')
            character = text[position]
            if character == '"':
                decoded, after = string(position)
                if location == pointer:
                    selected = (position, after, decoded.encode('utf-8'))
                return after
            if character in '{[':
                is_object = character == '{'
                closing = '}' if is_object else ']'
                position = whitespace(position + 1)
                if position < len(text) and text[position] == closing:
                    return position + 1
                keys, index = set(), 0
                while True:
                    if is_object:
                        key, position = string(position)
                        _require(key not in keys, 'Duplicate JSON object key')
                        keys.add(key)
                        position = whitespace(position)
                        _require(position < len(text) and text[position] == ':', 'Expected JSON colon')
                        position += 1
                        component = key.replace('~', '~0').replace('/', '~1')
                    else:
                        component = str(index)
                    position = whitespace(value(position, location + '/' + component, depth + 1))
                    _require(position < len(text), 'Incomplete JSON container')
                    if text[position] == closing:
                        return position + 1
                    _require(text[position] == ',', 'Expected JSON separator')
                    position = whitespace(position + 1)
                    index += 1
            _, after = decoder.raw_decode(text, position)
            return after

        after = whitespace(value(0, '', 0))
        _require(after == len(text), 'Trailing data after JSON document')
        _require(selected is not None, 'JSON pointer does not select a string value')
        char_start, char_end, decoded = selected
        _require(len(text[:char_start].encode()) == start and
                 len(text[:char_end].encode()) == end,
                 'JSON token is not the occurrence selected by the pointer')
        _require(hashlib.sha256(decoded).hexdigest() == representation['decoded_expression_sha256'],
                 'Decoded JSON expression digest changed')
        return decoded
    except (UnicodeError, RecursionError, json.JSONDecodeError) as exc:
        raise ValueError('Invalid complete UTF-8 JSON expression context') from exc
